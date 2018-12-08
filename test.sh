#!/bin/sh
for i in {1..100}; do
	python generator.py 3
	python npuzzle.py random.txt >> npuzzle.logs
done

