
# Handling imbalanced datasets: A review

## Contributions

  - Provides a review of methods for imbalance classification to date.

## Summary

  - Distinguishes between data-level and algorithm-level methods.
  - Data-level methods here focus on various resampling approaches: random, directed.
  - Algo-level: adjusting the costs of the various classes so as to counter the class imbalance, adjusting the decision threshold, and recognition-based (i.e., learning from one class) rather than discrimination-based (two class) learning.  Also mentions mixture-of-experts, which combines the results of more than one classifier.
  - Many learning methods prefer majority class.

### Data-level

  - Random undersampling discards potentially useful data.
  - "Another problem with this approach is that the purpose of machine learning is for the classifier to estimate the probability distribution of the target population. Since that distribution is unknown we try to estimate the population distribution using a sample distribution. Statistics tells us that as long as the sample is drawn randomly, the sample distribution can be used to estimate the population dis- tribution from where it was drawn. Hence, by learning the sample distribution we can learn to approximate the target distribution. Once we perform undersampling of the majority class, however, the sample can no longer be considered random."
  - Tomek links - "can be used as an under-sampling method or as a data cleaning method. As an under-sampling method, only examples belonging to the majority class are eliminated, and as a data cleaning method, examples of both classes are removed."

### Algo-level

### Combined methods

## Evaluation & Future Work