# Introduction to fingerprinting

**Welcome to the fingerprinting module!**

```{note}
While this code was tested and used for publication, it is still undergoing active development to improve it. Feel free to report any issues or suggestions by [opening an issue](https://github.com/stong3/sihnpy/issues)
```

## Rationale

Like in many fields, statistical analyses used in neuroimaging often rely on the assumption that **brains of similar individuals are relatively homogenous**; meaning that, for example, a group of 30 young individuals (18-30) can be grouped together without worrying too much that there might be important differences between them. However, many studies, mainly in the field of functional magnetic resonance imaging, have highlighted significant differences between individuals of the "same" group. [^Mueller_2013],[^Finn_2015] 

This is what prompted the development of the original functional connectome fingerprinting methodology by Finn et al. (2015)[^Finn_2015]. The general rationale behind **fingerprinting** is that if there is important variability between individuals in terms of brain connectivity patterns, the pattern of each individual should be unique, **just like a digital fingerprint**. Previous research has shown that these connectome fingerprints are indeed unique and accurate **1) across time**, **2) across functional MRI tasks** and **3) when using other neuroimaging modalities**. Note that in the package, particularly when using the {ref}` datasets module <0.pad_data/index:Prevent-AD cohort data and datasets module>` to practice, I will usually refer to fingerprinting using either the same modality over time or across functional MRI tasks.

## Definitions

The core idea behind **fingerprinting** is to determine how similar an individual is with themselves at a different point in time and whether this similarity is stronger than the similarity between said individual and rest of the sample. In principle, it's really not that different from the fingerprint on your fingertip!

```{figure} ../images/fp_metho.png
:name: Fingerprinting methodology
:scale: 30
:align: center

Illustration of the Fingerprinting methodology. In this method, an accurate fingerprint occurs when the correlation between the same individual across conditions is stronger than the correlation between the first person and any other individuals in the sample. In other words, a participant can be identified because their functional connectivity is unique to themselves across modalities.
```
<br>

Just like a digital fingerprint, a brain fingerprint is good when it can reliably identify the same individual over different conditions. In our context, this is determined by whether the correlation of the brain features of the same individual is higher than the correlation of the brain features of different individuals.

While there is no clear consensus in the field, we are using the definitions from Amico et al. (2018)[^Amico_2018] for the terms in the package.

```{admonition} Definitions
:class: important

- **Fingerprint identification accuracy**: whether a given individual was identified using a different brain imaging session
- **Self-identifiability**: within-individual correlation of two brain imaging sessions
- **Others-identifiability**: between-individual correlation of two brain imaging sessions
- **Differential identifiability**: the difference between the fingerprint strength and the alikeness coefficient. Effectively a measure of distance between how similar an individual is to themselves compared to others.
```

## Data type

**Fingerprinting** methodology has been used with different imaging modalities including fMRI[^Finn_2015], structural and diffusion MRI[^Mansour_2021]. It has also been used with imaging taken at multiple time points for every individuals.[^Finn_2015],[^Horien_2019] This measure could technically be applied to any type of data available for an individual where enough information is available (for example, extensive questionnaires and behavioral measures). *Note however that the quantity of data necessary per individual to make this work would need to be quite big; in functional MRI, small networks with a small number of edges (e.g., 20 nodes; 400 edges) tend to work poorly in identifying individuals*

The fingerprinting module currently expects two text files per participants: one text file per modality used for fingerprinting. It also expects at spreadsheet imported into Python (i.e., `pandas.DataFrame`) with the IDs of the participants.

Since `v0.4`, the fingerprinting module also accepts a long-format spreadsheet where each row represents a participant visit and each column is the value of interest in a cortical region. The `pandas.DataFrame` **must** have either a variable identifying the different visits OR you must supply two `DataFrame`s where each has a data for a specific visit. The functions are different from the matrix-input functions (refer to the {ref}`tutorial <1.fingerprinting/fp_tab_module:Fingerprinting analysis - Tabular data: Step-by-step>` for more information).

## Use cases and limitations

Generally, the conditions to use **fingerprinting** are:
* Highly dimensional data for each individual (e.g., measurements for many brain regions across the brain for a given individual)
* At least 2 different measurements for each individuals (either over time OR using different imaging modalities)
    * This last point is not strictly necessary if you are only interested in **others-identifiability** (i.e., see the work by Doucet et al. (2020)[^Doucet_2020]

**Fingerprinting** methodology has been used with different imaging modalities including fMRI[^Finn_2015], structural and diffusion MRI[^Mansour_2021]. It has also been used with imaging taken at multiple time points for every individuals.[^Finn_2015],[^Horien_2019] This measure could technically be applied to any type of data available for an individual where enough information is available (for example, extensive questionnaires and behavioral measures). *Note however that the quantity of data necessary per individual to make this work would need to be quite big; in functional MRI, small networks with a small number of edges (e.g., 20 nodes; 400 edges) tend to work poorly in identifying individuals*

|Strength|Limitations|
|:-------|:-----------|
| o Easy-to-apply individual-level <br> measure | x Hard to interpret (still unsure whether <br> a strong correlation is good or bad)|
| o Gives stable longitudinal measurements <br> in cognitively unimpaired cohorts| x Hard to determine which regions <br> contributes best to **fingerprinting**|
| o Can be done with whichever <br> combination of nodes you want | x Can be computationally demanding <br> if using many combinations |

```{warning}
A major difficulty in interpreting **fingerprinting** measures is that very little research has indicated whether or not having high or low fingerprint measures can indicate meaningful behavioral/clinical/biomarker changes. Some research (including my own) has showed that worse fingerprints were associated with mental health diagnoses[^Kaufmann_2017],[^Kaufmann_2018] and that lower brain volume was associated with lower **self-identifiability**. [^Ousdal_2020],[^St_Onge_2023]

However, it is still unclear how these fingerprints change with different diseases and disease stages. Caution should be used when interpreting the results from the fingerprinting analyses in the context of clinical applications.
```

## Logistical considerations

The fingerprinting module was written considering previous papers on the topic and without *much* consideration for very large sample sizes. In the original study where we used this methodology (St-Onge et al. (2023)[^St_Onge_2023]), we had close to 500 participants. One run of the fingerprinting script on the sample for a single network took around 2-3h. Therefore, careful consideration should be exercised when preparing and running this script.

The cause of this long run time is mostly due to the correlation between individuals being done sequentially (i.e., one correlation at a time). While not a priority, a future goal for this project would be to integrate some sort of parallel computing to cut down on the time needed to compute fingerprinting.

Here are some recommended parameters for using the script:
| Parameter | Amount |
|:-------|:-----------|
| CPU | 1 core |
| Memory | 4GB |

Again, some future considerations will aim to make this more efficient.

```{admonition} DRAC HPCs
:class: important

To mitigate the impact of the lack of parallelization of individual fingerprinting scripts, in St-Onge et al. (2023), most of the operations listed were done on Compute Canada's Beluga cluster. This way, fingerprint scripts could be assigned as individualized jobs with they own CPU and memory, which strongly accelerated the calculations.

Example scripts to launch this type of job on Compute Canada will soon be made available on `sihnpy`'s github page.
```

## References

Below is the list of references discussed on this page. This list is not extensive of the fingerprinting literature, but presents some key papers.

[^Mueller_2013]: Mueller et al. (2013). Neuron. [10.1016/j.neuron.2012.12.028](https://doi.org/10.1016/j.neuron.2012.12.028)
[^Finn_2015]: Finn et al. (2015). Nat Neuro. [10.1038/nn.4135](https://doi.org/10.1038/nn.4135)
[^Doucet_2020]: Doucet et al. (2020). JOURNAL. [10.1038/s41537-020-00128-x](https://doi.org/10.1038/s41537-020-00128-x)
[^Amico_2018]: Amico et al. (2018). Sci Reports. [10.1038/s41598-018-25089-1](https://doi.org/10.1038/s41598-018-25089-1)
[^Mansour_2021]: Mansour et al. (2021). Neuroimage. [10.1016/j.neuroimage.2020.117695](https://doi.org/10.1016/j.neuroimage.2020.117695)
[^Horien_2019]: Horien et al. (2019). Neuroimage. [10.1016/j.neuroimage.2019.02.002](https://doi.org/10.1016/j.neuroimage.2019.02.002)
[^Kaufmann_2017]: Kaufmann et al. (2017). Nat Neuro. [10.1038/nn.4511](https://doi.org/10.1038/nn.4511)
[^Kaufmann_2018]: Kaufmann et al. (2018). JAMA Psychiatry. [10.1001/jamapsychiatry.2018.0844](https://doi.org/10.1001/jamapsychiatry.2018.0844)
[^Ousdal_2020]: Ousdal et al. (2020). Hum Brain Mapp. [10.1002/hbm.24833](https://10.1002/hbm.24833)
[^Stonge_2023]: St-Onge F, Javanray M, Pichet Binette A, Strikwerda-Brown C, Remz J, Spreng RN, Shafiei G, Misic B, Vachon-Presseau E, Villeneuve S. (In press). Functional connectome fingerprinting across the lifespan. Network Neuroscience. doi: [10.1162/netn_a_00320](https://doi.org/10.1162/netn_a_00320)