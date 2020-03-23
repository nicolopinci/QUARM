#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 20:24:01 2020

@author: nicolo
"""
from plotly.offline import plot
import plotly.graph_objs as go

import numpy as np
from qiskit import IBMQ
from qiskit import(QuantumCircuit, execute, Aer)

def getIntermediateStatevector(circuit, simulator):
    result = execute(circuit, simulator).result()
    statevector = result.get_statevector(circuit)
    return statevector

def getProbabilityVector(statevector):
    return np.square(np.abs(statevector)).tolist()
    
def getProbabilities(circuit, simulator):
    return getProbabilityVector(getIntermediateStatevector(circuit, simulator))

def addToPlot(timeMatrix, circuit, simulator):
    timeMatrix.append(getProbabilities(circuit, simulator))
   
def transpose(matrix):
    numpy_array = np.array(matrix)
    transpose = numpy_array.T
    transpose_list = transpose.tolist()
    return transpose_list

def sort(matrix):
    sortedMatrix = matrix.copy()
    for i in range(0, len(sortedMatrix)):
        sortedMatrix[i].sort(reverse = True)
        
    return sortedMatrix
    
def convertToBinary(x, n=0): # from https://stackoverflow.com/questions/699866/python-int-to-binary-string
    return format(x, 'b').zfill(n)

timeMatrix = []
numbit = 2
sortValues = False

simulator = Aer.get_backend('statevector_simulator')

# Create a Quantum Circuit acting on the q register
circuit = QuantumCircuit(numbit, numbit)

# Add a H gate on qubit 0
circuit.h(0)
addToPlot(timeMatrix, circuit, simulator)

# Add a CX (CNOT) gate on control qubit 0 and target qubit 1
circuit.cx(0, 1)
addToPlot(timeMatrix, circuit, simulator)
 
# Map the quantum measurement to the classical bits
circuit.measure([0,1], [0,1])
addToPlot(timeMatrix, circuit, simulator)

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