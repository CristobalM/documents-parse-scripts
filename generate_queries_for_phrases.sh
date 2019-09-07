#!/usr/bin/env bash

phrases_qties=(1000 5000 10000 25000 50000 75000 100000)

for ph_q in ${phrases_qties[@]}
do
    ./generate_queries.sh OR phrases_${ph_q}.txt > OR_queries_phrases_${ph_q}.txt
    ./generate_queries.sh AND phrases_${ph_q}.txt > AND_queries_phrases_${ph_q}.txt
done
