#constructed 7.26, 2021
#modification of "y_sim_ref_bias.py" to randomly select patriarch lineages descending from Noah between 2 and 9 lineages


#a Y chromosome simulation to identify pattern of reference bias
#made initially for 1000G data. April 28, 2021.

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import math
import random
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
	mu_vars = [3,4,5,6,7,8]
	mu = choice(mu_vars)
	
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
	#print('# of men in world = ',len(list))
	#print('famine kill number = ', kill_num)
		
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
		mu = 3  #will not allow mutations to fall below 3 per generation
	return mu


def ref_bias(AC,num_men): #to bias the final AC by changing the reference
	#if AC < num_men/2 and AC > num_men/20:
# 	if AC < num_men/2:
# 		AC = num_men - AC
	if AC > 60:
		AC = num_men - AC
	return(AC)











		
#the simulation begins with Y-MRCA, who fathers from 2 to 7 sons, randomly chosen for generation 1

max_pop = 1500
bottle_neck_mortality = 85
bottle_neck_gens = [4,6,7,10,15,20,26,28,30,33,35,37,40,42,45,51,55,60,65,70,75,80,85,90,93,101,105,110,115,120,125,130,135,140,145,151,155,160,165,170,175]
c = 30 #patriarchal drive coefficient after Carter 2019

for MC in range(60):
	world = {0:[]}  #Y-MRCA is the reference and so has 0 mutations
	for g in range(0,100): #number of generations to run before analysis

		g_rate = randint(2,9) #growth rate per generation
		
		mort = randint(10,20)
		mu = mu_rate(g,c)
		
		sons = randint(50,150)
		if g == 0:
			p = random.uniform(.2,1)  #to set the initial number of lineages randomly between 2,9
			p = round(p,2)
			lin_num = int(10*p)
			
			world = growth(lin_num,world)  #set the initial number sons from Y-MRCA
			world = mutation(world,mu,0)		
			patriarch_gen_0 = world #this dictionary is the patriarchs and their patriarch mutations
			n_p_vars = mu
			print('generation = ',g,' number of patriarch lineages = ',len(world),' patriarch variants per lineage = ',mu)
			print('')
			print('gen, pop')
		elif g > 0 and g <= 3:
			world = growth(g_rate,world)
			count = mutation_count(world)
			world = mutation(world,mu,count)
			
			if len(world) > max_pop:
				world = famine(world,max_pop)
			
			
				
		elif g > 3 and g < 99:
			
			world = growth(g_rate,world)
			if len(world) > max_pop:
				world = famine(world,max_pop)
			world = death(world,mort)
			if g in bottle_neck_gens:
				man = randint(1,len(world))
				world = G_Khan(world,man,sons)
			count = mutation_count(world) 
			world = mutation(world,mu,count)
			if g in bottle_neck_gens:
				world = death(world,bottle_neck_mortality) #for generations with bottlenecks, the mortality is great
	
			
			
		else:
			world = growth(g_rate,world)
			if len(world) > max_pop:
				world = famine(world,max_pop)
			count = mutation_count(world) 
			world = mutation(world,mu,count)
			
				
		print(g,len(world))
			
			
				
	print('')
	print('patriarch world = ',patriarch_gen_0)
	p_list = []
	for key in patriarch_gen_0:  #get a list of the lowest number patriarch variant in each lineage
		v = min(patriarch_gen_0[key])
		p_list.append(v)
		
	
	#now to get the world's mutation frequencies
	#below are lines to compute the variant frequencies and plot the results

	num_men = len(world)
	if num_men > 1233:
		world = famine(world,1233) 
	num_men = len(world)	 
	print('number of men alive in world = ', num_men)


	variants = 0
	for key in world: #key is the individual man, values are the mutations he carries
		variants += len(world[key])  #counting all the mutations surviving in the world
	var_num = variants/num_men
	print('number of mutations in whole_world = ',variants)
	print('average mutations per man = ',var_num )


	AC_dict_biased = {} #here the keys will be the mutations of a given AC and the value the number of occurences in the population of mutations with that AC
	AC_accumulation_biased = {}
	
	for i in range(1,num_men+1):
		AC_dict_biased[i] = 0	#making AC bins for the number of men in world
		AC_accumulation_biased[i] = 0
	counted_list = []

	mut_list = []
	for key in world:
		val = world[key]#a list of mutations carried by a man (key)
		for e in val:
			mut_list.append(e) #making a list of all mutations in whole_world, many repeat mutations, of course


	extant_lins = 0
	for m in p_list:
		num_m = mut_list.count(m)  #if patriarch variants are absent from the mut_list then the lineage is extinct.
		if num_m > 0:
			extant_lins += 1

	bias_list = []
	b = randint(1,len(world)) #a single man in world is selected
	bias_list = world[b] #these should be all the mutations carried by b, the man who will become the reference
	p_var = min(bias_list)
	print('man chosen to be reference for bias = ',b,' patrarch variant = ',p_var)  #the patriarch variant of the man who will be the reference is the lowest numbered mutation in his list
	for key in patriarch_gen_0:
		if p_var in patriarch_gen_0[key]:
			print('patriarch lineage ',key,' is the biased lineage')
	ct = 0  #to count the number of men in bias lineage, all who will carry p_var
	for key in world:
		vals = world[key]
		if p_var in vals:
			ct += 1 
	print('number of men in bias lineage at generation 100 = ',ct)

	switched = []		
	for m in mut_list:
		AC = 0
		if not m in counted_list:
			counted_list.append(m)
			AC = mut_list.count(m)  #the mutations m are counted from the list of all mutations in world
			if m in bias_list:
				AC = ref_bias(AC,num_men)
				switched.append(m)  #at the end the switched list should be the same as the bias_list
			if AC == 0:
				AC = 1
			AC_dict_biased[AC] += 1
	kt = 0
	for j in range(1,1234):
		kt += AC_dict_biased[j]
		AC_accumulation_biased[j] = kt



	#You already have mut_list, patriarch_gen_0, and world, so men who have any patriarch mutation can be obtained
	patriarch_var_dict = {}
	pat_vars = []
	for key in patriarch_gen_0:
		vars = patriarch_gen_0[key]
		for v in vars:
			pat_vars.append(v) #get a list of the world's patriarch variants
			patriarch_var_dict[v] = 0 #initialize this dictionary for the patriarch variants to be counted in world


		
	for m in mut_list:
		if m in pat_vars:
			patriarch_var_dict[m] += 1
	
	
	print('')
	print('dictionary of patriarch variants and their AC = ',patriarch_var_dict)
	k = 0
	nu_non_zero_keys = 0
	for key in patriarch_var_dict:
		k += 1
		if patriarch_var_dict[key] != 0:
			nu_non_zero_keys += 1
		if key == p_var:
			n_men_bias_lin = patriarch_var_dict[key] #num men in the bias lineage is num of men with p_var
	n_patriarchs_gen100 = nu_non_zero_keys/n_p_vars #number of variants that are not 0 in final patrarch_var_dict divided by the number of variants per patriarch in gen 0
	
	IP = 1233 - n_men_bias_lin
	slope =(AC_accumulation_biased[1200] - AC_accumulation_biased[800])	/ 400
	slope = round(slope,2)
	target = int(IP*slope)
	Delta = int(748-target)
				
	#record_results(gens,num_men,lineage_nums[0],lineage_nums[1],lineage_nums[2],bias_lin_men,AC_bias_start,com_var_ct,len(switched),slope)				
	with open('Y_sim_variable_lineages_Bayes.txt','a') as record:
		
		record.write('\n')
		record.write(str(p))
		record.write('\t')
		record.write(str(lin_num)) #number of patriarchs in gen 0
		record.write('\t')
		
		record.write(str(extant_lins)) #number of extant patriarch lineages at gen 100
		record.write('\t')
		
		record.write(str(n_men_bias_lin))
		record.write('\t')
		
		record.write(str(IP))
		record.write('\t')

		record.write(str(slope))
		record.write('\t')

		record.write(str(target))
		record.write('\t')

		record.write(str(Delta))  #this is Delta, the difference in target from Y-sim vs 1000G data	
		record.write('\n')
	

		
	print('MC = ',MC,' Delta = ',Delta,'p = ',p)






# 
# 		
# 	below is code to plot the number vs AC bin using data from the AC_dict
# 	title = input('What is the plot title ? ')
# 	title = 'Biased AC plot after 100 generations'
# 
# 	to only look at common variants, AC > 5%, which are in AC bin > 0.05*num_men
# 	com_AC_bin = int(0.05*num_men)
# 	print('common AC bin cut off = ',com_AC_bin)
# 
# 
# 		
# 		
# 		
# 
# 	now get the patriarch lineages and their patriarch variants in the world after all generations
# 	mut_dict = {}
# 	mut_list = []
# 	unique_mu_list = []
# 
# 	for key in world:
# 		muts = world[key]
# 		for mu in muts:
# 			if not mu in unique_mu_list:
# 				unique_mu_list.append(mu)
# 			mut_list.append(mu)
# 		
# 		
# 	now get the common variants from the mutation list
# 	com_var_min = .05*len(world) #common variants are those with AC >5%
# 
# 
# 	the following lines plot the results
# 
# 	x = []
# 	y = []
# 	for key in AC_dict_biased:
# 		if key > com_AC_bin: #use this to count only common variants
# 			x.append(key)
# 			val = AC_dict_biased.get(key)
# 			num = key*val
# 			y.append(num)
# 
# 	
# 	print('x = ',x)
# 	print('y = ',y)
# 
# 
# 
# 	plt.plot(x,y,'-')
# 
# 	plt.ylabel('Number of variants in database')
# 
# 	plt.xlabel('AC bin')
# 	plt.title(title)
# 	plt.legend(labels=['Exons','Gene'])
# 
# 	plt.show()
# 
# 
# 	AC_dictionary = AC_dict_biased
# 	variant_accum = {} #dictionary to record the accumulation of variants as AC increases
# 
# 	num_var = 0
# 	for key in AC_dictionary:
# 		num = AC_dictionary[key]
# 		num_var += num
# 		variant_accum[key] = num_var
# 	
# 	print('variant accumulation dictionary = ',variant_accum)
# 
# 	x = []
# 	y = []
# 	for key in variant_accum:
# 		if key > 61:
# 			x.append(key)
# 			y.append(variant_accum[key])
# 
# 
#  
# 	plt.plot(x,y,'-')
# 	plt.xlabel('AC')
# 	plt.ylabel('Total variant positions')
# 	plt.title('Simulated Accumulation of Variants')
# 
# 	plt.show()
# 
# 	now to plot the average accumulation of mutations per Manifest
# 	first get the total accumulations per AC 
# 	total_mu = {}
# 	num_mu = 0
# 	for key in AC_dictionary:
# 		val = AC_dictionary[key]
# 		num_mu += key*val
# 		total_mu[key] = num_mu
# 
# 
# 	mu_per_man = {}
# 
# 	x2 = []
# 	y2 = []
# 	for key in total_mu:
# 		if key > 0:
# 			x2.append(key)
# 			y2.append(total_mu[key]/1233)
# 		
# 	plt.plot(x2,y2,'-')
# 	plt.xlabel('AC')
# 	plt.ylabel('Cumulative average mutations per man')
# 	plt.title('Simulated Accumulation of mutations per man')
# 
# 	plt.show()
# 
# 	now to plot accumulation of average mutations per man against AF
# 	total_mu_frequency = {}
# 	x3 = []
# 	y3 = []
# 	for key in total_mu:
# 		val = total_mu[key]/1233
# 		f_key = key/12.33
# 		total_mu_frequency[f_key] = val
# 	
# 	for key in total_mu_frequency:
# 		x3.append(key)
# 		y3.append(total_mu_frequency[key])	
# 	
# 	plt.plot(x3,y3,'-')
# 	plt.title('Simulated accumulated mutations per man')
# 	plt.xlabel('Allele frequency %')
# 	plt.ylabel('Cumulative mutations per man')
# 	plt.show()
# 
	
	
	










