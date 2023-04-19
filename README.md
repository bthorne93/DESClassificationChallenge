# fairuniverse 

## Cosmology Challenge Description

Cosmologists use supernovae to infer the rate at which the Universe is expanding. Discovering new supernovae will allow us to better constrain this measurement, as well as explore the emerging internal conflicts within the standard model of cosmology. 

In this challenge, users will use data from the Dark Energy Survey (DES) to design a machine learning model for the automatic detection of new supernovae in DES data. 

## Description of the data 

The data in this challenge was first collated for classification tasks for use in the DES supernova transient detection pipeline in [Goldstein et al 2015](https://arxiv.org/abs/1504.02936), and was subsequently updated in [Ayyar et al (2022)](https://arxiv.org/abs/2203.09908). Each example of the dataset consists of three images, centered on a candidate source. This source may either be an astrophysical transient of scientific interest, or an artifcat produced by the pipeline (e.g. imperfect differencing of a foreground star, imperfect beam modeling, imprecise astrometry leading to off-centered differencing). 

There are 898,693 independent samples, each consisting three 51x51 pixel images ("search", "template", and "difference"), and have an associated label of either 1 (artifact) or 0 (non-artifact). Below is a plot of three independent data points, one on each row, with each image type in a different column. 

![](example_plot.png)

## Evaluation

This is a binary classification problem. Each triplet of images can be characterized as an artifcat (true) or a non-artifact (false). The classifier is scored by the AUC metric. 

![](fpt_mdr.png)

## Extensions

- Full dataset is large (~60 GB), work with just a subset? 
- 
- How to frame challenge as extension to CNN work done by Venkitesh?
