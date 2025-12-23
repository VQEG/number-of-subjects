# VQEGNumSubjTool — Calculations for Number of Subjects

This repository hosts scripts and a web tool for estimating the required number of test subjects for typical Quality of Experience experiments.

The calculations are based on knowing:

- the number of statistical t-test comparisons to be performed
- the statistical significance level (alpha), typically 0.05
- the desired power of the test (1 - Type II error probability), typically 0.8
- the test conducted (paired or independent/two-sample), typically paired
- the expected effect size (expected MOS difference divided by standard deviation), which is automatically calculated

The result is the minimum number of subjects needed for the experiment in order to obtain enough data to perform statistical comparisons corrected for Type I errors.

## Interactive App

The calculations can be done interactively here:

**https://vqeg.github.io/number-of-subjects/**

### Legacy Shiny App

A legacy version of this tool is available as an R Shiny app at https://slhck.shinyapps.io/number-of-subjects/. The source code is in the [`shiny/`](shiny/) directory. It uses R underneath.

## R Scripts

The R scripts used for the original calculations can be found in the [`scriptRs/`](scripts/R) directory. They require:

- R
- `pwr` package
- `tidyverse` package (optional)

More information about running these calculations in R can be found [here](https://stats.idre.ucla.edu/r/dae/power-analysis-for-two-group-independent-sample-t-test/).

## Python

A Python version of the calculations is available in [`scripts/python/power_analysis.py`](scripts/python/power_analysis.py). It uses [uv](https://docs.astral.sh/uv/) inline script dependencies, so no manual installation is required.

```bash
# Run with defaults (stdev=0.8, MOS diff=1.0, 100 comparisons)
uv run scripts/python/power_analysis.py

# Custom parameters
uv run scripts/python/power_analysis.py --stdev 1.0 --mos-diff 0.5 --comparisons 1000

# Independent (two-sample) t-test instead of paired
uv run scripts/python/power_analysis.py --test-type independent

# Generate sample size tables (replicates R script output)
uv run scripts/python/power_analysis.py --table

# Interactive mode
uv run scripts/python/power_analysis.py --interactive

# JSON output for programmatic use
uv run scripts/python/power_analysis.py --json
```

## Background

The script contained in this repository was used for some of the calculations done for the article Brunnström and Barkowsky [1].

### Brief background

In video quality assessment experiments, panels of observers rate the quality of video clips that have been degraded in various ways. When analyzing the results, the experimenter often computes the mean over the experimental observations, a.k.a. the Mean Opinion Scores (MOS) and applies statistical hypothesis tests to draw statistical conclusions. A statistical hypothesis test is done by forming a null hypothesis (H0) and an alternative hypothesis (H1) that can be tested against each other. The hypothesis test will have the null hypothesis, H0, that two underlying MOS values are the same and the alternative hypothesis, H1, that they are different. If the result of the hypothesis test is significant, the experimenter knows with high probability (typically 95%) that H1 is true and thus the MOS values are different. However, there is still a small risk (5% in this case) that this observation is only by chance. If this happens, it is a Type I error—to incorrectly conclude that H1 is true when in reality H0 is true. When there are more pairs of MOS values to compare, each comparison has the above-mentioned small risk of error.

An example is trying to roll the dice and get the number six. If the dice is rolled once, there will be a probability of one-sixth to get the desired number six, and each time the dice is rolled the probability will be the same. However, the overall chance will increase with the number of times the dice is rolled. The same applies to risk of an error, which increases with the number of comparisons and can be estimated by 1 – (1 – α)n, where α is the risk to have an error at a certain confidence level per comparison and n is the number of comparisons.  For 100 comparisons at a 95% confidence level, this equal >99% risk of at least one Type I error.

The Bonferroni method [2] may be used to control for Type-I errors, where the considered significance level (α) must be divided by the number of comparisons (n) so that the significance level for each comparison will be α/n. For example, if there are 10 comparisons and the overall α = 0.05, then each comparison must have a significance level of 0.05/10 = 0.005.

In subjective video quality assessment based on standardized procedures category scales such as absolute category rating (ACR) is one of the most commonly used scales and especially its five-level version: excellent, good, fair, poor, and bad. We have looked at the interesting cases of MOS differences of 0.5 and 1.0 on a five-level scale. A MOS difference of 0.5 and 1 was chosen as they represent typical targets. One way to motivated it is based on the quantization of the ACR scale, the observers are forced to vote for an integer value even if their opinion is in between two attributes. A single observer who decides one way or the other changes the MOS score by 1/m (m being the number of observers). To obtain a MOS difference of 0.5, half the observers need to change their opinion and all need to change their opinion to get a MOS difference of 1.

### Implication for number of test subjects

The number of test subjects needed for a particular experiment is highly dependent on the planned number of comparisons, the expected standard deviation, and the difference in Mean Opinion Scores that is of interest. This can be seen in Table 1. For example; for a rather moderately sized experiment consisting of 100 videos, where it has been decided that only 100 comparisons should be performed i.e. one per video, and it is only interesting to find effects with about one MOS level of difference (e.g. good to fair), then 18 or 25 test subjects are needed depending on the expected standard deviation. On the other hand, if it is interesting to find smaller differences and all pairwise comparisons are investigated (i.e. 4950 comparison), then 81 or 121 test subjects are needed.

## References

- [1] Brunnström, K. and M. Barkowsky, Statistical quality of experience analysis: on planning the sample size and statistical significance testing. Journal of Electronic Imaging, 2018. 27(5): p. 11. ([Full text](http://urn.kb.se/resolve?urn=urn%3Anbn%3Ase%3Ari%3Adiva-35233))
- [2] Maxwell, S.E. and H.D. Delaney, Designing experiments and analyzing data: a model comparison perspective. 2nd ed. 2003, Mahwah, New Jersey, USA: Lawrence Erlbaum Associates, Inc.
- [3] Holm, S., A Simple Sequentially Rejective Multiple Test Procedure. Scandinavian Journal of Statistics, 1979. 6(2): p. 65-70.
- [4] Benjamini, Y. and D. Yekutieli, The Control of the False Discovery Rate in Multiple Testing under Dependency. The Annals of Statistics, 2001. 29(4): p. 1165-1188.
- [5] Benjamini, Y. and Y. Hochberg, Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing. Journal of the Royal Statistical Society. Series B (Methodological), 1995. 57(1): p. 289-300.

## Authors

Code:

- Kjell Brunnström
- Werner Robitza

Concept and related material:

- Marcus Barkowsky
- Kjell Brunnström
- Gunnar Heikkilä
- David Lindero
- Werner Robitza

## License

Copyright (c) 2019 Kjell Brunnström, Werner Robitza

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
