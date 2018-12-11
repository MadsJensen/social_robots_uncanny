import sys

import mne
import pandas as pd

from project_settings import data_path

subject = sys.argv[1]

# Selected channels
chs = [
    'CP1', 'CP5', 'CP2', 'CP6', 'Pz', 'P3', 'P7', 'P4', 'p8', 'Oz', 'O1', 'O2'
]
conditions = ['1', '2', '3', '4', '5']
times = [0.109, 0.232, 0.420]  # times to extract

epochs = mne.read_epochs(data_path + "%s-epo.fif" % subject)
epochs.set_eeg_reference()
epochs.apply_proj()
epochs.pick_channels(chs)

results = pd.DataFrame()

for tt in times:
    epochs_crop = epochs.copy()
    epochs_crop.crop(tt - 0.01, tt + 0.01)

    for condition in conditions:
        tmp = epochs_crop[condition]
        for jj in range(len(tmp)):
            row = pd.DataFrame([{
                'condition': condition,
                'value': tmp[jj].get_data().mean(),
                'time': tt,
                'subject': subject
            }])
            results = pd.concat((results, row))

results.to_csv(data_path + 'results_%s.csv' % subject, index=False)
