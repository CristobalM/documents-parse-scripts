#!/usr/bin/env bash

phrases_qties=(1000 5000 10000 25000 50000 75000 100000)

for ph_q in ${phrases_qties[@]}
do
    python find_phrases.py ~/ssd1tb/EDCompactas/datasets/blogger_dataset/blogs_cleaned_2 $ph_q phrases_${ph_q}.txt
done

