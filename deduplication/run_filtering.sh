#!/bin/zsh

# INPUT_FILE=data/filtered/oov/allcomments-filterOOV.txt
# OUTPUT_DIRECTORY=data/filtered/maxsim-oov
INPUT_FILE=data/raw/allcomments.txt
OUTPUT_DIRECTORY=data/filtered/maxsim-all
IGNORED_STRINGS='"@username"'
FILTER='maxsim'


for (( threshold=.05; $threshold < 1; threshold+=.05 )); do
	t=${threshold:2:2}

	if [ -f "${OUTPUT_DIRECTORY}/${FILTER}-${t}.txt" ]; then
		continue
	fi

	python similarity_filter.py \
		"${INPUT_FILE}" \
		"${FILTER}" \
		--threshold "0.${t}" \
		--ignore ${IGNORED_STRINGS} \
		--lowercase \
		--similarities "${OUTPUT_DIRECTORY}/all-sims.npy" \
		--output "${OUTPUT_DIRECTORY}/${FILTER}-${t}.txt"

	python ttr.py "${OUTPUT_DIRECTORY}/${FILTER}-${t}.txt" | tee "${OUTPUT_DIRECTORY}/${FILTER}-${t}-ttr.txt"
done