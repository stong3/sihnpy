# Introduction to sliding-window analysis

**Welcome to the sliding-window module!**

```{note}
While this code was tested and used for publication, it is still undergoing active development to improve it. Feel free to report any issues or suggestions by [opening an issue](https://github.com/stong3/sihnpy/issues)
```

## Rationale

```{warning}
The term **sliding-window** is often used in dynamic functional connectivity as a method of selecting different segments of functional connectivity during time. While the principle is similar, the goal is significantly different. All mentions of **sliding-window** in this module refer to **sample selection** and not dynamic functional connectivity.
```

The **sliding-window** analysis is slightly different from other analyses presented in `sihnpy`; contrary to most other analyses, the **sliding-window** could be better defined as a **sample-selection tool** rather than a purely statistical method. [^Vasa_2018]

The goal behind this method is to **generate overlapping sub-groups of participants based on a characteristic of the sample** [^Vasa_2018],[^Stonge_2023]. For example, let's take the original study using this methodology. In the study by Vasa et al. (2018),[^Vasa_2018] they had a sample of adolescents and young adults (n=297) aged between 14 and 24 years in which they wanted to study structural covariance changes during development. In such studies, one could decide to split the sample in a predetermined number of sub-samples (e.g., 14-15, 16-17, 18-19, 19-20, 20-21, 21-22, 22-23). But there are some inconvenients to this:

1) The divisions can be quite arbitrary or based on literature that doesn't necessarily fit with the current sample
2) The divisions could also miss more subtle change over time. For example, if a change in structural covariance in a specific region occurs between 14 and 16 years of age, you may notice the change in the first sub-group, but not the second.
3) The divisions could also incur bias depending on who is included in the sample. For instance, if a specific structural covariance is observed in the 14-15 group but is only driven by a few participants, this could be missed by the researchers.

The **sliding-window** analysis, while not perfect, aims to offer a more data-driven way to separate a sample while also accounting for the caveats mentioned above.

## Definitions

The **sliding-window** is defied as an **ordered sample selection method in which sub-samples of overlapping participants are created. The order is determined by ordering the variable researchers think may impact the outcome of interest.** In plain English, the **sliding-window** create overlapping samples based on a variable of interest.

Obviously, the variable chosen needs to be **continuous** as a categorical variable would already lend itself to spliting participants in groups.

```{admonition} Definitions
:class: important
- **Window**: Subsample of participants selected. Usually preceeded by the variable used to create the subsamples (e.g., age windows).
- **Window size**: Size of each subsample selected by the **sliding-window** method
- **Step size**: Inverse of the overlap between windows; i.e., if a window size is 100 participants and the step size is 20 participants, it means that the overlap between two windows is 80 participants. See Figure below for more details.
```

The **step size** of a **sliding-window** analysis is not particularly intuitive. Think of it this way: when we sort our participants, we select them by "sliding" across the ordered participant and selecting our windows. The **step size** is an indication of **how much** should we slide before selecting the next window of participants. A quick illustration below

```{figure} ../images/sw/sw_explanation.png
:name: Sliding-window methodology
:scale: 30
:align: center
```
*Illustration of the sliding-window approach to select sub-groups of participants. Subsamples of participants (window size) are chosen iteratively by taking the participants from the cohort, ordered by variable of interest, and slowly moving along (step size) the variable of interest. The half-rectangle represents the first window selected by the method while dotted half-rectangles represent the next few windows to be selected. This method yields subsets of overlapping participants across the original sample, offering a cross-sectional, semi-continuous overview of changes. Adapted from St-Onge et al. (2023).*[^Stonge_2023]

## Data type

The **sliding-window** currently only works for tabular (i.e., spreadsheet) data. Specifically, data input into `sihnpy` should be a `pandas.DataFrame` with the index set as the participants' IDs and the `DataFrame` should have the variable you want to use to create the windows. The variable used to create the windows should be continuous.

## Use cases and limitations

The **sliding-window** approach is a flexible and agnostic sample selection tool; it really only depends on your research question and the choices you make when selecting the window size and step size.

Some general strengths and limitations in using this method:
|Strengths|Limitations|
|:-------|:-----------|
| o Easy-to-apply sample selection method | x Requires the user to choose <br> a window size and a step size manually <br> which can be arbitrary |
| o Easy to use and input ready for next analyses | x Doesn't directly target individual differences, <br> but rather zooms in on group variability |
| o Easy computational load | x Using multiple sliding-window parameters <br> (i.e., multiple window and step size) are <br> necessary to insure the arbitrary choices <br> are justified, but this generally complicates the results <br> necessary to report as many <br> more figures are needed.|

## Logistical considerations

There are no specific computational considerations to consider for this module: running all of its function usually take under a minute. Functions run with fast vectorized `pandas` and `numpy` operations.

That said, it might be a different story for very large data files (with a lot of variable and/or participants). `sihnpy` will also create a lot of files following the **sliding-window** analysis (2 files per window). If your system as a file number limit, this may cause an issue if you make `sihnpy` create a large amount of windows.

Finally, as a general recommendation, you should compute **sliding windows** with multiple parameter combinations to ensure that your results are not driven by the specific grouping. That said, this usually complicates results and increases the logistic complexity, particularly for figures.

## Future considerations

There aren't currently a lot of future updates planned for the **sliding-window** analysis in `sihnpy`. However, one of them will be to include a brief tutorial on how to plot data from the **sliding-window** method in an efficient way.

## References

Using a **sliding-window** approach for participants has not been used extensively in the literature. Here are a few references using this method.

[^Vasa_2018]: Váša F, Seidlitz J, Romero-Garcia R, Whitaker KJ, Rosenthal G, Vértes PE, Shinn M, Alexander-Bloch A, Fonagy P, Dolan RJ, Jones PB, Goodyer IM; NSPN consortium; Sporns O, Bullmore ET. Adolescent Tuning of Association Cortex in Human Structural Brain Networks. Cereb Cortex. 2018 Jan 1;28(1):281-294. doi: 10.1093/cercor/bhx249. PMID: 29088339; PMCID: PMC5903415.
[^Stonge_2023]: St-Onge et al. (Accepted). Network Neuroscience.