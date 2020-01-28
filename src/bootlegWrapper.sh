#!/bin/bash

#SBATCH -p RM-shared
#SBATCH -t 2:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1

source /home/dhyang/MIR4/bin/activate
python3 getBootleg.py "$1" "$2" "$3" "$4"
