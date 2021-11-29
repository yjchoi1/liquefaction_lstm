import numpy as np
import pandas as pd
import copy
from matplotlib import pyplot as plt


# cut the dataframe
def cutDataFrame(time_steps, cols, dataframe):
    # make indices to iterate
    num_exps = len(dataframe[:])
    num_trials = []
    for exp in range(len(dataframe[:])):
        num_trials.append(len(dataframe[exp][:]))

    # create a list which has the same shape with df_all to contain cut dataframe
    df_cut = copy.copy(dataframe)

    # cut data with length of `time_steps`
    for exp in range(num_exps):
        for trial in range(num_trials[exp]):
            df_cut[exp][trial] = df_cut[exp][trial][cols][:time_steps]

    return df_cut


# choose experiment and trials to use in training and returns array
def data_array(expIndex, trialIndex, df_cut):
    data_list = []
    trialIndex_list = []
    for i in expIndex:
        for j in trialIndex[i]:
            value = pd.DataFrame.to_numpy(df_cut[i][j])
            data_list.append(value)
            trialIndex_list.append([i, j])
    data_array = np.asarray(data_list)

    return data_array, trialIndex_list


# normalize selected cols
def normalize_cols(data_array, cols_to_normalize):

    # unroll the dataset horizontally
    data_to_normalize = np.copy(data_array)  # copy the data_array
    data_array_shape = np.shape(data_to_normalize)  # get the shape of the dataset
    numTrials = data_array_shape[0]  # get the num of trials in the dataset
    numDataPoints = data_array_shape[1]  # get the num of data points in the dataset
    numCols = data_array_shape[2]  # get the num of cols in the dataset
    data_array_unroll = np.reshape(data_to_normalize, (numTrials * numDataPoints, numCols))  # unroll the dataset

    # make data container for the normalization factor and the normalized dataset
    max_val_cols = np.zeros((len(cols_to_normalize), 1))  # array to contain normalization factor
    data_array_unroll_normalized = np.copy(data_array_unroll[:, :])  # array to contain normalized dataset

    # normalize by the max val of each selected cols
    for i in cols_to_normalize:  # iterate over the selected cols
        max_val_cols[i, 0] = max(data_array_unroll[:, i])  # save the max vals of each col
        data_array_unroll_normalized[:, i] = data_array_unroll[:, i] / max_val_cols[i, 0]  # normalize each col by the max vals

    # reshape data to the shape before unrolling
    data_array_normalized = np.reshape(data_array_unroll_normalized, (numTrials, numDataPoints, numCols))

    return data_array_normalized, max_val_cols


# make x and y sets for RNN based on time window method
def windowDataset(x_array_train, y_array_train, x_array_test, y_array_test, length, time_steps):

    # container for the samples and targets
    x_rnn_train = list()
    y_rnn_train = list()
    x_rnn_test = list()
    y_rnn_test = list()

    # get the whole number of trials in the dataset
    numTrials_train = np.shape(x_array_train)[0]
    numTrials_test = np.shape(x_array_test)[0]

    # make a training time-series examples
    # step over the 8,600 in jumps of length
    for trialIndex in range(numTrials_train):
        for i in range(time_steps - length):  # grab from i to i + length
            sample_train = x_array_train[trialIndex, i:i+length, :]
            outcome_train = y_array_train[trialIndex, i+length, 0]
            x_rnn_train.append(sample_train)
            y_rnn_train.append(outcome_train)
    for trialIndex in range(numTrials_test):
        for i in range(time_steps - length):  # grab from i to i + length
            sample_test = x_array_test[trialIndex, i:i+length, :]
            outcome_test = y_array_test[trialIndex, i+length, 0]
            x_rnn_test.append(sample_test)
            y_rnn_test.append(outcome_test)

    x_rnn_train = np.asarray(x_rnn_train)
    y_rnn_train = np.array(y_rnn_train[:])
    x_rnn_test = np.asarray(x_rnn_test)
    y_rnn_test = np.array(y_rnn_test[:])

    return x_rnn_train, y_rnn_train, x_rnn_test, y_rnn_test


# add more features
def addFeatures():
    print('not yet')