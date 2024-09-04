#!/bin/bash
#SBATCH --job-name=load_container      # Specify job name
#SBATCH --partition=shared     # Specify partition name
#SBATCH --mem=100G              # Specify amount of memory needed
#SBATCH --time=48:00:00        # Set a limit on the total run time
#SBATCH --mail-type=FAIL       # Notify user by email in case of job failure
#SBATCH --account=aa0238       # Charge resources on this project account
#SBATCH --output=/home/a/a271093/my_job.o%j    # File name for standard output

set -e
ulimit -s 204800

#module load python3
conda init bash
source ~/.bashrc
conda activate MOAAP_env

# Execute serial programs, e.g.
python -u create_container_with_slurm.py
