#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import os.path
import numpy as np
import scipy.io.wavfile as wav
import librosa
import numbers
import audioread
import json

import spectral_utils
import constants
import utils


class AudioSignal(object):
    """Defines properties of an audio signal and performs basic operations such as Wav loading and STFT/iSTFT.

    Parameters:
        path_to_input_file (string): string specifying path to file. Either this or timeSeries must be provided
        audio_data_array (np.array): Numpy matrix containing a time series of a signal
        signal_starting_position (Optional[int]): Starting point of the section to be extracted in seconds. Defaults to 0
        signal_length (Optional[int]): Length of the signal to be extracted. Defaults to full length of the signal
        sample_rate (Optional[int]): sampling rate to read audio file at. Defaults to Constants.DEFAULT_SAMPLE_RATE
        stft (Optional[np.array]): Optional pre-computed complex spectrogram data.
        stft_params (Optional [StftParams object]):
  
    Examples:
        * create a new signal object:     ``sig=AudioSignal('sample_audio_file.wav')``
        * compute the spectrogram of the new signal object:   ``sigSpec,sigPow,F,T=sig.STFT()``
        * compute the inverse stft of a spectrogram:          ``sigrec,tvec=sig.iSTFT()``
  
    """

    def __init__(self, path_to_input_file=None, audio_data_array=None, signal_starting_position=0, signal_length=None,
                 sample_rate=constants.DEFAULT_SAMPLE_RATE, stft=None, stft_params=None):

        self.path_to_input_file = path_to_input_file
        self._audio_data = None
        self.sample_rate = sample_rate
        self._active_start = None
        self._active_end = None

        if (path_to_input_file is not None) and (audio_data_array is not None):
            raise Exception('Cannot initialize AudioSignal object with a path AND an array!')

        if path_to_input_file is not None:
            self.load_audio_from_file(self.path_to_input_file, signal_starting_position, signal_length)
        elif audio_data_array is not None:
            self.load_audio_from_array(audio_data_array, sample_rate)

        # stft data
        self.stft_data = stft  # complex spectrogram data
        self.power_spectrum_data = None  # power spectrogram
        self.stft_params = spectral_utils.StftParams(self.sample_rate) if stft_params is None else stft_params
        self.use_librosa_stft = constants.USE_LIBROSA_STFT

    def __str__(self):
        return 'AudioSignal'

    ##################################################
    # Plotting
    ##################################################

    def plot_time_domain(self):
        """
        Not implemented yet -- will raise and exception
        Returns:

        """
        raise NotImplementedError('Not ready yet!')

    _NAME_STEM = 'audio_signal'

    def plot_spectrogram(self, file_name=None, ch=None, use_librosa=constants.USE_LIBROSA_STFT):
        # TODO: use self.stft_data if not None
        # TODO: flatten to mono be default
        # TODO: make other parameters adjustable
        if file_name is None:
            name_stem = self.file_name if self.file_name is not None else self._NAME_STEM
        else:
            if os.path.isfile(file_name):
                name_stem = os.path.splitext(file_name)[0]
            else:
                name_stem = file_name

        if ch is None:
            if self.num_channels > 1:
                for i in range(1, self.num_channels+1):
                    name = name_stem + '_ch{}.png'.format(i)
                    spectral_utils.plot_stft(self.get_channel(i), name,
                                             sample_rate=self.sample_rate,
                                             use_librosa=use_librosa)
            else:
                name = name_stem + '.png'
                spectral_utils.plot_stft(self.get_channel(1), name,
                                         sample_rate=self.sample_rate,
                                         use_librosa=use_librosa)
        else:
            name = name_stem + '_ch{}.png'.format(ch)
            spectral_utils.plot_stft(self.get_channel(ch), name,
                                     sample_rate=self.sample_rate,
                                     use_librosa=use_librosa)

    ##################################################
    # Properties
    ##################################################

    # Constants for accessing _audio_data np.array indices
    _LEN = 1
    _CHAN = 0

    _STFT_BINS = 0
    _STFT_LEN = 1
    _STFT_CHAN = 2

    @property
    def signal_length(self):
        """
        Returns: (int) The length of the audio signal represented by this object in samples
        """
        if self.audio_data is None:
            return None
        return self.audio_data.shape[self._LEN]

    @property
    def signal_duration(self):
        """
        Returns: (float) The length of the audio signal represented by this object in seconds
        """
        if self.signal_length is None:
            return None
        return self.signal_length / self.sample_rate

    @property
    def num_channels(self):
        """
        The number of channels.
        Returns: (int) number of channels
        """
        # TODO: what if about a mismatch between audio_data and stft_data
        if self.audio_data is not None:
            return self.audio_data.shape[self._CHAN]
        if self.stft_data is not None:
            return self.stft_data.shape[self._STFT_CHAN]
        return None

    @property
    def audio_data(self):
        """
        A 2-D numpy array that represents the audio in the time domain.

        """
        if self._audio_data is None:
            return None

        start = 0
        end = self._audio_data.shape[self._LEN]

        if self._active_end is not None and self._active_end < end:
            end = self._active_end

        if self._active_start is not None and self._active_start > 0:
            start = self._active_start

        return self._audio_data[:, start:end]

    @audio_data.setter
    def audio_data(self, value):
        assert (type(value) == np.ndarray)

        self._audio_data = value

        if self._audio_data.ndim < 2:
            self._audio_data = np.expand_dims(self._audio_data, axis=self._CHAN)

    @property
    def file_name(self):
        """
        Returns: The name of the file wth extension, NOT the full path
        See Also:
            :ref: self.path_to_input_file
        """
        if self.path_to_input_file is not None:
            return os.path.split(self.path_to_input_file)[1]
        return None

    @property
    def time_vector(self):
        """
        Returns: A 1-D numpy array with timestamps (in seconds) for each sample in the time domain.

        """
        if self.signal_duration is None:
            return None
        return np.linspace(0.0, self.signal_duration, num=self.signal_length)

    @property
    def freq_vector(self):
        """
        Returns: A 1-D numpy array with frequency values that correspond to each frequency bin (vertical axis)
        for the STFT.
        Raises: AttributeError if self.stft_data is None. Run self.stft() before accessing this.
        """
        if self.stft_data is None:
            raise AttributeError('Cannot calculate freq_vector until self.stft() is run')
        return np.linspace(0.0, self.sample_rate // 2, num=self.stft_data.shape[self._STFT_BINS])

    @property
    def stft_length(self):
        """
        Returns: (int) The number of time windows the STFT has.
        Raises: AttributeError if self.stft_data is None. Run self.stft() before accessing this.
        """
        if self.stft_data is None:
            raise AttributeError('Cannot calculate stft_length until self.stft() is run')
        return self.stft_data.shape[self._STFT_LEN]

    @property
    def num_fft_bins(self):
        """
        Returns: (int) Number of FFT bins in self.stft_data
        Raises: AttributeError if self.stft_data is None. Run self.stft() before accessing this.
        """
        if self.stft_data is None:
            raise AttributeError('Cannot calculate num_fft_bins until self.stft() is run')
        return self.stft_data.shape[self._STFT_BINS]

    @property
    def active_region_is_default(self):
        """
        Returns: Returns true if active region is the full length of self.audio_data
        See Also:
            :ref: self.set_active_region
            :ref: self.set_active_region_to_default

        """
        return self._active_start == 0 and self._active_end == self.signal_length

    @property
    def _signal_length(self):
        if self._audio_data is None:
            return None
        return self._audio_data.shape[self._LEN]

    @property
    def power_spectrogram_data(self):
        """
        The power spectrogram is defined as Re(STFT)^2, where ^2 is element-wise squaring of entries of the STFT.
        Same size as self.stft_data.
        Returns: Real valued 2-D np.array with power spectrogram data.
        Raises: AttributeError if self.stft_data is None. Run self.stft() before accessing this.

        """
        if self.stft_data is None:
            raise AttributeError('Cannot calculate power_spectrogram_data until self.stft() is run')
        return np.abs(self.stft_data) ** 2

    ##################################################
    # I/O
    ##################################################

    def load_audio_from_file(self, input_file_path, signal_starting_position=0, signal_length=None):
        # type: (unicode, integer, integer) -> None
        """Loads an audio signal from a .wav file

        Parameters:
            input_file_path: path to input file.
            signal_length (Optional[int]): Length of signal to load. signal_length of 0 means read the whole file
             Defaults to the full length of the signal
            signal_starting_position (Optional[int]): The starting point of the section to be extracted (seconds).
             Defaults to 0 seconds

        """
        if signal_length is not None and signal_starting_position >= signal_length:
            raise IndexError('signal_starting_position cannot be greater than signal_length!')

        try:
            with audioread.audio_open(os.path.realpath(input_file_path)) as input_file:
                self.sample_rate = input_file.samplerate
                file_length = input_file.duration
                n_ch = input_file.channels

            read_mono = True
            if n_ch != 1:
                read_mono = False

            audio_input, self.sample_rate = librosa.load(input_file_path,
                                                         sr=input_file.samplerate,
                                                         offset=0,
                                                         duration=file_length,
                                                         mono=read_mono)

            # Change from fixed point to floating point
            if not np.issubdtype(audio_input.dtype, float):
                audio_input = audio_input.astype('float') / (np.iinfo(audio_input.dtype).max + 1.0)

            self.audio_data = audio_input

        except Exception:
            raise IOError("Cannot read from file, {file}".format(file=input_file_path))

        self.path_to_input_file = input_file_path
        self._active_end = signal_length if signal_length is not None else self._audio_data.shape[self._LEN]
        self._active_start = signal_starting_position

    def load_audio_from_array(self, signal, sample_rate=constants.DEFAULT_SAMPLE_RATE):
        """Loads an audio signal from a numpy array. Only accepts float arrays and int arrays of depth 16-bits.

        Parameters:
            signal (np.array): np.array containing the audio file signal sampled at sampleRate
            sample_rate (Optional[int]): the sample rate of signal. Default is Constants.DEFAULT_SAMPLE_RATE (44.1kHz)

        """
        assert (type(signal) == np.ndarray)

        self.path_to_input_file = None

        # Change from fixed point to floating point
        if not np.issubdtype(signal.dtype, float):
            if np.max(signal) > np.iinfo(np.dtype('int16')).max:
                raise ValueError('Please convert your array to 16-bit audio.')

            signal = signal.astype('float') / (np.iinfo(np.dtype('int16')).max + 1.0)

        self.audio_data = signal
        self.sample_rate = sample_rate
        self._active_start = 0
        self._active_end = self.signal_length

    def write_audio_to_file(self, output_file_path, sample_rate=None, verbose=False):
        """Outputs the audio signal to a .wav file

        Parameters:
            output_file_path (str): Filename where waveform will be saved
            sample_rate (Optional[int]): The sample rate to write the file at. Default is AudioSignal.SampleRate, which
            is the sample rate of the original signal.
            verbose (Optional[bool]): Flag controlling printing when writing the file.
        """
        if self.audio_data is None:
            raise Exception("Cannot write audio file because there is no audio data.")

        try:
            self.peak_normalize()

            if sample_rate is None:
                sample_rate = self.sample_rate

            audio_output = np.copy(self.audio_data)

            # TODO: better fix
            # convert to fixed point again
            if not np.issubdtype(audio_output.dtype, int):
                audio_output = np.multiply(audio_output, 2 ** (constants.DEFAULT_BIT_DEPTH - 1)).astype('int16')

            wav.write(output_file_path, sample_rate, audio_output.T)
        except Exception as e:
            print("Cannot write to file, {file}.".format(file=output_file_path))
            raise e
        if verbose:
            print("Successfully wrote {file}.".format(file=output_file_path))

    def set_active_region(self, start, end):
        """
        Determines the bounds of what gets returned when you access my_audio_signal.audio_data.
        None of the data in my_audio_signal.audio_data gets thrown out when you set the active region, it is just
        not accessible until you re-set the active region.

        This is useful for reusing a single AudioSignal object to do different operations on different parts of the
        audio data.

        Warnings:
            Many functions will raise exceptions while the active region is not default. Be aware that adding,
            subtracting, concatenating, truncating, and other utilities may not be available.
        See Also:
            :ref: set_active_region_to_default
            :ref: active_region_is_default
        Args:
            start: (int) Beginning of active region (in samples). Cannot be less than 0.
            end: (int) End of active region (in samples). Cannot be larger than self.signal_length.

        """
        start, end = int(start), int(end)
        self._active_start = start if start >= 0 else 0
        self._active_end = end if end < self._signal_length else self._signal_length

    def set_active_region_to_default(self):
        """
        Returns the active region of this AudioSignal object to it default value of the entire audio_data array.

        """
        self._active_start = 0
        self._active_end = self._signal_length

    ##################################################
    #               STFT Utilities
    ##################################################

    def stft(self, window_length=None, hop_length=None, window_type=None, n_fft_bins=None, remove_reflection=True,
             overwrite=True, use_librosa=constants.USE_LIBROSA_STFT):
        """Computes the Short Time Fourier Transform (STFT) of the audio signal

        Warning:
            If overwrite=True (default) this will overwrite any data in self.stft_data!

        Returns:
            * **calculated_stft** (*np.array*) - complex stft data
        """
        if self.audio_data is None or self.audio_data.size == 0:
            raise Exception("No time domain signal (self.audio_data) to make STFT from!")

        window_length = self.stft_params.window_length if window_length is None else window_length
        hop_length = self.stft_params.hop_length if hop_length is None else hop_length
        window_type = self.stft_params.window_type if window_type is None else window_type
        n_fft_bins = self.stft_params.n_fft_bins if n_fft_bins is None else n_fft_bins

        calculated_stft = self._do_stft(window_length, hop_length, window_type,
                                        n_fft_bins, remove_reflection, use_librosa)

        if overwrite or self.stft_data is None:
            self.stft_data = calculated_stft

        return calculated_stft

    def _do_stft(self, window_length, hop_length, window_type, n_fft_bins, remove_reflection, use_librosa):
        if self.audio_data is None or self.audio_data.size == 0:
            raise Exception('Cannot do stft without signal!')

        stfts = []

        stft_func = spectral_utils.librosa_stft_wrapper if use_librosa else spectral_utils.e_stft

        for i in range(1, self.num_channels + 1):
            stfts.append(stft_func(signal=self.get_channel(i), window_length=window_length,
                                   hop_length=hop_length, window_type=window_type,
                                   n_fft_bins=n_fft_bins,remove_reflection=remove_reflection))

        return np.array(stfts).transpose((1, 2, 0))

    def istft(self, window_length=None, hop_length=None, window_type=None, overwrite=True,
              reconstruct_reflection=False, use_librosa=constants.USE_LIBROSA_STFT):
        """Computes and returns the inverse Short Time Fourier Transform (STFT).

        Warning:
            If overwrite=True (default) this will overwrite any data in self.audio_data!

        Returns:
             * **calculated_signal** (np.array): time-domain audio signal
        """
        if self.stft_data is None or self.stft_data.size == 0:
            raise Exception('Cannot do inverse STFT without self.stft_data!')

        window_length = self.stft_params.window_length if window_length is None else window_length
        hop_length = self.stft_params.hop_length if hop_length is None else hop_length
        # TODO: bubble up center
        window_type = self.stft_params.window_type if window_type is None else window_type

        calculated_signal = self._do_istft(window_length, hop_length, window_type,
                                           reconstruct_reflection, use_librosa)

        if overwrite or self.audio_data is None:
            self.audio_data = calculated_signal

        return calculated_signal

    def _do_istft(self, window_length, hop_length, window_type, reconstruct_reflection, use_librosa):
        if self.stft_data.size == 0:
            raise ValueError('Cannot do inverse STFT without self.stft_data!')

        signals = []

        istft_func = spectral_utils.librosa_istft_wrapper if use_librosa else spectral_utils.e_istft

        for i in range(1, self.num_channels + 1):
            signals.append(istft_func(stft=self.get_stft_channel(i), window_length=window_length,
                                      hop_length=hop_length, window_type=window_type))

        return np.array(signals)

    ##################################################
    #                  Utilities
    ##################################################

    def concat(self, other):
        """
        Add two AudioSignal objects (by adding self.audio_data) temporally.

        Parameters:
            other (AudioSignal): Audio Signal to concatenate with the current one.
        """
        self._verify_audio(other, 'concat')

        self.audio_data = np.concatenate((self.audio_data, other.audio_data), axis=self._LEN)

    def truncate_samples(self, n_samples):
        """
        Truncates the signal leaving only the first n_samples in number of samples. This can only be done
        if self.active_region_is_default is True.
        Args:
            n_samples: (int) number of samples that will be left.

        """
        if n_samples > self.signal_length:
            raise Exception('n_samples must be less than self.signal_length!')

        if not self.active_region_is_default:
            raise Exception('Cannot truncate while active region is not set as default!')

        self.audio_data = self.audio_data[:, 0: n_samples]

    def truncate_seconds(self, n_seconds):
        """
        Truncates the signal leaving only the first n_seconds. This can only be done
        if self.active_region_is_default is True.
        Args:
            n_seconds: (float) number of seconds to truncate self.audio_data.

        """
        if n_seconds > self.signal_duration:
            raise Exception('n_seconds must be shorter than self.signal_duration!')

        if not self.active_region_is_default:
            raise Exception('Cannot truncate while active region is not set as default!')

        n_samples = n_seconds * self.sample_rate
        self.truncate_samples(n_samples)

    def zero_pad(self, before, after):
        """
        Adds zeros before and after the signal to all channels. Extends the length
        of self.audio_data by before + after.
        Args:
            before: (int) number of zeros to be put before the current contents of self.audio_data
            after: (int) number of zeros to be put after the current contents fo self.audio_data

        """
        if not self.active_region_is_default:
            raise Exception('Cannot zero-pad while active region is not set as default!')

        for ch in range(1, self.num_channels + 1):
            self.audio_data = np.lib.pad(self.get_channel(ch), (before, after), 'constant', constant_values=(0, 0))

    def get_channel(self, n):
        """Gets the n-th channel from ``self.audio_data``. **1-based.**

        Parameters:
            n (int): index of channel to get. **1-based**
        Returns:
            n-th channel (np.array): the audio data in the n-th channel of the signal
        """
        if n > self.num_channels:
            raise Exception(
                'Cannot get channel {0} when this object only has {1} channels!'.format(n, self.num_channels))

        if n <= 0:
            raise Exception('Cannot get channel {}. This will cause unexpected results'.format(n))

        return self._get_axis(self.audio_data, self._CHAN, n - 1)

    def get_stft_channel(self, n):
        """
        Returns the n-th channel from ``self.stft_data``. **1-based.**
        Args:
            n: (int) index of stft channel to get. **1 based**

        Returns:
            n-th channel (np.array): the stft data in the n-th channel of the signal
        """
        if n > self.num_channels:
            raise Exception(
                'Cannot get channel {0} when this object only has {1} channels!'.format(n, self.num_channels))

        return self._get_axis(self.stft_data, self._STFT_CHAN, n - 1)

    def get_power_spectrogram_channel(self, n):
        """
        Returns the n-th channel from ``self.power_spectrogram_data``. **1-based.**
        Args:
            n: (int) index of power spectrogram channel to get. **1 based**

        Returns:
            n-th channel (np.array): the power spectrogram data in the n-th channel of the signal
        """
        if n > self.num_channels:
            raise Exception(
                'Cannot get channel {0} when this object only has {1} channels!'.format(n, self.num_channels))

        # np.array helps with duck typing
        return self._get_axis(np.array(self.power_spectrogram_data), self._STFT_CHAN, n - 1)

    def peak_normalize(self, overwrite=True):
        """ Normalizes the whole audio file to 1.0.
            Notes:
            **If self.audio_data is not represented as floats this will convert the representation to floats!**

        """
        max_val = 1.0
        max_signal = np.max(np.abs(self.audio_data))
        if max_signal > max_val:
            normalized = self.audio_data.astype('float') / max_signal
            if overwrite:
                self.audio_data = normalized
            return normalized

    def add(self, other):
        """Adds two audio signal objects. This does element-wise addition on the ``self.audio_data`` array.

        Parameters:
            other (AudioSignal): Other audio signal to add.
        Returns:
            sum (AudioSignal): AudioSignal with the sum of the current object and other.
        """
        return self + other

    def sub(self, other):
        """Subtracts two audio signal objects. This does element-wise subtraction on the ``self.audio_data`` array.

        Parameters:
            other (AudioSignal): Other audio signal to subtract.
        Returns:
            diff (AudioSignal): AudioSignal with the difference of the current object and other.
        """
        return self - other

    def audio_data_as_ints(self, bit_depth=constants.DEFAULT_BIT_DEPTH):
        """
        Returns self.audio_data as a numpy array of ints with a specified bit depth.
        Notes:
            self.audio_data is regularly stored as an array of floats. This will not affect self.audio_data.
        Args:
            bit_depth: (int) (Optional) Bit depth of the integer array that will be returned

        Returns: (numpy array) Integer representation of self.audio_data

        """
        if bit_depth not in [8, 16, 24, 32]:
            raise TypeError('Cannot convert self.audio_data to integer array of bit depth = {}'.format(bit_depth))

        int_type = 'int' + str(bit_depth)

        return np.multiply(self.audio_data, 2 ** (constants.DEFAULT_BIT_DEPTH - 1)).astype(int_type)

    def to_json(self):
        """
        Converts this AudioSignal object to json.
        Returns: (string) json representation of the current AudioSignal object.
        See Also:
            :ref: self.from_json

        """
        return json.dumps(self, default=AudioSignal._to_json_helper)

    @staticmethod
    def _to_json_helper(o):
        if not isinstance(o, AudioSignal):
            raise TypeError
        import copy
        d = copy.copy(o.__dict__)
        for k, v in d.items():
            if isinstance(v, np.ndarray):
                d[k] = utils.json_ready_numpy_array(v)
        d['__class__'] = o.__class__.__name__
        d['__module__'] = o.__module__
        d['stft_params'] = o.stft_params.to_json()
        return d

    @staticmethod
    def from_json(json_string):
        """
        Creates a new AudioSignal object from a json encoded AudioSignal string.
        Args:
            json_string: (string) a json encoded AudioSignal string

        Returns: (AudioSignal) a new AudioSignal object based on the parameters
        See Also:
            :ref: self.to_json

        """
        return json.loads(json_string, object_hook=AudioSignal._from_json_helper)

    @staticmethod
    def _from_json_helper(json_dict):
        if '__class__' in json_dict:
            class_name = json_dict.pop('__class__')
            module = json_dict.pop('__module__')
            if class_name != AudioSignal.__name__ or module != AudioSignal.__module__:
                raise TypeError
            a = AudioSignal()
            stft_params = json_dict.pop('stft_params')
            a.stft_params = spectral_utils.StftParams.from_json(stft_params)
            for k, v in json_dict.items():
                if isinstance(v, dict) and constants.NUMPY_JSON_KEY in v:
                    a.__dict__[k] = utils.json_numpy_obj_hook(v[constants.NUMPY_JSON_KEY])
                else:
                    a.__dict__[k] = v if not isinstance(v, unicode) else v.encode('ascii')
            return a
        else:
            return json_dict

    def rms(self):
        """
        Calculates the root-mean-square of self.audio_data.
        Returns: (float) root-mean-square of self.audio_data.

        """
        return np.sqrt(np.mean(np.square(self.audio_data)))

    def to_mono(self, overwrite=False):
        """

        Args:
            overwrite:

        Returns:

        """
        mono = np.mean(self.audio_data, axis=self._CHAN)
        if overwrite:
            self.audio_data = mono
        return mono

    ##################################################
    #              Operator overloading
    ##################################################

    def __add__(self, other):
        self._verify_audio(other, 'add')

        if self.signal_length > other.signal_length:
            combined = np.copy(self.audio_data)
            combined[:, :other.signal_length] += other.audio_data
        else:
            combined = np.copy(other.audio_data)
            combined[:, :self.signal_length] += self.audio_data

        return AudioSignal(audio_data_array=combined)

    def __sub__(self, other):
        self._verify_audio(other, 'subtract')

        if self.signal_length > other.signal_length:
            combined = np.copy(self.audio_data)
            combined[:, :other.audio_data.size] -= other.audio_data
        else:
            combined = np.copy(other.audio_data)
            combined[:, :self.audio_data.size] -= self.audio_data

        return AudioSignal(audio_data_array=combined)

    def _verify_audio(self, other, op):
        if self.num_channels != other.num_channels:
            raise Exception('Cannot ' + op + ' with two signals that have a different number of channels!')

        if self.sample_rate != other.sample_rate:
            raise Exception('Cannot' + op + 'with two signals that have different sample rates!')

        if not self.active_region_is_default:
            raise Exception('Cannot' + op + 'while active region is not set as default!')

    def __iadd__(self, other):
        return self + other

    def __isub__(self, other):
        return self - other

    def __mul__(self, other):
        assert isinstance(other, numbers.Real)
        raise NotImplemented('Not implemented yet.')

    def __len__(self):
        return self.signal_length

    def __eq__(self, other):
        for k, v in self.__dict__.items():
            if isinstance(v, np.ndarray):
                if not np.array_equal(v, other.__dict__[k]):
                    return False
            elif v != other.__dict__[k]:
                return False
        return True

    def __ne__(self, other):
        return not self == other

    ##################################################
    #              Private utils
    ##################################################

    @staticmethod
    def _get_axis(array, axis_num, i):
        if array.ndim == 2:
            if axis_num == 0:
                return array[i, :]
            elif axis_num == 1:
                return array[:, i]
            else:
                return None
        elif array.ndim == 3:
            if axis_num == 0:
                return array[i, :, :]
            elif axis_num == 1:
                return array[:, i, :]
            elif axis_num == 2:
                return array[:, :, i]
            else:
                return None
        else:
            return None
