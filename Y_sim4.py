#a program to simulate mutation accumulation on a hypothetical population of Y chromosomes
#and to introduce lineage specific parameters of growth, mutation rate and mortality.
#this accomplished by breaking world into 3 subpopulations of different histories.
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from random import randint
from random import seed
from random import choice
from random import gauss
seed()
#inputs for each of 3 populations, representing Shem, Ham and Japheth
rate_s = int(input('what is the pop growth rate for Shem ? ')) #number of males in next generation for every male in current generation.
rate_h = int(input('what is the pop growth rate for Ham ? '))
rate_j = int(input('what is the pop growth rate for Japheth ? '))
mu_s = int(input('what is the mutation rate for S ? '))  #Y chromosome today has 2-3 mutations per generation
mu_h = int(input('what is the mutation rate for H ? ')) 
mu_j = int(input('what is the mutation rate for J ? ')) 
gen = int(input('how many generations ? '))
mort_s = int(input('what is the death rate (percent) for S ? '))
mort_h = int(input('what is the death rate (percent) for H ? '))
mort_j = int(input('what is the death rate (percent) for J ? '))
pop_max_s = int(input('what is the maximum population for S ? ')) #this reflects the carrying capacity
pop_max_h = int(input('what is the maximum population for H ? '))
pop_max_j = int(input('what is the maximum population for J ? '))
print()
print()
print('		These are the parameters you have selected : ')
print()
print('		Population growth rates for S,H,J = ',rate_s,rate_h,rate_j)
print('		Mutation rates are  for S,H,J = ',mu_s,mu_h,mu_j)
print()
print('		Number of generations = ', gen)
print()
print('		Death rates for S,H,J = ',mort_s,mort_h,mort_j)
print('		Max population for S,H,J = ',pop_max_s,pop_max_h,pop_max_j)

print()
print()
Q = input('		Are these parameters correct? (Y/N)')
if Q == 'N' or Q == 'No' or Q == 'no' or Q == 'n':
	print('let\'s start over ')
	rate_s = int(input('what is the pop growth rate for Shem ? ')) #number of males in next generation for every male in current generation.
	rate_h = int(input('what is the pop growth rate for Ham ? '))
	rate_j = int(input('what is the pop growth rate for Japheth ? '))
	mu_s = int(input('what is the mutation rate for S ? '))  #Y chromosome today has 2-3 mutations per generation
	mu_h = int(input('what is the mutation rate for H ? ')) 
	mu_j = int(input('what is the mutation rate for J ? ')) 
	gen = int(input('how many generations ? '))
	mort_s = int(input('what is the death rate (percent) for S ? '))#annual mortalities
	mort_h = int(input('what is the death rate (percent) for H ? '))
	mort_j = int(input('what is the death rate (percent) for J ? '))
	pop_max_s = int(input('what is the maximum population for S ? ')) #this reflects the carrying capacity
	pop_max_h = int(input('what is the maximum population for H ? '))
	pop_max_j = int(input('what is the maximum population for J ? '))
	print()
	print()
	print('		These are the parameters you have selected : ')
	print()
	print('		Population growth rates for S,H,J = ',rate_s,rate_h,rate_j)
	print('		Mutation rates are  for S,H,J = ',mu_s,mu_h,mu_j)
	print()
	print('		Number of generations = ', gen)
	print()
	print('		Death rates for S,H,J = ',mort_s,mort_h,mort_j)
	print('		Max population for S,H,J = ',pop_max_s,pop_max_h,pop_max_j)


	Q = input('Are these parameters correct? (Y/N)')
	if Q == 'N' or Q == 'No' or Q == 'no' or Q == 'n':
		print('Sorry. wrong input. try again later')
		sys.exit()
print('OK the simulation will run for ',gen,' generations')
	

gen_0_s = {1:[1,2,3,4,5,6,7,8,9,10]}
gen_0_h = {1:[11,12,13,14,15,16,17,18,19,20]}
gen_0_j = {1:[21,22,23,24,25,26,27,28,29,30]}
#gen_0_s ={1:[1,2,3]}
#gen_0_h = {1:[4,5,6,7,8,9,10,11,12]}
#gen_0_j = {1:[13,14,15,16,17,18,19,20,21,22,23]} #initial population of 3 men with 3 mutations each, Shem, Ham abd Japheth
#gen_0_s = {1:[1,2,3,4,5,6,7,8,9,10,11,12,13]}
#gen_0_h = {1:[10,11,12,13,14,15,16,17,18]}
#gen_0_j = {1:[19,20,21,22,23,24,25,26,27]}

#these below are based on 1000G data
#gen_0_s =  {1: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200]}
#gen_0_h = {1: [201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328]}
#gen_0_j = {1: [330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342,343]}

#a more realistic 1000G picture bases on the gen_0 dictionaries below since Shem picks up a lot of variants due to loss of liniages
#gen_0_s =  {1: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]}
#gen_0_h = {1: [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174]}
#gen_0_j = {1: [176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200]}

print('the initial population, representing 3 sons of Noah = ', gen_0_s,'   ',gen_0_h,'   ',gen_0_j)


def growth(rate,world):
	#rate is the population growth rate, the number of males born per man in the population per year 
	#world is a dictionary of lists, representing the world of men (keys) with their Y mutations numbered in a list (values).
		
	j=1
	new_pop = {} #the next generation
	for key in world:    #new men are added and consecutively numbered to make up the next generation
		for i in range(j,rate+j):
			new_pop[i] = world[key] #for each new male, his fathers mutations are assigned
		j += rate 
			
	return new_pop  ##the next generation replaces the old, who dies. So 'world' is replaced with 'new_pop' which is larger by the rate of growth
#these new_pop males have their father's mutations but no new mutations yet assigned		

def mutation_count(world): #to keep track of the numbered mutations and continue the numbered sequence.
	large = max(world) #the number of keys in world
	count = world[large][-1] #since mutations are numbered sequentially as are the keys (males).
	return count		


def mutation(world,mu,count): #assigns each person in the new world 'mu' additional mutations 
	#mu = mutation rate
	#count is the unique mutation count from the function 'mutation_count'
	mu_ct = count
	mu_vars = [1,1,1,1,2,3,3,4,4,4,5,5,5,5]
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
		kill = choice(list) #random selection of a man from the list
		kill_list.append(kill)
		list.remove(kill)

		
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
		

	
	
	
	
	
	
	
	
	
	
			
#the following lines execute the program and graph the results.
world_s = gen_0_s  #this is Shem, Ham, and Japheth with their Y mutations received from Noah.
world_h = gen_0_h  #the order of s,h,j is important for consecutive mutation numbering.
world_j = gen_0_j

print('gen		S	H	J')

#generation 1 growth according to Genesis 10 to give Noah the listed 16 grandchildren. 
world_s = growth(5,world_s)
count = mutation_count(world_j) #initial mutations must end with Japheth's world	
world_s = mutation(world_s,3,count) #mutations are added to the new men's list of inherited mutations.
pop_s = len(world_s)
	
world_h = growth(4, world_h)
count = mutation_count(world_s) #initial mutations must end with Japheth's world, then Shem's world	
world_h = mutation(world_h,5,count) #mutations are added to the new men's list of inherited mutations.
pop_h = len(world_h)
	
world_j = growth(7,world_j)
count = mutation_count(world_h) #mutations are numbered sequentially by taking the last mutation from the last world mutated.	
world_j = mutation(world_j,4,count) #mutations are added to the new men's list of inherited mutations.
pop_j = len(world_j)

g = 1	
print(g,'		',pop_s,'	',pop_h,'	',pop_j) 

khan_s = []
khan_h = []
khan_j = []	
#now, after the initial generation, the loop to run through the specified number of generations, 'gen'.	 
#for Shem's descendants...Shem must go first to keep count of mutations
for g in range(2,gen +1):
	m = randint(65,85)  #to determine the bottleneck mortality
	#m = 80
	sons = randint(50,150)
	#sons = 100
	
#SHEM
	#Shem's bottlenecks and GKhan events
	sb_list = [4,7,9,10,12,22,26,31,36,41,46,51,56,61,65,71,76,81,85,91,96,101,105,111,116,121,126,131,136,141,145,151,156,161,166,171]#list of generations with bottlenecks
#	sb_list = [4,6,9,11,13,22]
#	sb_list = [104,106,109,11,113,122]
#	sb_list = [4,7,9,10,12,22,32,42,52,62,72,82,92,102,112,122,132,142,152,162,172]
	sgk_list = sb_list
#	sgk_list = [5,8,10,12,32,52,72,92,112,132,152,172] #generations with GKhan events	

	if g <4:	
		world_s = growth(5,world_s)	
		#this represents high growth rate before Babel, based on Noah's 16 grandchildren
		#print('pre-Babel pop = ',len(new_pop))

	else:
		gro_list = [2,3,4,5,6] 
		gro= choice(gro_list)
		world_s = growth(gro,world_s)
		#print('length of new population = ',len(new_pop))

	if g in sgk_list:
		khan_s.append(g)
		world_s = G_Khan(world_s,7,sons)  #one man reproduces many sons. Both the man and the number of sons are designated here.

			
	count = mutation_count(world_j) #initial mutations must end with Japheth's world	
	world_s = mutation(world_s,mu_s,count) #mutations are added to the new men's list of inherited mutations.
	
	
	if len(world_s) > pop_max_s:
		famine_survivors = famine(world_s,pop_max_s)
		world_s = famine_survivors

	if g in sb_list:
		#m = randint(65,85)
		world_s = death(world_s,m) #bottlenecks
				  

	if g > 4 and not g in sb_list:
		if len(world_s)	> 100:
			world_s = death(world_s,mort_s)
			
	pop_s = len(world_s)


		
#HAM	
#for Ham's descendants...Ham must go after Shem to keep count of mutations
#	hb_list = [4,7,9,10,12,22,26,31,36,41,46,51,56,61,65,71,76,81,85,91,96,101,105,111,116,121,126,131,136,141,145,151,156,161,166,171]#list of generations with bottlenecks
#	hb_list = [4,6,9,10,12,22,32,42,52,62,72,82,92,102,112,122,132,142,152,162,172]
	hb_list = sb_list

	hgk_list = hb_list
#	hgk_list = [5,8,10,12,32,52,72,92,112,132,152,172]
	
	if g < 4:
		world_h = growth(4,world_h) #this represents high growth rate before Babel, based on Noah's 16 grandchildren
		#print('pre-Babel pop = ',len(new_pop))
			
	else:
		gro_list = [2,3,4,5,6] 
		gro= choice(gro_list)	 
		world_h = growth(gro,world_h)		

	if g in hgk_list:
		khan_h.append(g)
		world_h = G_Khan(world_h,4,sons)  #one man reproduces many sons. Since it doesn't matter which man, an arbitrary male number is chosen
			
	count = mutation_count(world_s)	
	world_h = mutation(world_h,mu_h,count)
	
	if len(world_h) > pop_max_h:
		famine_survivors = famine(world_h,pop_max_h)
		world_h = famine_survivors

	if g in hb_list:
		#m = randint(60,80)
		world_h = death(world_h,m) #bottleneck death rate % is here set.  



	if g > 4 and not g in hb_list:
		if len(world_h) > 100:	
			world_h = death(world_h,mort_h)
			
	pop_h = len(world_h)



#JAPHETH	
#for Japheth's descendants...must come after Ham to keep track of mutation count.
#	jb_list = [4,7,9,10,12,22,26,31,36,41,46,51,56,61,65,71,76,81,85,91,96,101,105,111,116,121,126,131,136,141,145,151,156,161,166,171]#list of generations with bottlenecks
#	jb_list = [4,6,9,10,12,22,32,42,52,62,72,82,92,102,112,122,132,142,152,162,172]
	jb_list = sb_list
	jgk_list = jb_list
#	jgk_list = [5,8,10,12,32,52,72,92,112,132,152,172]

	if g < 4:
		world_j = growth(7,world_j) #this represents high growth rate before Babel, based on Noah's 16 grandchildren
		#print('pre-Babel pop = ',len(new_pop))
			
	else:	
		gro_list = [2,3,4,5,6] 
		gro= choice(gro_list)
		world_j = growth(gro,world_j)
		#print('length of new population = ',len(new_pop))

	if g in jgk_list:
		khan_j.append(g)
		world_j = G_Khan(world_j,16,sons)  #one man reproduces many sons

		
	count = mutation_count(world_h)	
	world_j = mutation(world_j,mu_j,count)
	
	if len(world_j) > pop_max_j:
		famine_survivors = famine(world_j,pop_max_j)
		world_j = famine_survivors

	if g in jb_list:
		#m = randint(60,80)
		world_j = death(world_j,m)		


	if g > 4 and not g in jb_list:
		if len(world_j) > 100:	
			world_j = death(world_j,mort_j)
			
	pop_j = len(world_j)


	
	
	print(g,'		',pop_s,'	',pop_h,'	',pop_j)
	
print('')
print('')

print('khan events in S = ',khan_s)
print('khan events in H = ',khan_h)
print('khan events in J = ',khan_j)
#print('generation ',gen,' = ',world)  #there will be 4 generations from S,H,J, and 5 generations from Noah, to Babel.

#to get population specific mutation accumulations:
n_mu_s = 0
for key in world_s:
	n = len(world_s[key])
	n_mu_s += n
men = len(world_s)
print('mutations per man in S = ',n_mu_s/men)

n_mu_h = 0
for key in world_h:
	n = len(world_h[key])
	n_mu_h += n
men = len(world_h)
print('mutations per man in H = ',n_mu_h/men)

n_mu_j = 0
for key in world_j:
	n = len(world_j[key])
	n_mu_j += n
men = len(world_j)
print('mutations per man in J = ',n_mu_j/men)




#now the three worlds need to be merged to allow world-wide variant ACs to be calculated...
#but first the keys need to be renumbered to make each man have his unique key number...
k_num_s = len(world_s)
k_num_h = len(world_h)
k_num_j = len(world_j)
new_k_num = k_num_s + k_num_h + k_num_j

whole_world = {}
num_s = 0
for key in world_s:
	whole_world[key] = world_s[key]
	num_s += 1
	
num_h = 0	
for key in world_h: #keys have been numbered from 1, but need to be numbered from where world_s left off.
	num = num_s + key
	whole_world[num] = world_h[key]
	num_h += 1


num_j = 0	
for key in world_j:
	num = num_s + num_h + key
	whole_world[num] = world_j[key]
	num_j += 1

#print(whole_world) #values are variants; no variant is found in all keys, unlike the case with the subpopulations, S,H,J.


	

#below are lines to compute the variant frequencies and plot the results

num_men = len(whole_world)  
print('number of men alive in world = ', num_men,' = ',new_k_num)


variants = 0
for key in whole_world:
	variants += len(whole_world[key])  #counting all the mutations surviving in the world
var_num = variants/num_men
print('number of mutations in whole_world = ',variants)
print('average mutations per man = ',var_num )


AC_dict = {} #here the keys will be the mutations and the value the number of occurences in the population for that key
AC_minor = int(num_men/2) #the cut off AC for looking only at minor variant bins

for i in range(1,AC_minor+1): #assigns 0 to each AC bin for 1 to AC_minor.
	AC_dict[i] = 0 #now there is a key for every minor AC bin, all set to 0.
	
counted_list = []

mut_list = []
for key in whole_world:
	val = whole_world[key]
	for e in val:
		mut_list.append(e) #making a list of all mutations in whole_world
#print(mut_list)

for m in mut_list:
	if not m in counted_list:
		counted_list.append(m)
		AC = mut_list.count(m) #this will count the number of times mutation m is in the mut_list.
				
		if AC > AC_minor:
			AC = num_men - AC  #folding over to look only at minor AC:
# 		if AC <= 0:
# 			AC = 1
		AC_dict[AC] += 1
	AC = 0

	
#print('AC_dictionary = ', AC_dict)
		

#below is code to plot the number vs AC bin using data from the AC_dict
title = input('What is the plot title ? ')

#to only look at common variants, AC > 5%, which are in AC bin > 0.05*num_men
com_AC_bin = int(0.05*num_men)
print('common AC bin cut off = ',com_AC_bin)



x = []
y = []
for key in AC_dict:
	if key > com_AC_bin: #use this to count only common variants
		x.append(key)
		val = AC_dict.get(key)
		y.append(val)

	
#print('x = ',x)
#print('y = ',y)



plt.plot(x,y,'-')

plt.ylabel('Number of variants in database')

plt.xlabel('AC bin')
plt.title(title)
#plt.legend(labels=['Exons','Gene'])

plt.show()




	


	
	
	
	
	
	
	
	
	