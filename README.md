This repository serves as part of submission to the [ICTV Computational Virus Taxonomy Challenge](https://ictv-vbeg.github.io/ICTV-TaxonomyChallenge/). The challenge, as defined by the ICTV:

> The ICTV Computational Virus Taxonomy Challenge is a challenge for bioinformaticians who build methods to classify 
> unknown sequences into the current ICTV-approved taxonomy. We ask you to classify a set of viral sequences using a 
> bioinformatics pipeline of your choice or design. The classification will be evaluated using the Taxonomy Release 
> MSL39. Importantly, we ask that your pipeline be fully and easily reproducible and that you make available the 
> necessary code and environment to run it. [...]

## Repository Overview

This repository is divided into several folders, as follows:

- `ICTVTaxoChallenge_vConTACT3/`
    - `results/`: Contains classification results
        - `classification_results.csv`: Classification file
        - `classification_template.csv`: Example results template file
    - `v3_outputs/`: Limited outputs from vContact3 run used to generate predictions
        - `final_assignments.csv.bz2`: Original output from vContact3
    - `output_converter.py`: Converts vContact3 predictions to classification result
    - `README.md`: 'This' file, provides documentation
    - `vcontact3.def`: Apptainer defitions file

## Steps to Reproduce

After installation ([below](#installation)) and downloading the [dataset_challenge.tar.gz](https://github.com/ICTV-VBEG/ICTV-TaxonomyChallenge/tree/main/dataset) file, 
the following steps will be needed to reproduce the results.

```bash
# Install the latest database (this can be skipped for the Apptainer version)
vcontact3 prepare_databases --get-version "223" --set-location /suitable/db/path
# Download ICTV challenge file
wget https://github.com/ICTV-VBEG/ICTV-TaxonomyChallenge/raw/refs/heads/main/dataset/dataset_challenge.tar.gz
# Decompress
tar xzf dataset_challenge.tar.gz
# Concatenate all files 
find dataset_challenge/ -type f -name "*.fasta" -print0 | xargs -0 cat > ICTVTaxoChallenge.fasta
# Remove the 59,907 files
rm -rf dataset_challenge
# Run vConTACT3
run --nucleotide ICTVTaxoChallenge.fasta --db-path /suitable/db/path --db-version 223 --output ICTVTaxoChallenge_vcontact3_run --db-domain prokaryotes --pyrodigal-gv --min-shared-genes 3
```

## Installation

Below are 3 ways of installing vConTACT3:

### Conda

The recommended means of installing vConTACT3 is to use an Anaconda-based package manager, such as [Mamba](https://github.com/conda-forge/miniforge):

```bash
mamba install -c bioconda vcontact3
```

### Pip

Pip can be used to install the latest version (always available on Bitbucket)

```bash
git clone https://bitbucket.org/MAVERICLab/vcontact3.git
cd vcontact3
python -m pip install .
```

Additionally, pip installs will require installing [MMSeqs2]((https://github.com/soedinglab/MMseqs2#installation))

### Singularity/Apptainer

A Singularity/Apptainer [definitions file](vcontact3.def) is provided.

```bash
# To build
sudo apptainer build vConTACT3.sif vcontact3.def
```

Other methods also exist. For the full set of instructions, please refer to the original [website](https://bitbucket.org/MAVERICLab/vcontact3/).

## Notes regarding the challenge

- As noted in the [steps to reproduce](#steps-to-reproduce), the original fasta file needed to be concatenated for input suitable for vContact3
- The version used to run was 3.0.0.b79, which is later than the latest available version on Bioconda (currently 3.0.0.b75). Bioconda will eventually update, but take care which version is being run.

### Reprodicibility

vConTACT3 is (as far as small-scale testing goes) 100% reproducible *post-profile* (*.<domain>.profile.pkl.gz), meaning 
that deleting files after that file is generated and re-running, will always generate equivalent outputs. This is due to 
the non-deterministic nature of MMSeqs2, which is used to generate protein clusters (and their IDs, most importantly) 
that vConTACT3 uses to assign protein cluster IDs. Re-running the tool from scratch may result in slightly different 
prediction **names**, though reference-associated taxonomic groups will be unaffected.