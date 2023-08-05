"""
*******************************
Generalized Linear Mixed Models
*******************************

Example
^^^^^^^

.. doctest::

    >>> from limix_inference.random import bernoulli_sample
    >>> from limix_inference import ExpFamEP
    >>> from numpy.random import RandomState
    >>> offset = 5
    >>> G = [[1, -1], [2, 1]]
    >>> (Q0, Q1), S0 = econommic_qs_linear(G)
    >>> y = bernoulli_sample(offset, G, random_state=RandomState(0))
    >>> covariantes = [1., 0.6]
    >>> glmm = ExpFamEP(BernoulliProdLik(Logit), covariantes, Q0, Q1, S0)
    >>> glmm.optmize()
    >>> glmm.lml()
    23.3

Expectation propagation
^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: ExpFamEP
    :members: covariates_variance, genetic_variance, environmental_variance,
              heritability, K, m, beta, v, delta, lml, optimize, fixed_ep
"""

from ._ep import ExpFamEP
