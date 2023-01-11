# Prevent-AD cohort data and datasets module

```{image} ../images/pad_logo.png
:align: center
:scale: 150
```

Data used in exemples for the different modules available were collected as part of the [PREVENT-AD cohort](http://dx.doi.org/10.14283/jpad.2016.121). After many years of work, the data was shared for [open access and use](https://doi.org/10.1016/j.nicl.2021.102733) by the research community, with data sharing enabled through the [Canadian Open Neuroscience Platform (CONP)](https://conp.ca/). Any qualified researcher can have access to the Open PREVENT-AD dataset available [here, in BIDS format](https://portal.conp.ca/dataset?id=projects/preventad-open-bids), by asking for access [here](https://openpreventad.loris.ca).

More information on the cohort:
> The PREVENT-AD (Pre-symptomatic Evaluation of Experimental or Novel Treatments for Alzheimer Disease) cohort is composed of cognitively healthy participants over 55 years old, at risk of developing Alzheimer Disease (AD) as their parents and/or siblings were/are affected by the disease. These ‘at-risk’ participants have been followed for a naturalistic study of the presymptomatic phase of AD since 2011 using multimodal measurements of various disease indicators. One clinical trial intended to test a pharmaco-preventive agent has also been conducted. The PREVENT-AD research group is now releasing data openly with the intention to contribute to the community’s growing understanding of AD pathogenesis. More detailed information about the study design can be found in the [LORIS instance of Open PREVENT-AD](https://openpreventad.loris.ca).
> From BIDS dataset on the CONP platform

The PREVENT-AD cohort contains information on over 318 participants, with rich phenotyping which includes multimodal imaging (T1, T2, fMRI, ASL, etc.), behavioral data, etc. A subset of 15 participants were downloaded, preprocessed and added to `sihnpy`. Details on the data integrated in `sihnpy` is available in [the next section](datasets_usage.md).

Due to the sheer size of the files, I don't recommend downloading the entire dataset, nor downloading the entire dataset on a personal computer. In my case, I have processed the data using the [Beluga cluster](https://docs.alliancecan.ca/wiki/B%C3%A9luga/en), a high-performance computing cluster managed by the [Digital Research Alliance of Canada](https://alliancecan.ca/en)

```{toctree}
datasets_usage.ipynb
download_pad_data.md
```