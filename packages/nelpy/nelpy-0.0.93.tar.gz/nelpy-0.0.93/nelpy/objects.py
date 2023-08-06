#encoding : utf-8
"""This module contains the core nelpy object definitions:
 * EventArray
 * EpochArray
 * SpikeTrain and SpikeTrainArray
 * AnalogSignal and AnalogSignalArray
 * BinnedSpikeTrain and BinnedSpikeTrainArray
"""

__all__ = ['EpochArray',
           'EventArray',
           'EpochArray',
           'AnalogSignal',
           'AnalogSignalArray',
           'SpikeTrain',
           'SpikeTrainArray',
           'BinnedSpikeTrain',
           'BinnedSpikeTrainArray']

# TODO: how should we organize our modules so that nelpy.objects.np does
# not shpw up, for example? If I type nelpy.object.<tab> I only want the
# actual objects to appear in the list. I think I do this with __all__,
# but still haven't quite figured it out yet. __all__ seems to mostly be
# useful for when we want to do from xxx import * in the package
# __init__ method

from .utils import is_sorted, get_contiguous_segments, linear_merge


import warnings
import numpy as np
# from shapely.geometry import Point

########################################################################
# Helper functions
########################################################################

#----------------------------------------------------------------------#
#======================================================================#

# TODO: how should AnalogSignal handle its support? As an EpochArray?
# then what about binning issues? As explicit bin centers? As bin
# indices?
#
# it seems best to have a BinnedEpoch class, so that bin centers can be
# computed lazily when needed, and that duration etc. will be trivial,
# but we also really, REALLY need to be able to index AnalogSignal with
# a regular Epoch or EpochArray object, ...
#
# a nice finish to AnalogSignal would be to plot AnalogSignal on its
# support along with a smoothed version of it

### contested classes --- unclear whether these should exist or not:

# class Event
# class Epoch
# class Spike(Event)

def fsgetter(self):
    """(float) [generic getter] Sampling frequency."""
    if self._fs is None:
        warnings.warn("No sampling frequency has been specified!")
    return self._fs

def fssetter(self, val):
    """(float) [generic setter] Sampling frequency."""
    if self._fs == val:
        return
    try:
        if val <= 0:
            pass
    except:
        raise TypeError("sampling rate must be a scalar")
    if val <= 0:
        raise ValueError("sampling rate must be positive")

    # if it is the first time that a sampling rate is set, do not
    # modify anything except for self._fs:
    if self._fs is None:
        pass
    else:
        warnings.warn(
            "Sampling frequency has been updated! This will "
            "modify the spike times."
            )
        self.time = self.samples / val
    self._fs = val

########################################################################
# class EpochArray
########################################################################
class EpochArray:
    """An array of epochs, where each epoch has a start and stop time.

    Parameters
    ----------
    samples : np.array
        If shape (n_epochs, 1) or (n_epochs,), the start time for each
        epoch (which then requires a duration to be specified).
        If shape (n_epochs, 2), the start and stop times for each epoch.
    fs : float, optional
        Sampling rate in Hz. If fs is passed as a parameter, then time
        is assumed to be in sample numbers instead of actual time.
    duration : np.array, float, or None, optional
        The length of the epoch. If (float) then the same duration is
        assumed for every epoch.
    meta : dict, optional
        Metadata associated with spiketrain.

    Attributes
    ----------
    time : np.array
        The start and stop times for each epoch. With shape (n_epochs, 2).
    samples : np.array
        The start and stop samples for each epoch. With shape (n_epochs, 2).
    fs: float
        Sampling frequency (Hz).
    meta : dict
        Metadata associated with spiketrain.
    """

    def __init__(self, samples, *, fs=None, duration=None, meta=None):

        samples = np.squeeze(samples)  # coerce samples into np.array

        # all possible inputs:
        # 1. single epoch, no duration    --- OK
        # 2. single epoch and duration    --- ERR
        # 3. multiple epochs, no duration --- OK
        # 4. multiple epochs and duration --- ERR
        # 5. single scalar and duration   --- OK
        # 6. scalar list and duratin list --- OK
        #
        # Q. won't np.squeeze make our life difficult?
        #
        # Strategy: determine if duration was passed. If so, try to see
        # if samples can be coerced into right shape. If not, raise 
        # error. 
        # If duration was NOT passed, then do usual checks for epochs.

        if duration is not None:  # assume we received scalar starts
            samples = np.array(samples, ndmin=1)
            duration = np.squeeze(duration).astype(float)
            if duration.ndim == 0:
                duration = duration[..., np.newaxis]

            if samples.ndim == 2 and duration.ndim == 1:
                raise ValueError(
                    "duration not allowed when using start and stop "
                    "times")

            if len(duration) > 1:
                if samples.ndim == 1 and samples.shape[0] != duration.shape[0]:
                    raise ValueError(
                        "must have same number of time and duration "
                        "samples"
                        )
            if samples.ndim == 1 and duration.ndim == 1:
                stop_epoch = samples + duration
                samples = np.hstack(
                    (samples[..., np.newaxis], stop_epoch[..., np.newaxis]))
        else:  # duration was not specified, so assume we recived epochs

            # Note: if we have an empty array of samples with no 
            # dimension, then calling len(samples) will return a
            # TypeError.
            try:
                # if no samples were received, return an empty EpochArray:
                if len(samples) == 0:
                    self._emptyEpochArray()
                    return
            except TypeError:
                warnings.warn("unsupported type (" 
                    + str(type(samples))
                    + "); creating empty EpochArray")
                self._emptyEpochArray()
                return
            
            # Only one epoch is given eg EpochArray([3,5,6,10]) with no
            # duration and more than two values:
            if samples.ndim == 1 and len(samples) > 2:  # we already know duration is None
                raise TypeError(
                    "samples of size (n_epochs, ) has to be accompanied by "
                    "a duration")

            if samples.ndim == 1:  # and duration is None:
                samples = np.array([samples])

        if samples.ndim > 2:
            raise ValueError("samples must be a 1D or a 2D vector")

        # set initial fs to None
        self._fs = None
        # then attempt to update the fs; this does input validation:
        self.fs = fs

        try:
            if samples[:, 0].shape[0] != samples[:, 1].shape[0]:
                raise ValueError(
                    "must have the same number of start and stop times")
        except Exception:
            raise Exception("Unhandled EpochArray.__init__ case.")

        # TODO: what if start == stop? what will this break? This situation
        # can arise automatically when slicing a spike train with one or no
        # spikes, for example in which case the automatically inferred support
        # is a delta dirac

        if samples.ndim == 2 and np.any(samples[:, 1] - samples[:, 0] < 0):
            raise ValueError("start must be less than or equal to stop")

        # TODO: why not just sort in-place here? Why store sort_idx? Why do
        # we explicitly sort epoch samples, but not spike times?
        # sort_idx = np.argsort(samples[:, 0])
        # samples = samples[sort_idx]

        # if a sampling rate was given, relate time to samples using fs:
        if fs is not None:
            time = samples / fs
        else:
            time = samples

        self.time = time
        self.samples = samples
        self._fs = fs
        self._meta = meta

    def _emptyEpochArray(self):
        """Clears all instance variables."""
        self.samples = np.array([])
        self.time = np.array([])
        self._fs = None
        self._meta = None
        return

    def __repr__(self):
        if self.isempty:
            return "<empty EpochArray>"
        if self.n_epochs > 1:
            nstr = "%s epochs" % (self.n_epochs)
        else:
            nstr = "1 epoch"
        dstr = "totaling %s seconds" % self.duration
        return "<EpochArray: %s> %s" % (nstr, dstr)

    def __iter__(self):
        """EpochArray iterator initialization."""
        # initialize the internal index to zero when used as iterator
        self._index = 0
        return self

    def __next__(self):
        """EpochArray iterator advancer."""
        index = self._index
        if index > self.n_epochs - 1:
            raise StopIteration
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            epoch = EpochArray(
                        np.array([self.samples[index, :]]),
                        fs=self.fs,
                        meta=self.meta
                        )
        self._index += 1
        return epoch

    def __getitem__(self, idx):
        """EpochArray index access.
        
        Accepts integers, slices, and EpochArrays.
        """
        if isinstance(idx, EpochArray):
            # case #: (self, idx):
            # case 0: idx.isempty == True
            # case 1: (fs, fs) = (None, const)
            # case 2: (fs, fs) = (const, None)
            # case 3: (fs, fs) = (None, None)
            # case 4: (fs, fs) = (const, const)
            # case 5: (fs, fs) = (constA, constB)
            if idx.isempty:  # case 0:
                return EpochArray([])
            if idx.fs != self.fs:  # cases (1, 2, 5):
                epoch = self.intersect(
                    epoch=EpochArray(idx.time, fs=None),
                    boundaries=True
                    )
            else:  # cases (3, 4)
                epoch = self.intersect(
                    epoch=idx,
                    boundaries=True
                    ) # what if fs of slicing epoch is different?
            if epoch.isempty:
                return EpochArray([])
            return epoch
        elif isinstance(idx, int):
            try:
                epoch = EpochArray(
                    np.array([self.samples[idx, :]]),
                    fs=self.fs,
                    meta=self.meta
                    )
                return epoch
            except IndexError:
                # index is out of bounds, so return an empty EpochArray
                return EpochArray([])
        else:
            try:
                epocharray = EpochArray(
                    np.array([self.starts[idx], self.stops[idx]]).T,
                    fs=self.fs,
                    meta=self.meta
                    )
                return epocharray
            except Exception:
                raise TypeError(
                    'unsupported subsctipting type {}'.format(type(idx)))

    @property
    def meta(self):
        """Meta data associated with SpikeTrain."""
        if self._meta is None:
            warnings.warn("meta data is not available")
        return self._meta

    @meta.setter
    def meta(self, val):
        self._meta = val

    @property
    def fs(self):
        """(float) Sampling frequency."""
        return fsgetter(self)

    @fs.setter
    def fs(self, val):
        """(float) Sampling frequency."""
        fssetter(self, val)

    @property
    def centers(self):
        """(np.array) The center of each epoch."""
        if self.isempty:
            return []
        return np.mean(self.time, axis=1)

    @property
    def durations(self):
        """(np.array) The duration of each epoch."""
        if self.isempty:
            return 0
        return self.time[:, 1] - self.time[:, 0]

    @property
    def duration(self):
        """(float) The total duration of the epoch array."""
        if self.isempty:
            return 0
        return np.array(self.time[:, 1] - self.time[:, 0]).sum()

    @property
    def starts(self):
        """(np.array) The start of each epoch."""
        if self.isempty:
            return []
        return self.time[:, 0]

    @property
    def _sampleStarts(self):
        """(np.array) The start of each epoch, in samples"""
        if self.isempty:
            return []
        return self.samples[:, 0]

    @property
    def start(self):
        """(np.array) The start of the first epoch."""
        if self.isempty:
            return []
        return self.time[:, 0][0]

    @property
    def _sampleStart(self):
        """(np.array) The start of the first epoch, in samples"""
        if self.isempty:
            return []
        return self.samples[:, 0][0]

    @property
    def stops(self):
        """(np.array) The stop of each epoch."""
        if self.isempty:
            return []
        return self.time[:, 1]

    @property
    def _sampleStops(self):
        """(np.array) The stop of each epoch, in samples"""
        if self.isempty:
            return []
        return self.samples[:, 1]

    @property
    def stop(self):
        """(np.array) The stop of the last epoch."""
        if self.isempty:
            return []
        return self.time[:, 1][-1]

    @property
    def _sampleStop(self):
        """(np.array) The stop of the first epoch, in samples"""
        return self.samples[:, 0][0]

    @property
    def n_epochs(self):
        """(int) The number of epochs."""
        if self.isempty:
            return 0
        return len(self.time[:, 0])

    @property
    def issorted(self):
        """(bool) Left edges of epochs are sorted in ascending order."""
        return is_sorted(self.starts)

    @property
    def isempty(self):
        """(bool) Empty SpikeTrain."""
        return len(self.time) == 0

    def copy(self):
        """(EpochArray) Returns a copy of the current epoch array."""
        new_starts = np.array(self._sampleStarts)
        new_stops = np.array(self._sampleStops)
        return EpochArray(
            new_starts,
            duration=new_stops - new_starts,
            fs=self.fs,
            meta=self.meta
            )

    def intersect(self, epoch, boundaries=True, meta=None):
        """Finds intersection (overlap) between two sets of epoch arrays.
        Sampling rates can be different.
        Parameters
        ----------
        epoch : nelpy.EpochArray
        boundaries : bool
            If True, limits start, stop to epoch start and stop.
        meta : dict, optional
            New dictionary of meta data for epoch ontersection.
        Returns
        -------
        intersect_epochs : nelpy.EpochArray
        """
        if self.isempty or epoch.isempty:
            warnings.warn('epoch intersection is empty')
            return EpochArray([], duration=[], meta=meta)

        new_starts = []
        new_stops = []
        epoch_a = self.copy().merge()
        epoch_b = epoch.copy().merge()

        for aa in epoch_a.time:
            for bb in epoch_b.time:
                if (aa[0] <= bb[0] < aa[1]) and (aa[0] < bb[1] <= aa[1]):
                    new_starts.append(bb[0])
                    new_stops.append(bb[1])
                elif (aa[0] < bb[0] < aa[1]) and (aa[0] < bb[1] > aa[1]):
                    new_starts.append(bb[0])
                    if boundaries:
                        new_stops.append(aa[1])
                    else:
                        new_stops.append(bb[1])
                elif (aa[0] > bb[0] < aa[1]) and (aa[0] < bb[1] < aa[1]):
                    if boundaries:
                        new_starts.append(aa[0])
                    else:
                        new_starts.append(bb[0])
                    new_stops.append(bb[1])
                elif (aa[0] >= bb[0] < aa[1]) and (aa[0] < bb[1] >= aa[1]):
                    if boundaries:
                        new_starts.append(aa[0])
                        new_stops.append(aa[1])
                    else:
                        new_starts.append(bb[0])
                        new_stops.append(bb[1])

        if not boundaries:
            new_starts = np.unique(new_starts)
            new_stops = np.unique(new_stops)
        
        # case 1: (fs, fs) = (None, const)
        # case 2: (fs, fs) = (const, None)
        # case 3: (fs, fs) = (None, None)
        # case 4: (fs, fs) = (const, const)
        # case 5: (fs, fs) = (constA, constB)

        if self.fs != epoch.fs:  # cases (1, 2, 5)
            warnings.warn(
                "sampling rates are different; intersecting along "
                "time only and throwing away fs"
                )
            return EpochArray(
                np.hstack(
                    [np.array(new_starts)[..., np.newaxis],
                     np.array(new_stops)[..., np.newaxis]]
                    ),
                fs=None,
                meta=meta
                )
        elif self.fs is None:  # cases (1, 3) [1 already handled]
            return EpochArray(
                np.hstack(
                    [np.array(new_starts)[..., np.newaxis],
                     np.array(new_stops)[..., np.newaxis]]
                    ),
                fs=None,
                meta=meta
                )
        else:  # case (4, )
            return EpochArray(
                np.hstack(
                    [np.array(new_starts)[..., np.newaxis],
                     np.array(new_stops)[..., np.newaxis]])*self.fs,
                fs=self.fs,
                meta=meta
                )

    def merge(self, gap=0.0):
        """Merges epochs that are close or overlapping.
        Parameters
        ----------
        gap : float, optional
            Amount (in time) to consider epochs close enough to merge.
            Defaults to 0.0 (no gap).
        Returns
        -------
        merged_epochs : nelpy.EpochArray
        """
        if self.isempty:
            return self

        if gap < 0:
            raise ValueError("gap cannot be negative")

        epoch = self.copy()

        if self.fs is not None:
            gap = gap * self.fs

        stops = epoch._sampleStops[:-1] + gap
        starts = epoch._sampleStarts[1:]
        to_merge = (stops - starts) >= 0

        new_starts = [epoch._sampleStarts[0]]
        new_stops = []

        next_stop = epoch._sampleStops[0]
        for i in range(epoch.time.shape[0] - 1):
            this_stop = epoch._sampleStops[i]
            next_stop = max(next_stop, this_stop)
            if not to_merge[i]:
                new_stops.append(next_stop)
                new_starts.append(epoch._sampleStarts[i + 1])

        new_stops.append(epoch._sampleStops[-1])

        new_starts = np.array(new_starts)
        new_stops = np.array(new_stops)

        return EpochArray(
            new_starts,
            duration=new_stops - new_starts,
            fs=self.fs,
            meta=self.meta
            )

    def expand(self, amount, direction='both'):
        """Expands epoch by the given amount.
        Parameters
        ----------
        amount : float
            Amount (in time) to expand each epoch.
        direction : str
            Can be 'both', 'start', or 'stop'. This specifies
            which direction to resize epoch.
        Returns
        -------
        expanded_epochs : nelpy.EpochArray
        """
        if direction == 'both':
            resize_starts = self.time[:, 0] - amount
            resize_stops = self.time[:, 1] + amount
        elif direction == 'start':
            resize_starts = self.time[:, 0] - amount
            resize_stops = self.time[:, 1]
        elif direction == 'stop':
            resize_starts = self.time[:, 0]
            resize_stops = self.time[:, 1] + amount
        else:
            raise ValueError(
                "direction must be 'both', 'start', or 'stop'")

        return EpochArray(
            np.hstack((
                resize_starts[..., np.newaxis],
                resize_stops[..., np.newaxis]
                ))
            )

    def shrink(self, amount, direction='both'):
        """Shrinks epoch by the given amount.
        Parameters
        ----------
        amount : float
            Amount (in time) to shrink each epoch.
        direction : str
            Can be 'both', 'start', or 'stop'. This specifies
            which direction to resize epoch.
        Returns
        -------
        shrinked_epochs : nelpy.EpochArray
        """
        both_limit = min(self.durations / 2)
        if amount > both_limit and direction == 'both':
            raise ValueError("shrink amount too large")

        single_limit = min(self.durations)
        if amount > single_limit and direction != 'both':
            raise ValueError("shrink amount too large")

        return self.expand(-amount, direction)

    def join(self, epoch, meta=None):
        """Combines [and merges] two sets of epochs. Epochs can have
        different sampling rates.

        Parameters
        ----------
        epoch : nelpy.EpochArray
        meta : dict, optional
            New meta data dictionary describing the joined epochs.

        Returns
        -------
        joined_epochs : nelpy.EpochArray
        """

        if self.isempty:
            return epoch
        if epoch.isempty:
            return self

        if self.fs != epoch.fs:
            warnings.warn(
                "sampling rates are different; joining along time "
                "only and throwing away fs"
                )
            join_starts = np.concatenate(
                (self.time[:, 0], epoch.time[:, 0]))
            join_stops = np.concatenate(
                (self.time[:, 1], epoch.time[:, 1]))
            #TODO: calling merge() just once misses some instances.
            # I haven't looked carefully enough to know which edge cases
            # these are...
            # merge() should therefore be checked!
            # return EpochArray(join_starts, fs=None,
            # duration=join_stops - join_starts, meta=meta).merge()
            # .merge()
            return EpochArray(
                join_starts,
                fs=None,
                duration=join_stops - join_starts,
                meta=meta
                )
        else:
            join_starts = np.concatenate(
                (self.samples[:, 0], epoch.samples[:, 0]))
            join_stops = np.concatenate(
                (self.samples[:, 1], epoch.samples[:, 1]))

        # return EpochArray(join_starts, fs=self.fs, duration=
        # join_stops - join_starts, meta=meta).merge().merge()
        return EpochArray(
            join_starts,
            fs=self.fs,
            duration=join_stops - join_starts,
            meta=meta
            )

    def contains(self, value):
        """Checks whether value is in any epoch.

        Parameters
        ----------
        epochs: nelpy.EpochArray
        value: float or int

        Returns
        -------
        boolean

        """
        # TODO: consider vectorizing this loop, which should increase
        # speed, but also greatly increase memory? Alternatively, if we
        # could assume something about epochs being sorted, this can
        # also be made much faster than the current O(N)
        for start, stop in zip(self.starts, self.stops):
            if start <= value <= stop:
                return True
        return False
#----------------------------------------------------------------------#
#======================================================================#


########################################################################
# class EventArray
########################################################################
class EventArray:
    """Class description.

    Parameters
    ----------
    samples : np.array
        If shape (n_epochs, 1) or (n_epochs,), the start time for each
        epoch.
        If shape (n_epochs, 2), the start and stop times for each epoch.
    fs : float, optional
        Sampling rate in Hz. If fs is passed as a parameter, then time
        is assumed to be in sample numbers instead of actual time.

    Attributes
    ----------
    time : np.array
        The start and stop times for each epoch. With shape (n_epochs, 2).
    """

    def __init__(self, *, samples, fs=None, duration=None, meta=None):

        # if no samples were received, return an empty EpochArray:
        if len(samples) == 0:
            self.samples = np.array([])
            self.time = np.array([])
            self._fs = None
            self._meta = None
            return

        self._fs = fs
        self._meta = meta

    def __repr__(self):
        if self.isempty:
            return "<empty EventArray>"
        # return "<EventArray: %s> %s" % (nstr, dstr)
        return "<EventArray"

    def __getitem__(self, idx):
        raise NotImplementedError(
            'EventArray.__getitem__ not implemented yet')

    @property
    def isempty(self):
        """(bool) Empty EventArray."""
        raise NotImplementedError(
            'EventArray.isempty not implemented yet')
#----------------------------------------------------------------------#
#======================================================================#


########################################################################
# class AnalogSignal
########################################################################
class AnalogSignal:
    """A continuous, analog signal, with a regular sampling rate.

    Parameters
    ----------
    ydata : np.array(dtype=np.float)
    xdata : np.array(dtype=np.float), optional
        if fs is provided xdata is assumed to be sample numbers
        else it is assumed to be time but xdata can be a non time 
        variable
    fs : float, optional
        Sampling rate in Hz. If fs is passed as a parameter, then time
        is assumed to be in sample numbers instead of actual time.
    support : EpochArray, optional
        EpochArray array on which spiketrain is defined.
        Default is [0, last spike] inclusive.

    Attributes
    ----------
    ydata : np.array
        With shape (n_samples,).
    xdata : np.array
        With shape (n_samples,).
    time : np.array
        With shape (n_samples,).
    fs : float, scalar, optional
        See Parameters
    support : EpochArray, optional
        See Parameters

    """
    def __init__(self, ydata, *, xdata=None, fs=None, support=None):
        ydata = np.squeeze(ydata).astype(float)
        

        # Note; if we have an empty array of ydata with no dimension,
        # then calling len(ydata) will return a TypeError
        try:
            # if no ydata are given return empty AnalogSignal
            if len(ydata) == 0:
                self._emptyAnalogSignal()
                return
        except TypeError:
            warnings.warn("unsupported type; creating empty AnalogSignal")
            self._emptyAnalogSignal()
            return

        # Note: if both xdata and ydata are given and dimensionality does not 
        # match, then TypeError!
        if(xdata is not None):
            xdata = np.squeeze(xdata).astype(float)
            if(xdata.shape[0] != ydata.shape[0]):
                self._emptyAnalogSignal()
                raise TypeError("xdata and ydata size mismatch!")

        self.ydata = ydata

        # set initial fs to None
        self._fs = None
        # then attempt to update the fs; this does input validation:
        self.fs = fs

        # Note: time will be None if this is not a time series and fs isn't 
        # specified set xtime to None. 
        self._time = None
        time = None

        # Alright, let's handle all the possible parameter cases!
        if xdata is not None:
            if fs is not None:
                time = xdata / fs
                self.xdata = xdata
                if support is not None:
                    # xdata, fs, support passed properly
                    # self.support = support
                    self._time = time
                    self._restrict_to_epoch_array(epocharray=support)
                # xdata, fs and no support
                else: 
                    warnings.warn("support created with given xdata and sampling rate, fs!")
                    self._time = time
                    self.support = EpochArray(get_contiguous_segments(xdata,
                        step=1/fs), fs=fs)
            else:
                time = xdata
                self.xdata = xdata
                # xdata and support
                if support is not None: 
                    # self.support = support
                    self._time = time
                    self._restrict_to_epoch_array(epocharray=support)
                    warnings.warn("support created with specified epoch array but no specified sampling rate")
                # xdata
                else: 
                    warnings.warn("support created with just xdata! no sampling rate specified so support is entire range of signal")
                    self._time = time
                    self.support = EpochArray(np.array([0, time[-1]]))
        else:
            xdata = np.arange(0, len(ydata), 1)
            if fs is not None:
                time = xdata / fs
                # fs and support
                if support is not None:
                    self._emptyAnalogSignal()
                    raise TypeError("xdata must be passed if support is specified")
                # just fs
                else:
                    self._time = time
                    warnings.warn("support created with given sampling rate, fs")
                    self.support = EpochArray(np.array([0, time[-1]]))
            else:
                # just support
                if support is not None:
                    self._emptyAnalogSignal()
                    raise TypeError("xdata must be passed if support is "
                        +"specified")
                # just ydata
                else:
                    self._time = xdata
                    warnings.warn("support created with given ydata! support is entire signal")
                    self.support = EpochArray(np.array([0, xdata[-1]]))
            self.xdata = xdata

    def _restrict_to_epoch_array(self, *, epocharray=None, update=True):
        """Restrict self._time and self.ydata to an EpochArray. If no
        EpochArray is specified, self. support is used.

        Parameters
        ----------
        epocharray : EpochArray, optional
        	EpochArray on which to restrict AnalogSignal. Default is 
        	self.support
        update : bool, optional
        	Overwrite self.support with epocharray if True (default).
        """
        if epocharray is None:
            epocharray = self.support
            update = False # support did not change; no need to update

        if epocharray.isempty:
            warnings.warn("Support specified is empty")
            self._emptyAnalogSignal()
            return

        indices = []
        for eptime in epocharray.time:
            t_start = eptime[0]
            t_stop = eptime[1]
            indices.append((self.time >= t_start) & (self.time <= t_stop))
        indices = np.any(np.column_stack(indices), axis=1)
        if np.count_nonzero(indices) < len(self._time):
            warnings.warn(
                'ignoring signal outside of support')
        self.ydata = self.ydata[indices]
        self._time = self._time[indices]
        self.xdata = self.xdata[indices]
        if update:
            self.support = epocharray

    def _emptyAnalogSignal(self):
        """Empty all the instance attributes for an empty object."""
        self.ydata = np.array([])
        self.xdata = np.array([])
        self.support = EpochArray([])
        self._fs = None
        self._time = None
        return

    def __repr__(self):
        if self.isempty:
            return "<empty AnalogSignal>"
        if self.n_epochs > 1:
            nstr = "%s epochs in analog signal" % (self.n_epochs)
        else:
            nstr = "1 epoch"
        dstr = "totalling %s seconds" % self.support.duration
        return "<AnalogSignal: %s> %s" % (nstr,dstr)

    # @property
    # def ydata(self):
    #     return self.ydata

    # @ydata.setter
    # def ydata(self, val):
    #     """set ydata...user should NOT be able to call"""
    #     self.ydata = val

    # @property
    # def xdata(self):
    #     if self.xdata is None:
    #         warnings.warn("No xdata specified")
    #     return self.xdata

    @property
    def time(self):
        if self._time is None:
            warnings.warn("No time calculated. This should be due to no xdata specified")
        return self._time

    # @property
    # def support(self):
    #     if self.support is None:
    #         warnings.warn("No support specified")
    #     return self.support

    @property
    def fs(self):
        """(float) Sampling frequency"""
        if self._fs is None:
            warnings.warn("No sampling frequency has been specified")
        return self._fs

    @fs.setter
    def fs(self, val):
        if self._fs == val:
            return
        try:
            if val <= 0:
                pass
        except Exception:
            raise TypeError("sampling rate must be a scalar")
        if val <= 0:
            raise ValueError("sampling rate must be positive")

        # if it is the first time that a sampling rate is set,
        # do not modify anything except for self._fs
        if self._fs is None:
            pass
        else:
            warning.warn(
                "Sampling frequency has been updated! This will "
                "modify internal times!"
                )
            self._time = self.xdata / val
        self._fs = val

    @property
    def isempty(self):
        """(bool) checks length of ydata input"""
        return len(self.ydata) == 0

    @property
    def n_epochs(self):
        """(int) number of epochs in AnalogSignal"""
        return self.support.n_epochs


    def __iter__(self):
        """AnalogSignal iterator initialization"""
        # initialize the internal index to zero when used as iterator
        self._index = 0
        return self

    def __next__(self):
        """AnalogSignal iterator advancer."""
        index = self._index
        if index > self.n_epochs - 1:
            raise StopIteration
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            epoch = EpochArray(
                    np.array([self.support.samples[index,:]])
                )
        self._index += 1
        return AnalogSignal(self.ydata,
                            fs=self.fs,
                            xdata=self.xdata,
                            support=epoch
        )     

    def __getitem__(self, idx):
        """AnalogSignal index access.
        Parameters
        Parameters
        ----------
        idx : EpochArray, int, slice
            intersect passed epocharray with support,
            index particular a singular epoch or multiple epochs with slice
        """
        epoch = self.support[idx]
        if epoch.isempty:
            warnings.warn("Index resulted in empty epoch array")
            return self._emptyAnalogSignal()
        else:
            return AnalogSignal(self.ydata,
                                fs=self.fs,
                                xdata=self.xdata,
                                support=epoch
            )
    
    def mean(self):
        """Calculates the mean of all of ydata"""
        return np.mean(self.ydata)

    def std(self):
        """Calculates the standard deviation of all of ydata"""
        return np.std(self.ydata)

    def max(self):
        """Returns the maximum of all of ydata"""
        return np.max(self.ydata)

    def min(self):
        """Returns the minimum of all of ydata"""
        return np.min(self.ydata)

    def clip(self, min, max):
        """Clip (limit) the values in ydata to min and max as specified. 

        Parameters
        ----------
        min : scalar
            Minimum value
        max : scalar
            Maximum value

        Returns
        ----------
        clipped_array : ndarray
            An array with the elements of ydata, but where the values < 
            min are replaced with min and the values > max are replaced 
            with max. 
        """
        return np.clip(self.ydata, min, max)
#----------------------------------------------------------------------#
#======================================================================#


########################################################################
# class AnalogSignalArray
########################################################################
class AnalogSignalArray:
    """Class description.

    Parameters
    ----------
    samples : np.array
        If shape (n_epochs, 1) or (n_epochs,), the start time for each
        epoch.
        If shape (n_epochs, 2), the start and stop times for each epoch.
    fs : float, optional
        Sampling rate in Hz. If fs is passed as a parameter, then time
        is assumed to be in sample numbers instead of actual time.

    Attributes
    ----------
    time : np.array
        The start and stop times for each epoch. With shape (n_epochs, 2).
    """

    def __init__(self, *, samples, fs=None, duration=None, meta=None):

        # if no samples were received, return an empty EpochArray:
        if len(samples) == 0:
            self.samples = np.array([])
            self.time = np.array([])
            self._fs = None
            self._meta = None
            return

        self._fs = fs
        self._meta = meta

    def __repr__(self):
        if self.isempty:
            return "<empty AnalogSignalArray"
        # return "<AnalogSignalArray: %s> %s" % (nstr, dstr)
        return "<AnalogSignalArray"

    def __getitem__(self, idx):
        raise NotImplementedError(
            'AnalogSignalArray.__getitem__ not implemented yet')

    @property
    def isempty(self):
        """(bool) Empty AnalogSignalArray."""
        raise NotImplementedError(
            'AnalogSignalArray.isempty not implemented yet')
#----------------------------------------------------------------------#
#======================================================================#


########################################################################
# class SpikeTrain
########################################################################
class SpikeTrain:
    """A set of action potential (spike) times of a putative unit/neuron.

    Parameters
    ----------
    samples : np.array(dtype=np.float64)
    fs : float, optional
        Sampling rate in Hz. If fs is passed as a parameter, then time
        is assumed to be in sample numbers instead of actual time.
    support : EpochArray, optional
        EpochArray array on which spiketrain is defined.
        Default is [0, last spike] inclusive.
    label : str or None, optional
        Information pertaining to the source of the spiketrain.
    cell_type : str or other, optional
        Identified cell type indicator, e.g., 'pyr', 'int'.
    meta : dict
        Metadata associated with spiketrain.

    Attributes
    ----------
    time : np.array(dtype=np.float64)
        With shape (n_samples,). Always in seconds.
    samples : np.array(dtype=np.float64)
        With shape (n_samples,). Sample numbers corresponding to spike
        times, if available.
    support : EpochArray on which spiketrain is defined.
    n_spikes: integer
        Number of spikes in SpikeTrain.
    fs: float
        Sampling frequency (Hz).
    cell_type : str or other
        Identified cell type.
    label : str or None
        Information pertaining to the source of the spiketrain.
    meta : dict
        Metadata associated with spiketrain.
    """

    def __init__(self, samples, *, fs=None, support=None, label=None,
                 cell_type=None, meta=None):

        samples = np.squeeze(samples)

        if samples.shape == (): #TODO: doesn't this mean it's empty?
            samples = samples[..., np.newaxis]

        if samples.ndim != 1:
            raise ValueError("samples must be a vector")

        # if no spike times are given, return an empty spiketrain:
        if len(samples) == 0:
            self._emptySpikeTrain()
            return

        # set initial fs to None
        self._fs = None
        # then attempt to update the fs; this does input validation:
        self.fs = fs

        # if a sampling rate was given, relate time to samples using fs:
        if fs is not None:
            time = samples / fs
        else:
            time = samples

        if label is not None and not isinstance(label, str):
            raise ValueError("label must be a string")

        # set self.samples and self.time before restricting to support:
        self.time = time
        self.samples = samples

        # determine spiketrain array support:
        if support is None:
            self.support = EpochArray(np.array([0, samples[-1]]), fs=fs)
            # in the above, there's no reason to restrict to support
        else:
            # restrict spikes to only those within the spiketrain
            # array's support:
            self.support = support
            self._restrict_to_epoch_array()

        self.label = label
        self._cell_type = cell_type
        self._meta = meta

    def _restrict_to_epoch_array(self, *, epocharray=None, update=True):
        """Restrict self.time and self.samples to an EpochArray. If no
        EpochArray is specified, self.support is used.

        Parameters
        ----------
        epocharray : EpochArray, optional
            EpochArray on which to restrict SpikeTrain. Default is
            self.support
        update: bool, optional
            Overwrite self.support with epocharray if True (default).
        """
        if epocharray is None:
            epocharray = self.support
            update = False  # support did not change; no need to update

        indices = []
        for eptime in epocharray.time:
            t_start = eptime[0]
            t_stop = eptime[1]
            indices.append((self.time >= t_start) & (self.time <= t_stop))
        indices = np.any(np.column_stack(indices), axis=1)
        if np.count_nonzero(indices) < len(self.time):
            warnings.warn(
                'ignoring spikes outside of spiketrain support')
        self.samples = self.samples[indices]
        self.time = self.time[indices]
        if update:
            self.support = epocharray

    def _emptySpikeTrain(self):
        """empty all the instance attributes for an empty object."""
        self.samples = np.array([])
        self.time = np.array([])
        self.support = EpochArray([])
        self.label = None
        self._fs = None
        self._cell_type = None
        self._meta = None
        return

    def __repr__(self):
        if self.isempty:
            return "<empty SpikeTrain>"
        if self.fs is not None:
            fsstr = " at %s Hz" % self.fs
        else:
            fsstr = ""
        if self.label is not None:
            labelstr = " from %s" % self.label
        else:
            labelstr = ""
        if self.cell_type is not None:
            typestr = "[%s]" % self.cell_type
        else:
            typestr = ""

        return "<SpikeTrain%s: %s spikes%s>%s" % (
            typestr, self.n_spikes, fsstr, labelstr)

    def __getitem__(self, idx):
        if isinstance(idx, EpochArray):
            if idx.isempty:
                return SpikeTrain([])
            epoch = self.support.intersect(idx, boundaries=True)
            if epoch.isempty:
                return SpikeTrain([])
            indices = []
            for eptime in epoch.time:
                t_start = eptime[0]
                t_stop = eptime[1]
                indices.append(
                    (self.time >= t_start) & (self.time <= t_stop)
                    )
            indices = np.any(np.column_stack(indices), axis=1)
            return SpikeTrain(self.samples[indices],
                              fs=self.fs,
                              support=epoch,
                              label=self.label,
                              cell_type=self.cell_type,
                              meta=self.meta)
        elif isinstance(idx, int):
            try:
                epoch = EpochArray(
                    np.array([self.samples[idx], self.samples[idx]]),
                    fs=self.fs,
                    meta=self.meta
                    )
            except (StopIteration, IndexError): # index out of bounds, so return an empty spiketrain
                # TODO: if I raise an index error for the iterator, how
                # can I make sure to return an empty object for a simple
                # out of bounds access?
                # raise IndexError # this signals iterators to stop...
                epoch = EpochArray([])
                return SpikeTrain([], support=epoch)

            return SpikeTrain(
                self.samples[idx],
                fs=self.fs,
                support=epoch,
                label=self.label,
                cell_type=self.cell_type,
                meta=self.meta
                )
        elif isinstance(idx, slice):
            # TODO: add step functionality
            start = idx.start
            if start is None:
                start = 0
            if start >= self.n_spikes:
                return SpikeTrain(
                    [],
                    fs=self.fs,
                    support=None,
                    label=self.label,
                    cell_type=self.cell_type,
                    meta=self.meta
                    )
            stop = idx.stop
            if stop is None:
                stop = -1
            else:
                stop = np.min(np.array([stop - 1, self.n_spikes - 1]))
            epoch = EpochArray(
                np.array([self.samples[start], self.samples[stop]]),
                fs=self.fs,
                meta=self.meta
                )
            return SpikeTrain(
                self.samples[idx],
                fs=self.fs,
                support=epoch,
                label=self.label,
                cell_type=self.cell_type,
                meta=self.meta
                )
        else:
            raise TypeError(
                'unsupported subsctipting type {}'.format(type(idx)))

    def bin(self, *, ds=None):
        """Bin spiketrain."""
        return BinnedSpikeTrain(self, ds=ds)

    @property
    def n_active(self):
        """Number of active units per epoch with shape (n_epochs,)."""
        return np.array([self[ep].n_spikes for ep in self.support])

    @property
    def n_spikes(self):
        """(int) The number of spikes."""
        return len(self.time)

    @property
    def isempty(self):
        """(bool) Empty SpikeTrain."""
        return len(self.time) == 0

    @property
    def issorted(self):
        """(bool) Sorted SpikeTrain."""
        return is_sorted(self.samples)

    @property
    def cell_type(self):
        """The neuron cell type."""
        if self._cell_type is None:
            warnings.warn("Cell type has not yet been specified!")
        return self._cell_type

    @cell_type.setter
    def cell_type(self, val):
        self._cell_type = val

    @property
    def meta(self):
        """Meta information associated with SpikeTrain."""
        if self._meta is None:
            warnings.warn("meta data is not available")
        return self._meta

    @meta.setter
    def meta(self, val):
        self._meta = val

    @property
    def fs(self):
        """(float) Sampling frequency."""
        return fsgetter(self)

    @fs.setter
    def fs(self, val):
        """(float) Sampling frequency."""
        fssetter(self, val)

    def time_slice(self, t_start, t_stop):
        """Creates a new nelpy.SpikeTrain corresponding to the time
        slice of the original between (and including) times t_start and
        t_stop. Setting either parameter to None uses infinite endpoints
        for the time interval.

        Parameters
        ----------
        spikes : nelpy.SpikeTrain
        t_start : float
        t_stop : float

        Returns
        -------
        sliced_spikes : nelpy.SpikeTrain
        """
        if t_start is None:
            t_start = -np.inf
        if t_stop is None:
            t_stop = np.inf

        if t_start > t_stop:
            raise ValueError("t_start cannot be greater than t_stop")

        indices = (self.time >= t_start) & (self.time <= t_stop)

        warnings.warn(
            "Shouldn't use this function anymore! Now use slicing or "
            "epoch-based indexing instead.",
            DeprecationWarning
            )

        return self[indices]

    def time_slices(self, t_starts, t_stops):
        """Creates a new object corresponding to the time slice of
        the original between (and including) times t_start and t_stop.
        Setting either parameter to None uses infinite endpoints for the
        time interval.

        Parameters
        ----------
        spiketrain : nelpy.SpikeTrain
        t_starts : list of floats
        t_stops : list of floats

        Returns
        -------
        sliced_spiketrain : nelpy.SpikeTrain
        """

        # TODO: check if any stops are before starts, like in EpochArray class
        if len(t_starts) != len(t_stops):
            raise ValueError(
                "must have same number of start and stop times")

        indices = []
        for t_start, t_stop in zip(t_starts, t_stops):
            indices.append(
                (self.time >= t_start) & (self.time <= t_stop)
                )
        indices = np.any(np.column_stack(indices), axis=1)

        warnings.warn(
            "Shouldn't use this function anymore! Now use slicing or "
            "epoch-based indexing instead.",
             DeprecationWarning
            )

        return self[indices]

    def shift(self, time_offset, fs=None):
        """Creates a new object corresponding to the original spike
        train, but shifted by time_offset (can be positive or negative).

        Parameters
        ----------
        spiketrain : nelpy.SpikeTrain
        time_offset : float
            Time offset, either in actual time (default) or in sample
            numbers if fs is specified.
        fs : float, optional
            Sampling frequency.

        Returns
        -------
        spiketrain : nelpy.SpikeTrain
        """
        raise NotImplementedError(
            "SpikeTrain.shift() has not been implemented yet!")
########################################################################
########################################################################


########################################################################
# class SpikeTrainArray
########################################################################
class SpikeTrainArray:
    """A multiunit spiketrain array with shared support.

    Parameters
    ----------
    samples : array (of length n_units) of np.array(dtype=np.float64)
        containing spike times in in seconds (unless fs=None).
    fs : float, optional
        Sampling rate in Hz. If fs is passed as a parameter, then time
        is assumed to be in sample numbers instead of actual time.
    support : EpochArray, optional
        EpochArray on which spiketrains are defined.
        Default is [0, last spike] inclusive.
    label : str or None, optional
        Information pertaining to the source of the spiketrain array.
    cell_type : list (of length n_units) of str or other, optional
        Identified cell type indicator, e.g., 'pyr', 'int'.
    unit_ids : list (of length n_units) of indices corresponding to
        curated data. If no unit_ids are specified, then [1,...,n_units]
        will be used. WARNING! The first unit will have index 1, not 0!
    meta : dict
        Metadata associated with spiketrain array.

    Attributes
    ----------
    time : array of np.array(dtype=np.float64) spike times in seconds.
        Array of length n_units, each entry with shape (n_samples,)
    samples : list of np.array(dtype=np.float64) spike times in samples.
        Array of length n_units, each entry with shape (n_samples,)
    support : EpochArray on which spiketrain array is defined.
    n_spikes: np.array(dtype=np.int) of shape (n_units,)
        Number of spikes in each unit.
    fs: float
        Sampling frequency (Hz).
    cell_types : np.array of str or other
        Identified cell type for each unit.
    label : str or None
        Information pertaining to the source of the spiketrain.
    meta : dict
        Metadata associated with spiketrain.
    """

    # TODO: .flatten()
    # TODO: .n_units
    # TODO: .unit_ids
    # TODO: indexing
    # TODO: support for single spiketrain
    # TODO: init input validation to mimic EpochArray

    def __init__(self, samples, *, fs=None, support=None, label=None,
                 cell_types=None, unit_ids=None, meta=None):

        samples = np.squeeze(samples)  # coerce samples into np.array

        # Note: if we have an empty array of samples with no dimension,
        # then calling len(samples) will return a TypeError.
        try:
            # if no samples were received, return an empty EpochArray:
            if len(samples) == 0:
                self._emptySpikeTrainArray()
                return
        except TypeError:
            warnings.warn("unsupported type; creating empty EpochArray")
            self._emptySpikeTrainArray()
            return

        # BUG: we cannot yet differentiate between a single spike train
        # and a spike train array with multiple units. See issue #46

        # standardize input so that a list of lists is converted to an
        # array of arrays: BUG: this assumes more than one unit!!!
        sampleArray = np.array(
            [np.array(st, ndmin=1, copy=False) for st in samples])

        # if only empty samples were received, return an empty
        # SpikeTrainArray:
        if np.sum([st.size for st in sampleArray]) == 0:
            self._emptySpikeTrainArray()
            return

        # set initial fs to None
        self._fs = None
        # then attempt to update the fs; this does input validation:
        self.fs = fs

        # if a sampling rate was given, relate time to samples using fs:
        if fs is not None:
            time = sampleArray / fs
        else:
            time = sampleArray

        # determine spiketrain array support:
        if support is None:
            # first_st = np.array([unit[0] for unit in sampleArray]).min()
            # BUG: if spiketrain is empty np.array([]) then unit[-1]
            # raises an error in the following:
            # FIX: list[-1] raises an IndexError for an empty list,
            # whereas list[-1:] returns an empty list.
            last_st = np.array([unit[-1:] for unit in sampleArray]).max()
            self.support = EpochArray(np.array([0, last_st]), fs=fs)
            # in the above, there's no reason to restrict to support
        else:
            # restrict spikes to only those within the spiketrain
            # array's support:
            self.support = support

            time, sampleArray = self._restrict_to_epoch_array(epocharray=support, time=time, samples=sampleArray)

        # if no samples remain after restricting to the support, return
        # an empty SpikeTrainArray:
        if np.sum([st.size for st in sampleArray]) == 0:
            self._emptySpikeTrainArray()
            return

        # set self.samples and self.time:
        self.time = time
        self.samples = sampleArray

        # inherit unit IDs if available, otherwise initialize to default
        if unit_ids is None:
            self._unit_ids = list(range(1,self.n_units + 1))
        else:
            # do a few basic checks to see if unit_ids look right:
            if len(unit_ids) != self.n_units:
                raise TypeError("unit_ids inconsistent with n_units")
            if len(set(unit_ids)) < len(unit_ids):
                raise TypeError("duplicate unit_ids encountered")
            self._unit_ids = unit_ids

        self.label = label
        self._cell_types = cell_types
        self._meta = meta

    def __iter__(self):
        """SpikeTrainArray iterator initialization."""
        # initialize the internal index to zero when used as iterator
        self._index = 0
        return self

    def __next__(self):
        """SpikeTrainArray iterator advancer."""
        index = self._index
        if index > self.support.n_epochs - 1:
            raise StopIteration
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            support = self.support[index]
            time, samples = self._restrict_to_epoch_array(
                epocharray=support,
                time=self.time,
                samples=self.samples,
                copy=True
                )
            sta = SpikeTrainArray(
                samples = samples,
                support = support,
                fs = self.fs,
                label = self.label,
                cell_types = self._cell_types,
                meta = self._meta,
                unit_ids = self.unit_ids
                )  # return sta one epoch at a time
        self._index += 1
        return sta

    def __getitem__(self, idx):
        """SpikeTrainArray index access."""
        # TODO: allow indexing of form sta[4,1:5] so that the STs of
        # epochs 1 to 5 (exlcusive) are returned, for neuron id 4.
        if isinstance(idx, EpochArray):
            if idx.isempty:
                return SpikeTrainArray([])
            if idx.fs != self.support.fs:
                support = self.support.intersect(
                    epoch=EpochArray(
                        idx.time*self.support.fs,
                        fs=self.support.fs),
                    boundaries=True
                    )
            else:
                support = self.support.intersect(
                    epoch=idx,
                    boundaries=True
                    ) # what if fs of slicing epoch is different?
            if support.isempty:
                return SpikeTrainArray([])
            time, samples = self._restrict_to_epoch_array(
                epocharray=support,
                time=self.time,
                samples=self.samples,
                copy=True
                )
            sta = SpikeTrainArray(
                samples = samples,
                support = support,
                fs = self.fs,
                label = self.label,
                cell_types = self._cell_types,
                meta = self._meta,
                unit_ids = self.unit_ids
                )
            return sta
        elif isinstance(idx, int):
            if (idx >= self.support.n_epochs) or idx < (-self.support.n_epochs):
                return SpikeTrainArray([])
            try:
                support = self.support[idx]
                time, samples = self._restrict_to_epoch_array(
                    epocharray=support,
                    time=self.time,
                    samples=self.samples,
                    copy=True
                    )
                sta = SpikeTrainArray(
                    samples = samples,
                    support = support,
                    fs = self.fs,
                    label = self.label,
                    cell_types = self._cell_types,
                    meta = self._meta,
                    unit_ids = self.unit_ids
                    )
                return sta
            except IndexError:
                # index out of bounds: return an empty SpikeTrainArray
                return SpikeTrainArray([])
        else:
            try:
                support = self.support[idx]
                time, samples = self._restrict_to_epoch_array(
                    epocharray=support,
                    time=self.time,
                    samples=self.samples,
                    copy=True
                    )
                sta = SpikeTrainArray(
                    samples = samples,
                    support = support,
                    fs = self.fs,
                    label = self.label,
                    cell_types = self._cell_types,
                    meta = self._meta,
                    unit_ids = self.unit_ids
                    )
                return sta
            except Exception:
                raise TypeError(
                    'unsupported subsctipting type {}'.format(type(idx)))

    def CalcFiringRate():
        """Calculate firing rate over unit."""

        raise NotImplementedError("CalcFiringRate not implemented yet.")

    def flatten(self, *, multiunit_id=None):
        """Collapse spike trains across units.
        
        Parameters
        ----------
        multiunit_id: (int)
            (unit) ID to assign to flattened spike train, default is 0.
        """
        if self.n_units == 1:
            return self

        # raise NotImplementedError until SpikeTrainArray supports one
        # unit spike trains:
        raise NotImplementedError(
            "SpikeTrainArray.flatten() has not been implemented yet!")

        if multiunit_id is None:
            multiunit_id = 0
        allspikes = self.samples[0]
        for unit in range(1,self.n_units):
            allspikes = linear_merge(allspikes, self.samples[unit])

        flatspiketrain = SpikeTrainArray(
            samples = list(allspikes),
            fs = self.fs,
            support = self.support,
            label = self.label,
            cell_types = None,
            unit_ids=[multiunit_id]
            )
        return flatspiketrain
        
    def _restrict_to_epoch_array(self, *, epocharray, time, samples,
                                 copy=True):
        """Returns time and samples restricted to an EpochArray.

        Parameters
        ----------
        epocharray : EpochArray, optional
            EpochArray on which to restrict SpikeTrainArray. Default is
            self.support
        """
        # Potential BUG: not sure if time and samples point to same
        # object (like when only time was passed to __init__), then
        # doing samples[unit] = ... followed by time[unit] = ... might
        # be applying the shrinking twice, no? We need a thorough test
        # for this! And I need to understand the shared memory 100%.
        if copy:
            time = time.copy()
            samples = samples.copy()
        # BUG: this assumes multiple units for the enumeration to work
        for unit, st_time in enumerate(time):
            indices = []
            for eptime in epocharray.time:
                t_start = eptime[0]
                t_stop = eptime[1]
                indices.append((st_time >= t_start) & (st_time <= t_stop))
            indices = np.any(np.column_stack(indices), axis=1)
            if np.count_nonzero(indices) < len(st_time):
                warnings.warn(
                    'ignoring spikes outside of spiketrain support')
            samples[unit] = samples[unit][indices]
            time[unit] = time[unit][indices]
        return time, samples

    # def _restrict_to_epoch_array(self, *, epocharray=None, update=True):
    #     """Restrict self.time and self.samples to an EpochArray. If no
    #     EpochArray is specified, self.support is used.

    #     Parameters
    #     ----------
    #     epocharray : EpochArray, optional
    #         EpochArray on which to restrict SpikeTrainArray. Default is
    #         self.support
    #     update: bool, optional
    #         Overwrite self.support with epocharray if True (default).
    #     """
    #     if epocharray is None:
    #         epocharray = self.support
    #         update = False  # support did not change; no need to update

    #     # BUG: this assumes multiple units for the enumeration to work
    #     for unit, st_time in enumerate(self.time):
    #         indices = []
    #         for eptime in epocharray.time:
    #             t_start = eptime[0]
    #             t_stop = eptime[1]
    #             indices.append((st_time >= t_start) & (st_time <= t_stop))
    #         indices = np.any(np.column_stack(indices), axis=1)
    #         if np.count_nonzero(indices) < len(st_time):
    #             warnings.warn(
    #                 'ignoring spikes outside of spiketrain support')
    #         self.samples[unit] = self.samples[unit][indices]
    #         self.time[unit] = self.time[unit][indices]
    #     if update:
    #         self.support = epocharray

    def _emptySpikeTrainArray(self):
        """empty all the instance attributes for an empty object."""
        self.samples = np.array([])
        self.time = np.array([])
        self.support = EpochArray([])
        self.label = None
        self._fs = None
        self._cell_types = None
        self._meta = None
        return

    def __repr__(self):
        if self.isempty:
            return "<empty SpikeTrainArray>"
        if self.fs is not None:
            fsstr = " at %s Hz" % self.fs
        else:
            fsstr = ""
        if self.label is not None:
            labelstr = " from %s" % self.label
        else:
            labelstr = ""
        numstr = " %s units" % self.n_units
        return "<SpikeTrainArray:%s>%s%s" % (numstr, fsstr, labelstr)

    def bin(self, *, ds=None):
        """Bin spiketrain array."""
        return BinnedSpikeTrainArray(self, ds=ds)

    @property
    def n_units(self):
        """(int) The number of units."""
        return len(self.time)

    @property
    def unit_ids(self):
        """(n_units, ) Unit IDs contained in the SpikeTrainArray."""
        return self._unit_ids

    @property
    def n_spikes(self):
        """(np.array) The number of spikes in each unit."""
        if self.isempty:
            return 0
        return np.array([len(unit) for unit in self.time])

    @property
    def n_active(self):
        """Number of active units per epoch with shape (n_epochs,)."""
        raise NotImplementedError(
            'SpikeTrainArray.n_active not implemented yet')

    @property
    def isempty(self):
        """(bool) Empty SpikeTrainArray."""
        return np.sum([len(st) for st in self.time]) == 0

    @property
    def issorted(self):
        """(bool) Sorted SpikeTrainArray."""
        return np.array(
            [is_sorted(spiketrain) for spiketrain in self.samples]
            ).all()

    @property
    def cell_types(self):
        """The neuron cell type."""
        raise NotImplementedError(
            'SpikeTrainArray.cell_types not implemented yet')
        if self._cell_types is None:
            warnings.warn("Cell types have not yet been specified!")
        return self._cell_types

    @cell_types.setter
    def cell_types(self, val):
        raise NotImplementedError(
            'SpikeTrainArray.cell_types(setter) not implemented yet')
        self._cell_types = val

    @property
    def meta(self):
        """Meta information associated with SpikeTrainArray."""
        if self._meta is None:
            warnings.warn("meta data is not available")
        return self._meta

    @meta.setter
    def meta(self, val):
        self._meta = val

    @property
    def fs(self):
        """(float) Sampling frequency."""
        return fsgetter(self)

    @fs.setter
    def fs(self, val):
        """(float) Sampling frequency."""
        fssetter(self, val)

#----------------------------------------------------------------------#
#======================================================================#


########################################################################
# class BinnedSpikeTrain
########################################################################
class BinnedSpikeTrain:
    """A set of binned action potential (spike) times of a putative unit
    (neuron).

    Parameters
    ----------
    spiketrain : nelpy.SpikeTrain
        The spiketrain to bin.
    ds : float, optional
        Bin size (width) in seconds. Default is 0.625 seconds, which
        corresponds to half of a typical rodent theta cycle.

    Attributes
    ----------
    ds : float
        Bin width, in seconds.
    centers : np.array
        The centers of the bins. With shape (n_bins, 1).
    data : np.array
    bins : np.array
        The edges of the bins. With shape (??? depends on n_epochs).
        # TODO: check what is the format that numpy takes.
        Also, consider making this an EventArray, so that the bins can
        easily be overlayed on plots.
    support : nelpy.EpochArray on which binned spiketrain is defined.
    _binnedSupport : np.array of shape (n_epochs, 2) with the start and
        stop bin index associated w each epoch.
    """

    # TODO: considerations.
    #
    # We need an efficient data representation: consider a case where we
    # have a support of [0,1] U [9999,10000]. In this case, we do not
    # want to (needlessly) allocate space for all the bins in [1,9999].
    # So a better approach might be to intelligently pre-compute the bin
    # edges before binning. Bins should also be such that they
    # completely enclose all epochs in the spiketrain's support.
    #
    # For example, with 0.5 second bins, and a spiketrain
    # [0.8, 0.9 1.2 1.8 2.4 2.51] with support [0.8, 2.51] we would need
    # bins 0.5--3.0 (left- to right-edge), that is,
    # [0.5,1.0) U [1.0,1.5) U [1.5,2.0) U [2.5,3.0).
    #
    # In the first example, with a 5 second bin, we'd need
    # [0,5) U [9995,10000) U [10000,10005), and NOT simply
    # [0,5) U [9999,10004) because such an approach can cause lots of
    # headaches down the road.
    #
    # Now implementation-wise: should we store the numpy arrays
    # separately for each epoch? Should we have only one array, but keep
    # track of the bin centers (most useful for plotting and other
    # analysis) and the True support epochs? How about slicing and
    # indexing? If we index a BinnedSpikeTrain with an EpochArray, then
    # we should get only those bins back that fall in the intersection
    # of the BinnedSpikeTrain's support and the indexing EpochArray. If
    # we slice, should we slice by bins, or by epochs? I am still
    # leaning towards slicing by epoch, so that BinnedSpikeTrain[2:5]
    # will return binned data corresponding to epochs 2,3 and 4.
    #
    # It is also possible that the best hing to do is to have a dynamic
    # representation, where one option is to store an array of bin
    # centers, and another is to store compact representations
    # (start, stop)-tuples for each bin epoch. This might save a lot of
    # memory for large, contiguous segments, but it may be painfully
    # slow for cases with lots of short epochs. For now, I think I will
    # simply do the expanded (non-compact) representation.
    #
    # Also, should a BinnedSpikeTrain keep an unbinned copy of the
    # associated SpikeTrain? That way we can re-bin and maybe do some
    # interesting things, but it may also be pretty wasteful space
    # (memory) wise...?

    def __init__(self, spiketrain, *, ds=None):
        # by default, the support of the binned spiketrain will be
        # inherited from spiketrain

        if not isinstance(spiketrain, SpikeTrain):
            raise TypeError(
                'spiketrain must be a nelpy.SpikeTrain object.')

        self._ds = None
        self._centers = np.array([])

        if ds is None:
            warnings.warn('no bin size was given, assuming 62.5 ms')
            ds = 0.0625

        # TODO: this is not a good empty object to return; fix it!
        # if no samples were received, return an empty BinnedSpikeTrain:
        if spiketrain.isempty:
            self.ds = ds
            return

        self._spiketrain = spiketrain # TODO: remove this if we don't need it, or decide that it's too wasteful
        self._support = spiketrain.support
        self.ds = ds

        self._bin_spikes(
            spiketrain=spiketrain,
            epochArray=self.support,
            ds=ds
            )

    def __repr__(self):
        if self.isempty:
            return "<empty BinnedSpikeTrain>"
        if self.n_bins == 1:
            bstr = " {} bin of width {} ms".format(self.n_bins, self.ds*1000)
            dstr = ""
        else:
            bstr = " {} bins of width {} ms".format(self.n_bins, self.ds*1000)
            dstr = " for a total of {} seconds.".format(self.n_bins*self.ds)
        return "<BinnedSpikeTrain:%s>%s" % (bstr, dstr)

    def __getitem__(self, idx):
        raise NotImplementedError(
            'BinnedSpikeTrain.__getitem__ not implemented yet')

    @property
    def centers(self):
        """(np.array) The bin centers (in seconds)."""
        return self._centers

    @property
    def data(self):
        """(np.array) The spike counts in all the bins.
        See also BinnedSpikeTrain.centers
        """
        return self._data

    @property
    def bins(self):
        """(np.array) The bin edges (in seconds)."""
        return self._bins

    @property
    def support(self):
        """(nelpy.EpochArray) The support of the underlying spiketrain
        (in seconds).
         """
        return self._support

    @property
    def binnedSupport(self):
        """(np.array) The binned support of the binned spiketrain (in
        bin IDs) of shape (2, n_epochs).
        """
        return self._binnedSupport

    @property
    def lengths(self):
        """Lenghts of contiguous segments, in number of bins."""
        return self.binnedSupport[1,:] - self.binnedSupport[0,:] + 1

    @property
    def spiketrain(self):
        """(nelpy.SpikeTrain) The original spiketrain associated with
        the binned data.
        """
        return self._spiketrain

    @property
    def n_bins(self):
        """(int) The number of bins."""
        return len(self.centers)

    @property
    def isempty(self):
        """(bool) Empty BinnedSpikeTrain."""
        return len(self.centers) == 0

    @property
    def n_active(self):
        """Number of active units per time bin with shape (n_bins,)."""
        return self.data.clip(max=1)

    @property
    def ds(self):
        """(float) Bin width in seconds."""
        return self._ds

    @ds.setter
    def ds(self, val):
        if self._ds is not None:
            raise AttributeError("can't set attribute")
        else:
            try:
                if val <= 0:
                    pass
            except:
                raise TypeError("bin width must be a scalar")
            if val <= 0:
                raise ValueError("bin width must be positive")
            self._ds = val

    def _get_bins_to_cover_epoch(self, epoch, ds):
        """(np.array) Return bin edges to cover an epoch."""
        # start = ep.start - (ep.start % ds)
        # start = ep.start - (ep.start / ds - floor(ep.start / ds))
        # because e.g., 1 % 0.1 is messed up (precision error)
        start = ds * np.floor(epoch.start / ds)
        num = np.ceil((epoch.stop - start) / ds)
        stop = start + ds * num
        bins = np.linspace(start, stop, num+1)
        centers = bins[:-1] + np.diff(bins) / 2
        return bins, centers

    def _bin_spikes(self, spiketrain, epochArray, ds):
        b = []
        c = []
        s = []
        left_edges = []
        right_edges = []
        counter = 0
        for epoch in epochArray:
            bins, centers = self._get_bins_to_cover_epoch(epoch, ds)
            spike_counts, _ = np.histogram(
                spiketrain.time,
                bins=bins,
                density=False,
                range=(epoch.start,epoch.stop)
                ) # TODO: is it faster to limit range, or to cut out spikes?
            left_edges.append(counter)
            counter += len(centers) - 1
            right_edges.append(counter)
            counter += 1
            b.extend(bins.tolist())
            c.extend(centers.tolist())
            s.extend(spike_counts.tolist())
        self._bins = np.array(b)
        self._centers = np.array(c)
        self._data = np.array(s)
        self._binnedSupport = np.vstack(
            (np.array(left_edges),
             np.array(right_edges))
            )
#----------------------------------------------------------------------#
#======================================================================#


########################################################################
# class BinnedSpikeTrainArray
########################################################################
class BinnedSpikeTrainArray:
    """Binned spiketrain array.

    Parameters
    ----------
    fs : float, optional
        Sampling rate in Hz. If fs is passed as a parameter, then time
        is assumed to be in sample numbers instead of actual time.

    Attributes
    ----------
    time : np.array
        The start and stop times for each epoch. With shape (n_epochs, 2).
    """
    def __init__(self, spiketrainarray, *, ds=None):
        if not isinstance(spiketrainarray, SpikeTrainArray):
            raise TypeError(
                'spiketrainarray must be a nelpy.SpikeTrainArray object.')

        self._ds = None
        self._centers = np.array([])

        if ds is None:
            warnings.warn('no bin size was given, assuming 62.5 ms')
            ds = 0.0625

        # TODO: this is not a good empty object to return; fix it!
        # if no samples were received, return an empty BinnedSpikeTrain:
        if spiketrainarray.isempty:
            self.ds = ds
            return

        self._spiketrainarray = spiketrainarray # TODO: remove this if we don't need it, or decide that it's too wasteful
        self._support = spiketrainarray.support
        self.ds = ds

        self._bin_spikes(
            spiketrainarray=spiketrainarray,
            epochArray=self.support,
            ds=ds
            )

    def __repr__(self):
        if self.isempty:
            return "<empty BinnedSpikeTrainArray>"
        ustr = " {} units in".format(self.n_units)
        if self.n_bins == 1:
            bstr = " {} bin of width {} ms".format(self.n_bins, self.ds*1000)
            dstr = ""
        else:
            bstr = " {} bins of width {} ms".format(self.n_bins, self.ds*1000)
            dstr = " for a total of {} seconds.".format(self.n_bins*self.ds)
        return "<BinnedSpikeTrainArray:%s%s>%s" % (ustr, bstr, dstr)

    def __getitem__(self, idx):
        raise NotImplementedError(
            'BinnedSpikeTrain.__getitem__ not implemented yet')

    @property
    def centers(self):
        """(np.array) The bin centers (in seconds)."""
        return self._centers

    @property
    def data(self):
        """(np.array) The spike counts in all the bins.
        See also BinnedSpikeTrain.centers
        """
        return self._data

    @property
    def bins(self):
        """(np.array) The bin edges (in seconds)."""
        return self._bins

    @property
    def n_units(self):
        """(int) The number of units."""
        return self.data.shape[0]

    @property
    def support(self):
        """(nelpy.EpochArray) The support of the underlying spiketrain
        (in seconds).
         """
        return self._support

    @property
    def binnedSupport(self):
        """(np.array) The binned support of the binned spiketrain (in
        bin IDs) of shape (2, n_epochs).
        """
        return self._binnedSupport

    @property
    def lengths(self):
        """Lenghts of contiguous segments, in number of bins."""
        return self.binnedSupport[1,:] - self.binnedSupport[0,:] + 1

    @property
    def spiketrainarray(self):
        """(nelpy.SpikeTrain) The original spiketrain associated with
        the binned data.
        """
        return self._spiketrainarray

    @property
    def n_bins(self):
        """(int) The number of bins."""
        return len(self.centers)

    @property
    def isempty(self):
        """(bool) Empty BinnedSpikeTrain."""
        return len(self.centers) == 0

    @property
    def ds(self):
        """(float) Bin width in seconds."""
        return self._ds

    @ds.setter
    def ds(self, val):
        if self._ds is not None:
            raise AttributeError("can't set attribute")
        else:
            try:
                if val <= 0:
                    pass
            except:
                raise TypeError("bin width must be a scalar")
            if val <= 0:
                raise ValueError("bin width must be positive")
            self._ds = val

    def _get_bins_to_cover_epoch(self, epoch, ds):
        """(np.array) Return bin edges to cover an epoch."""
        # start = ep.start - (ep.start % ds)
        # start = ep.start - (ep.start / ds - floor(ep.start / ds))
        # because e.g., 1 % 0.1 is messed up (precision error)
        start = ds * np.floor(epoch.start / ds)
        num = np.ceil((epoch.stop - start) / ds)
        stop = start + ds * num
        bins = np.linspace(start, stop, num+1)
        centers = bins[:-1] + np.diff(bins) / 2
        return bins, centers

    def _bin_spikes(self, spiketrainarray, epochArray, ds):
        b = []
        c = []
        s = []
        for nn in range(spiketrainarray.n_units):
            s.append([])
        left_edges = []
        right_edges = []
        counter = 0
        for epoch in epochArray:
            bins, centers = self._get_bins_to_cover_epoch(epoch, ds)
            for uu, spiketraintimes in enumerate(spiketrainarray.time):
                spike_counts, _ = np.histogram(
                    spiketraintimes,
                    bins=bins,
                    density=False,
                    range=(epoch.start,epoch.stop)
                    ) # TODO: is it faster to limit range, or to cut out spikes?
                s[uu].extend(spike_counts.tolist())
            left_edges.append(counter)
            counter += len(centers) - 1
            right_edges.append(counter)
            counter += 1
            b.extend(bins.tolist())
            c.extend(centers.tolist())
        self._bins = np.array(b)
        self._centers = np.array(c)
        self._data = np.array(s)
        self._binnedSupport = np.vstack(
            (np.array(left_edges),
             np.array(right_edges))
            )

    @property
    def n_active(self):
        """Number of active units per time bin with shape (n_bins,)."""
        # TODO: profile several alternatves. Could use data > 0, or
        # other numpy methods to get a more efficient implementation:
        return self.data.clip(max=1).sum(axis=0)

#----------------------------------------------------------------------#
#======================================================================#

# count number of spikes in an interval:
        # spks_bin, bins = np.histogram(st_array/fs, bins=num_bins, density=False, range=(0,maxtime))
