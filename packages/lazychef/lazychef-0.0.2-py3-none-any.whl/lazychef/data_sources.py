"""DataSources are a way of creating a data pipeline.

They are used as a way of both describing the transformation of data and computing it.
"""

import os
from collections import Iterable
from abc import abstractmethod
import h5py
import numpy as np
from numbers import Integral

from .lookup_tables import TTVLookupTable


class DataSource(object):
    """Base class for all datasources.

    Note that the default __getitem__ returns a generator (for lazier evaluation).
    """

    def __getitem__(self, key):
        if isinstance(key, Iterable) and type(key) != str:
            return [self._process(uri) for uri in key]
        else:
            return self._process(key)

    @abstractmethod
    def _process(self, ident):
        pass


class AddressAdapter(DataSource):
    """Used to change the naming scheme bewteen two datasources."""

    def __init__(self, adapt_ident, data_source):
        self.adapt_ident = adapt_ident
        self.data_source = data_source

    def _process(self, ident):
        adapted = self.adapt_ident(ident)
        return self.data_source[adapted]


class FileDataSource(DataSource):
    """Wrapper around file system"""

    def __init__(self, base_dir='', suffix=''):
        self.base_dir = base_dir
        self.suffix = suffix

    def _process(self, ident):
        path_to_file = os.path.join(self.base_dir, ident + self.suffix)
        assert os.path.exists(path_to_file), path_to_file + ' does not exist'
        return path_to_file


class WaveformDataSource(DataSource):
    """Datasource which produces waveforms from a path to file.

    The file source must produce a path to a sound file when given a string id
    """

    def __init__(self, file_source, process_waveform):
        self.file_source = file_source
        self.process_waveform = process_waveform
        self.waveform_frequency = None
        self.waveform_length = None

    def _process(self, ident):
        frequency, waveform = self.process_waveform(self.file_source[ident])

        if self.waveform_frequency is None and self.waveform_length is None:
            self.waveform_frequency = frequency
            self.waveform_length = len(waveform)
        else:
            try:
                assert frequency == self.waveform_frequency
                assert len(waveform) == self.waveform_length
            except Exception as e:
                e.args += ('Waveform structure not consistent.\n',)
                raise e
        return waveform


class SpectrogramDataSource(DataSource):
    """Datasource which produces spectrograms from a waveform.

    The waveform source must produce a waveform when given a string id (i.e. a WaveformDataSource)
    """
    def __init__(self, waveform_source, process_spectrogram):
        self.waveform_source = waveform_source
        self.process_spectrogram = process_spectrogram
        self.spectrogram_frequencies = None
        self.spectrogram_times = None

    def _process(self, key):
        frequencies, times, spectrogram = self.process_spectrogram(
            self.waveform_source[key],
            self.waveform_source.waveform_frequency
        )

        if self.spectrogram_frequencies is None:
            self.spectrogram_frequencies = frequencies
        if self.spectrogram_times is None:
            self.spectrogram_times = times

        try:
            assert frequencies.shape == self.spectrogram_frequencies.shape
            assert times.shape == self.spectrogram_times.shape
        except Exception as e:
            e.message += ('Spectrogram shape not consistent.\n',)
            raise e

        return spectrogram


class LambdaDataSource(DataSource):
    def __init__(self, function, data_source):
        self.function = function
        self.data_source = data_source

    def _process(self, ident):
        return self.function(self.data_source[ident])


class ArrayLikeDataSource(DataSource):
    """Base clas for ArrayLikeDataSources. These are used as a way of treating the data as if it were one big numpy array.

    All calls for __getitem___ in classes inheriting form this should return __instantiated__ data.
    """
    @abstractmethod
    def __getitem___(self, key):
        pass

    @abstractmethod
    def __len__(self):
        pass

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]


class TTVArrayLikeDataSource(ArrayLikeDataSource):
    """Uses a ttv split to create a lookup table from uri -> index and vice versa."""
    def __init__(self, data_source, ttv):
        self.data_source = data_source
        self.lookup = TTVLookupTable(ttv, shuffle_in_set=True)

    def __getitem__(self, key):
        if is_int_like(key):
            return self.data_source[self.lookup[key]]
        elif is_array_like(key):
            return [x for x in self.data_source[self.lookup[key]]]
        elif type(key) == slice:
            return [x for x in self.data_source[self.lookup[key]]]
        else:
            raise RuntimeError('key: {} is not compatible with this datasource'.format(str(key)))

    def __len__(self):
        return len(self.lookup)

    def get_set(self, set_name):
        return SubArrayLikeDataSource(self, *self.lookup.get_set_bounds(set_name))


class SubArrayLikeDataSource(ArrayLikeDataSource):
    """Only shows a slice of another ArrayLikeDataSource."""
    def __init__(self, parent, lower, upper):
        assert len(parent) >= upper - lower

        self.parent = parent
        self.lower = lower
        self.upper = upper

    def __getitem__(self, key):
        if is_int_like(key):
            key += self.lower
            assert key < self.upper
            return self.parent[key]
        elif type(key) == slice:
            s = key
            start, stop = s.start, s.stop
            if start is None:
                start = 0
            if stop is None:
                stop = len(self)
            s = slice(
                self.__resolve_slice_for_array_boundaries(start),
                self.__resolve_slice_for_array_boundaries(stop),
                s.step
            )
            return self.parent[s]
        if is_array_like(key):
            keyarr = key
            return np.array([self.parent[i + self.lower] for i in keyarr if i + self.lower < self.upper])
        else:
            raise RuntimeError('key: {} is not compatible with this datasource'.format(str(key)))

    def __resolve_slice_for_array_boundaries(self, edge_index):
        if edge_index >= 0:
            edge_index = min(self.upper, self.lower + edge_index)
        else:
            edge_index = max(self.lower, self.upper - edge_index)
        return edge_index

    def __len__(self):
        return self.upper - self.lower


class CachedTTVArrayLikeDataSource(TTVArrayLikeDataSource):
    CACHE_BITARRAY_SUFFIX = '_bitarray'
    """
    Cache computed examples after they are called.

    If a cache file already exists with the same file name, it will try to use that as a cache, and will break if it's
    not compatible.
    """

    def __init__(self, data_source, ttv, data_name='data', cache_name='ttv_cache'):
        super().__init__(data_source, ttv)
        self.cache = h5py.File(cache_name + '.cache.hdf5', 'a')
        self.data_name = data_name
        if data_name in self.cache:
            self.__assert_cache_compatibility(self.cache[data_name])

        # instantiate the existence_cache now, even if there is no cache created at all
        self.__init_existence_cache()

    def __assert_cache_compatibility(self, h5_group):
        assert len(h5_group) == len(self), 'Cache has a different size to the datasource'
        exaple_data = self.cache[self.data_name][0]
        assert exaple_data.shape == h5_group[0].shape, (
            'Cache for datasource contains differently shaped data to actual datasource'
        )
        assert np.all(exaple_data == h5_group[0][:]), (
            'Cache for datasource contains different data to actual datasource'
        )

    def __init_existence_cache(self):
        if self.data_name not in self.cache or len(self.cache[self.data_name]) == 0:
            self.existence_cache = np.zeros(len(self), dtype=bool)
        else:
            self.existence_cache = self.cache[self.data_name + self.CACHE_BITARRAY_SUFFIX][:]

    def __get_from_data_source(self, key):
        data = super().__getitem__(key)
        if is_array_like(data):
            data = np.array(data)

        if self.data_name not in self.cache or len(self.cache[self.data_name]) == 0:
            if is_int_like(key):
                example_data = data
            elif is_array_like(key) or type(key) == slice:
                example_data = data[0]
            self.__init_cache(example_data)

        self.cache[self.data_name][key] = data

        self.existence_cache[key] = True
        self.cache[self.data_name + self.CACHE_BITARRAY_SUFFIX][key] = True

        return data

    def __init_cache(self, example_input):
        number_of_samples = len(self)
        self.cache.create_dataset(
            self.data_name,
            shape=(number_of_samples,) + example_input.shape,
            dtype=example_input.dtype
        )
        # currently not a bit array techincally
        self.cache.create_dataset(
            self.data_name + self.CACHE_BITARRAY_SUFFIX,
            data=self.existence_cache
        )

    def __getitem__(self, key):
        if type(key) == slice:
            # if all in cache, then use slice, else don't
            start, stop, step = key.start, key.stop, key.step

            in_cache = self.existence_cache[start:stop:step]
            if np.all(in_cache):
                return self.cache[self.data_name][start:stop:step]
            elif np.all(np.logical_not(in_cache)):
                return self.__get_from_data_source(slice(start, stop, step))

            key = slice_to_range(key, len(self))

        if is_int_like(key):
            index = key
            if self.existence_cache[index]:
                return self.cache[self.data_name][index]
            else:
                return self.__get_from_data_source(index)

        if is_array_like(key):
            data = []

            for index, in_cache in zip(key, self.existence_cache[key]):
                if in_cache:
                    datum = self.cache[self.data_name][index]
                else:
                    datum = self.__get_from_data_source(index)

                data.append(datum)
            return np.array(data)

        else:
            raise RuntimeError('key: {} is not compatible with this datasource'.format(str(key)))


def is_array_like(x):
    return isinstance(x, Iterable) and type(x) != str


def is_int_like(x):
    return isinstance(x, Integral) or (isinstance(x, np.ndarray) and np.shape(x) == ())


def slice_to_range(s, max_value):
    start = s.start if s.start is not None else 0
    stop = s.stop if s.stop is not None else max_value
    step = s.step if s.step is not None else 1
    return range(start, stop, step)


def merge_dicts(*dicts):
    merged = {}
    for d in dicts:
        merged.update(d)
    return merged
