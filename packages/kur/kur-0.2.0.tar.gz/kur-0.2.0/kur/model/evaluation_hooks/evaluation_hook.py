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

from kur.utils import get_subclasses

###############################################################################
class EvaluationHook:					# pylint: disable=too-few-public-methods
	""" Base class for all evaluation hooks.

		Evaluation hooks are post-evaluation callbacks that can take a crack at
		modifying or reviewing the evaluation results.
	"""

	###########################################################################
	@staticmethod
	def from_specification(spec):
		""" Creates a new evaluation hook from a specification.

			# Arguments

			spec: str or dict. The specification object that was given.

			# Return value

			New EvaluationHook instance.
		"""
		if isinstance(spec, str):
			name = spec
			target = EvaluationHook.get_hook_by_name(spec)
			params = {}
			meta = {}
		elif isinstance(spec, dict):
			candidates = {}
			for key in spec:
				try:
					cls = EvaluationHook.get_hook_by_name(key)
					candidates[key] = cls
				except ValueError:
					pass

			if not candidates:
				raise ValueError('No valid evaluation hook found in '
					'Kurfile: {}'.format(spec))
			elif len(candidates) > 1:
				raise ValueError('Too many possible evaluation hooks found in '
					'Kurfile: {}'.format(spec))
			else:
				name, target = candidates.popitem()
				meta = dict(spec)
				meta.pop(name)
				params = spec[name] or {}

		else:
			raise ValueError('Expected the evaluation hooks to be a string or '
				'dictionary. We got this instead: {}'.format(spec))

		# At this point:
		# - name: the name of the evaluation hook, as specified in the spec.
		# - target: the class of the evaluation hook
		# - meta: dictionary of "other" keys in the spec that sit alongside the
		#   evaluation hook specification.
		# - params: parameters to be passed to the evaluation hook.

		return target(**params)

	###########################################################################
	@classmethod
	def get_name(cls):
		""" Returns the name of the evaluation hook.

			# Return value

			A lower-case string unique to this evaluation hook.
		"""
		return cls.__name__.lower()

	###########################################################################
	@staticmethod
	def get_all_hooks():
		""" Returns an iterator to the names of all evaluation hooks.
		"""
		for cls in get_subclasses(EvaluationHook):
			yield cls

	###########################################################################
	@staticmethod
	def get_hook_by_name(name):
		""" Finds a evaluation hook class with the given name.
		"""
		name = name.lower()
		for cls in EvaluationHook.get_all_hooks():
			if cls.get_name() == name:
				return cls
		raise ValueError('No such evaluation hook with name "{}"'.format(name))

	###########################################################################
	def __init__(self, *args, **kwargs):
		""" Creates a new evaluation hook.
		"""
		if args or kwargs:
			raise ValueError('One or more unexpected or unsupported arguments '
				'to the evaluation hook: {}'.format(
					', '.join(args + list(kwargs.keys()))
			))

	###########################################################################
	def apply(self, data, truth=None, model=None):
		""" Applies the hook to the data.

			# Arguments

			data: dict. Dictionary whose keys are the names of the output layers
				in the model, and whose values are a list of output tensors.
			truth: dict or None (default: None). If not None, then a dictionary
				with the same keys as `data` which contains ground truth data.

			# Return value

			A dictionary in the same format as `data` which can be passed on to
			the next hook.
		"""
		raise NotImplementedError

### EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF
