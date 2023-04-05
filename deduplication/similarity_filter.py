#!/usr/bin/python3
"""
Similarity Filter

Usage:
	similarity_filter.py path/to/comments.txt filter_name [filter_params] [pre-processing params]

Examples:
	similarity_filter.py path/to/comments.txt originality
	similarity_filter.py path/to/comments.txt threshold --threshold 0.7
	similarity_filter.py path/to/comments.txt maxsim --threshold 0.7
"""

import argparse, os

import numpy as np

from Levenshtein import ratio

from ttr import get_token_statistics


def parse_arguments():
	arg_parser = argparse.ArgumentParser(description='Similarity Filter')
	arg_parser.add_argument('input', help='path to newline-separated comments')
	arg_parser.add_argument('filter', choices=['threshold', 'originality', 'ttr', 'maxsim', 'maxttr'], help='type of filter to apply')
	# filter parameters
	arg_parser.add_argument('--threshold', type=float, help='similarity threshold (threshold filter)')
	# pre-processing paramters
	arg_parser.add_argument('--ignore', nargs='*', default=[], help='list of string sequences to ignore')
	arg_parser.add_argument('--lowercase', action='store_true', default=False, help='set flag to lowercase all inputs')
	# file parameters
	arg_parser.add_argument('--similarities', help='path to an optional similarities file to load/save')
	arg_parser.add_argument('--output', help='path to an optional output file')
	return arg_parser.parse_args()


def apply_preprocessing(comments, ignored_strings, lowercase):
	# pre-process comments for similarity comparison
	scrubbed_comments = []
	for comment_idx, comment in enumerate(comments):
		scrubbed_comment = str(comment)
		# apply lowercasing
		if lowercase:
			scrubbed_comment = scrubbed_comment.lower()
		# iterate over and remove ignored strings
		for ignored_string in ignored_strings:
			scrubbed_comment = scrubbed_comment.replace(ignored_string, '')
			scrubbed_comment = scrubbed_comment.strip()
		scrubbed_comments.append(scrubbed_comment)
	print(
		f"Removed {len(ignored_strings)} ignored string(s). "
		f"{'Applied lowercasing. ' if lowercase else ''}"
		f"{sum([1 for sc in scrubbed_comments if len(sc) < 1])} empty comment(s)."
	)
	return scrubbed_comments


def compute_similarities(comments):
	# initialize comment-to-comment similarity matrix
	similarities = np.zeros((len(comments), len(comments)))
	np.fill_diagonal(similarities, 1)

	# compute similarities across all unique comment pairs
	for i in range(len(comments)):
		for j in range(i + 1, len(comments)):
			print(f"\r[{((i * len(comments) + j) - i)/(len(comments)**2/100):.2f}%] Computing similarities...", end='', flush=True)
			similarity = ratio(comments[i], comments[j])
			similarities[i, j] = similarity
			similarities[j, i] = similarity
	print(f"\rComputed similarities for {len(comments)**2} pairs.")
	return similarities


def originality_filter(comments, similarities):
	print(f"Applying originality filter...")
	filtered_comment_idcs = []

	# sort comments by their cumulative similarity to all other comments
	cumulative_similarities = np.sum(similarities, axis=0)
	comment_idcs_by_similarity = np.argsort(-cumulative_similarities)

	non_self_similarities = np.copy(similarities)
	np.fill_diagonal(non_self_similarities, -float('inf'))
	max_similar_comment_idcs = np.argmax(non_self_similarities, axis=0)
	
	comment_mask = np.ones(similarities.shape[0], dtype=bool)
	for candidate_idx in range(similarities.shape[0]):
		# get first non-masked comment with highest similarity to everything else
		comment_idx = comment_idcs_by_similarity[candidate_idx]
		if not comment_mask[comment_idx]:
			continue
		filtered_comment_idcs.append(comment_idx)
		# mask out all comments where the current comment is the most similar
		comment_idcs_to_filter = np.nonzero(max_similar_comment_idcs == comment_idx)[0]
		comment_mask[comment_idcs_to_filter] = False
		comment_mask[comment_idx] = False
		max_similar_comment_idcs[~comment_mask] = -1

		# print(f"{cumulative_similarities[comment_idx]:.2f}\t{comments[comment_idx]}:")
		# for similar_idx in comment_idcs_to_filter:
		# 	print(f"    {similarities[comment_idx, similar_idx]:.2f}\t{comments[similar_idx]}")
	return filtered_comment_idcs


def merge_comment_idcs(comments, deduplication_map):
	filtered_comment_idcs = set()

	# resolve deduplication map
	for comment_idx in deduplication_map:
		map_to_idx = deduplication_map[comment_idx]
		while map_to_idx in deduplication_map:
			map_to_idx = deduplication_map[map_to_idx]
		# print(f"Merged '{comments[comment_idx]}' -> '{comments[map_to_idx]}'")
		filtered_comment_idcs.add(map_to_idx)

	# add remaining comments (which are not similar enough to each other)
	filtered_comment_idcs |= set(range(len(comments))) - set(deduplication_map.keys())

	return list(filtered_comment_idcs)


def maxsim_filter(comments, similarities, threshold):
	print(f"Applying maximum similarity filter with merge threshold >{threshold}...")
	cumulative_similarities = np.sum(similarities, axis=0)

	# get all non-self, non-duplicate similarities
	unique_similarities = np.copy(similarities)
	unique_similarities[np.tril_indices(unique_similarities.shape[0])] = -float('inf')

	# mask out all similarities below threshold
	unique_similarities[unique_similarities <= threshold] = -float('inf')

	# gather relevant pair indices
	relevant_pair_indices = np.where(unique_similarities > -float('inf'))

	# sort only the values of relevant pairs
	relevant_pairs_by_similarity = np.argsort(-unique_similarities[relevant_pair_indices], axis=None)

	deduplication_map = {}

	# iterate over all relevant pairs and compute which ones to merge
	print(f"Computing merges for {len(relevant_pairs_by_similarity)} relevant pairs above the threshold...")
	sorted_relevant_pair_idx = -1
	# while np.sum(unique_similarities != -float('inf')) > 0:
	while sorted_relevant_pair_idx < len(relevant_pairs_by_similarity) - 1:
		# check out the next relevant pair
		sorted_relevant_pair_idx += 1
		# get globally most similar pair
		print(f"\r[{100 * sorted_relevant_pair_idx/len(relevant_pairs_by_similarity):.2f}%] Computing maximum similarity merges...", end='', flush=True)
		# map index of relevant pair to global indices
		max_similar_relevant_pair_idx = relevant_pairs_by_similarity[sorted_relevant_pair_idx]
		max_similar_pair = (relevant_pair_indices[0][max_similar_relevant_pair_idx], relevant_pair_indices[1][max_similar_relevant_pair_idx])

		# check if it has already been merged
		if np.sum(unique_similarities[max_similar_pair]) == -float('inf'):
			continue

		# keep comment that is more similar to everything else
		map_from, map_to = sorted(max_similar_pair, key=lambda i: cumulative_similarities[i])
		# map_to, map_from = sorted(max_similar_pair, key=lambda i: cumulative_similarities[i])
		deduplication_map[map_from] = map_to

		# mask out current maximum similar pair
		unique_similarities[max_similar_pair] = -float('inf')

	# resolve deduplication map
	filtered_comment_idcs = merge_comment_idcs(comments, deduplication_map)
	filtered_comment_idcs = sorted(filtered_comment_idcs, key=lambda i: cumulative_similarities[i], reverse=True)
	print(f"\rCompleted maximum similarity filtering after {len(deduplication_map)} merge(s) with {len(filtered_comment_idcs)} comment(s) remaining.")

	return filtered_comment_idcs


def ttr_filter(comments, similarities, threshold=None):
	if threshold is None:
		print(f"Applying maximum TTR filter...")
	else:
		print(f"Applying TTR filter with threshold >{threshold}...")

	filtered_comment_idcs = set()

	cumulative_similarities = np.sum(similarities, axis=0)

	unique_similarities = np.copy(similarities)
	unique_similarities[np.tril_indices(unique_similarities.shape[0])] = -float('inf')

	token_type_ratios = []
	deduplication_map = []

	while np.sum(unique_similarities != -float('inf')) > 0:
		# compute current TTR
		filtered_comment_idcs = merge_comment_idcs(comments, dict(deduplication_map))
		filtered_comments = [comments[comment_idx] for comment_idx in filtered_comment_idcs]
		ttr = get_token_statistics(filtered_comments)[-1]
		if (threshold is not None) and (ttr > threshold):
			break
		token_type_ratios.append(ttr)
		# print(f'{len(deduplication_map)}: {ttr:.2f}')

		# get globally most similar pair
		max_similar_pair = np.unravel_index(np.argmax(unique_similarities), unique_similarities.shape)

		# keep comment that is more similar to everything else
		map_from, map_to = sorted(max_similar_pair, key=lambda i: cumulative_similarities[i])
		deduplication_map.append((map_from, map_to))

		# mask out current maximum similar pair
		unique_similarities[max_similar_pair] = -float('inf')

	# retrieve deduplication map with maximum TTR
	if threshold is None:
		max_ttr = max(token_type_ratios)
		max_ttr_idx = token_type_ratios.index(max_ttr)
		max_deduplication_map = dict(deduplication_map[:max_ttr_idx])
		print(f"Found maximum TTR of {max_ttr:.2f} at merge step {max_ttr_idx}.")
	else:
		max_deduplication_map = dict(deduplication_map)
		print(f"Found TTR of {token_type_ratios[-1]:.2f} > {threshold} after {len(deduplication_map)} merge(s).")

	# resolve deduplication map
	filtered_comment_idcs = merge_comment_idcs(comments, max_deduplication_map)
	filtered_comment_idcs = sorted(filtered_comment_idcs, key=lambda i: cumulative_similarities[i], reverse=True)

	return filtered_comment_idcs


def threshold_filter(comments, similarities, threshold):
	print(f"Applying threshold filter >{threshold}...")
	filtered_comment_idcs = []

	comment_idcs_by_length, _ = zip(*sorted(zip(list(range(len(comments))), comments), key=lambda e: len(e[1]), reverse=True))

	comment_mask = np.ones(len(comments), dtype=bool)
	for comment_idx in comment_idcs_by_length:
		if not comment_mask[comment_idx]:
			continue

		similar_comment_idcs = np.where(similarities[comment_idx, :] > threshold)[0]
		comment_mask[similar_comment_idcs] = False
		filtered_comment_idcs.append(comment_idx)

	return filtered_comment_idcs


def main():
	args = parse_arguments()

	# load comments line-by-line
	comments = []
	with open(args.input, 'r', encoding='utf8') as fp:
		for line in fp:
			comments.append(line.strip())
	print(f"Loaded {len(comments)} comment(s) from {args.input}.")

	# apply pre-processing
	scrubbed_comments = apply_preprocessing(comments, args.ignore, args.lowercase)

	# compute pair-wise similarities
	if (args.similarities is not None) and (os.path.exists(args.similarities)):
		similarities = np.load(args.similarities)
		assert similarities.shape[0] == similarities.shape[1] == len(scrubbed_comments), \
			f"[Error] Shape of pre-computed similarities does not match input comments."
		print(f"Loaded {similarities.shape} pre-computed similarities from '{args.similarities}'.")
	else:
		similarities = compute_similarities(scrubbed_comments)
		if args.similarities is not None:
			np.save(args.similarities, similarities)
			print(f"Saved pre-computed similarities to '{args.similarities}'.")

	# apply filter
	if args.filter == 'threshold':
		assert args.threshold is not None, '[Error] Please set a --threshold for this filter.'
		filtered_comment_idcs = threshold_filter(scrubbed_comments, similarities, threshold=args.threshold)
	elif args.filter == 'maxsim':
		assert args.threshold is not None, '[Error] Please set a --threshold for this filter.'
		filtered_comment_idcs = maxsim_filter(scrubbed_comments, similarities, threshold=args.threshold)
	elif args.filter == 'maxttr':
		filtered_comment_idcs = ttr_filter(scrubbed_comments, similarities)
	elif args.filter == 'ttr':
		assert args.threshold is not None, '[Error] Please set a --threshold for this filter.'
		filtered_comment_idcs = ttr_filter(scrubbed_comments, similarities, threshold=args.threshold)
	elif args.filter == 'originality':
		filtered_comment_idcs = originality_filter(scrubbed_comments, similarities)

	print('-'*64)
	for comment_idx in filtered_comment_idcs:
		print(f"{comments[comment_idx]}")
	print('-'*64)
	if args.output is not None:
		with open(args.output, 'w', encoding='utf8') as fp:
			fp.write('\n'.join([comments[i] for i in filtered_comment_idcs]))
		print(f"Saved filtered comments to '{args.output}'.")
	print(f"Filtered {len(comments)} to {len(filtered_comment_idcs)} comment(s).")


if __name__ == '__main__':
	main()