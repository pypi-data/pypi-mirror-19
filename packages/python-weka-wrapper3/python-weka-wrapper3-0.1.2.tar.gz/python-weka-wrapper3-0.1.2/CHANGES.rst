Changelog
=========

0.1.2 (2017-01-04)
------------------

- `typeconv.double_matrix_to_ndarray` no longer assumes a square matrix
  (https://github.com/fracpete/python-weka-wrapper3/issues/4)
- `len(Instances)` now returns the number of rows in the dataset (module `weka.core.dataset`)
- added method `insert_attribute` to the `Instances` class
- added class method `create_relational` to the `Attribute` class
- upgraded Weka to 3.9.1


0.1.1 (2016-10-19)
------------------

- `plot_learning_curve` method of module `weka.plot.classifiers` now accepts a list of test sets;
  `*` is index of test set in label template string
- added `missing_value()` methods to `weka.core.dataset` module and `Instance` class
- output variable `y` for convenience method `create_instances_from_lists` in module
  `weka.core.dataset` is now optional
- added convenience method `create_instances_from_matrices` to `weka.core.dataset` module to easily create
  an `Instances` object from numpy matrices (x and y)


0.1.0 (2016-05-09)
------------------

- initial release of Python3 port



