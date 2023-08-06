"""
Copyright 2017 Deepgram

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import logging
import numpy
from . import EvaluationHook

logger = logging.getLogger(__name__)

###############################################################################
class TranscriptHook(EvaluationHook):
	""" Post-evaluation hook for MNIST data, which prints summary statistics
		specific to the MNIST data set.
	"""

	###########################################################################
	@classmethod
	def get_name(cls):
		""" Returns the name of the evaluation hook.
		"""
		return 'transcript'

	###########################################################################
	@staticmethod
	def argmax_decode(output, rev_vocab, blank):
		""" output = matrix: timesteps * characters
		"""
		x = numpy.argmax(output, axis=1)
		tokens = []
		prev = None
		for c in x:
			if c == prev:
				continue
			if c != blank:
				tokens.append(c)
			prev = c
		offset = 1 if blank == 0 else 0
		return ''.join([rev_vocab[i-offset] for i in tokens])

	###########################################################################
	def __init__(self, warp=False, **kwargs):
		""" Creates a new transcript hook.
		"""

		super().__init__(**kwargs)
		self.warp = warp

	###########################################################################
	def apply(self, data, truth=None, model=None):
		""" Applies the hook to the data.
		"""

		if truth is None:
			return

		k = model.provider.keys.index('transcript_raw')
		vocab = model.provider.sources[k].vocab
		rev = {v : k for k, v in vocab.items()}

		blank = len(vocab) if not self.warp else 0
		prediction = data['asr'][0]

		print('Prediction: "{}"'.format(
			self.argmax_decode(
				prediction,
				rev,
				blank
			)
		))
		print('Truth: "{}"'.format(''.join(
			rev.get(i, '') for i in truth['transcript_raw'][0]
		)))

#### EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF
