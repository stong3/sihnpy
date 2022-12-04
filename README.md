# sihnpy: Study of inter-individual heterogeneity of neuroimaging in Python

:sunny: Welcome to `sihnpy`! :sunny:

My goal in creating `sinhpy`'s goal was to provide researchers with an easy-to-use, one-stop-shop for simple methods and analyses aimed at studying inter-individual differences in neuroimaging. 

Over the past few years, studies using multiple brain imaging modalities have highlighted that individuals in homogenous groups tend to show considerable inter-individual differences. This leads to several challenges:
1) Comparing groups considered to be relatively homogenous may lead to hard-to-reproduce results as individual variability will not be the same from cohort to cohort
2) Developping biomarkers and treatments using group-based methods may not suit all participants, particularly when a specific disease shows a lot of heterogeneity

As such, during my PhD program, I aimed to study these inter-individual differences in aging and Alzheimer's disease. However, many times I got stuck as either there was no package existing to study a specific measure of inter-individual differences, the package was written in a different programming language or was difficult to use. 

This lead us to develop `sinhpy`, as a way to adapt and store existing methodology and create new methods to study inter-individual differences. Full documentation available here: (LINK)

Please note that I do not have a formal computing background and I am learning software development as the package moves forward. I welcome any advice and contribution you may have!

## Authors
Frédéric St-Onge - MSc - PhD candidate at McGill University

Gabriel St-Onge - MSc - Research Scientist

If you use `sinhpy`, please consider citing the paper detailing the development of the first few modules of this package (REF).
Also consider citing the package directly: (ADD CITATION)

## Installation

You can install the most recent version of `sinhpy` using pip:

```bash
$ pip install sihnpy
```

## Usage

The package contains multiple different tools, each with their own usage. More information is available in the documentation (LINK HERE). A short summary of the tools available is made here:
- Fingerprinting - Computes individual-specific brain signatures of each individual and the related metrics

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`sihnpy` was created by Frederic St-Onge. It is licensed under the terms of the MIT license.

## Credits

`sihnpy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter). This package was developped alongside my reading of the book *Python packages*, an open-source book written by Tomas Beuzen & Tiffany Timbers, available [here](https://py-pkgs.org/welcome).