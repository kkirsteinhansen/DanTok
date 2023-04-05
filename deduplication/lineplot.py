#!/usr/bin/python3

import argparse

import matplotlib.pyplot as plt
import numpy as np


def parse_arguments():
	arg_parser = argparse.ArgumentParser(description='Line Plot')
	arg_parser.add_argument('--x-title', help='title of x-axis')
	arg_parser.add_argument('--x-values', required=True, nargs='+', type=float, help='list of x-axis values')
	arg_parser.add_argument('--y-title', help='title of y-axis')
	arg_parser.add_argument('--y-values', required=True, nargs='+', type=float, help='list of y-axis values')
	arg_parser.add_argument('--y2-title', help='title of second y-axis')
	arg_parser.add_argument('--y2-values', required=True, nargs='+', type=float, help='list of second y-axis values')
	return arg_parser.parse_args()


def main():
	args = parse_arguments()
	assert len(args.x_values) == len(args.y_values) == len(args.y2_values), "[Error] All axes must have the same number of values."

	colors = ['lightcoral', 'mediumseagreen']
	markers = ['o', 'P']


	fig, ax = plt.subplots(figsize=(6.3 * 1, 6.3 * 0.5))

	# ax.set_xticks(args.x_values)

	# plot primary y-values
	ax.plot(args.x_values, args.y_values, color=colors[0], marker=markers[0])

	# plot secondary y-values
	ax2 = ax.twinx()
	ax2.plot(args.x_values, args.y2_values, color=colors[1], marker=markers[1])

	ax.set_xlabel(args.x_title, fontsize='x-large', alpha=.5)
	ax.set_xticks(np.arange(0., 1., 0.1))
	ax.set_xlim(0.05, 0.95)

	ax.set_ylabel(args.y_title, fontsize='x-large', color=colors[0], alpha=.5)
	ax.set_ylim(0.0, 1.0)
	plt.setp(ax.get_yticklabels(), color=colors[0])

	ax2.set_ylabel(args.y2_title, fontsize='x-large', color=colors[1], alpha=.5)
	plt.setp(ax2.get_yticklabels(), color=colors[1])

	fig.tight_layout()
	plt.show()


if __name__ == '__main__':
	main()