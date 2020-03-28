#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 20:24:01 2020

@author: nicolo
"""

numbit = 3 # Number of bits
sortValues = False # decides whether the state values have to be sorted according to probability or not

from plotly.offline import plot
import plotly.graph_objs as go

from tkinter import Tk
from tkinter.filedialog import askopenfilename

import numpy as np
from qiskit import IBMQ
from qiskit import(QuantumCircuit, execute, Aer)

def getIntermediateStatevector(circuit, simulator):
    result = execute(circuit, simulator).result()
    statevector = result.get_statevector(circuit)
    return statevector

def getProbabilityVector(statevector): # for every state, gets the probability associated to it
    return np.square(np.abs(statevector)).tolist()
    
def getProbabilities(circuit, simulator):
    return getProbabilityVector(getIntermediateStatevector(circuit, simulator))

def addToPlot(timeMatrix, circuit, simulator): # adds to the final matrix, that will be used for the plot
    timeMatrix.append(getProbabilities(circuit, simulator))
   
def transpose(matrix): # matrix transposition to have time on the x axis
    numpy_array = np.array(matrix)
    transpose = numpy_array.T
    transpose_list = transpose.tolist()
    return transpose_list

def sort(matrix): # sort starting from the highest probability to the lowest
    sortedMatrix = matrix.copy()
    for i in range(0, len(sortedMatrix)):
        sortedMatrix[i].sort(reverse = True)
        
    return sortedMatrix
    
def convertToBinary(x, n=0): # from https://stackoverflow.com/questions/699866/python-int-to-binary-string
    return format(x, 'b').zfill(n)

# GUI definition
# Upload a file
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

file = open(filename, "r")
code = file.read()

code = "\naddToPlot(timeMatrix, circuit, simulator)\n".join(code.split("\n"))

timeMatrix = []

simulator = Aer.get_backend('statevector_simulator')

# Execute the quantum code simulation
exec(code)

if(sortValues == True):
    timeMatrix = sort(timeMatrix)
    
timeMatrix = transpose(timeMatrix)

fig = go.Figure(data=[{'type': 'heatmap', 'z': timeMatrix}])
fig.update_layout(
    title="SQUARM Graph",
    xaxis_title="Instruction number",
    yaxis_title="State",
    xaxis = dict(tickmode = 'linear', tick0 = 0.0, dtick = 1.0),
    yaxis = dict(
        tickmode = 'array',
        tickvals = []
    )
)
    
if(sortValues == False):
    fig.update_layout(
        title="QUARM Graph",
        yaxis = dict(
            tickmode = 'array',
            dtick = 1.0,
            tickvals = list(range(numbit**2)),
            ticktext = [convertToBinary(x, numbit) for x in list(range(numbit**2))]
        )
    )
    
plot(fig)