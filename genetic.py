"""
   Genetic.py
   Code for CS 361: Evolutionary Computing and Artificial Life Final Project
   Authors:  Nicki Polyakov, Barr Iserloth, and Carolyn Ryan
   Majority of code base taken from open github repository found at https://github.com/groger/crossword-solver

   executable: python genetic.py <mask_size>.mask <dictionary>.txt
   Current version successful on mask size small and extrasmall

   """


# -*- coding: utf-8 -*-
import sys, os, math, string, random
from time import time
from individual import Individual

letterValues = {'A':1, 'B':3, 'C':3, 'D':2, 'E':1, 'F':4, 'G':2, 'H':4, 'I':1, 'J':8, 'K':5, 'L':1, 'M':3, 'N':1, 'O':1, 'P':3, 'Q':10, 'R':1, 'S':1, 'T':1, 'U':1, 'V':4, 'W':4, 'X':8, 'Y':4, 'Z':10}

def readSettings():
    settings = open("settings.txt", "r")

    global MINLEN
    MINLEN = int(settings.readline().split("=")[1])

    global mutation_rate
    mutation_rate = float(settings.readline().split("=")[1])

    global crossover_rate
    crossover_rate = float(settings.readline().split("=")[1])

    global pop_size
    pop_size = int(settings.readline().split("=")[1])

    global max_gens
    max_gens = int(settings.readline().split("=")[1])

    global printNumBest
    printNumBest = int(settings.readline().split("=")[1])

    global grid
    grid_type = (settings.readline().split("=")[1]).strip('\n') + '.mask'
    grid_type = grid_type.strip(' ')
    grid = open(grid_type).read().rstrip(' ').splitlines()

    global grid_h
    grid_h = len(grid)
    global grid_w
    grid_w = len(grid[0])

    global lines
    linesString = (settings.readline().split("=")[1]).strip('\n') + '.txt'
    linesString = linesString.strip(' ')
    lines = open(linesString)

    settings.close()

new_generation_list= []
horizontal=[]
vertical=[]
def main():
#######################select horizontal and vertical words##############################################

    while grid and not grid[0]:
        del grid[0]
    findIntersections(grid)
    # Extract horizontal words
    word = []
    predefined = {}
    for line in range(len(grid)):
        for column in range(len(grid[line])):
            char = grid[line][column]
            if not char.isspace():
                word.append((line, column))
                if char != "#":
                    predefined[line, column] = char
            elif word:
                if len(word) >= MINLEN:
                    horizontal.append(word[:])
                del word[:]
        if word:
            if len(word) >= MINLEN:
                horizontal.append(word[:])
            del word[:]

    # Extract vertical words
    validcolumn = True
    column = 0
    while validcolumn:
        validcolumn = False
        for line in range(len(grid)):
            if column >= len(grid[line]):
                if word:
                    if len(word) >= MINLEN:
                        vertical.append(word[:])
                    del word[:]
            else:
                validcolumn = True
                char = grid[line][column]
                if not char.isspace():
                    word.append((line, column))
                    if char != "#":
                        predefined[line, column] = char
                elif word:
                    if len(word) >= MINLEN:
                        vertical.append(word[:])
                    del word[:]
        if word:
            if len(word) > MINLEN:
                vertical.append(word[:])
            del word[:]
        column += 1

    hnames = ["h%d" % i for i in range(len(horizontal))]
    vnames = ["v%d" % i for i in range(len(vertical))]

    wordsbylen = {}
    chromosome_parent1_list = []
    chromosome_parent2_list = []
    chromosome_child_1 = []
    chromosome_child_2 = []
    generation_list = []
    iterations = 0
    fit=pop_size
    solution_found = False
    new_generation_pair = []

    for hword in horizontal:
        wordsbylen[len(hword)] = []
    for vword in vertical:
        wordsbylen[len(vword)] = []

    for line in lines:
        line = line.strip()
        l = len(line)
        if l in wordsbylen:
            wordsbylen[l].append(line.upper())

    for i in range(pop_size):
        #we get a list of two lists: the first one is the generated chromosome and the second is a list containing lengths of words
        temp=generate_parent(horizontal,vertical,wordsbylen)
        chromosome_parent1_list=temp[0]#we take the generated chromosome
        chromosome_parent1=" ".join(x for x in chromosome_parent1_list)# list to string
        length_words=temp[1]#we take the list containing the lengths of words
        generation_list.append(chromosome_parent1_list)#generation_list is a list of chromosomes(chromosome=list of genes and gene=word)


    startDate = time()

    generations = 0
    while generations < max_gens:
        iterations = 0
        while iterations != pop_size:
            #we pick two chromosomes from the generation list
            chromosome_parent1_list = random.choice(generation_list)
            chromosome_parent2_list = random.choice(generation_list)

            #crossover operation
            chromosome_child_1 = crossover(chromosome_parent1_list,chromosome_parent2_list,length_words)
            chromosome_child_2 = mutate(chromosome_child_1,wordsbylen,length_words)

            #new_generation_list is a list of new chromosomes created by mutation and crossover(chromosome=list of genes and gene=word)
            new_generation_list.append(chromosome_child_2)
            iterations += 1

        #faire une liste de paires (chromosome,fitness(chromosome))
        #et la sorter en fonction de la valeur de fitness

        # Take list, loop through to determine dominance so find all non-dominated points
        # pull them out, give fitness of 1, do the same with 2 ,3 -.....
        # assign final fit based on dominance
        # can still minimize one and maximize other!
        # NSGA
        # + fitness sharing
        # old v. new
        individualList = []
        for i in new_generation_list:
            string= "".join(x for x in i)

            conflictFit, weightFit = fitness(string, grid)

            # new way
            myIndividual = Individual(i, conflictFit, weightFit)
            individualList.append(myIndividual)

            # old way
            # new_generation_pair.append((i,weightFit - 10*conflictFit))


        frontList, chromFrontList = findNonDominatedFronts(individualList)
        #### WE STILL WANT TO:
        # do fitness sharing among individuals in the same front to obtain more of the pareto-front
        # complete selection process using this method
        # currently this is a place holder that is doing the exact same as our old method but using the front lists to do so
        choiceInd = 0
        for i in range(len(frontList)):
            for j in range(len(frontList[i])):
                if choiceInd < printNumBest:
                    new_generation_pair.append((frontList[i][j].chromosome, frontList[i][j].letterWeightFit - 10*frontList[i][j].countConflictFit))


        #we sort chromosome in fonction of the value of their fitness
        new_generation_pair.sort(key=lambda x: x[1])

        #reverses list so that higher fitnesses are valued instead of lower fitnesses
        new_generation_pair=new_generation_pair[::-1]

        n_best = []
        i = 0
        for pair in new_generation_pair:
            if not pair in n_best:
                n_best.append(pair)
                i += 1
            if i == 250:
                break

        if (printNumBest > len(n_best)):
            print "\n\n List of top "+str(len(n_best))+" pairs (chromosome, fitness) is : \n"
        else:
            print "\n\n List of top "+str(printNumBest)+" pairs (chromosome, fitness) is : \n"

        for k in range(printNumBest):
            if (k < len(n_best)):
                print str(n_best[k]) + "\n"

        #we check if we have a solution among the new generation
        for i in n_best:
            fit = i[1]
            if generations == max_gens-1:
                print "fitness is :" + str(fit)+ "\n"
                solution_found = True
                chromosome_solution = i #we keep the chromosome solution
                print "************************************************************"
                print "Solution chromosome is :"
                print chromosome_solution
                print "************************************************************"
                break
            else:
                del generation_list[:]
                for k in n_best:
                    generation_list.append(k[0]) #we're going to create the new child generation from the k best chromosome in generation_list


        generations += 1

        # print the computation time every 10 interations
        if iterations%10 == 0:
            delta1 = time() - startDate
            elapsedTime = round(delta1,1)
            print "Intermediate time (every ten iterations ) = " + str(elapsedTime) + " sec \n\n"

    delta = time() - startDate
    elapsedTime = round(delta,1)
    print "Final time = " + str(elapsedTime)
    print_solution(horizontal, vertical, chromosome_solution)
    

def print_solution(h, v, sol):
    
    width, height = grid_w, grid_h;
    wordstr = ''.join(str(i) for i in sol[0])
    wordstr.replace('[','')
    wordstr.replace("''", '')
    wordstr.replace(',', '')
    wordstr.replace(']','')
    i = 0

    sol_board = [[u"\u25A0" for x in range(width)] for y in range(height)]

    for words in h:
        for x in range(len(words)):
            num1 = words[x][0]
            num2 = words[x][1]
            sol_board[num1][num2] = wordstr[i]
            i += 1

    for words in v:
        for x in range(len(words)):
            num1 = words[x][0]
            num2 = words[x][1]

            if(sol_board[num1][num2] == wordstr[i] or sol_board[num1][num2] == u"\u25A0"):
                sol_board[num1][num2] = wordstr[i]
            else:
                sol_board[num1][num2] = '!'
            i += 1

    for x in range(height):
        print "----"*width
        for y in range(width):
            if y != width-1:
                print "| " + sol_board[x][y],
            else:
                print "| " + sol_board[x][y] + " |"
    print "----"*width
    
    return sol_board

def generate_parent(horizontal,vertical,wordsbylen):
    full_horizontal_parent1 = []
    full_vertical_parent1 = []
    full_horizontal_parent2 = []
    full_vertical_parent2 = []
    length_words = []
    chromosome = []
    for hi, hword in enumerate(horizontal):
        words = wordsbylen[len(hword)]
        random.shuffle(words)
        full_horizontal_parent1.append(random.choice(words))
        random.shuffle(words)
        full_horizontal_parent2.append(random.choice(words))
        length_words.append(len(hword))
    for vi, vword in enumerate(vertical):
        words = wordsbylen[len(vword)]
        random.shuffle(words)
        full_vertical_parent1.append(random.choice(words))
        random.shuffle(words)
        full_vertical_parent2.append(random.choice(words))
        length_words.append(len(vword))
    chromosome_parent1_list=full_horizontal_parent1+full_vertical_parent1
    chromosome.append(chromosome_parent1_list)
    chromosome.append(length_words)
    return chromosome



##################################################write in the grid 0 where there are no conflicts letter and 1 where there is one conflict letter############################################
def findIntersections(grid):
    intersectionList = []
    horizontalPositions = []
    verticalPositions = []
    x = 0
    y = 0
    v_check = False
    h_check = False
    for raw in range(len(grid)):
        for column in range(len(grid[raw])):
            char = grid[raw][column]
            if not char.isspace():
                # check if the cell belongs to a minimum 3-chars length horizontal word
                for pos0 in range(column-2, column+3):
                    if pos0 >= 0 and pos0 < len(grid[raw]):
                        if not grid[raw][pos0].isspace():
                            y = y+1
                            if(y == 3):
                                h_check = True
                        else:
                            y = 0

                # check if the cell belongs to a minimum 3-chars length vertical word
                for pos in range(raw-2, raw+3):
                    if pos >= 0 and pos < len(grid):
                        if not grid[pos][column].isspace():
                            x = x+1
                            if(x == 3):
                                v_check = True
                        else:
                            x = 0
                if(v_check == True and h_check== True):
                    intersectionList.append((raw, column))
                x = 0
                y = 0
                h_check = False
                v_check = False
    print "\nThe length of the intersection list is : " + str(len(intersectionList)) + '\n'
    return intersectionList

# counts the number of existing conflicts in the chromosome
# The chromosome contains only the valid words in the grid
def countConflicts2(chromosome,grid):
    nbrConflicts = 0
    horizontal_list = []
    vertical_list = []
    conflicts_dict = []
    n = 0
    #########################################
    word = []
    for line in range(len(grid)):
        for column in range(len(grid[line])):
            char = grid[line][column]
            if not char.isspace():
                word.append((line, column))
            elif word:
                if len(word) >= MINLEN:
                    tmp = ""
                    for i in range(len(word)):
                        tmp = tmp + chromosome[n]
                        n = n + 1
                    horizontal_list.append(word[:])
                del word[:]

        if word:
            if len(word) >= MINLEN:
                tmp = ""
                for i in range(len(word)):
                    tmp = tmp + chromosome[n]
                    n = n + 1
                horizontal_list.append(word[:])
            del word[:]

    #########################################
    validcolumn = True
    column = 0
    while validcolumn:
        validcolumn = False
        for line in range(len(grid)):
            if column >= len(grid[line]):
                if word:
                    if len(word) >= MINLEN:
                        tmp = ""
                        for i in range(len(word)):
                            tmp = tmp + chromosome[n]
                            n += 1
                        vertical_list.append(word[:])
                    del word[:]
            else:
                validcolumn = True
                char = grid[line][column]
                if not char.isspace():
                    word.append((line, column))
                elif word:
                    if len(word) >= MINLEN:
                        vertical_list.append(word[:])
                    del word[:]
        if word:
            if len(word) >= MINLEN:
                vertical_list.append(word[:])
            del word[:]
        column += 1

    for sublist in horizontal_list:
        for pair in sublist:
            conflicts_dict.append(pair)
    y = len(conflicts_dict)

    conf_list = []
    flattened_list = []
    for sublist in vertical_list:
        for pair in sublist:
            flattened_list.append(pair)

    for sublist in vertical_list:
        for pair in sublist:
            if pair in conflicts_dict:
                x = conflicts_dict.index(pair)
                z = y + flattened_list.index(pair)
                if chromosome[x]  != chromosome[z]:
                    conf_list.append((pair, chromosome[x], chromosome[z]))
                    nbrConflicts += 1
            conflicts_dict.append(pair)

    return nbrConflicts



def findNonDominatedFronts(individualList):
    fronts = []
    fronts.append([])
    for i in individualList:
        # print str(i)
        for other in individualList:
            if (i.dominates(other)):
                #print str(i) + " dominates " + str(other)
                i.dominateSet.append(other)
            elif (other.dominates(i)):
                # print str(other) + " dominates " + str(i)
                i.dominatedByCount += 1

        if (i.dominatedByCount == 0):
            # individual is non-dominated
            # want to add individual to the first front
            fronts[0].append(i)
            i.rank = 0

    currentFront = 0
    while (len(fronts[currentFront]) > 0):
        nextFront = []
        for i in fronts[currentFront]:
            for other in i.dominateSet:
                other.dominatedByCount -= 1
                if (other.dominatedByCount == 0):
                    other.rank = currentFront + 1
                    nextFront.append(other)
        fronts.append(nextFront)
        currentFront += 1

    index = 0
    frontChromosome = []
    for i in range(len(fronts)):
        frontChromosome.append([])
        print("Front "+ str(index))
        for j in fronts[i]:
            frontChromosome[i].append(j)
            print str(j)
            print str(j.rank)

        index += 1

    #now returns chromosomes as they have been handled originally
    return fronts, frontChromosome # [[front1], [front2], ... ] and frontN = [ind1, ind2, ind3, ... ]



##################################################encode and put horizontal and vertical words in a same string############################################
# Do probablistic crossover operation.
def crossover(chromosome_list_parent1,chromosome_list_parent2,length_words):
    chromosome_child = []
    crossover_point = random.randint(0,len(length_words))
    if(random.random() <= crossover_rate):
		chromosome_child = chromosome_list_parent1[:crossover_point] + chromosome_list_parent2[crossover_point:]
    else:
        chromosome_child = chromosome_list_parent1
    return chromosome_child

# Do probablistic mutation operation.
def mutate(chromosome_child,wordsbylen,length_words):
    for i in range(len(length_words)):
    	if(random.random() <= mutation_rate):
            words = wordsbylen[len(chromosome_child[i])]
            random.shuffle(words)
            chromosome_child[i]=random.choice(words)
    return chromosome_child


""" TODO
    ADD MOB HERE FOR FITNESS """
def fitness(chromosome_child,grid):
    #check conflicts
    fitConflict = countConflicts2(chromosome_child,grid)

    #finds Value of Letters
    fitValue = findTotalValue(chromosome_child)

    # Finds total Fitness
    return fitConflict, fitValue


def findTotalValue(chromosome_child):
    width, height = grid_w, grid_h
    i = 0
    sol_board = [["" for x in range(width)] for y in range(height)]

    for words in horizontal:
        for x in range(len(words)):
            num1 = words[x][0]
            num2 = words[x][1]
            sol_board[num1][num2] = chromosome_child[i]
            i += 1

    for words in vertical:
        for x in range(len(words)):
            num1 = words[x][0]
            num2 = words[x][1]

            if(sol_board[num1][num2] == chromosome_child[i] or sol_board[num1][num2] == ""):
                sol_board[num1][num2] = chromosome_child[i]
            else:
                sol_board[num1][num2] = ''
            i += 1
    
    totalValueCount=0
    for line in sol_board:
        for char in line:
            if (char!=''):
                totalValueCount=totalValueCount+letterValues[char]
    
    return totalValueCount

if __name__ == "__main__":
    #if len(sys.argv) != 2:
     #  sys.exit("Usage: genetic.py <wordsfile>")

    readSettings()
    main()
