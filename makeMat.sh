#!/bin/bash

# vcf is argument 1
echo "();" > empty.nwk
usher -t empty.nwk -v $1 -o temp.pb
matOptimize -i temp.pb -v $1 -o $1.optimized.pb -T 15