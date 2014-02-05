# ECS 152A Fall 2013
# Project 2, part 1
# Authors: Abilio de Oliveira (999550263) and Alan Gutstein (997256938)

import simpy
import random
import math
from matplotlib import pyplot

LAMBDAVALUES = [0.2, 0.4, 0.6, 0.8, 0.9, 0.99];
BUFFERVALUES = [10, 50];
SERVICERATE = 1;
RANGE = 10000

print('Running (the results will be saved automatically in the project folder)...')

# queue buffer
class Buffer(object):
    def __init__(self, env, capacity):
        self.env = env
        self.capacity = capacity
        self.packetsBeingHold = 0
        self.action = env.process(self.run())

    def run(self): # release a packet at a negative exponential rate
        while True:
            # a packet will be taken from the queue every random.expovariate(SERVICERATE)
            if (self.packetsBeingHold > 0):
                self.packetsBeingHold = self.packetsBeingHold - 1
                tib = random.expovariate(SERVICERATE)
                yield env.timeout(tib)
            else: # if its empty the timeout event will be at every iteration of the environment.
                yield env.timeout(1)

class System(object):
    def __init__(self, env, arrival_rate, buffer_capacity):
        self.env = env
        self.arrival_rate = arrival_rate
        self.buffer = Buffer(self.env, buffer_capacity)
        self.action = env.process(self.run())
        self.droppedPackets = 0

    def run(self):
        while True:
            if (self.buffer.packetsBeingHold < self.buffer.capacity):
                self.buffer.packetsBeingHold = self.buffer.packetsBeingHold + 1
            else:
                self.droppedPackets = self.droppedPackets + 1
            t = random.expovariate(self.arrival_rate)
            
            yield env.timeout(t) # a new packet will arrive at every timeout event

env = simpy.Environment()

system101 = System(env, LAMBDAVALUES[0], BUFFERVALUES[0])
system102 = System(env, LAMBDAVALUES[1], BUFFERVALUES[0])
system103 = System(env, LAMBDAVALUES[2], BUFFERVALUES[0])
system104 = System(env, LAMBDAVALUES[3], BUFFERVALUES[0])
system105 = System(env, LAMBDAVALUES[4], BUFFERVALUES[0])
system106 = System(env, LAMBDAVALUES[5], BUFFERVALUES[0])
system501 = System(env, LAMBDAVALUES[0], BUFFERVALUES[1])
system502 = System(env, LAMBDAVALUES[1], BUFFERVALUES[1])
system503 = System(env, LAMBDAVALUES[2], BUFFERVALUES[1])
system504 = System(env, LAMBDAVALUES[3], BUFFERVALUES[1])
system505 = System(env, LAMBDAVALUES[4], BUFFERVALUES[1])
system506 = System(env, LAMBDAVALUES[5], BUFFERVALUES[1])
        
env.run(until=RANGE)

yPoints = [system101.droppedPackets/float(RANGE), system102.droppedPackets/float(RANGE), system103.droppedPackets/float(RANGE), system104.droppedPackets/float(RANGE), system105.droppedPackets/float(RANGE), system106.droppedPackets/float(RANGE)];

pyplot.plot(LAMBDAVALUES, yPoints)
pyplot.xlabel('arrivalrate (pkts/sec)');
pyplot.ylabel('probability of packet drop')
pyplot.title('Project 2, part1: simple queue system \n Buffer Capacity = 10 pkts')
pyplot.grid(True)
pyplot.savefig("Project2Part1-Bequals10.jpeg")

pyplot.clf()

yPoints = [system501.droppedPackets/float(RANGE), system502.droppedPackets/float(RANGE), system503.droppedPackets/float(RANGE), system504.droppedPackets/float(RANGE), system505.droppedPackets/float(RANGE), system506.droppedPackets/float(RANGE)];

pyplot.plot(LAMBDAVALUES, yPoints)
pyplot.xlabel('arrivalrate (pkts/sec)');
pyplot.ylabel('probability of packet drop')
pyplot.title('Project 2, part1: simple queue system \n Buffer Capacity = 50 pkts')
pyplot.grid(True)
pyplot.savefig("Project2Part1-Bequals50.jpeg")

print('Done!')