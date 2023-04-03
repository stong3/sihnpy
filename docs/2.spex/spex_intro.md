# Introduction to spatial extent

**Welcome to the spatial extent module!**

```{note}
While this code was tested and used for publication, it is still undergoing active development to improve it. Feel free to report any issues or suggestions by [opening an issue](https://github.com/stong3/sihnpy/issues)
```

## Rationale

If you are a neuroscientist like I am, one of the questions that probably occupies a lot of your time is **where** in the brain a certain phenomenon occurs. This is reflected by the vast plethora of software available to look at the brain [(a few examples here, if you are curious on how to do this)](https://sidchop.shinyapps.io/braincode_selector).

In Alzheimer's disease, the discipline I specialized on during my PhD, a hot current topic (or well at the time of writing this guide) is **where** tau pathology--a hallmark of the disease--deposits in the brain. Traditionally, tau was thought to follow a specific "trail" in the brain: the pathology would accumulate first in the medial temporal lobe, before encroaching on the rest of the temporal lobe and, finally, expand to the rest of the cortex. This is called the Braak stages of tau pathology. [^Braak_1995]

For a long time, it was assumed that this pathway was **homogenous across individuals**. However, like we I discuss in the {ref}` fingerprinting module <1.fingerprinting/fp_intro:Rationale>`, everyone's brain is different: so should we really expect that the way the pathology goes through the brain is exactly the same for everyone?

Specifically in the field of Alzheimer's disease, some recent (again, at the time of writing) studies have found that this is not exactly the case. Sure, there are common patterns across people of where we expect to see tau, particularly in the medial temporal lobe [^Therriault_2022][^Vogel_2020], but the patterns of tau can change between individuals [^Vogel_2021] and depending on the clinical presentation. [^Singleton_2020][^Lajoie_2020] This means that a single set of region or a single pattern of progression of the disease might not fit everyone properly.

So, how can we better target the progress of tau in the brain accounting for individual differences? This is where the **spatial extent** comes in.

## Definitions

We define the **spatial extent** as the **extent (number) of brain regions with "abnormal" values for a specific disease marker**.

What do we mean by abnormal here? We developed the **spatial extent** methodology with, in mind, Alzheimer's disease pathology (amyloid and tau) as measured with positron emission tomography. While I did mention that there is some doubt as to **where** the pathology deposits in the brain, we do know from overwhelming evidence that:
1) People who develop the disease **consistently have more** pathology [^Jagust_2018]
2) Most people without the disease will have low values (normally distribution, but very tight) of pathology, while people on their way to the disease will have high values of pathology (normally distributed, but very spread out) [^Mormino_2014] [^Vogel_2020] [^Ozlen_2022]

Using these assumptions, we can then zoom in each brain region and take a look at who has abnormally high values in a given region. Since we look at each region separately, we can paint a very specific and individualized portrait of tau pathology uptake for each individual. Perhaps person A has 5 regions with abnormally high regions, while person B has 7. We can also check whether these regions overlap.

But perhaps the best advantage of this method is that we can **summarize, for each individual, the extent to which a given pathology is spread out in the brain**. This is done very simply; by summing the number of regions that have abnormal levels of pathology in a given person. We then get a simple, individualized measure of just how much pathology is in the brain, in a data-driven way and that also ignore potential biases of using the same set of regions for each individual.

Below are a few definitions for terms I will reuse across the documentation. Note that the definitions here might be a bit broad, as the **spatial extent** can be calculated in many different ways, which come with their own definition. More info in the tutorial page. ADD REFERENCE TO PAGE HERE

```{admonition} Definitions
:class: important

- **Spatial extent**: the extent to which a given pathology is present across the brain
- **Spatial extent index**: The sum of regions with abnormal levels of pathology in a given individual
- **Spatial extent individualized mask**: A weighted mask of the original pathology values, where regions with no abnormal values are set to 0. This can be useful in cases where you want to use continuous values in the same scale as the original data, but want to leverage the abnormality status by region.
```

## Use cases and limitations

The **spatial extent** is a very flexible method that can be adapted to include many different methodologies to determine "abnormality". As such, the use cases and limitations highly depend on the methodology chosen. For methodology-specific drawbacks, please look {ref}`at the tutorial <2.spex/spex_module:Spatial extent analysis>` for each of the methods currently implemented in `sihnpy`.

Some general conditions to use the **spatial extent** are:
* Have more than 1 brain region under study
* Have data available for each brain region that, based on theory or observation, can be binarized or thresholded into "normal"/"abnormal" or "low"/"high" categories

Some general strengths and limitations in using this method:
|Strength|Limitations|
|:-------|:-----------|
| o Easy-to-apply individual-level <br> measure | x Need to binarize the data to get the measure <br> which might preclude complex data organization |
| o Easy to interpret (i.e., number of abnormal regions) | x Thresholds vary between methods and between data <br> collected, meaning that a high spatial extent in <br> one study might not be directly comparable to a <br> different study |
| o Easy computational load | x Dependant on the number of regions included in the model, <br> computational and logistical complexity may increase |

```{note}
We developed this methodology with, in mind, Alzheimer's disease pathology (amyloid and tau) as measured with positron emission tomography; but any set of continuous brain measures (e.g., atrophy, thickness, connectivity) that **can be binarized or clustered** should be able to work with the spatial extent.
```

## Logistical considerations

No specific computational considerations are needed for this module: running all of its functions usually take under a minute.

This module was developed during an ongoing projet (St-Onge et al. (2023)) [^Stonge_2023] using data from the Alzheimer's disease neuroimaging initiative, including a total of 832 participants and 70 brain regions. While the scripts rely mostly on quick `numpy`, `pandas`, `scikit-learn` and `scipy` functions, it hasn't been tested in much larger datasets or including a much higher number of brain regions and as such the computational time may differ if you are using voxel-wise data for instance.

Practical implications of using many regions and many thresholds may also complicate interpretations and management of the data.

## References

Below are a list of references discussed on this page. This list is not extensive, but present some key papers for the rationale behind the fingerprinting.

[^Braak_1995]: Braak H, Braak E. Staging of Alzheimer's disease-related neurofibrillary changes. Neurobiol Aging. 1995 May-Jun;16(3):271-8; discussion 278-84. doi: 10.1016/0197-4580(95)00021-6. PMID: 7566337.
[^Therriault_2022]: Therriault, J., Pascoal, T.A., Lussier, F.Z. et al. Biomarker modeling of Alzheimer’s disease using PET-based Braak staging. Nat Aging 2, 526–535 (2022). https://doi.org/10.1038/s43587-022-00204-0
[^Vogel_2020]: Vogel JW, Iturria-Medina Y, Strandberg OT, Smith R, Levitis E, Evans AC, Hansson O; Alzheimer’s Disease Neuroimaging Initiative; Swedish BioFinder Study. Spread of pathological tau proteins through communicating neurons in human Alzheimer's disease. Nat Commun. 2020 May 26;11(1):2612. doi: 10.1038/s41467-020-15701-2. Erratum in: Nat Commun. 2021 Aug 5;12(1):4862. PMID: 32457389; PMCID: PMC7251068.
[^Vogel_2021]: Vogel JW, Young AL, Oxtoby NP, Smith R, Ossenkoppele R, Strandberg OT, La Joie R, Aksman LM, Grothe MJ, Iturria-Medina Y; Alzheimer’s Disease Neuroimaging Initiative; Pontecorvo MJ, Devous MD, Rabinovici GD, Alexander DC, Lyoo CH, Evans AC, Hansson O. Four distinct trajectories of tau deposition identified in Alzheimer's disease. Nat Med. 2021 May;27(5):871-881. doi: 10.1038/s41591-021-01309-6. Epub 2021 Apr 29. PMID: 33927414; PMCID: PMC8686688.
[^Singleton_2020]: Singleton EH, Pijnenburg YAL, Sudre CH, Groot C, Kochova E, Barkhof F, La Joie R, Rosen HJ, Seeley WW, Miller B, Cardoso MJ, Papma J, Scheltens P, Rabinovici GD, Ossenkoppele R. Investigating the clinico-anatomical dissociation in the behavioral variant of Alzheimer disease. Alzheimers Res Ther. 2020 Nov 14;12(1):148. doi: 10.1186/s13195-020-00717-z. PMID: 33189136; PMCID: PMC7666520.
[^Lajoie_2020]: La Joie R, Visani AV, Lesman-Segev OH, Baker SL, Edwards L, Iaccarino L, Soleimani-Meigooni DN, Mellinger T, Janabi M, Miller ZA, Perry DC, Pham J, Strom A, Gorno-Tempini ML, Rosen HJ, Miller BL, Jagust WJ, Rabinovici GD. Association of APOE4 and Clinical Variability in Alzheimer Disease With the Pattern of Tau- and Amyloid-PET. Neurology. 2021 Feb 2;96(5):e650-e661. doi: 10.1212/WNL.0000000000011270. Epub 2020 Dec 1. PMID: 33262228; PMCID: PMC7884991.
[^Jagust_2018]: Jagust W. Imaging the evolution and pathophysiology of Alzheimer disease. Nat Rev Neurosci. 2018 Nov;19(11):687-700. doi: 10.1038/s41583-018-0067-3. PMID: 30266970; PMCID: PMC7032048.
[^Mormino_2014]: Mormino EC, Betensky RA, Hedden T, Schultz AP, Ward A, Huijbers W, Rentz DM, Johnson KA, Sperling RA; Alzheimer's Disease Neuroimaging Initiative; Australian Imaging Biomarkers and Lifestyle Flagship Study of Ageing; Harvard Aging Brain Study. Amyloid and APOE ε4 interact to influence short-term decline in preclinical Alzheimer disease. Neurology. 2014 May 20;82(20):1760-7. doi: 10.1212/WNL.0000000000000431. Epub 2014 Apr 18. PMID: 24748674; PMCID: PMC4035706.
[^Ozlen_2022]: Ozlen H, Pichet Binette A, Köbe T, Meyer PF, Gonneaud J, St-Onge F, Provost K, Soucy JP, Rosa-Neto P, Breitner J, Poirier J, Villeneuve S; Alzheimer’s Disease Neuroimaging Initiative, the Harvard Aging Brain Study, the Presymptomatic Evaluation of Experimental or Novel Treatments for Alzheimer Disease Research Group. Spatial Extent of Amyloid-β Levels and Associations With Tau-PET and Cognition. JAMA Neurol. 2022 Oct 1;79(10):1025-1035. doi: 10.1001/jamaneurol.2022.2442. PMID: 35994280; PMCID: PMC9396472.
[^Stonge_2023]: St-Onge et al. (2023). In preparation