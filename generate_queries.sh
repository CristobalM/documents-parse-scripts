#!/usr/bin/env bash

function generate_queries (){
    local query_name=$1;
    local phrases_fp=$2;
    awk -v op="$query_name" '{print op " " $0 }' ${phrases_fp}
}

query_name=$1
phrases_file=$2;

generate_queries ${query_name} ${phrases_file}