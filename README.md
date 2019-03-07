# Calculations for Number of Subjects

This repository hosts scripts and data for estimating the required number of test subjects for typical Quality of Experience experiments.

The calculations are based on knowing:

- the number of statistical t-test comparisons to be performed
- the statistical significance level (alpha), typically 0.05
- the desired power of the test (1 - Type II error probability), typically 0.8
- the test conducted (paired or independent/two-sample), typically paired
- the expected effect size (expected MOS difference divided by standard deviation), which is automatically calculated

The result is the minimum number of subjects needed for the experiment in order to obtain enough data to perform statistical comparisons corrected for Type I errors.

# Shiny App

The calculations can be done interactively here:

https://slhck.shinyapps.io/number-of-subjects/

# Requirements

To run the scripts:

- R
- `pwr` package
- `tidyverse` package (optional)

More information about running these calculations in R can be found [here](https://stats.idre.ucla.edu/r/dae/power-analysis-for-two-group-independent-sample-t-test/).

# Authors

Code:

- Kjell Brunnström
- Werner Robitza

Concept and related material:

- Marcus Barkowsky
- Kjell Brunnström
- Gunnar Heikkilä
- David Lindero
- Werner Robitza