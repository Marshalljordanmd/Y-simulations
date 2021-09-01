#from y_MC_3_pop_random_walk.py on June 28,2021
#for Bayesian Data Analysis
#Plan: prior will be a random probability drawn from uniform distribution, and p will determine the fraction of the maximum pop for the lineage of bias
#then the other 2 lineages will be divided by the same p to fractionate the remainder.
#the posterior will be the p values that cause DElta to be in the range (-10,10)


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
import pickle
import math

# if os.path.exists('Y_sim_Bayes.txt'):
# 	os.remove('Y_sim_Bayes.txt')
# 
# 
# with open('Y_sim_Bayes.txt','a') as record:
# 	record.write('#A record of Y_sim_3_pop_Bayes.py Monte Carlo runs')	
# 	record.write('\n')
# 	record.write('p')
# 	record.write('\t')		
# 	record.write('L1')
# 	record.write('\t')		
# 	record.write('L2')
# 	record.write('\t')		
# 	record.write('L3')
# 	record.write('\t')		
# 	record.write('Bias L')
# 	record.write('\t')
# 	record.write('B Vars')
# 	record.write('\t')
# 	record.write('IP')
# 	record.write('\t')			
# 	record.write('Slope')
# 	record.write('\t')
# 	record.write('Target')
# 	record.write('\t')
# 	record.write('Delta')
# 	record.write('\n')





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
	if kill_num > 0:
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


def ref_bias(AC,num_men): #to bias the final AC by changing the reference to alternate and alt to ref
	#if AC > 6:
	AC = num_men - AC  #variants assumed to be bi-allelic, so this line switches the ref with the alt allele
	return(AC)




def maxpops(p):
#to generate the maximum pops for S, H, J based on a single 'p' randomly drawn from uniform Distribution
	pop_max_s = int(p*1233)
	remainder = 1233 - pop_max_s
	pr = np.random.normal(0.3,0.04)
	pop_max_h = int(pr*remainder) #the remainder is then randomly divided for H and J
	pop_max_j = remainder - pop_max_h
	pops = [pop_max_s,pop_max_h,pop_max_j]
	return(pops)



	




# mu_s = 3 
# mu_h = 4  
# mu_j = 5  

mort_s = 15 
mort_h = 20 
mort_j = 15 
pop_max_s = 500 #may adjust settings for MC
pop_max_h = 500 
pop_max_j = 500
print()

gen_0_s = {1:[1,2,3]}
gen_0_h = {1:[4,5,6]}
gen_0_j = {1:[7,8,9]}

patriarch_gen_0 = {1:[1,2,3],2:[4,5,6],3:[7,8,9]}
 

gen = 100 #number of generations per MC run

c = 25  #c=25 is the ideal setting which gives Delta mean = 1
prior_list = []
posterior_list = []
delta_list = []

for MC in range(900):
		
	print('')
	print('')
	p = np.random.normal(.3,.04) #adjusted to be a more informative prior
	p = round(p,4) #to have only 4 decimal places
	print('random probability parameter = ',p)
	prior_list.append(p)
	pops = maxpops(p) #gives a list of 3 max pops for the subpopulations S,H,J
	final_s = pops[0]
	final_h = pops[1]
	final_j = pops[2]
	
#the following lines execute the program and graph the results.
	world_s = gen_0_s  #this is Shem, Ham, and Japheth with their Y mutations received from Noah.
	world_h = gen_0_h  #the order of s,h,j is important for consecutive mutation numbering.
	world_j = gen_0_j
	

	print('gen	c	S	H	J')

	#generation 1 growth according to Genesis 10 to give Noah the listed 16 grandchildren. 
	world_s = growth(5,world_s)
	count = mutation_count(world_j) #initial mutations must end with Japheth's world	
	world_s = mutation(world_s,5,count) #mutations are added to the new men's list of inherited mutations.
	pop_s = len(world_s)
	
	world_h = growth(4, world_h)
	count = mutation_count(world_s) #initial mutations must end with Japheth's world, then Shem's world	
	world_h = mutation(world_h,6,count) #mutations are added to the new men's list of inherited mutations.
	pop_h = len(world_h)
	
	world_j = growth(7,world_j)
	count = mutation_count(world_h) #mutations are numbered sequentially by taking the last mutation from the last world mutated.	
	world_j = mutation(world_j,7,count) #mutations are added to the new men's list of inherited mutations.
	pop_j = len(world_j)

	g = 1	
	print(g,'		',pop_s,'	',pop_h,'	',pop_j) 
	
	
	bottle_neck_mortality = randint(60,80)
	bottlenecks = [4,6,7,10,15,18,26,28,30,33,35,37,40,42,45,51,55,60,65,70,75,80,85,90,93,101,105,115,120,125,130,135,140,145,151,155,160,165,170,175]
	#c = 30 #patriarchal drive coefficient (after Carter 2019)
	#sons = randint(50,75)
	sons = 50
	
	
	for g in range(2,gen +1):
	
		mu_s = mu_rate(g,c) #set all the mutation rates the same
		mu_j = mu_s
		mu_h = mu_s
#SHEM
#for Shem's descendants...Shem must go first to keep count of mutations		
		sb_list = bottlenecks		#list of generations with bottlenecks
		sgk_list = sb_list	
		
		if g <4:	
			world_s = growth(5,world_s)	
			#this represents high growth rate before Babel, based on Noah's 16 grandchildren
		
		
		else:	
			if not g in sb_list:
				gro_list = [3,4,5,6,7] 
				gro= choice(gro_list)
				world_s = growth(gro,world_s)
				#print('length of new population = ',len(new_pop))

			
		count = mutation_count(world_j) #initial mutations must end with Japheth's world
			
		world_s = mutation(world_s,mu_s,count) #mutations are added to the new men's list of inherited mutations.
	
		if len(world_s) > pop_max_s:
			famine_survivors = famine(world_s,pop_max_s)
			world_s = famine_survivors

		if g < gen - 3:
			if g in sb_list:
				world_s = death(world_s,bottle_neck_mortality)
			
 
			if g in sgk_list:
				man = randint(1,50)	
				world_s = G_Khan(world_s,man,sons)  #one man reproduces many sons. Both the man and the number of sons are designated here.
						
			 
		if len(world_s)	> 100:
			world_s = death(world_s,mort_s)
		
		
		if g == gen:
			world_s = growth(4,world_s)				
			if len(world_s) > final_s:
				famine_survivors = famine(world_s,final_s)
				world_s = famine_survivors
	
		pop_s = len(world_s)


		
#HAM	
	#for Ham's descendants...Ham must go after Shem to keep count of mutations
		hb_list = bottlenecks		#list of generations with bottlenecks
		hgk_list = sb_list	
		
		if g <4:	
			world_h = growth(5,world_h)	
			#this represents high growth rate before Babel, based on Noah's 16 grandchildren
		
		
		else:	
			if not g in hb_list:
				gro_list = [2,3,4,5,6] 
				gro= choice(gro_list)
				world_h = growth(gro,world_h)
				#print('length of new population = ',len(new_pop))

			
		count = mutation_count(world_s) #initial mutations must begin with Seth's and  end with Japheth's world	
		world_h = mutation(world_h,mu_h,count) #mutations are added to the new men's list of inherited mutations.
	
		if len(world_h) > pop_max_h:
			famine_survivors = famine(world_h,pop_max_h)
			world_h = famine_survivors

		if g < gen - 3:
			if g in hb_list:
				world_h = death(world_h,bottle_neck_mortality)
			
 
			if g in hgk_list:
				man = randint(10,60)	
				world_h = G_Khan(world_h,man,sons)  #one man reproduces many sons. Both the man and the number of sons are designated here.
						
			 
		if len(world_h)	> 100:
			world_h = death(world_h,mort_h)
		
		
		if g == gen:
			world_h = growth(4,world_h)
			if len(world_h) > final_h:
				famine_survivors = famine(world_h,final_h)
				world_h = famine_survivors
		
		pop_h = len(world_h)



#JAPHETH
	
	#for Japheth's descendants...must come after Ham to keep track of mutation count.
		jb_list = bottlenecks		#list of generations with bottlenecks
		jgk_list = sb_list	
		
		if g <4:	
			world_j = growth(5,world_j)	
			#this represents high growth rate before Babel, based on Noah's 16 grandchildren
		
		
		else:	
			if not g in jb_list:
				gro_list = [2,3,4,5,6] 
				gro= choice(gro_list)
				world_j = growth(gro,world_j)
				#print('length of new population = ',len(new_pop))

			
		count = mutation_count(world_h) #initial mutations must end with Japheth's world	
		world_j = mutation(world_j,mu_j,count) #mutations are added to the new men's list of inherited mutations.
	
		if len(world_j) > pop_max_j:
			famine_survivors = famine(world_j,pop_max_j)
			world_j = famine_survivors

		if g < gen - 3:
			if g in jb_list:
				world_j = death(world_j,bottle_neck_mortality)
			
 
			if g in jgk_list:
				man = randint(5,25)	
				world_j = G_Khan(world_j,7,sons)  #one man reproduces many sons. Both the man and the number of sons are designated here.
						
			 
		if len(world_j)	> 100:
			world_j = death(world_j,mort_j)

		if g == gen:
			world_j = growth(4,world_j)			
			if len(world_j) > final_j:
				famine_survivors = famine(world_j,final_j)
				world_j = famine_survivors


		pop_j = len(world_j)

	
		print(g,'	',c,'	',pop_s,'	',pop_h,'	',pop_j)











	print('')
	print('Final world: S,H,J ',len(world_s),len(world_h),len(world_j))
	
	
	
	world = len(world_s) + len(world_h) + len(world_j)	
	print('generation ',gen,' = ',world)  #there will be 4 generations from S,H,J, and 5 generations from Noah, to Babel.

#	to get population specific mutation accumulations:
	n_mu_s = 0
	for key in world_s:
		n = len(world_s[key])
		n_mu_s += n
	men = len(world_s)
	print('mutations per man in S = ',n_mu_s/men)
	print('men in world of S = ', men)
	print('mutations in world of S = ',n_mu_s)
	
	n_mu_h = 0
	for key in world_h:
		n = len(world_h[key])
		n_mu_h += n
	men = len(world_h)
	print('mutations per man in H = ',n_mu_h/men)
	print('men in world of H = ', men)
	print('mutations in world of H = ',n_mu_h)
	
	n_mu_j = 0
	for key in world_j:
		n = len(world_j[key])
		n_mu_j += n
	men = len(world_j)
	print('mutations per man in J = ',n_mu_j/men)
	print('men in world of J = ', men)
	print('mutations in world of J = ',n_mu_j)
	


	#next get a list of variants to bias when making the bias world from world
	bias_list = world_s[1] #the first man's list of variants
	

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
	if num_men > 1233:
		whole_world = famine(whole_world,1233)  #even though the man in Shem chosen for bias variants may have died in this famine, his common mutations are carried by others in Shem
	num_men = len(whole_world)	

	world = whole_world

	#now to get the world's mutation frequencies
	variants = 0
	com_vars = 0
	for key in world: #key is the individual man, values are the mutations he carries
		variants += len(world[key])  #counting all the mutations surviving in the world
	var_num = variants/num_men
	#print('number of mutations in whole_world = ',variants)
	#print('average mutations per man = ',var_num )


	#now initialize 2 dictionaries, one for the unbiased and one for the biased data
	AC_dict = {} #here the keys will be the AC of the mutations and the value the number of occurences in the population of mutations with that AC
	AC_dict_biased = {} #this will be the world with biased reference
	
	for i in range(1,num_men+1):
		AC_dict[i] = 0	#making AC bins for the number of men in world
		AC_dict_biased[i] = 0

	counted_list = []
	mut_list = []
	for key in world:
		val = world[key]#a list of mutations carried by a man (key)
		for e in val:
			mut_list.append(e) #making a list of all mutations in whole_world, many repeat mutations, of course

	
	seg_sites = set(mut_list)
	print('')
	print('number of total mutations, extinct and extant, is ',max(seg_sites))
	print('maximum counted mutations =',mutation_count(world)) #should give the maximum mutation number since all mutations are sequentially numbered
	print('')
	num_seg_sites = len(seg_sites) #the total number of mutations in the world
	
	

	

	bias_lin_men = mut_list.count(1)  #the number of men in the biased lineage, should = men who have mutation 1, first mutation in Shem
	lineage_pops = []
	for key in patriarch_gen_0:
		patriarch_vars = patriarch_gen_0[key]
		pv = min(patriarch_vars)#taking the lowest numbered patriarch variant as the one to use
		if not pv in mut_list:
			lineage_pops.append(0) #if a patriarch variant is not in the mut_list, that lineage went extinct
		for m in mut_list:
			if m == pv:
				pAC = mut_list.count(m)
				lineage_pops.append(pAC) #add to the list the number of men in the pop who carry the patriarch variant
				break
			
# 	lineage_nums = sorted(lineage_pops)
# 	lineage_nums.reverse() #to list the lineage pops from high to low
	lineage_nums = lineage_pops
	
	AC_bias_start = sum(lineage_nums) - bias_lin_men  #biased variants start at the summed numbers of the non-bias lineages, the inflection point on the accumulation plots
	
	switched = []
	biased_AC_list = []	
	biased_AC_zero = []	
	for m in mut_list:
		AC = 0
		if not m in counted_list:
			counted_list.append(m)
			AC = mut_list.count(m)  #the mvariants m are counted from the list of all variants in world to get the AC for the variant m
			AC_dict[AC] += 1
			if m in bias_list: #for biased positions the two dictionaries are handled differently below
				if m == 0:
					print('m = 00000000000000000000') #this should never happen !
				new_AC = ref_bias(AC,num_men)#the AC will be changed by the bias and added to the AC_dict_biased dictionary
				if new_AC == 0:
					new_AC = 1 #casting the error into singleton bin effectively ignores it.
					biased_AC_zero.append(new_AC)
				AC_dict_biased[new_AC] += 1
				biased_AC_list.append(new_AC) # a list of AC for all the variants that are biased
				
				switched.append(m)  #at the end the switched list should be the same as the bias_list
			else:
				AC_dict_biased[AC] += 1 #these AC are the same as in the AC_dict, so not biased
	
	inflection_pt = min(biased_AC_list) #compare to AC_biased start and they should agree
	print('number of biased variants with AC = 0 converted to AC = 1233 is ',len(biased_AC_zero))
	if inflection_pt != AC_bias_start:
		print('PROBLEM : inflection point is not determined')
		print('AC_bias_start = ',AC_bias_start,'inflection point = ',inflection_pt)
	com_var_ct = 0
	for key in AC_dict:
		if key > 60:
			com_var_ct += AC_dict[key] #variants in each AC bin are added to get the total common variant count
	
	variant_accum = {} #dictionary to record the accumulation of variants as AC increases
	variant_accum_bias = {}
		
	num_var = 0
	num_var_bias = 0
	for i in range(1,num_men+1):
		num = AC_dict[i]
		num_var += num
		variant_accum[i] = num_var  #summing the number of variants going from low to high AC
		num_bias = AC_dict_biased[i]
		num_var_bias += num_bias
		variant_accum_bias[i] = num_var_bias

	slope = (variant_accum_bias[1200] - variant_accum_bias[800])/400
	target = AC_bias_start*slope
	#target = round(target,2)
	target = int(target)  #lopping off the decimals, leaving only the digits above 0, so it is not rounding
	Delta = 748-target		
	
	delta_list.append(Delta)
	
	
					
	#record_results(gens,num_men,lineage_nums[0],lineage_nums[1],lineage_nums[2],bias_lin_men,AC_bias_start,com_var_ct,len(switched),slope)				
	with open('Y_sim_Bayes.txt','a') as record:
		
		record.write('\n')
		record.write(str(p))
		record.write('\t')
		record.write(str(lineage_nums[0]))
		record.write('\t')		
		record.write(str(lineage_nums[1]))
		record.write('\t')		
		record.write(str(lineage_nums[2]))
		record.write('\t')		
		record.write(str(bias_lin_men))
		record.write('\t')
		record.write(str(len(switched)))
		record.write('\t')		
		record.write(str(AC_bias_start))
		record.write('\t')
		record.write(str(slope))
		record.write('\t')
		record.write(str(target))
		record.write('\t')
		record.write(str(Delta))  #this is Delta, the difference in target from Y-sim vs 1000G data	
		record.write('\n')
	

		
	print('MC = ',MC,' Delta = ',Delta,'p = ',p)
	


for el in range(len(prior_list)):
	if delta_list[el] >= -100 and delta_list[el] <=100:
		posterior_list.append(prior_list[el])  #a list of the probabilities from prior_list where Delta in range (10,10), the data filtering step



	
print('')
print('length of prior list of p = ',len(prior_list))
print('length of posterior list of p = ',len(posterior_list))

p_hat = np.mean(posterior_list)
print('')
print('mean posterior p list = ',p_hat)
print('SD of posterior p list = ',np.std(posterior_list))
print('')
print('calculation of the subpops based on mean p :')

print('S pop max = ',int(p_hat*1233),' This is the mean bias lineage size')
remainder = 1233 - int(p_hat*1233)
print('H pop max = ',int(p_hat*remainder))
print('J pop max = ',remainder - int(p_hat*remainder))

plt.hist(posterior_list)
plt.show()











