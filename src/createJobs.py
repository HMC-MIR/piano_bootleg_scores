#!/bin/python3
import os
import time
import subprocess
import random
import sys

# Basepath is the imslp pdf directory
# filelist is the list of files you want to extract features from
# tmpbasepath is a temporary directory created to store images converted from pdfs
basepath = "/pylon5/ir5phqp/dhyang/imslp/"
filelist = "/home/dhyang/imslp_convert_psc/filelist.txt"
tmpbasepath = "/pylon5/ir5phqp/dhyang/tmp_dir/"
outdirbasepath = "/pylon5/ir5phqp/dhyang/imslp_bootleg_dir/"
errorbasepath = "/pylon5/ir5phqp/dhyang/error_dir/"
count = 1

# To only extract some features, set mode="some"
# To extract all frature, set mode="all"
mode = "some"
random.seed(5)


with open(filelist, 'r') as f:
    # If mode is some, numFiles signifies how many friles you are extracting bootleg features from
    numFiles = 5
    # SLURM has a job number cap, so you should set a max number of jobs
    # so it doesn't exceed this cap
    maxJobs = 4000
    lines = f.read().splitlines()
    lineList = []
    running_id = []
    if mode == "some":
        for i in range(numFiles):
            lineList.append(random.choice(lines))
    else:
        for line in lines:
            lineList.append(line)

    for line in lineList:
        input_pdf_file = basepath+line.strip()
        fname = line.strip()
        tmp_file = tmpbasepath+fname[30:-4]+"/page.png"
        output_pkl_file = outdirbasepath+fname[30:-4]+'.pkl'
        error_file = errorbasepath+fname[30:-4]+'.txt'
        if os.path.exists(output_pkl_file):
            continue

        if len(running_id) == maxJobs:
            # If we have too many ids stored, check if we can remove ids
            # so we can submit more jobs
            check = True
            while(check):
                firstID = running_id[0]
                process = subprocess.Popen(
                    ['sacct', '--jobs='+firstID], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = process.communicate()
                out = str(out)
                if "completed" in out.lower():
                    running_id.pop(0)
                    check = False
                time.sleep(.1)

        if not os.path.exists(os.path.dirname(error_file)):
            os.makedirs(os.path.dirname(error_file))

        #SBATCH command to extract bootleg features
        subprocess.call(['sbatch', '--output='+error_file, '--error='+error_file, 'bootlegWrapper.sh',
                         input_pdf_file, tmp_file, output_pkl_file, error_file])
        f.close()
        with open("/home/dhyang/tmp.txt", 'r') as f:
            out = f.readline()

        # SBATCH job submissions should output the submitted job id. We store this id
        # to ensure we don't submit too many jobs.
        out = str(out)
        outIdx = out.split(" ")[-1][:-1].strip()
        running_id.append(outIdx)
        print(line)
        print("Running ", outIdx)
        print("Ran ", count)
        count += 1
