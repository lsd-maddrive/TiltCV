import matplotlib.pyplot as plt
import scipy.io as sio
import numpy as np


def plot_graph(time_control_syst, x_control_syst, y_control_syst):

    plt.figure(1)
    for i in range(len(x_control_syst)):
        plt.plot(time_control_syst[i],x_control_syst[i])

    plt.grid()
    plt.xlabel('Time ')
    plt.ylabel('x_value')

    plt.figure(2)
    for i in range(len(y_control_syst)):
        plt.plot(time_control_syst[i],y_control_syst[i])

    plt.grid()

    plt.xlabel('Time ')
    plt.ylabel('y_value')

    plt.show()



def clear_data(time_control_syst, x_control_syst, y_control_syst):

    time_control_syst =[]
    x_control_syst = []
    y_control_syst = []

    return time_control_syst, x_control_syst, y_control_syst



def write_to_mat(time, x, y):
    sio.savemat('x.mat', {'x': x})
    sio.savemat('y.mat', {'y': y})
    sio.savemat('time.mat', {'time': time})
