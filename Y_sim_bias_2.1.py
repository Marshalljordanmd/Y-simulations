#from "Y_sim_bias_2.py" altered to show on single plot both bias and unbiased data
#made initially for 1000G data. August 25, 2021.

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import math
from random import randint
from random import seed
from random import choice
from random import gauss
seed()


def growth(rate,world):
	#rate is the population growth rate, the number of males born per man in the population per generation
	#world is a dictionary of lists, representing the world of men (keys) with their Y mutations numbered in a list (values).
		
	j=1
	new_pop = {} #the next generation
	for key in world:    #new men are added and consecutively numbered to make up the next generation. key = man in world
		for i in range(j,rate+j):
			new_pop[i] = world[key] #for each new male, his fathers mutations are assigned
		j += rate 
			
	return new_pop  ##the next generation replaces the old, who dies. So 'world' is replaced with 'new_pop' which is larger by the rate of growth
#these new_pop males have their father's mutations but no new mutations yet assigned		

def mutation_count(world): #to keep track of the numbered mutations and continue the numbered sequence.
	large = max(world) #the number of keys in world
	if large == 0:
		count == 0
	else:
		count = world[large][-1] #since mutations are numbered sequentially as are the keys (males).
	return count		


def mutation(world,mu,count): #assigns each person in the new world 'mu' additional mutations 
	#mu = mutation rate
	#count is the unique mutation count from the function 'mutation_count'
	mu_ct = count
	#mu_vars = [3,4,5,6,7,8]
	#mu = choice(mu_vars)
	
	for key in world:  #this loop adds mutations to the new world population.
		new_muts = []
		new_list = []

		old_muts = world[key]
					
		for i in range(mu):
			new_muts.append(mu_ct + 1)
			mu_ct += 1
		new_list = old_muts + new_muts #the new mutations are added to the old for each male, that is each key
		world[key] = new_list
		
	return world


def famine(world,pop_max):
#introducing bottlenecks to the population, keeping population at, or below, a specified max population level .
#the max population is due to a carrying capacity that can't be exceeded
#those men selected to die are chosen randomly by 'choice'
#this function needs to add a duration of the bottleneck, to keep the population low for several years.	
	list = []
	kill_list = []
	for key in world:
		list.append(key)#a list of all the men in the world or sub-population
		
	kill_num = len(list) - pop_max   #this number assumed to be above 0.
	for i in range(kill_num):		
		kill = choice(list) #random selection of a man from the list
		kill_list.append(kill)
		list.remove(kill) #as each male is killed, he is removed from the list

	
	for k in kill_list:  #here world is purged of the number of men who must die in the famine.
		del world[k]   #this produces gaps in the numbered key sequence, so world is renumbered next.
	
	i = 1
	new_world = {}
	for key in world:  #re-number keys consecutively
		new_world[i] = world[key]
		i += 1
			
	return new_world
	
	
def death(world,mort):
#introducing a random death function, removing 0 to 'mort' percent of the population each generation, accounting for diseases and murders.
#this serves to keep the population constant and low enough so the computer can handle the data.	
	pop = len(world)
	d_num = mort*pop/100 # the average number of men to die per generation based on 'mort', which is a percent
	a = int(0.9*d_num)
	b = int(1.1*d_num)
	die =randint(a,b)
	#die = int(d_num)
	list = []
	kill_list = []
	for key in world:
		list.append(key)
		
	for i in range(die):		
		kill = choice(list) #random selection of a man to be killed from the list
		kill_list.append(kill)
		list.remove(kill)#removes all the men selected to be killed

		
	for k in kill_list: #world is purged of those men murdered of dying of disease, and so not reproducing.
		del world[k]
	
	i = 1
	new_world = {}
	for key in world:  #re-number keys consecutively
		new_world[i] = world[key]
		i += 1
								
	return new_world	
	
def G_Khan(world,man,sons): #this adds many sons to one man
#man is the key number to be addressed. Sons is the number of males to come from this key
	new_pop = {}
	for key in world:
		if key < man:
			new_pop[key] = world[key]
		if key == man:
			for i in range(0,sons+1):
				new_pop[man+i] = world[man]#each son gets his fathers mutation list. Unique mutations must be added by 'def: mutation_count and  def: mutation'
		if key > man:
			new_pop[key+sons] = world[key] #without '-1' the first man after the expansion of sons is dropped.
			
	return new_pop


def mu_rate(g,c): #to compute the mutation rate based on exponential approx. of Figure 9 in Carter 2019. Patriarchal Drive function.
	mu = int(c*math.exp(-0.09*g)) #c = patriarchial drive constant (set from 10 to 60 mutations for S,H,J)
	mu = int(gauss(mu,2))
	
	if mu < 3:
		mu = 3 #will not allow mutations to fall too low
	return mu


def ref_bias(AC,num_men): #to bias the final AC by changing the reference
	#if AC < num_men/2 and AC > num_men/20:
# 	if AC < num_men/2:
# 		AC = num_men - AC
	if AC > 6:
		AC = num_men - AC
	return(AC)





















print('')
print('gen, pop')
		
#the simulation begins with Y-MRCA, who fathers from 2 to 7 sons, randomly chosen for generation 1
world = {0:[]}  #Y-MRCA is the reference and so has 0 mutations
max_pop = 1450
bottle_neck_mortality = randint(70,85)
bottle_neck_gens = [4,6,7,10,15,18,26,28,30,33,35,37,40,42,45,51,55,60,65,70,75,80,85,90,93,101,105,110,115,120,125,130,135,140,145,151,155,160,165,170,175]
c = 40 #patriarchal drive coefficient (after Carter 2019)
#gens = int(input('How many generations ?'))
gens = 100

for g in range(0,gens): #number of generations to run before analysis
	g_rate = randint(2,9) #growth rate per generation
	man = randint(1,len(world)) #random man selected to be G Khan  and have many sons
	mort = randint(10,20)
	mu = mu_rate(g,c)
	sons = randint(50,150)
	if g == 0:
		world = growth(3,world)  #set the initial number sons from Y-MRCA
		world = mutation(world,mu,0)		
		patriarch_gen_0 = world #this dictionary is the patriarchs and their patriarch mutations
		print(g,len(world))
	if g > 0 and g <= 3:
		world = growth(g_rate,world)
		count = mutation_count(world)
		world = mutation(world,mu,count)
		print(g,len(world))
		
	if g > 3:
		world = growth(g_rate,world)
		if len(world) > max_pop:
			world = famine(world,max_pop)
		world = death(world,mort)
		if g in bottle_neck_gens:
			world = G_Khan(world,man,sons)
		count = mutation_count(world) 
		world = mutation(world,mu,count)
		if g in bottle_neck_gens:
			world = death(world,bottle_neck_mortality) #for generations with bottlenecks, the mortality is great
		print(g,len(world))
	
	if g == gens - 2:
		world = growth(g_rate,world)
		count = mutation_count(world)
		world = mutation(world,mu,count)
		print(g,len(world))
		
	if g == gens - 1:
		if len(world) > 1233:
			world = famine(world,1233)
		elif len(world) <= 1233:
			world = growth(g_rate,world)
			world = famine(world,1233)
		
print('')
print('patriarch world = ',patriarch_gen_0)






#now to get the world's mutation frequencies
#below are lines to compute the variant frequencies and plot the results

num_men = len(world)  
print('number of men alive in world = ', num_men)


variants = 0
for key in world: #key is the individual man, values are the mutations he carries
	variants += len(world[key])  #counting all the mutations surviving in the world
var_num = variants/num_men
print('number of mutations in whole_world = ',variants)
print('average mutations per man = ',var_num )


#now initialize 2 dictionaries, one for the unbiased and one for the biased data
AC_dict = {} #here the keys will be the mutations of a given AC and the value the number of occurences in the population of mutations with that AC
for i in range(1,num_men+1):
	AC_dict[i] = 0	#making AC bins for the number of men in world


AC_dict_biased = {}
for i in range(1,num_men+1):
	AC_dict_biased[i] = 0






counted_list = []
mut_list = []
for key in world:
	val = world[key]#a list of mutations carried by a man (key)
	for e in val:
		mut_list.append(e) #making a list of all mutations in whole_world, many repeat mutations, of course
#print(mut_list)

seg_sites = set(mut_list)
num_seg_sites = len(seg_sites)
print('Number of segregating sites = ',len(seg_sites))


#to bias the data so that one man's mutations are all biased:
bias_list = []
b = randint(1,len(world)) #a single man in world is selected to bias the reference
bias_list = world[b] #these should be all the mutations carried by b, the man who will become the reference
p_var = min(bias_list) #a patriarch variant of the man who will become the reference bias
print('b = ',b,' patrarch variant = ',p_var)  #a patriarch variant of the man who will be the reference is the lowest numbered mutation in his list
for key in patriarch_gen_0:
	if p_var in patriarch_gen_0[key]:
		bias_lineage = key
		print('patriarch lineage ',key,' is the biased lineage')

switched = []		
for m in mut_list:
	AC = 0
	if not m in counted_list:
		counted_list.append(m)
		AC = mut_list.count(m)  #the mvariants m are counted from the list of all variants in world to get the AC for the variant m
		AC_dict[AC] += 1
		if m in bias_list: #for biased positions the two dictionaries are handled differently below
			if m == 0:
				print('m = 00000000000000000000')
			AC = ref_bias(AC,num_men)#the AC will be changed by the bias and added to the AC_dict_biased dictionary
			AC_dict_biased[AC] += 1
			switched.append(m)  #at the end the switched list should be the same as the bias_list
		else:
			AC_dict_biased[AC] += 1

print('')
print('number variants switched due to bias = ',len(switched))
print('')
print('highest AC of switched sites = ',min(switched))

#You already have mut_list, patriarch_gen_0, and world, so men who have any patriarch mutation can be obtained
patriarch_var_dict = {}
pat_vars = []
for key in patriarch_gen_0:
	vars = patriarch_gen_0[key]
	for v in vars:
		patriarch_var_dict[v] = 0 #initialize this dictionary for the patriarch variants to be counted in world
		pat_vars.append(v) #get a list of the world's patriarch variants

for m in mut_list:
	if m in pat_vars:
		patriarch_var_dict[m] += 1
			
	
print('')
print('dictionary of patriarch variants and their AC = ',patriarch_var_dict)
lineage_men = set(patriarch_var_dict.values())
print('')
print('lineages have these men in final world : ',lineage_men)
print('')
print('men in lineage ',bias_lineage,' = ',patriarch_var_dict[p_var])




		
#below is code to plot the number vs AC bin using data from the AC_dict
title = input('What is the plot title ? ')

#to only look at common variants, AC > 5%, which are in AC bin > 0.05*num_men
com_AC = int(0.05*num_men) #set to 0 to look at all variants
print('common AC bin cut off = ',com_AC)


		
		
		

		
#now get the common variants from the mutation list
com_var_min = .05*len(world) #common variants are those with AC >5%







#the following lines plot the results

x = []
y = []
for key in AC_dict:
	if key > com_AC: #use this to count only common variants
		x.append(key)
		val = AC_dict.get(key)
		y.append(val)
plt.plot(x,y)

plt.ylabel('Number of Variants')

plt.xlabel('Allele Count')
plt.title('Simulated Variants')

plt.show()






x1 = []
y1 = []
for key in AC_dict_biased:
	if key >com_AC:
		x1.append(key)
		val = AC_dict_biased.get(key)
		y1.append(val)
plt.plot(x1,y1)

plt.ylabel('Number of Variants')

plt.xlabel('Allele Count')
plt.title('Simulated Variants - Biased')

plt.show()





variant_accum = {} #dictionary to record the accumulation of variants as AC increases
variant_accum_bias = {}

num_var = 0
for key in AC_dict:
	num = AC_dict[key]
	num_var += num
	variant_accum[key] = num_var
	
num_var_bias = 0
for key in AC_dict_biased:
	num = AC_dict_biased[key]
	num_var_bias += num
	variant_accum_bias[key] = num_var_bias
	

	
#print('variant accumulation dictionary = ',variant_accum)

x2 = []
y2 = []
for key in variant_accum:
	if key > com_AC:
		x2.append(key)
		var = variant_accum[key]
		
		y2.append(var)
# print('x2 = ',x2)
# print('')
# print('y2 = ',y2)

x3 = []
y3 = []
for key in variant_accum_bias:
	if key > com_AC:
		x3.append(key)
		var = variant_accum_bias[key]
		
		y3.append(var)

  			
#to get the slope of the line in the biased data from AC 800 to AC 1200
ac_800 = variant_accum_bias[800]
slope = (num_seg_sites - ac_800)/400
print('slope of high frequency biased variants above AC 800 = ',slope)

 
plt.plot(x2,y2,'b')
plt.plot(x3,y3,'r')
plt.xlabel('Allele Count')
plt.ylabel('Number of Variants')
plt.title('Simulated Cumulative Density')
plt.legend(labels=['No Bias','With Bias'])

plt.show()

	









