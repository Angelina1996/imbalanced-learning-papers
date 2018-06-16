
# Learning from imbalanced data sets: a comparison of various strategies

## Contributions

  - Looks at basic data characterization/factors on difficulty
  - Compares methods (random under-sampling, random over-sampling, boundary-focused resampling, basic recognition) on simple synthetic data.
  
## Summary

### Data factors/characterization

  - Data generated synthetically with 'backbone' model; essentially alternating classes on the number line, where their definition of 'complexity' is related to the number of alternations over the given interval.
  - Important to note very complex data gives poor accuracy even for non-imbalanced data, so important to make any comparisons with this in mind.
  - Linearly separable data not sensitive to any degree of imbalance, regardless of training set size.
  - More complex data more sensitive to imbalance; increasing complexity correlated with increased sensitivity to imbalance.
  - Suggests that we should concentrate both on (reducing) complexity and re-balancing the data as the most important aspects of the problem.
  
### Methods

  - Purely random over- and under-sampling found to work reasonably well, especially as higher complexities.
  - Boundary-focused resampling (over- and under-) found to work about as well as purely random; no suggestion that these perform notably better.
  - Down-sampling appears to work better than over-sampling for large domains.
  - Recognition-based approach doesn't work as well until the data is at the highest complexities.
  - Recognition-based expected to perform better when there are very few minority class examples.
  - Recognition-based methods that learn the majority class work **much** better than those which learn the minority class.

## Evaluation & Future Work

  - Only tests on *very* simple synthetic data.  More complex data might show different trends/results.  In particular:
    - Data are 1-dimensional
    - Adhere to simple 'backbone' model
    - 'Balanced imbalance' only; no sub-clustering of the classes with different characteristics.
  - Only makes use of simple feed-forward networks.
  - Only tests simple methods.