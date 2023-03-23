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

The **spatial extent** is a very flexible method that can be adapted to include many different methodologies to determine "abnormality". As such, the use cases and limitations highly depend on the methodology chosen. For methodology-specific drawbacks, please look at the tutorial, where a section for Use cases and limitations ADD REFERENCE TO PAGE is available for each of the methods currently in `sihnpy`.

Some general conditions to use the **spatial extent** are:
* Have more than 1 brain region under study
* Have data available for each brain region that, based on theory or observation, can be binarized or thresholded into "normal"/"abnormal" or "low"/"high" categories

Some general strengths and limitations in using this method:
|Strength|Limitations|
|:-------|:-----------|
| o Easy-to-apply individual-level <br> measure | x Need to binarize the data to get the measure <br> which might preclude complex data organization |
| o Easy to interpret (i.e., number of abnormal regions) | x Thresholds vary between methods and between data <br> collected, meaning that a high spatial extent in <br> one study might not be directly comparable to a  <br> different study |
| o Easy computational load | x Dependant on the number of regions included in the model, <br> which might differ between studies and which may <br> increase computational and logistical complexity |

```{note}
We developed this methodology with, in mind, Alzheimer's disease pathology (amyloid and tau) as measured with positron emission tomography; but any set of continuous brain measures (e.g., atrophy, thickness, connectivity) that **can be binarized or clustered** should be able to work with the spatial extent.
```

## Logistical considerations

No specific computational considerations are needed for this module: running all of its functions usually take under a minute.

This module was developed during an ongoing projet (St-Onge et al. (2023)) [^St_Onge_2023] using data from the Alzheimer's disease neuroimaging initiative, including a total of 832 participants and 70 brain regions. While the scripts rely mostly on quick `numpy`, `pandas`, `scikit-learn` and `scipy` functions, it hasn't been tested in much larger datasets or including a much higher number of brain regions and as such the computational time may differ if you are using voxel-wise data for instance.

Practical implications of using many regions and many thresholds may also complicate interpretations and management of the data.

## References

Below are a list of references discussed on this page. This list is not extensive, but present some key papers for the rationale behind the fingerprinting.