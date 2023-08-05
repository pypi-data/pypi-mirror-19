
Why?
----



* We regularly misconceive the `Mean` as the `Most likely value`. This regularly leads to fatal decisions, actions and results.
* The `Most likely value` however, must not be confused with the mode.

* `Mean`: equal sum of deviations
* `Median`: equal number of deviations
* `Most likely value`: highest density of values

Example: Let's take a look on missing teeth among 966 young German adults (2015):

* Mean: 2 / Median: 1 / Most likely value: ⅓ 
* ⅕ th of 966 young German adults make up ⅔ rds of all of their missing teeth in 2015.

If you want the second, `effectus` is for you.




We know three principal statistical measures:

* `Mean`: equal sum of deviations
* `Median`: equal number of deviations
* `Most likely value`: what we actually misconceive `mean` to be (not to be confused with the mode)

Each has its deficiencies:

* `Mean`

  * is quite often a value that is very unlikely to expect.
  * assumes that all observations are equal — it robs the value from the value!
  * in short: if you base your decision on it, it is likely to act against reality.

* `Median`

  * is still quite indifferent to the most probable value.

* `Most likely value`

  * is the value which is most likely.
  * is too complicated and unreliable to calculate.
  * can not be directly translated into action.

.



Features
--------

* Employs entropy based model by `Grosfeld-Nir, Ronen and Kozlovsky <http://www.boazronen.org/PDF/The%20Pareto%20managerial%20principle%20-%20when%20does%20it%20apply.pdf>`_.
* CLI tools that read directly CSV data.
* CLI tools that read directly from Excel (`Demo <https://youtu.be/eymcGbplVUg>`_) — no export required.
* 11 real life data sets where a pareto distribution is present.



Statistics
----------

* 43 functions, 6 classes
* 685 lines of code (7 files) / 693 for testing (5 files)
