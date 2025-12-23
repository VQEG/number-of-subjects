library(pwr)

alphas <- c(0.05, 0.01, 0.005, 0.001, 0.0005, 0.0001, 0.00005, 0.00001)
dvals <- seq(0.2,2.4,0.1)

p <- seq(.8,.8,.1)

ndvals <- length(dvals)
nalphas <- length(alphas)

sample_size_paired <- matrix(1:ndvals*nalphas, nrow=ndvals, ncol=nalphas)
for (j in 1:length(dvals)) {
    for (i in 1:nalphas) {
            result <- pwr.t.test(
              n=NULL, # Number of observations (per sample)
              d=dvals[j], # Effect size (Cohen's d) - difference between the means divided by the pooled standard deviation
              sig.level=alphas[i], # Significance level (Type I error probability
              power=p[1], # Power of test (1 minus Type II error probability)
              type="paired" # Type of t test : one- two- or paired-sampl
            )
            sample_size_paired[j,i] <- ceiling(result$n)
    }
}

sample_size_two_tailed <- matrix(1:ndvals*nalphas, nrow=ndvals, ncol=nalphas)
for (j in 1:ndvals) {
    for (i in 1:nalphas) {
            result <- pwr.t.test(
                n=NULL,
                d=dvals[j],
                sig.level=alphas[i],
                power=p[1],
                type="two.sample"
            )
            sample_size_two_tailed[j,i] <- ceiling(result$n)
    }
}