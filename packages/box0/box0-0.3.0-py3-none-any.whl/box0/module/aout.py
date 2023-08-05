#
# This file is part of pyBox0.
# Copyright (C) 2014-2016 Kuldeep Singh Dhaka <kuldeepdhaka9@gmail.com>
#
# pyBox0 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyBox0 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyBox0.  If not, see <http://www.gnu.org/licenses/>.
#

from box0._binding import libbox0, ffi, string_array_converter, \
						mode_bitsize_speeds, DummyObject
from box0.exceptions import ResultException
import numpy as np
from box0.module import ModuleInstance
from box0.module.module import np_dtype_map, bitsize_speed_set, \
	bitsize_speed_get, chan_seq_set, chan_seq_get

class Aout(ModuleInstance):
	"""
	.. uml::

	   [*] -d-> Opened : Aout()
	   Opened -d-> Closed : close()
	   Closed -d-> [*]

	   Opened -r-> Stream
	   Stream -l-> Opened

	   Opened -l-> Snapshot
	   Snapshot -r-> Opened

	   state Stream {
	      state "Running" as StreamRunning
	      state "Stopped" as StreamStopped

	      [*] -d-> StreamStopped : stream_prepare()

	      StreamStopped -u-> StreamRunning : stream_start()
	      StreamRunning -d-> StreamStopped : stream_stop()
	      StreamStopped --> [*]

	      StreamStopped -u-> StreamStopped : chan_seq_value(), bitsize_speed_set(), repeat_set()
	      StreamRunning --> StreamRunning: stream_write()
	   }

	   state Snapshot {
	      state "Running" as SnapshotRunning
	      state "Stopped" as SnapshotStopped

	      [*] -d-> SnapshotStopped : snapshot_prepare()
	      SnapshotStopped -u-> SnapshotRunning : snapshot_start()
	      SnapshotRunning -d-> SnapshotStopped : snapshot_stop(), [Repeat complete]
	      SnapshotStopped --> [*]

	      SnapshotStopped -u-> SnapshotStopped : bitsize_speed_set(), chan_seq_set(), repeat_set()
	   }
	"""

	_open = libbox0.b0_aout_open
	_close = libbox0.b0_aout_close

	_chan_seq_set = libbox0.b0_aout_chan_seq_set
	_chan_seq_get = libbox0.b0_aout_chan_seq_get
	_bitsize_speed_set = libbox0.b0_aout_bitsize_speed_set
	_bitsize_speed_get = libbox0.b0_aout_bitsize_speed_get
	_repeat_set = libbox0.b0_aout_repeat_set
	_repeat_get = libbox0.b0_aout_repeat_get

	_stream_prepare = libbox0.b0_aout_stream_prepare
	_stream_write = libbox0.b0_aout_stream_write
	_stream_write_double = libbox0.b0_aout_stream_write_double
	_stream_write_float = libbox0.b0_aout_stream_write_float
	_stream_start = libbox0.b0_aout_stream_start
	_stream_stop = libbox0.b0_aout_stream_stop

	_snapshot_prepare = libbox0.b0_aout_snapshot_prepare
	_snapshot_start = libbox0.b0_aout_snapshot_start
	_snapshot_start_double = libbox0.b0_aout_snapshot_start_double
	_snapshot_start_float = libbox0.b0_aout_snapshot_start_float
	_snapshot_stop = libbox0.b0_aout_snapshot_stop
	_snapshot_calc = libbox0.b0_aout_snapshot_calc

	chan_count = None
	"""Number of channels"""

	buffer_size = None
	"""Number of bytes available"""

	capab = None
	"""Capabilities mask"""

	label = None
	"""String related to module (Names of channel in `self.label.chan`)"""

	ref = None
	"""Reference. attributes `high: HIGH_VALUE, low: LOW_VALUE, type: TYPE_OF_REFERENCE`"""

	stream = None
	"""Stream mode list"""

	snapshot = None
	"""Snapshot mode list"""

	def __init__(self, dev, index):
		ModuleInstance.__init__(self, dev, index, "b0_aout**")
		self.chan_count = self._pointer.chan_count
		self.buffer_size = self._pointer.buffer_size
		self.capab = self._pointer.capab
		self.label = DummyObject()
		self.label.chan = string_array_converter(self._pointer.label.chan, \
								self._pointer.chan_count)
		self.ref = self._pointer.ref
		self.stream = mode_bitsize_speeds(self._pointer.stream)
		self.snapshot = mode_bitsize_speeds(self._pointer.snapshot)

	def stream_prepare(self):
		"""
		Prepare for streaming mode

		:raises ResultException: if libbox0 return negative result code
		"""
		ResultException.act(self._stream_prepare(self._pointer))

	"""
	currently double only supported
	data is numpy array
	"""
	def stream_write(self, data):
		"""
		wrtie data to stream

		:param numpy.ndarray data: Store readed data
		:raises ResultException: if libbox0 return negative result code
		"""
		sel = np_dtype_map(data.dtype,
			void = ("void *", self._stream_write),
			float32 = ("float *", self._stream_write_float),
			float64 = ("double *", self._stream_write_double))
		data_ptr = ffi.cast(sel[0], data.ctypes.data)
		ResultException.act(sel[1](self._pointer, data_ptr, data.size))

	def stream_start(self):
		"""
		Start streaming

		:raises ResultException: if libbox0 return negative result code
		"""
		ResultException.act(self._stream_start(self._pointer))

	def stream_stop(self):
		"""
		Stop streaming

		:raises ResultException: if libbox0 return negative result code
		"""
		ResultException.act(self._stream_stop(self._pointer))

	def snapshot_prepare(self):
		"""
		Prepare for Snapshot mode
		:raises ResultException: if libbox0 return negative result code
		"""
		ResultException.act(self._snapshot_prepare(self._pointer))

	def snapshot_start(self, data):
		"""
		Get data in snapshot mode

		:param numpy.ndarray data: NumPy array to output
		:raises ResultException: if libbox0 return negative result code
		"""
		sel = np_dtype_map(data.dtype,
			void = ("void *", self._snapshot_start),
			float32 = ("float *", self._snapshot_start_float),
			float64 = ("double *", self._snapshot_start_double))
		data_ptr = ffi.cast(sel[0], data.ctypes.data)
		ResultException.act(sel[1](self._pointer, data_ptr, data.size))

	def snapshot_stop(self):
		"""
		Stop snapshot output

		:raises ResultException: if libbox0 return negative result code
		"""
		ResultException.act(self._snapshot_stop(self._pointer))

	def snapshot_calc(self, freq, bitsize):
		"""
		Calculate best speed and count for a given frequency
		:return: count, speed
		:raises ResultException: if libbox0 return negative result code
		"""
		count = ffi.new("size_t *")
		speed = ffi.new("uint32_t *")
		ResultException.act(self._snapshot_calc(self._pointer,
				freq, bitsize, count, speed))
		return count[0], speed[0]

	def repeat_get(self):
		value = ffi.new("unsigned long *")
		ResultException.act(self._repeat_get(self._pointer, value))
		return value[0]

	def repeat_get(self, value):
		ResultException.act(self._repeat_set(self._pointer, value))

	# Reuse common part

	bitsize_speed_set = bitsize_speed_set
	bitsize_speed_get = bitsize_speed_get

	chan_seq_set = chan_seq_set
	chan_seq_get = chan_seq_get
