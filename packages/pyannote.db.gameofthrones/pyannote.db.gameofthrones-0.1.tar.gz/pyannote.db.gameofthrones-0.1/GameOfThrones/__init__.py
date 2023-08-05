#!/usr/bin/env python
# encoding: utf-8

# The MIT License (MIT)

# Copyright (c) 2017 CNRS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# AUTHORS
# Hervé BREDIN - http://herve.niderb.fr


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


from pyannote.database import Database
from pyannote.database.protocol import SpeakerDiarizationProtocol
from pyannote.parser import MDTMParser
import os.path as op
from pyannote.core import Segment, Annotation


class GameOfThronesSpeakerDiarizationProtocol(SpeakerDiarizationProtocol):
    """Base speaker diarization protocol for GameOfThrones database

    This class should be inherited from, not used directly.

    Parameters
    ----------
    preprocessors : dict or (key, preprocessor) iterable
        When provided, each protocol item (dictionary) are preprocessed, such
        that item[key] = preprocessor(**item). In case 'preprocessor' is not
        callable, it should be a string containing placeholder for item keys
        (e.g. {'wav': '/path/to/{uri}.wav'})
    """

    def __init__(self, preprocessors={}, **kwargs):
        super(GameOfThronesSpeakerDiarizationProtocol, self).__init__(
            preprocessors=preprocessors, **kwargs)
        self.mdtm_parser_ = MDTMParser()

    @staticmethod
    def get_audio_path(uri):
        return op.join(
            op.dirname(op.realpath(__file__)),
            'data', 'audio', '{uri}.txt'.format(uri=uri))

    def load_speaker(self, uri):
        speaker = Annotation(uri=uri)
        path = self.get_audio_path(uri)
        with open(path, 'r') as fp:
            for line in fp:
                start, duration, name, _, _ = line.strip().split()
                start = float(start)
                end = start + float(duration)
                speaker[Segment(start, end)] = name
        return speaker.smooth()

    def _subset(self, protocol, subset):

        data_dir = op.join(op.dirname(op.realpath(__file__)), 'data')

        # load annotations
        path = op.join(
            data_dir,
            '{protocol}.{subset}.lst'.format(subset=subset, protocol=protocol))

        with open(path, 'r') as fp:

            for line in fp:
                uri = line.strip()
                annotation = self.load_speaker(uri)
                item = {
                    'database': 'GameOfThrones',
                    'uri': uri,
                    'annotation': annotation}
                yield item


class Season1(GameOfThronesSpeakerDiarizationProtocol):
    """Season 1

    * Training set:    episode #1, #2, #3, #4, #5
    * Development set: episode #6
    * Test set:        episode #7, #8, #9, #10
    """

    def trn_iter(self):
        return self._subset('Season1', 'trn')

    def dev_iter(self):
        return self._subset('Season1', 'dev')

    def tst_iter(self):
        return self._subset('Season1', 'tst')


class Season1Test(GameOfThronesSpeakerDiarizationProtocol):
    """Season 1

    * Training set:    -- not available --
    * Development set: -- not available --
    * Test set:        episode #1, #2, #3, #4, #5, #6, #7, #8, #9, #10
    """

    def tst_iter(self):
        return self._subset('Season1Test', 'tst')


class GameOfThrones(Database):
    """GameOfThrones corpus

Parameters
----------
preprocessors : dict or (key, preprocessor) iterable
    When provided, each protocol item (dictionary) are preprocessed, such
    that item[key] = preprocessor(**item). In case 'preprocessor' is not
    callable, it should be a string containing placeholder for item keys
    (e.g. {'wav': '/path/to/{uri}.wav'})

Reference
---------

Citation
--------

Website
-------
    """

    def __init__(self, preprocessors={}, **kwargs):
        super(GameOfThrones, self).__init__(preprocessors=preprocessors, **kwargs)

        self.register_protocol(
            'SpeakerDiarization', 'Season1', Season1)

        self.register_protocol(
            'SpeakerDiarization', 'Season1Test', Season1Test)
