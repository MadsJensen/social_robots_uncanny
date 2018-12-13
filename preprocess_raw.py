import sys
import mne
import numpy as np
from autoreject import (AutoReject)  # noqa
from project_settings import data_path

seed = 234241

subject = sys.argv[1]  # get subject name from command line

# Autoreject parameters
n_interpolates = np.arange(1, 13, 1)
consensus_percs = np.linspace(0, 1.0, 11)

# Epoch parameters
tmin, tmax = -0.2, 0.5

event_id = {
    'A/1': 20,
    'A/2': 22,
    'A/3': 24,
    'A/4': 26,
    'A/5': 28,
    'B/1': 30,
    'B/2': 32,
    'B/3': 34,
    'B/4': 36,
    'B/5': 38,
    'C/1': 40,
    'C/2': 42,
    'C/3': 44,
    'C/4': 46,
    'C/5': 48,
    'D/1': 50,
    'D/2': 52,
    'D/3': 54,
    'D/4': 56,
    'D/5': 58
}

montage = mne.channels.read_montage('standard_1020')

reject_params = {
    # 'eeg': 40e-6,  # V (EEG channels)
    'eog': 250e-6  # V (EOG channels)
}

eog_channles = {'VEOG': 'eog', 'HEOG': 'eog'}

# load the raw data
raw = mne.io.read_raw_brainvision(
    data_path + '%s.vhdr' % subject, preload=True)
raw.set_channel_types(eog_channles)  # make the eog channels behave as EOG
raw.filter(None, 40)  # lowpass filter
raw.filter(1, None)  # highpass filter
raw.set_montage(montage)  # tell mne where the channels are located; standard
#  10-20

events = mne.find_events(raw)  # find the time of
# events, i.e. triggers,
# in the
# data

picks = mne.pick_types(
    raw.info,
    meg=False,
    eeg=True,
    stim=False,
    eog=False,
    include=[],
    exclude=[])

# Make epochs from the raw data
epochs = mne.Epochs(
    raw,
    picks=picks,
    events=events,
    event_id=event_id,
    tmin=tmin,
    tmax=tmax,
    preload=True,
    reject=None)

# Setup AutoReject
ar = AutoReject(
    n_interpolates,
    consensus_percs,
    thresh_method='random_search',
    random_state=seed)

# Fit, i.e. calculate AutoReject
ar.fit(epochs)

epochs_clean = ar.transform(epochs)  # Clean the epochs
epochs_clean.save(data_path + '%s-epo.fif' % subject)  # Save the epochs
