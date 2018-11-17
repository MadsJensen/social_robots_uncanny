import mne
import sys
from project_settings import data_path

subject = sys.argv[1]

epochs = mne.read_epochs(data_path + '%s-epo.fif' % subject)


ave_1 = epochs['1'].average()
ave_2 = epochs['2'].average()
ave_3 = epochs['3'].average()
ave_4 = epochs['4'].average()
ave_5 = epochs['5'].average()

fig = ave_1.plot(show=False)
fig.savefig(data_path + 'ave_1_%s.png' % subject)
fig = ave_1.plot_joint(show=False)
fig.savefig(data_path + 'ave_1_joint_%s.png' % subject)

fig = ave_2.plot(show=False)
fig.savefig(data_path + 'ave_2_%s.png' % subject)
fig = ave_2.plot_joint(show=False)
fig.savefig(data_path + 'ave_2_joint_%s.png' % subject)

fig = ave_3.plot(show=False)
fig.savefig(data_path + 'ave_3_%s.png' % subject)
fig = ave_3.plot_joint(show=False)
fig.savefig(data_path + 'ave_3_joint_%s.png' % subject)

fig = ave_4.plot(show=False)
fig.savefig(data_path + 'ave_4_%s.png' % subject)
fig = ave_4.plot_joint(show=False)
fig.savefig(data_path + 'ave_4_joint_%s.png' % subject)

fig = ave_5.plot(show=False)
fig.savefig(data_path + 'ave_5_%s.png' % subject)
fig = ave_5.plot_joint(show=False)
fig.savefig(data_path + 'ave_5_joint_%s.png' % subject)

diff_1_5 = mne.combine_evoked([ave_1, -ave_5], weights='equal')
fig = diff_1_5.plot(show=False)
fig.savefig(data_path + 'diff_1_5_%s.png' % subject)
fig = diff_1_5.plot_joint(show=False)
fig.savefig(data_path + 'diff_1_5_joint_%s.png' % subject)
