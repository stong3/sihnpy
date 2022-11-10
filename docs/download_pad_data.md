# Using the Prevent-AD Open Data from the Canadian Open Neuroscience Platform (CONP)

Data used in exemples for the different modules available were collected as part of the [PREVENT-AD cohort](http://dx.doi.org/10.14283/jpad.2016.121). After many years of work, the data was finally shared for [open access](https://doi.org/10.1016/j.nicl.2021.102733) by the research community, with data sharing enabled through the [Canadian Open Neuroscience Platform (CONP)](https://conp.ca/). Any qualified researcher can have access to the Open PREVENT-AD dataset available [here, in BIDS format](https://portal.conp.ca/dataset?id=projects/preventad-open-bids), by asking for access [here](https://openpreventad.loris.ca).

More information on the cohort:
> The PREVENT-AD (Pre-symptomatic Evaluation of Experimental or Novel Treatments for Alzheimer Disease) cohort is composed of cognitively healthy participants over 55 years old, at risk of developing Alzheimer Disease (AD) as their parents and/or siblings were/are affected by the disease. These ‘at-risk’ participants have been followed for a naturalistic study of the presymptomatic phase of AD since 2011 using multimodal measurements of various disease indicators. One clinical trial intended to test a pharmaco-preventive agent has also been conducted. The PREVENT-AD research group is now releasing data openly with the intention to contribute to the community’s growing understanding of AD pathogenesis. More detailed information about the study design can be found in the [LORIS instance of Open PREVENT-AD](https://openpreventad.loris.ca).
> From BIDS dataset on the CONP platform

The PREVENT-AD cohort contains information on over 318 participants, with T1 and resting-state fMRI sequences being available. A subset of 100 participants were downloaded and used for the analyses presented in this Python package. Due to the sheer size of the files, I don't recommend downloading the entire dataset, nor downloading the entire dataset on a personal computer. In my case, I have processed the data using the [Beluga cluster](https://docs.alliancecan.ca/wiki/B%C3%A9luga/en), a high-performance computing cluster managed by the [Digital Research Alliance of Canada](https://alliancecan.ca/en)

Below are the steps to take to obtain and preprocess the data should you be interested.

## Step 1 - Downloading the dataset

The PREVENT-AD's open access dataset is enabled through [Datalad](https://handbook.datalad.org/en/latest/index.html). Instructions to download the dataset are [here](https://portal.conp.ca/dataset?id=projects/preventad-open-bids). Note that instructions vary depending on what platform you are downloading the dataset.

Datalad downloads (`datalad install`) a set of symbolic links to avoid having to download the entire dataset locally all at once. Once the dataset is installed, you can then get the data using `datalad get <filepath>`, where `filepath` is the path to the file you want to download. Once you use `datalad get`, you will be prompted to enter your username and password for the [LORIS Open dataset](https://openpreventad.loris.ca). Normally, you should only enter this password once, and datalad should remember it next time `datalad get` is run.

To download the data of a full participant at once, you can do `datalad get -r sub-001`, where sub-001 is the subject number.

```{note} Datalad on an HPC
Datalad is usually very easy to install, but may require a bit more work to install on a super computer. Datalad has more extensive information on the topic [here](https://handbook.datalad.org/en/latest/intro/installation.html#linux-machines-with-no-root-access-e-g-hpc-systems).

Specific instructions on how to install a dataset on the Digital Research Alliance of Canada (previously Compute Canada) are available [here](https://cbs-discourse.uwo.ca/t/installing-datalad-on-compute-canada/23).

Briefly, `git-annex` and `python/3` should already be installed on the DRAC's clusters. The code below should install datalad.

`module load git-annex python/3` --> Load git-annex and Python, dependencies for Datalad
`virtualenv ~/venv_datalad` --> Create a virtual environment for Datalad
`source ~/venv_datalad/bin/activate` --> Source the virtual environment to use `pip` to install
`pip install datalad` --> Install datalad using `pip`

The rest of the instructions for the PREVENT-AD dataset can then be followed [here](https://portal.conp.ca/dataset?id=projects/preventad-open-bids).

**Note:** It is impossible to download data from the internet using a compute node on DRAC's clusters (or at least on Beluga as I have been using). However, the memory usage allowed on a login node is also limited, as the cluster will kill a user's access if the memory usage is too much. The recommendation for now is to force a single `get` command at a time to ensure that a single subject is downloaded at a time, and to force datalad to only download a single file at a time, with the code below

`datalad get -r -J 1 sub-001`
```

Once `datalad get` is executed, the files are downloaded locally and can then be moved or copied. Moving or copying the data before `get` is run will only result in copying the symbolic links, which means it will no longer be working.

## Step 2 - Preprocessing the fMRI data

Before any analysis can be run, we need to preprocess the data. I used [fMRIPrep v.X.X](https://fmriprep.org/en/stable/) to preprocess the data.