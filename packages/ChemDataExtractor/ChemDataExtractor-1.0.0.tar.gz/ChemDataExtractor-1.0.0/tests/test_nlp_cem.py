#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_nlp_ner
~~~~~~~~~~~~

Unit tests for named entity recognition.

:copyright: Copyright 2016 by Matt Swain.
:license: MIT, see LICENSE file for more details.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
import unittest

from chemdataextractor.nlp.cem import CiDictCemTagger, CrfCemTagger


logging.basicConfig(level=logging.DEBUG)
logging.getLogger('cde').setLevel(logging.DEBUG)
log = logging.getLogger(__name__)


class TestCrfCemTagger(unittest.TestCase):

    def test_false_pos(self):
        """Test the Chem CRF Tagger on a simple sentence."""
        dt = CrfCemTagger()
        self.assertEqual(
            [
                (('UV-vis', 'JJ'), 'O'),
                (('spectrum', 'NN'), 'O'),
                (('of', 'IN'), 'O'),
                (('Coumarin', 'NN'), 'B-CM'),
                (('343', 'CD'), 'O'),
                (('in', 'IN'), 'O'),
                (('THF', 'NN'), 'B-CM')
            ],
            dt.tag([
                ('UV-vis', 'JJ'),
                ('spectrum', 'NN'),
                ('of', 'IN'),
                ('Coumarin', 'NN'),
                ('343', 'CD'),
                ('in', 'IN'),
                ('THF', 'NN')
            ])
        )


# TODO: Test entity recognition on a sentence containing a generic abbreviation that is only picked up through its definition


if __name__ == '__main__':
    unittest.main()
