"""
Copyright 2016 Deepgram

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

import json
import os
import logging
import random

import numpy

from ..sources import DerivedSource, VanillaSource, ChunkSource
from ..utils import Shuffleable
from . import Supplier
from ..utils import package
from ..utils import count_lines
from ..utils import get_audio_features
from ..utils import Normalize

logger = logging.getLogger(__name__)

###############################################################################
class UtteranceLength(DerivedSource):
	""" Data source for audio lengths.
	"""
	def __init__(self, source):
		super().__init__()
		self.source = source
	def derive(self, inputs):
		utterances, = inputs
		return numpy.array([[len(x)] for x in utterances], dtype='int32')
	def shape(self):
		return (1, )
	def requires(self):
		return (self.source, )

###############################################################################
class Utterance(DerivedSource):
	""" Data source for model-ready audio samples. Unlike `RawUtterance`, this
		ensures that all data products are rectangular tensors (rather than
		ragged arrays).
	"""
	def __init__(self, source, raw):
		super().__init__()
		self.source = source
		self.raw = raw
	def derive(self, inputs):
		utterances, = inputs
		max_len = max(len(x) for x in utterances)
		output = numpy.zeros(
			shape=(len(utterances), max_len, self.raw.features)
		)
		for i, row in enumerate(utterances):
			output[i][:len(row)] = row
		return output
	def shape(self):
		return (None, self.raw.features)
	def requires(self):
		return (self.source, )

###############################################################################
class RawUtterance(ChunkSource, Shuffleable):
	""" Data source for audio samples
	"""

	NORMALIZATION_DEPTH = 100

	###########################################################################
	@classmethod
	def default_chunk_size(cls):
		""" Returns the default chunk size for this source.
		"""
		return ChunkSource.USE_BATCH_SIZE

	###########################################################################
	def __init__(self, audio_paths, feature_type=None,
		normalization=None, max_frequency=None, *args, **kwargs):
		""" Creates a new raw utterance source.
		"""

		super().__init__(*args, **kwargs)
		self.audio_paths = audio_paths
		self.indices = numpy.arange(len(self))
		self.feature_type = feature_type
		self.features = None
		self.max_frequency = max_frequency

		self._init_normalizer(normalization)

	###########################################################################
	def _init_normalizer(self, normalization):
		norm = Normalize()
		if normalization is not None:
			normalization = os.path.expanduser(os.path.expandvars(
				normalization))
			if os.path.exists(normalization):
				if not os.path.isfile(normalization):
					raise ValueError('Normalization data must be a regular '
						'file. This is not: {}'.format(normalization))
				logger.info('Restoring normalization statistics: %s',
					normalization)
				norm.restore(normalization)
				self.features = norm.get_state()['mean'].shape[0]
			else:
				self.train_normalizer(norm)
				norm.save(normalization)
		else:
			logger.info('No normalization data available. We will use '
				'on-the-fly (non-persistent) normalization. In the future, '
				'you probably want to give a filename to the "normalization" '
				'key in the speech recognition supplier.')
			self.train_normalizer(norm)

		# Register the normalizer
		self.norm = norm

	###########################################################################
	def load_audio(self, paths):
		""" Loads unnormalized audio data.
		"""
		return [
			get_audio_features(
				path,
				feature_type=self.feature_type,
				high_freq=self.max_frequency
			)
			for path in paths
		]

	###########################################################################
	def train_normalizer(self, norm):
		""" Trains the normalizer on the data.

			# Arguments

			norm: Normalize instance. The normalization transform to train.
		"""
		logger.info('Training normalization transform.')
		num_entries = min(
			RawUtterance.NORMALIZATION_DEPTH,
			len(self.audio_paths)
		)
		paths = random.sample(self.audio_paths, num_entries)
		data = self.load_audio(paths)
		self.features = data[0].shape[-1]
		norm.learn(data)
		logger.debug('Finished training normalization transform.')

	###########################################################################
	def __iter__(self):
		""" Return an iterator to the data.
		"""
		start = 0
		num_entries = len(self)
		while start < num_entries:
			end = min(num_entries, start + self.chunk_size)

			paths = [self.audio_paths[i] for i in self.indices[start:end]]
			batch = self.load_audio(paths)
			batch = [self.norm.apply(data) for data in batch]
			yield batch
			start = end

	###########################################################################
	def __len__(self):
		""" Returns the total number of entries that this source can return, if
			known.
		"""
		return len(self.audio_paths)

	###########################################################################
	def shape(self):
		""" Return the shape of the tensor (excluding batch size) returned by
			this data source.
		"""
		return (None, self.features)

	###########################################################################
	def shuffle(self, indices):
		""" Applies a permutation to the data.
		"""
		if len(indices) > len(self):
			raise ValueError('Shuffleable was asked to apply permutation, but '
				'the permutation is longer than the length of the data set.')
		self.indices[:len(indices)] = self.indices[:len(indices)][indices]

###############################################################################
class TranscriptLength(DerivedSource):
	""" Data source for computing transcript lengths.
	"""
	def __init__(self, source):
		super().__init__()
		self.source = source
	def derive(self, inputs):
		transcript, = inputs
		return numpy.array([[len(x)] for x in transcript], dtype='int32')
	def shape(self):
		return (1, )
	def requires(self):
		return (self.source, )

###############################################################################
class Transcript(DerivedSource):
	""" Data source for neat (non-ragged) transcript arrays.
	"""
	def __init__(self, source):
		super().__init__()
		self.source = source
	def derive(self, inputs):
		transcript, = inputs
		max_len = max(len(x) for x in transcript)
		output = numpy.zeros(shape=(len(transcript), max_len), dtype='int32')
		for i, row in enumerate(transcript):
			output[i][:len(row)] = row
		return output
	def shape(self):
		return (None, )
	def requires(self):
		return (self.source, )

###############################################################################
class RawTranscript(ChunkSource, Shuffleable):
	""" Data source for variable-length transcripts.
	"""

	###########################################################################
	def __init__(self, transcripts, vocab=None, *args,
		**kwargs):
		""" Creates a new raw transcript source.
		"""
		super().__init__(*args, **kwargs)
		self.transcripts = transcripts
		self.indices = numpy.arange(len(self))
		self.vocab = self.make_vocab(vocab)

	###########################################################################
	def make_vocab(self, vocab):
		""" Loads or infers a vocabulary.
		"""
		if vocab is None:
			flat = set(x for transcript in self.transcripts \
				for x in transcript.lower())
		else:
			with open(vocab) as fh:
				data = json.loads(fh.read())
			flat = set(x.lower() for x in data)

		logger.info('Loaded a %d-word vocabulary.', len(flat))
		return {x : i for i, x in enumerate(sorted(flat))}

	###########################################################################
	def word_to_integer(self, data):
		""" Maps a character transcript to its integer representation.
		"""
		result = [None]*len(data)
		for i, row in enumerate(data):
			result[i] = [self.vocab.get(word) for word in row]
			result[i] = [x for x in result[i] if x is not None]
		return result

	###########################################################################
	def __iter__(self):
		""" Return an iterator to the data.
		"""
		start = 0
		num_entries = len(self)
		while start < num_entries:
			end = min(num_entries, start + self.chunk_size)

			batch = [self.transcripts[i] for i in self.indices[start:end]]
			batch = self.word_to_integer(batch)
			yield batch
			start = end

	###########################################################################
	def __len__(self):
		""" Returns the total number of entries that this source can return, if
			known.
		"""
		return len(self.transcripts)

	###########################################################################
	def shape(self):
		""" Return the shape of the tensor (excluding batch size) returned by
			this data source.
		"""
		return (None, )

	###########################################################################
	def shuffle(self, indices):
		""" Applies a permutation to the data.
		"""
		if len(indices) > len(self):
			raise ValueError('Shuffleable was asked to apply permutation, but '
				'the permutation is longer than the length of the data set.')
		self.indices[:len(indices)] = self.indices[:len(indices)][indices]

###############################################################################
class SpeechRecognitionSupplier(Supplier):
	""" A supplier which handles parsing of audio + transcript data sets for
		speech recognition purposes.
	"""

	DEFAULT_UNPACK = True
	SUPPORTED_TYPES = ('wav', 'mp3', 'flac')

	###########################################################################
	@classmethod
	def get_name(cls):
		""" Returns the name of the supplier.
		"""
		return 'speech_recognition'

	###########################################################################
	def __init__(self, url=None, path=None, checksum=None, unpack=None, 
		type=None, normalization=None, max_duration=None, max_frequency=None,
		*args, **kwargs):
		""" Creates a new speech recognition supplier.

			# Arguments
		"""
		super().__init__(*args, **kwargs)

		if unpack is None:
			unpack = SpeechRecognitionSupplier.DEFAULT_UNPACK
		self.load_data(url=url, path=path, checksum=checksum, unpack=unpack,
			max_duration=max_duration)

		logger.debug('Creating sources.')
		utterance_raw = RawUtterance(
			self.data['audio'],
			feature_type=type or 'mfcc',
			normalization=normalization,
			max_frequency=max_frequency
		)
		self.sources = {
			'transcript_raw' : RawTranscript(self.data['transcript']),
			'transcript_length' : TranscriptLength('transcript_raw'),
			'transcript' : Transcript('transcript_raw'),
			'utterance_raw' : utterance_raw,
			'utterance_length' : UtteranceLength('utterance_raw'),
			'utterance' : Utterance('utterance_raw', utterance_raw),
			'duration' : VanillaSource(numpy.array(self.data['duration']))
		}

	###########################################################################
	def load_data(self, url=None, path=None, checksum=None, unpack=None,
		max_duration=None):
		""" Loads the data for this supplier.
		"""
		local_path, is_packed = package.install(
			url=url,
			path=path,
			checksum=checksum
		)

		if is_packed and unpack:
			logger.debug('Unpacking input data: %s', local_path)
			extracted = package.unpack(local_path, recursive=True)
			is_packed = False
		elif is_packed and not unpack:
			logger.debug('Using packed input data.')
			raise NotImplementedError
		elif not is_packed and unpack:
			logger.debug('Using already unpacked input data.')
			extracted = []
			for dirpath, _, filenames in os.walk(local_path):
				extracted.extend([
					package.canonicalize(os.path.join(dirpath, filename))
					for filename in filenames
				])
		elif not is_packed and not unpack:
			logger.debug('Ignore "unpack" for input data, since it is already '
				'unpacked.')
		else:
			logger.error('Unhandled data package requirements. This is a bug.')

		self.metadata, self.data = self.get_metadata(extracted, max_duration)

	###########################################################################
	def get_metadata(self, package_contents, max_duration):
		""" Scans the package for a metadata file, makes sure everything is in
			order, and returns some information about the data set.
		"""
		logger.debug('Looking for metadata file.')
		metadata_file = None
		for filename in package_contents:
			parts = os.path.splitext(filename)
			if parts[1].lower() == '.jsonl' and \
				not os.path.basename(filename).startswith('.'):
				metadata_file = filename
				source = os.path.join(os.path.dirname(metadata_file), 'audio')
				break

		if metadata_file is None:
			raise ValueError('Failed to find a JSONL metadata file.')

		logger.debug('Found metadata file: %s', metadata_file)
		logger.debug('Inferred source path: %s', source)

		logger.debug('Scanning metadata file.')
		lines = count_lines(metadata_file)
		logger.debug('Entries counted: %d', lines)

		logger.debug('Loading metadata.')
		data = {
			'audio' : [None]*lines,
			'transcript' : [None]*lines,
			'duration' : [None]*lines
		}

		entries = 0
		with open(metadata_file, 'r') as fh:
			for line_number, line in enumerate(fh, 1):
				try:
					entry = json.loads(line)
				except json.decoder.JSONDecodeError:
					logger.warning('Failed to parse valid JSON on line %d of '
						'file %s', line_number, metadata_file)
					continue
				if any(k not in entry for k in ('text', 'duration_s', 'uuid')):
					logger.warning('Line %d is missing one of its required '
						'keys in metadata file %s', line_number, metadata_file)
					continue

				duration = entry['duration_s']
				if max_duration and duration > max_duration:
					continue

				data['duration'][entries] = entry['duration_s']
				data['transcript'][entries] = entry['text']

				audio = os.path.join(source, entry['uuid'])
				for ext in SpeechRecognitionSupplier.SUPPORTED_TYPES:
					candidate = '{}.{}'.format(audio, ext)
					if os.path.isfile(candidate):
						data['audio'][entries] = candidate
						break
				else:
					logger.warning('Line %d in the metadata file (%s) '
						'references UUID %s, but we could not find a '
						'supported audio file type: %s.*', line_number,
						metadata_file, entry['uuid'], audio)
					continue

				entries += 1

		logger.debug('Entries kept: %d', entries)
		for k in data:
			data[k] = data[k][:entries]

		metadata = {
			'entries' : entries,
			'filename' : metadata_file,
			'source' : source
		}

		return metadata, data

	###########################################################################
	def get_data(self, start, end):
		""" Loads data.

			# Arguments

			start: int. First index to grab.
			end: int. One plus the last index to grab.

			# Return value

			Returns `end - end` entries, because this gets indices
			[start, end).
		"""
		if start < 0 or end > self.metadata['entries']:
			raise IndexError('Out-of-range indices: must be >= 0 and <= {}. '
				'Received start={}, end={}.'.format(self.metadata['entries'],
				start, end))

		if start > end:
			raise IndexError('Starting index must be <= the end index.')

		if start == end:
			raise NotImplementedError

	###########################################################################
	def get_sources(self, sources=None):
		""" Returns all sources from this provider.
		"""

		if sources is None:
			sources = list(self.sources.keys())
		elif not isinstance(sources, (list, tuple)):
			sources = [sources]

		for source in sources:
			if source not in self.sources:
				raise KeyError(
					'Invalid data key: {}. Valid keys are: {}'.format(
						source, ', '.join(str(k) for k in self.sources.keys())
				))

		return {k : self.sources[k] for k in sources}

### EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF
