import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.svm import SVR
import csv

def string_process(x):
    y = x[0].split('-')
    return int(y[0]) * 100 + int(y[1]) * 3


def predict_state_confirmed(state_index, data_given, test_data_given):
    data_state = data_given.iloc[state_index::50, :]
    X_temp = data_state.iloc[:, 0:1].values
    X = np.array([[string_process(x)] for x in X_temp])
    y = data_state.iloc[:, 1].values
    polynomial_features = PolynomialFeatures(degree=3)
    reg = SVR(C=1e5, max_iter=1000)
    reg.fit(X, y)
    test_data_state = test_data_given.iloc[::50, :]
    test_x_temp = test_data_state.iloc[:, 0:1].values
    test_x = np.array([[string_process(x)] for x in test_x_temp])
    predicted_y = reg.predict(test_x)
    return predicted_y


def plot_confirmed(state_no, result_matrix_given, data_given, test_data_given):
    data_state = data_given.iloc[state_no::50, :]
    X_temp = data_state.iloc[:, 0:1].values
    X = np.array([[string_process(x)] for x in X_temp])
    y = data_state.iloc[:, 1].values
    plt.plot(X, y)
    test_data_state = test_data_given.iloc[::50, :]
    test_x_temp = test_data_state.iloc[:, 0:1].values
    test_x = np.array([[string_process(x)] for x in test_x_temp])
    pred_y = result_matrix_given[state_no]
    plt.plot(test_x, pred_y)
    plt.show()


data = pd.read_csv("../../data/train.csv")
data = data.fillna(data.mean())
data_dead = data[['Date', 'Deaths']]
data = data[['Date', 'Confirmed']]
test_data = pd.read_csv("../../data/test.csv")
test_data = test_data[['Date']]

result_matrix_confirmed = np.array([predict_state_confirmed(i,data, test_data) for i in range(50)])
result_matrix_dead = np.array([predict_state_confirmed(i,data_dead, test_data) for i in range(50)])

with open('basic_pred.csv', mode='w') as prediction_file:
    prediction_writer = csv.writer(prediction_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,lineterminator = '\n')

    prediction_writer.writerow(['ForecastID','Confirmed','Deaths'])
    index = range(1300)
    confirmed_vals = result_matrix_confirmed.T.ravel()
    death_vals = result_matrix_dead.T.ravel()
    for i in index:
        prediction_writer.writerow([str(i), str(confirmed_vals[i]), str(death_vals[i])])