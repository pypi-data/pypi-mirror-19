# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015-2016 Tiago Baptista
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------

"""
This module provides several ready-made simulator classes. Used mainly for the
examples given in the Complex Systems course. In this current version, these
should *not* be considered stable in terms of API.

"""

from __future__ import division
from simcx import Simulator
import numpy as np

__docformat__ = 'restructuredtext'
__author__ = 'Tiago Baptista'


class FunctionIterator(Simulator):
    def __init__(self, func, initial_states):
        super(FunctionIterator, self).__init__()

        # Allow initial states to be a list or a single value
        if not isinstance(initial_states, list):
            initial_states = [initial_states]

        self._state = initial_states[:]
        self._n_states = len(self._state)
        self.func = func
        self.time = 0
        self.x = [0]
        self.y = [[state] for state in initial_states]

    def step(self, delta=0):
        self.time += 1
        for i in range(self._n_states):
            self._state[i] = self.func(self._state[i])
            self.y[i].append(self._state[i])
        self.x.append(self.time)

    def reset(self):
        self._state = [y[0] for y in self.y]
        self.time = 0
        self.x = [0]
        self.y = [[state] for state in self._state]


class FunctionIterator2D(Simulator):
    def __init__(self, func, initial_state):
        super(FunctionIterator2D, self).__init__()

        self._func = func
        self._state = initial_state
        self.time = 0
        self.x = [0]
        self.y = [[initial_state[0]], [initial_state[1]]]

    def step(self, delta=0):
        self.time += 1
        self._state = self._func(*self._state)
        self.x.append(self.time)
        self.y[0].append(self._state[0])
        self.y[1].append(self._state[1])


class FinalStateIterator(Simulator):
    def __init__(self, func, seed, start, end, discard=1000, samples=250,
                 delta=0.01):
        super(FinalStateIterator, self).__init__()

        self._func = func
        self._seed = seed
        self._a = start
        self.start = start
        self.end = end
        self._discard = discard
        self._samples = samples
        self._delta = delta

        self.x = self.y = np.zeros(self._samples)
        self.y = self.y = np.zeros(self._samples)

    def step(self, delta=0):
        if self._a <= self.end:
            x = self._seed
            for i in range(self._discard):
                x = self._func(self._a, x)
            for i in range(self._samples):
                x = self._func(self._a, x)
                self.y[i] = x

            self.x = np.zeros(self._samples)
            self.x += self._a
            self._a += self._delta


class IFS(Simulator):
    """An Iterated Function Systems simulator using the Chaos Game."""

    def __init__(self, transforms, probs, step_size=100):
        super(IFS, self).__init__()

        self._discard = 10
        self._step_size = step_size
        self._transforms = transforms[:]
        self._n = len(transforms)
        self._probs = probs[:]

        self._point = np.array([0.0, 0.0], dtype=np.float64)
        self.draw_points = []

        for i in range(self._discard):
            self.step(0, discard=True)

    def _get_random_transform(self):
        i = np.random.choice(self._n, p=self._probs)
        return self._transforms[i]

    def step(self, delta=0, discard=False):
        for _ in range(self._step_size):
            transform = self._get_random_transform()
            self._point = transform.transform_point(self._point)
            if not discard:
                self.draw_points.append(self._point)


class JuliaSet(Simulator):
    """A simulator to calculate the Julia Set of a function in the form
    f(z) = z^2 + c. The simulator will compute de full Julia Set for the
    given range (min_x, min_y) to (max_x, max_y) on creation of the instance."""

    def __init__(self, c, min_x=-2, max_x=2, min_y=-2, max_y=2, samples=500,
                 iterations=100):
        super(JuliaSet, self).__init__()

        self._c = c
        self._min_x = min_x
        self._max_x = max_x
        self._min_y = min_y
        self._max_y = max_y
        self._samples = samples
        self._iterations = iterations

        self._data = self._compute()
        self.draw_points = [[x, y] for x, y, count in self._data
                            if count == iterations]

    def step(self, delta=0):
        pass

    def _compute(self):
        r = max(2, abs(self._c))
        xs = np.linspace(self._min_x, self._max_x, self._samples)
        ys = np.linspace(self._min_y, self._max_y, self._samples)

        data = []

        for y in ys:
            for x in xs:
                z = complex(x, y)
                count = 0
                while count < self._iterations and abs(z) <= r:
                    z = z*z + self._c
                    count += 1

                data.append((x, y, count))

        return data
