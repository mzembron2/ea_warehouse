import numpy as np
import matplotlib.pyplot as plt
import os

DIRNAME = os.path.dirname(__file__)
FILENAME= os.path.join(DIRNAME, '../data/performance.txt')


def read_file():
    all_data = []
    new_data = [[],[]]
    title = ''
    first_line = True
    performance_file = open(FILENAME, 'r') 
    lines = performance_file.readlines()
    for line in lines:
        if("Population" in line):
            if(first_line):
                title = line
                first_line =False
            else:
                all_data.append(new_data)
                new_data = [[],[]]
        else:
            splited_data = line.split()
            new_data[0].append(int(splited_data[0]))
            new_data[1].append(float(splited_data[1]))
    all_data.append(new_data)
    set_same_iteration_length(all_data)
    plot_data(all_data, title)

def set_same_iteration_length(data):
    iter, _= max(data, key= lambda i : i[0][-1])
    highiest_iter = iter[-1]
    for element in data:
        element[0].append(highiest_iter+10)
        element[1].append(element[1][-1])

def plot_data(data, title):
    for element in data:
        name = "Final score: "+str(element[1][-1])
        plt.step(element[0],element[1], label = name, where = 'post')
    plt.legend()
    plt.title(title)
    plt.show()

if __name__ == "__main__":
    read_file()