from pandas import read_csv
from matplotlib import pyplot, rcParams

rcParams['lines.linewidth'] = 1

def plot(apikey, file, fig_file):
	# load dataset
	dataset = read_csv(file, header=0, index_col=0)
	values = dataset.values
	# specify columns to plot
	groups = [0, 1, 2, 3, 4]
	i = 1
	# plot each column
	figure = pyplot.figure()
	figure.suptitle("Metrics for \"{apikey}\"".format(apikey=apikey), fontsize=14)
	for group in groups:
		subplot = pyplot.subplot(len(groups), 1, i)
		subplot.plot(values[:, group])
		subplot.set_title(dataset.columns[group], y=0.5, loc='right')
		i += 1
	figure.savefig(fig_file, dpi=300)