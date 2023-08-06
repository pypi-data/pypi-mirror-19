# Copyright 2014-2016 The ODL development group
#
# This file is part of ODL.
#
# ODL is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ODL is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ODL.  If not, see <http://www.gnu.org/licenses/>.

"""Tests for the factory functions to create proximal operators."""

# Imports for common Python 2/3 codebase
from __future__ import print_function, division, absolute_import
from future import standard_library
standard_library.install_aliases()

import numpy as np
import pytest
import scipy.special
import odl
from odl.util.testutils import (noise_element, all_almost_equal,
                                simple_fixture)
from odl.solvers.functional.functional import FunctionalDefaultConvexConjugate

pytestmark = odl.util.skip_if_no_largescale


stepsize = simple_fixture('stepsize', [0.1, 1.0, 10.0])
offset = simple_fixture('offset', [False, True])
dual = simple_fixture('dual', [False, True])


func_params = ['l1', 'l2', 'l2^2', 'kl', 'kl_cross_ent', 'const',
               'groupl1-1', 'groupl1-2',
               'nuclearnorm-1-1', 'nuclearnorm-1-2', 'nuclearnorm-1-inf']
func_ids = [' f = {} '.format(p.ljust(10)) for p in func_params]


@pytest.fixture(scope="module", ids=func_ids, params=func_params)
def functional(request, offset, dual):
    """Return functional whose proximal should be tested."""
    name = request.param.strip()

    space = odl.uniform_discr(0, 1, 2)

    if name == 'l1':
        func = odl.solvers.L1Norm(space)
    elif name == 'l2':
        func = odl.solvers.L2Norm(space)
    elif name == 'l2^2':
        func = odl.solvers.L2NormSquared(space)
    elif name == 'kl':
        func = odl.solvers.KullbackLeibler(space)
    elif name == 'kl_cross_ent':
        func = odl.solvers.KullbackLeiblerCrossEntropy(space)
    elif name == 'const':
        func = odl.solvers.ConstantFunctional(space, constant=2)
    elif name.startswith('groupl1'):
        exponent = float(name.split('-')[1])
        space = odl.ProductSpace(space, 2)
        func = odl.solvers.GroupL1Norm(space, exponent=exponent)
    elif name.startswith('nuclearnorm'):
        outer_exp = float(name.split('-')[1])
        singular_vector_exp = float(name.split('-')[2])

        space = odl.ProductSpace(odl.ProductSpace(space, 2), 3)
        func = odl.solvers.NuclearNorm(space,
                                       outer_exp=outer_exp,
                                       singular_vector_exp=singular_vector_exp)
    else:
        assert False

    if offset:
        g = noise_element(space)
        if name.startswith('kl'):
            g = np.abs(g)
        func = func.translated(g)

    if dual:
        func = func.convex_conj

    return func


# Margin of error
EPS = 1e-6


def proximal_objective(functional, x, y):
    """Objective function of the proximal optimization problem."""
    return functional(y) + (1.0 / 2.0) * (x - y).norm() ** 2


def test_proximal_defintion(functional, stepsize):
    """Test the defintion of the proximal:

        prox[f](x) = argmin_y {f(y) + 1/2 ||x-y||^2}

    Hence we expect for all x in the domain of the proximal

        x* = prox[f](x)

        f(x*) + 1/2 ||x-x*||^2 <= f(y) + 1/2 ||x-y||^2
    """
    proximal = functional.proximal(stepsize)

    assert proximal.domain == functional.domain
    assert proximal.range == functional.domain

    for _ in range(100):
        x = noise_element(proximal.domain) * 10
        prox_x = proximal(x)
        f_prox_x = proximal_objective(stepsize * functional, x, prox_x)

        y = noise_element(proximal.domain)
        f_y = proximal_objective(stepsize * functional, x, y)

        if not f_prox_x <= f_y + EPS:
            print(repr(functional), x, y, prox_x, f_prox_x, f_y)

        assert f_prox_x <= f_y + EPS


def cconj_objective(functional, x, y):
    """CObjective function of the convex conjugate problem."""
    return x.inner(y) - functional(x)


def test_cconj_defintion(functional):
    """Test the defintion of the convex conjugate:

        f^*(y) = sup_x {<x, y> - f(x)}

    Hence we expect for all x in the domain of the proximal

        <x, y> - f(x) <= f^*(y)
    """
    f_cconj = functional.convex_conj
    if isinstance(functional.convex_conj, FunctionalDefaultConvexConjugate):
        pytest.skip('functional has no convex conjugate')
        return

    for _ in range(100):
        y = noise_element(functional.domain)
        f_cconj_y = f_cconj(y)

        x = noise_element(functional.domain)
        lhs = x.inner(y) - functional(x)

        if not lhs <= f_cconj_y + EPS:
            print(repr(functional), repr(f_cconj), x, y, lhs, f_cconj_y)

        assert lhs <= f_cconj_y + EPS


def test_proximal_cconj_kl_cross_entropy_solving_opt_problem():
    """Test for proximal operator of conjguate of 2nd kind KL-divergence.

    The test solves the problem

        min_x lam*KL(x | g) + 1/2||x-a||^2_2,

    where g is the nonnegative prior, and a is any vector.  Explicit solution
    to this problem is given by

        x = lam*W(g*e^(a/lam)/lam),

    where W is the Lambert W function.
    """

    # Image space
    space = odl.uniform_discr(0, 1, 10)

    # Data
    g = space.element(np.arange(10, 0, -1))
    a = space.element(np.arange(4, 14, 1))

    # Creating and assembling linear operators and proximals
    id_op = odl.IdentityOperator(space)
    lin_ops = [id_op, id_op]
    lam_kl = 2.3
    kl_ce = odl.solvers.KullbackLeiblerCrossEntropy(space, prior=g)
    g_funcs = [lam_kl * kl_ce,
               0.5 * odl.solvers.L2NormSquared(space).translated(a)]
    f = odl.solvers.ZeroFunctional(space)

    # Staring point
    x = space.zero()

    odl.solvers.douglas_rachford_pd(x, f, g_funcs, lin_ops,
                                    tau=2.1, sigma=[0.4, 0.4], niter=100)

    # Explicit solution: x = W(g * exp(a)), where W is the Lambert W function.
    x_verify = lam_kl * scipy.special.lambertw(
        (g / lam_kl) * np.exp(a / lam_kl))
    assert all_almost_equal(x, x_verify, places=6)

if __name__ == '__main__':
    pytest.main([str(__file__.replace('\\', '/')), '-v', '--largescale'])
