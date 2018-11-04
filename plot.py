from pandas import read_csv
from matplotlib import pyplot, rcParams
from os.path import isfile

rcParams['lines.linewidth'] = 1

def plot(apikey, file, fig_file):
	# load dataset
	if (isfile(file)):
		dataset = read_csv(file, header=0, index_col=0, parse_dates=True)
		figure = pyplot.figure()
		figure.suptitle("Metrics for \"{apikey}\"".format(apikey=apikey), fontsize=14)
		for index, feature in enumerate(dataset.columns):
			subplot = pyplot.subplot(len(dataset.columns), 1, index + 1)
			pyplot.subplots_adjust(hspace = 0.4)
			subplot.tick_params(labelsize=6)
			subplot.plot(dataset[feature])
			subplot.set_title(feature, y=0.7, loc='right', fontsize=6)
		figure.savefig(fig_file, dpi=300)
		pyplot.close()