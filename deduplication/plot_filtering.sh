#!/bin/zsh

OUTPUT_DIRECTORY=data/filtered/maxsim-all

x_values=()
y_values=()
y2_values=()

for (( threshold=.05; $threshold < 1; threshold+=.05 )); do
	t=${threshold:2:2}
	x_values+=("${threshold:0:4}")
	y_values+=("$(sed -nr 's/TTR: ([0-9\.]+)/\1/p' ${OUTPUT_DIRECTORY}/maxsim-${t}-ttr.txt)")
	y2_values+=("$(sed -nr 's/Total number of tokens: ([0-9]+)/\1/p' ${OUTPUT_DIRECTORY}/maxsim-${t}-ttr.txt)")
done

python lineplot.py \
	--x-title "Merge Threshold" \
	--x-values "${x_values[@]}" \
	--y-title "Token-Type-Ratio" \
	--y-values "${y_values[@]}" \
	--y2-title "Number of Tokens" \
	--y2-values "${y2_values[@]}"