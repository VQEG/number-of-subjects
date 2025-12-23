library(tidyverse)
library(pwr)
library(broom)

d = expand.grid(
  d = seq(0.2, 2.4, 0.1),
  sig.level = c(0.05, 0.01, 0.005),
  power = 0.8,
  type = c("paired", "two.sample"),
  stringsAsFactors = FALSE
) %>%
  as_tibble %>%
  mutate(
    htest = pmap(., pwr.t.test) %>% map(tidy)
  ) %>%
  unnest(htest) %>%
  select(-sig.level1, -power1) %>%
  mutate_at("n", ceiling)
