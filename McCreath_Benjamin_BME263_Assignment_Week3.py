import csv
import math

import matplotlib.pyplot as plt


def load_data():
    with open('BME163_Input_Data_2.txt', 'r') as file_in:
        data = list(csv.reader(file_in, delimiter='\t'))
    for datum in data:
        if "NA" in datum[2]:
            datum[2] = 0
        else:
            datum[2] = float(datum[2].lower())
    for datum in data:
        if "NA" in datum[1]:
            datum[1] = 0
        else:
            datum[1] = float(datum[1].lower())
    return data


def main():
    # load the raw data as a two dim list
    data = load_data()
    # Set the stylesheet
    plt.style.use('BME163.mplstyle')
    # Set the figure size, make the axes, and set axes properties
    plt.figure(figsize=(3, 3))
    panel = plt.axes([0.5 / 3, 0.5 / 3, 2 / 3, 2 / 3])
    panel.set(xlim=(-12, 12), ylim=(0, 60), xlabel="$log_2(fold\ change)$", ylabel="-$log_{10}$(p-value)")
    # Strip out the x data
    data_x = [datum[1] for datum in data]
    # Stripping the Y data is hard because sometimes it needs to be 0 not 'na'
    data_y = []
    # Loop over the data and convert it, if it's 0 keep it 0 and move on
    for datum in data:
        if datum[2]:
            data_y.append(math.log10(datum[2]) * -1)
        else:
            data_y.append(0)
    # Make an array of colors for the scatter function. array[i] is 'red' if 2^x  > 10 and y > 8
    colors = ['red' if 2 ** math.fabs(x[0]) > 10 and x[1] > 8 else 'black' for x in zip(data_x, data_y)]
    # Plots the points
    panel.scatter(data_x[:], data_y[:], color=colors, s=2.1, edgecolor=None, linewidths=0)
    # Loops over the X and Y data and determines if the point needs to be labeled. Points labeled are x < 2^value
    # y value must be > 30. If these criteria are met label the poitn with the gene from the raw data.
    for i, point in enumerate(zip(data_x, data_y)):
        if 2 ** point[0] < 10 and point[1] > 30:
            panel.text(point[0] - 0.3, point[1], data[i][0], va='center', ha='right', fontsize=6)
    # Save the figure.
    plt.savefig('McCreath_Benjamin_BME263_Assignment_Week3.png', dpi=600)


if __name__ == '__main__':
    main()
