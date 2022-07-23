from json import dumps, loads
from math import exp
from random import random, randint



LAYERS = [10,   11,   12,   11,   10,   9]
MUTATION_RATE = 1 / 100



class neuron:
    def __init__(self, activationFunction, weight: float = None):
        self.weight = weight if weight else random()

        self.inputs: list[float] = []
        self.output: float = 0

        self.activationFunction = activationFunction

    def update(self) -> None:
        self.output = self.activationFunction(sum(self.inputs) / (len(self.inputs) if len(self.inputs) else 1) * self.weight)
        self.inputs.clear()

    def child(self):
        newWeight = self.weight + rand() * MUTATION_RATE
        return neuron(self.activationFunction, newWeight)



class synapse:
    def __init__(self, start: neuron, end: neuron, weight: float = None):
        self.start = start
        self.end = end

        self.weight = weight if weight else random()

    def update(self) -> None:
        self.end.inputs.append(self.start.output * self.weight)

    def child(self):
        newWeight = self.weight + rand() * MUTATION_RATE
        return synapse(self.start, self.end, newWeight)



class neuralNetwork:
    def __init__(self, neuronWeights: list[list[float]] = None, synapseWeights: list[list[float]] = None):
        self.layers = len(LAYERS)
        self.afuncs = [RELU] * (self.layers - 1) + [sigmoid]

        self.neuronLayers: list[list[neuron]] = []
        self.synapseLayers: list[list[synapse]] = []
        
        if neuronWeights and synapseWeights:
            for i, neurons in enumerate(LAYERS):
                self.neuronLayers.append([neuron(self.afuncs[i], neuronWeights[i][j]) for j in range(neurons)])

            for i in range(self.layers - 1):
                self.synapseLayers.append([synapse(n1, n2) for n2 in self.neuronLayers[i + 1] for n1 in self.neuronLayers[i]])
            for i in range(self.layers - 1):
                for j in range(i):
                    self.synapseLayers[i][j].weight = synapseWeights[i][j]

        else:
            for i, neurons in enumerate(LAYERS):
                self.neuronLayers.append([neuron(self.afuncs[i]) for _ in range(neurons)])

            for i in range(self.layers - 1):
                self.synapseLayers.append([synapse(n1, n2) for n2 in self.neuronLayers[i + 1] for n1 in self.neuronLayers[i]])

    def setInputs(self, inputs: list[float]) -> None:
        for i in range(len(self.neuronLayers[0])):
            self.neuronLayers[0][i].inputs.append(inputs[i])

    def run(self) -> list[float]:
        for i in range(self.layers):
            for n in self.neuronLayers[i]:
                n.update()
            if i != self.layers - 1:
                for s in self.synapseLayers[i]:
                    s.update()
        return [n.output for n in self.neuronLayers[self.layers - 1]]

    def child(self):
        new = neuralNetwork([0], self.afuncs)
        new.layers = self.layers
        new.neuronLayers = [[n.child() for n in layer] for layer in self.neuronLayers]
        new.synapseLayers = [[s.child() for s in layer] for layer in self.synapseLayers]
        return new

    def save(self) -> None:
        data = {
            'layers': [len(l) for l in self.neuronLayers],
            'neuronWeights': [[n.weight for n in layer] for layer in self.neuronLayers],
            'synapseWeights': [[s.weight for s in layer] for layer in self.synapseLayers],
        }

        with open(f'saves/{randint(0, 10000)}.json', 'w') as f:
            f.write(dumps(data))

    @staticmethod
    def load(filename: str):
        with open(filename, 'r') as f:
            data = loads(f.read())

        return neuralNetwork(**data)



def rand() -> float:
    return random() * 2 - 1

def sigmoid(x: float) -> float:
    return 1 / (1 + exp(-x))

def RELU(x: float) -> float:
    return max(0, x)