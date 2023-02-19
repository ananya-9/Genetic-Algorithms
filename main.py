import numpy as np
import client as server
import random

key = 'L7gzAslLfqoRYngJG9EKl3ACAE28k3OgezoLaUDeEwGl0UclO7'
pop_size = 60
iter = 5
mutate_range=0.2
prob_mut_cross = 0.7
MATING_POOL_SIZE = 20
to_write_file = "generation_39.txt"
train_error = 1.5

def mutateall(temp, mutate_range):
	vector = np.copy(temp)
	for i in range(len(vector)):
		fact=random.uniform(-mutate_range, mutate_range)
		vector[i] = np.random.choice([vector[i]*(fact+1), vector[i]], p=[prob_mut_cross,1-prob_mut_cross])
		if(vector[i]<-10) :
			vector[i]=-10
		elif(vector[i]>10) : 
			vector[i]=10
	return vector

def crossover(parent1, parent2):
	# child1 = np.empty(11)
	# child2 = np.empty(11)
	
	# u = random.random()
	# n_c = 3
	
	# if (u < 0.5):
	#  	beta = (2 * u)**((n_c + 1)**-1)
	# else:
	# 	beta = ((2*(1-u))**-1)**((n_c + 1)**-1)
		
	# parent1 = np.array(parent1)
	# parent2 = np.array(parent2)
	# child1 = 0.5*((1 + beta) * parent1 + (1 - beta) * parent2)
	# child2 = 0.5*((1 - beta) * parent1 + (1 + beta) * parent2)
	
	# return child1, child2
	a = random.randint(0,9)
	b = random.randint(a+1,10)

	child1 = []*11
	child2 = []*11

	for i in range(a+1):
		child1.append(parent1[i])
		child2.append(parent2[i])
	for i in range(a+1,b+1):
	  	child1.append(parent2[i])
	  	child2.append(parent1[i])
	for i in range(b+1,11):
	 	child1.append(parent1[i])
	 	child2.append(parent2[i])

	return child1, child2

def main():

	global mutate_range
	global train_error
	global prob_mut_cross

	population = [[]*11]*pop_size
	parenterrors1 = [(0,0)]*(pop_size+5)
	parenterrors2 = [(0,0)]*(pop_size+5)
	parenterrors = [(10**20,0)]*(pop_size+5)

	vector_og = [0.0, -2.5774265807662704e-14, -1.5632263887936168e-13, 1.1976290255247071e-11, -2.93244391576615e-10, -8.893516137831612e-16, 1.7567397634342773e-17, 9.490495598051973e-06, -1.3575054368166263e-06, -2.044882274041745e-09, 5.068540350570879e-10]


	soln =np.copy(vector_og)
	err = server.get_errors(key, vector_og)
	#err = (random.randint(10**12, 10**14),random.randint(10**12, 10**14))

	file1 = open("temp.txt",'w')

	min_err = err[0]+train_error*err[1]
	gen_min = 0

	file1.write("Generation1\n\n")

	file1.write("Initial population\n\n")

	mutate_range = 0.95
	
	for i in range(pop_size):
		temp = np.copy(vector_og)
		population[i] = np.copy(mutateall(temp, mutate_range))
		file1.write(str(population[i])+"\n\n")

	for k in range(iter):
		mutate_range = random.random()
		if(k==0 or k==1):
			train_error = 1.5
		elif(k==2 or k==3):
			train_error = 1
		elif(k==4):
		 	train_error = 1

		if(k==1 or k==3):
			prob_mut_cross += 0.02

		for j in range(pop_size):
			temp = population[j].tolist()
			err = server.get_errors(key, temp)
			#err = (random.randint(10**12, 10**14),random.randint(10**12, 10**14)) 
	
			parenterrors1[j] = (err[0],temp)
			parenterrors2[j] = (err[1],temp)
			parenterrors[j] = (err[0]+train_error*err[1],temp)

			print(parenterrors[j])

			if min_err > parenterrors[j][0]:
				min_err = parenterrors[j][0]
				soln = np.copy(parenterrors[j][1])
				gen_min = k+1
				
			file1.write(str(population[j])+"\n\n")

		parenterrors.sort(key = lambda x: x[0])

		if(k!=0):
			new_pop = parenterrors + parent_population #initialising new population for this iteration
			new_pop.sort(key = lambda x: x[0])
			arr = new_pop[:pop_size]
			new_pop = arr
			#print(new_pop)
		else:
			new_pop = parenterrors

		file1.write("Initial population\n\n")
		for p in new_pop:
			file1.write(str(p[1])+"\n\n")

		parenterrors = new_pop

		mating_pool = parenterrors[:MATING_POOL_SIZE]
		file1.write("After Selection\n\n")
		for i in range(MATING_POOL_SIZE):
			file1.write(str(parenterrors[i][1])+"\n\n")

		parent_population = parenterrors
		
		population.clear()
		population = [[]*11]*pop_size
		after_mutation = [[]*11]*pop_size
		file1.write("After crossover\n\n")
		
		for p in range(0, pop_size, 2):

			p1 = random.randint(0, MATING_POOL_SIZE-1)
			p2 = random.randint(0, MATING_POOL_SIZE-1)
			
			while(p2==p1):
				p2 = random.randint(0, MATING_POOL_SIZE-1)
			
			parent1 = parenterrors[p1][1]
			parent2 = parenterrors[p2][1]

			# file1.write(parent1)
			# file1.write(parent2)

			child1, child2 = crossover(parent1, parent2)
			file1.write(str(child1)+"\n\n")
			file1.write(str(child2)+"\n\n")
			population[p] = np.copy(mutateall(child1,mutate_range))
			population[p+1] = np.copy(mutateall(child2,mutate_range))

		file1.write("After mutation\n\n")
		for j in range(pop_size):
			file1.write(str(population[j])+"\n\n")
		if k!=iter-1:
			file1.write("----------------------------\n\n")
			file1.write("Generation"+str(k+2)+"\n\n")
			
	file1.close()
	strin = "Generation"+str(gen_min)
	#copying into actual file
	with open('temp.txt') as infile, open(to_write_file, 'w') as outfile:
		for line in infile:
			if line.strip() == strin:
				break
			else:
				outfile.write(line+"\n\n")
	
	realsoln=soln.tolist()
	print("final min_err and soln")
	print(realsoln)
	
	print(min_err)
	server.submit(key,realsoln)
	outfile = open(to_write_file, 'a')
	outfile.write("Submitted soln\n\n")
	outfile.write(str(realsoln)+"\n\n")
	outfile.close()
	infile.close()
	print("submitted soln")

main()
