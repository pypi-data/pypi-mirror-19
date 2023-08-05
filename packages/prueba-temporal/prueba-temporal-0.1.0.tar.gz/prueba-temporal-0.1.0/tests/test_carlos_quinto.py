#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests del modulo carlos_quinto."""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import with_statement
import unittest
import nose

import carlos_quinto


class CarlosQuintoTestCase(unittest.TestCase):

    def test_sumar_numeros(self):
        self.assertEqual(carlos_quinto.carlos_quinto.sumar_numeros(1, 2), 3)


if __name__ == '__main__':
    nose.run(defaultTest=__name__)
