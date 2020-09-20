import config
import requests
import json
import os
import time

url = "https://api.datamuse.com/words?sp=" #+ word #Datamuse API

urlMw = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/" #?key=
api_key = config.api_key #MWebster dict

def solver(word,length):
    global url, urlMw, api_key
    sortedWord = sorted(word)

    solutions = set()
    for loop in range(len(word)//2): #must loop as many times as the result may not show in first 1000 results
                                     #this loop is to check words of lengths less than the actual word
        for char in word:
            qm = len(word)-1-1*loop -length #number of chars to the right in request
            qminv = len(word)-1-qm -length #number of chars to the left in request

            r = requests.get(url+"?"*qminv+char+"?"*qm+"&max=1000").json() #? represents any char
            possible = set(r[i]["word"] for i in range(len(r)))

            for pos_word in possible:
                if sortedWord == sorted(pos_word): #this will only work for full length
                    solutions.add(pos_word)
                elif length>0: #when checking any length other than whole word
                    pos_wordc = pos_word
                    sortedWordc = "".join(sortedWord)
                    c=0
                    while c < len(pos_wordc):
                        if pos_wordc[c] in sortedWordc:
                            sortedWordc = sortedWordc.replace(pos_wordc[c],"",1)
                            pos_wordc = pos_wordc.replace(pos_wordc[c],"",1)
                        else:
                            break
                    if len(pos_wordc) ==0:
                        solutions.add(pos_word)
        if qm ==0: #After having looped enough times for qm to become 0 it should
            break  #stop looping as the qm and qminv will become erroneous and show
                   #results outside the requested length (i.e. length 3 for word of
                   #length 9 would cause errors.
    solutionsReal = set()
    for w in solutions: #Vetting Datamuse solutions through another API - are they real words?
        r = requests.get(urlMw+w+"?key="+api_key).json()
        try:
            if r[0]["meta"]["id"]:
                solutionsReal.add(w)
        except:
            pass
    return solutionsReal

def validation(word): #validation
    if len(word.split())>=2 and word.split()[0].isalpha()==True:
        choice = word.split()[1]
        word = word.split()[0]

        if choice.isdigit() and int(choice)<3: #only find words that are a min of 3 chars long
            choice =3
        elif choice.isdigit() and int(choice)>len(word):
            choice = len(word)
        elif choice.isdigit():
            pass
        else:
            choice = "all"
    elif len(word.split())==1 and word.isalpha() == True:
        word = word.split()[0]
        choice = len(word)
    else:
        word = choice = ""

    if len(word)<3: #minimum size of words should be 3
        word = choice = ""

    return word.lower(),choice #word must all be lower case, same as the API

def countdown(word): #This is only for when importing this functionality elsewhere
    word,choice = validation(word) #apply validation to the input
    if word==choice=="" or choice =="all":
        return "N/A"
    return solver(word, len(word)-int(choice))

if __name__ == "__main__":
    while True:
        os.system('cls' if os.name=='nt' else 'clear') #clear the screen
        #sample words:
        #vegdances moveycast greensods cillyalex vinewrite ismyslave giddiemus
        word = input("Enter a word you would like to find the anagram(s) for: ")

        word,choice = validation(word) #apply validation to the input
        if word==choice=="":
            continue

        start_time = time.time()#begin timer for solutions

        if choice == "all":
            lengths =list(range(len(word)-3+1)) #check all chars down to minimum 3 chars
        else:
            lengths = [len(word) - int(choice)] #just check the specific length

        for length in lengths:
            solutionsReal = solver(word,length)
            end_time = time.time()
            print(str(round(end_time-start_time,2))+"s") #print the time it took to solve for each length

            if len(solutionsReal)==0:
                print("No solutions found")
            else:
                print(*solutionsReal)
            print("")

        input("\nPress enter to continue")
