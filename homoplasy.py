#Homoplasy generator
#consider 10.4 MB of Y chromosome sequence, set mutation rate, and randomly mutate the Y chromosomes of all men in that population

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from random import randint
from random import seed
from random import choice
from random import gauss
import math
seed()

mut_dict = {}  #a dictionary to count the mutations to each base


for i in range(1,10400001): #making an artificial Y chromosome dictionary of positions to mutate
	mut_dict[i] = 0
print('length of mutation dictionary = ',len(mut_dict))	

mu = int(input('What is the mutation rate per generation ?'))

gens = int(input('How many generations ?'))  #total mutations in the pop are the mu rate times the generations

homo_count = 0
x = []
y = []

for mc in range(50):
	population = randint(100,2000)
	tot_mu = population * mu * gens #total mutations accumulate as the generations progress
	x.append(population)
	
	for i in range(tot_mu):
		p = randint(1,10400000) #randomly assign the mutation to a base in the 10.4 MB of Y chromosome
	#above step randomly assigns mutations in the population to positions on the Y c
		mut_dict[p] += 1
	print('mc = ',mc)

	for key in mut_dict: #after randomly placing all the mutation in the sample onto 10.4 MB of sequence, the number of homoplasies is counted
		n = mut_dict[key]
		if n > 1:
			homo_count += n - 1  #so one site may have multiple homoplasies, and total homoplasies is unlimited
	y.append(homo_count)
	homo_count = 0
	for i in range(1,10400001): #making an artificial Y chromosome dictionary of positions to mutate
	 	mut_dict[i] = 0 #zero mutations to start the next iteration
	 	
	 	
print('x = ',x)
print('')
print('y = ',y)

plt.scatter(x,y,alpha=.7,marker='o',color='b')
plt.scatter
plt.xlabel('Population')
plt.ylabel('Number of Homoplasies')
plt.title('Homoplasy vs Population')
plt.show()		
		
		




	
	
	
	
	
	
	
	
	
	
