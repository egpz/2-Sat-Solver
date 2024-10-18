#!/usr/bin/env python3
import random
import csv
import time

 
#########################################
#ALGORITHM
#--------------------
#Funciton to generate random assingments to be used in the flips function
def generate_assignment(num_variables):
    return [random.choice([1, 0]) for _ in range(num_variables)]



#Function to evaluate if the clause is satifiable
def evaluate_clause(clause, assignment):
    for lit in clause:
        if assignment[abs(lit)-1] == (lit > 0):
            return True
    return False


#Function to flip assignments
def flips(Wff, max_flips, p, num_variables):
    
    assignment=generate_assignment(num_variables)

    for _ in range(max_flips):
        
        unsatisfied_clauses= [clause for clause in Wff if not evaluate_clause(clause, assignment)]
        


        if not unsatisfied_clauses:
            return True, assignment
        
        #if random.random() < p:
        random_unsatisfied_clause= random.choice(unsatisfied_clauses)
        random_literal = random.choice(random_unsatisfied_clause)

        var=abs(random_literal) - 1

        assignment[var] = not assignment[var]

        return False, None


#Function to call get the result and assignment
def check(Wff, num_variables, max_flips=1000000000, p=0.5):
    result, assignment=flips(Wff, max_flips, p, num_variables)
    return result, assignment


#------------- -
###############################


#_________________________________
#Funtion to track number of variables and clauses
def num_vars_clas(section):
 
    num_variables=0
    num_clauses=0

    for line in section:
        line=section[0]
        
        if line.startswith('p,cnf'):
            _, _, variable, clauses= line.split(',')
            num_variables = int(variable)
            num_clauses = int(clauses)
            break

    return num_variables, num_clauses

#_______________________




#_______________________
#Do the actions to the section of the cnf
#DO EVERYTHING HERE// CALL FUNCTIONS HERE
def process_section(section, f1, problem_number):

    num_variables, num_clauses= num_vars_clas(section)
    rm_p_section=section[1:]
    
    #list comprehension to split string into individual numbers, convert into integer, and place into sublists
    clean_section=[[int(num) for num in string.split(',')] for string in rm_p_section]
    
    #Find the satifiable assignments by calling function
    start= time.time()#start timer
    result, assignment = check(clean_section, num_variables)
    end= time.time()#end timer
    exec_time=int((end-start)*1e6)#Calculate time to get the time it takes to generate 
    
    if result==True:
        result="S"

    if result==False:
        result="U"
    
    total_literals=2*num_clauses
    max_literals=2
    answer=0

    if assignment is not None:
        sat_assignment= ','.join(map(str, assignment))
        final_assignments=sat_assignment
        f1.write(f'{problem_number},{num_variables},{num_clauses},{max_literals},{total_literals},{result},{answer},{exec_time},{final_assignments}')
        f1.write(f'\n')

    else:
        f1.write(f'{problem_number},{num_variables},{num_clauses},{max_literals},{total_literals},{result},{answer},{exec_time}')
        f1.write(f'\n')

#_______________________
#read in the cnf to a list of lists
def read_cnf_file(filename):
    
    f1=open("resultsFile.csv", 'w')

    with open(filename, 'r') as file:

        current_section = []

        for line in file:
            line = line.strip()

            if line.startswith('c'):
                _, probNum, _, _= line.split(',')
                problem_number=int(probNum)

                #print(problem_number)

            if line.startswith('c') or line.startswith('p'):
                if current_section:
                    process_section(current_section, f1, problem_number)
                    current_section = []

                if line.startswith('p,cnf'):
                    current_section.append(line)
            else:
                current_section.append(line)
            
        if current_section:
            process_section(current_section, f1, problem_number)

    f1.write("2SAT,egpz,100")
    f1.close()
    print("Program complete. Output to resultsFile.csv")

if __name__ == "__main__":
    cnf_file = '2SAT.cnf'
    read_cnf_file(cnf_file)
