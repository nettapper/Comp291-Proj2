import sys
import datetime
import random
import bsddb3 as bsddb
import os

# This will display the menu and handle input to the menu
# after creating/population tables.
def main():
    if(len(sys.argv) != 2):
        sys.exit("Warning: Arguments not properly specified!\n" + \
        "First argument creates specifies database type (btree/hash/indexfile).\n" + \
        "Quitting.")

    try:
        answer = open("answers", 'w')
    except Exception as e:
        print(e)

# Display main menu and get selection
    while(True):
        print(
"""----------------------------------------
Please Select from the following:
        1:Create and Populate Database
        2:Retrieve records with Key
        3:Retrive records with Data
        4:Retrieve records with Key Range
        5:Destroy Database
        6:Quit""")
        
        choice = getNumber("Choice (1-6): ", 1, 1, 6, 1)

        if choice == 1:
            print("Creating/Populating Database")
            db_P, db_S = create(100000, 10000000)

        elif choice == 2:
            print("Retrieving Records with Key:")
            key(db_P, answer)
        elif choice == 3:
            print("Retrieving Records with Data:")
            data(db_P, db_S, answer)
        elif choice == 4:
            print("Retrieving Records with Key Range:")
            keyRange(db_P, answer, sys.argv[1])
        elif choice == 5:
            print("Destroying Database")
            db_P, db_S = destroy(db_P, db_S)
        elif choice == 6:
            print("Good Bye.")
            break
        else:
            print ("Invalid Input!")

# Destroy databases and close answer file before finishing
    db_P.close()
    if db_S is not None:
        db_S.close()
        try:
            os.remove("tmp/sbaergen_db2")
        except:
            print("Error removing secondary database")
    try:
        os.remove("tmp/sbaergen_db")  # TODO: what happens if the file is already removed?
    except:
        print("Error removing primary database")
    try:
        answer.close()
    except:
        print("Error closing answer file")
    
# TODO: Should we be creating the databases in this function?
def create(length, seed):
    db_P, db_S = open_db()
    start = datetime.datetime.now()
    random.seed(seed)
    new_value = None
    new_key = None
    count = 0
    while count < length:
        new_key = ""
        new_value = ""

        for increment in range(integer_generator()):
            new_key += str(char_generator())

        for increment in range(integer_generator()):
            new_value += str(char_generator())
        
        new_key = new_key.encode(encoding ='UTF-8')
        new_value = new_value.encode(encoding = 'UTF-8')

        if db_P.has_key(new_key) == False:
            db_P[new_key] = new_value
            count+=1
        else:
            continue
        
        if db_S != None:
            if db_S.has_key(new_value) == False:
                db_S[new_value] = new_key
            else:
                S = db_S[new_value].decode(encoding = 'UTF-8')
                S += ";;;" + new_key.decode(encoding = 'UTF-8')
                db_S[new_value] =  S.encode(encoding = 'UTF-8')
    end = datetime.datetime.now()
    print("Key :", new_key)
    print("Value:", new_value)
    print("Database Populated Successfully")
    print(end-start)
    return db_P, db_S
# Perform a search by key
def key(db, answer):
    search_key = input("Enter the key value you wish to search for: ") 
    start = datetime.datetime.now()
    search_key = search_key.encode(encoding ='UTF-8')
    try:
        data = db[search_key]
        answer.write(search_key.decode(encoding ='UTF-8') + '\n')
        answer.write(data.decode(encoding = 'UTF-8') + '\n')
        answer.write('\n')
    except Exception as e:
        print(e)
        print("Key does not exist")
    end = datetime.datetime.now()
    print(end - start)

# Perform a search by data
def data(db_P, db_S, answer):
    search_data = input("Enter the data you wish to search for: ")
    start = datetime.datetime.now()
    search_data = search_data.encode(encoding = 'UTF-8')
    count = 0
    if db_S == None:
        try:
            for key in db_P:
                if db_P[key] == search_data:
                    answer.write(key.decode(encoding ='UTF-8') + '\n')
                    answer.write(search_data.decode(encoding = 'UTF-8') + '\n')
                    answer.write('\n')
        except Exception as e:
            print(e)
            print("Data does not exist")
    else:
        
        try:
            data = db_S[search_data]
            data = data.decode(encoding = 'UTF-8')
            for key in data.split(";;;"):
                answer.write(key + '\n')    
                answer.write(search_data.decode(encoding = 'UTF-8') + '\n')
                answer.write('\n')  
        except Exception as e:
            print(e)
            print("Data does not exist")
    end = datetime.datetime.now()
    print(end - start)

# Get Range of data
def keyRange(db, answer, dbType):
    search_key_min = input("Enter the minimum key value you wish to search for: ").encode(encoding ='UTF-8')
    search_key_max = input("Enter the maximum key value you wish to search for: ").encode(encoding ='UTF-8')
    start = datetime.datetime.now()
    count = 0
    if dbType != "hash":
        try:
            current = db.set_location(search_key_min)
            while current[0] < search_key_max:
                answer.write(current[0].decode(encoding ='UTF-8') + '\n')
                answer.write(current[1].decode(encoding = 'UTF-8') + '\n')
                answer.write('\n')
                count+=1  
                current = db.next()
        except:
            pass

    else:
        try:
            for key in db:  # inclusive key range search
                if key >= search_key_min and key <= search_key_max:
                    count+=1
                    solution_key = key
                    solution_data = db[solution_key]
                    answer.write(solution_key.decode(encoding ='UTF-8') + '\n')
                    answer.write(solution_data.decode(encoding = 'UTF-8') + '\n')
                    answer.write('\n')

            print("Number of records found is: " + str(count))
            print("Result Recorded")
        except Exception as e:
            print(e)
            print("Key does not exist")
    
    print(count, "entries found!")   
    end = datetime.datetime.now()
    print(end - start)

# Destroy database, Clear Answer
def destroy(db_P, db_S):  # TODO: destroy? why are we returning a new db then?
    if db_P is not None:
        db_P.close()
    if db_S is not None:
        db_S.close()
    return open_db()
    

# Get random integer between 64 and 127 inclusive
def integer_generator():
    return random.randint(64,127)

# Get random char between ASCII value 97 and 122 inclusive
def char_generator():
    return chr(random.randint(97,122))

# Open the database(s)
def open_db():
    db_S = None
    DATABASE = "tmp/sbaergen_db"
    DATABASE2 = "tmp/sbaergen_db2"
    if not os.path.exists("tmp/"):
        os.makedirs("tmp/") 
    if(str(sys.argv[1]).lower() == "btree"):     
        try:
            db_P = bsddb.btopen(DATABASE, 'w')
        except:
            db_P = bsddb.btopen(DATABASE, 'c')
    elif(str(sys.argv[1]).lower() == "hash"):
        try:
            db_P = bsddb.hashopen(DATABASE, 'w')
        except:
            db_P = bsddb.hashopen(DATABASE, 'c')
    elif(str(sys.argv[1]).lower() == "indexfile"):
        #TODO finish berkely db open
        try:
            db_P = bsddb.btopen(DATABASE, 'w')
        except:
            dp_P = bsddb.btopen(DATABASE, 'c')
        try:
            db_S = bsddb.hashopen(DATABASE2, 'w')
        except:
            dp_S = bsddb.hashopen(DATABASE2, 'c')
    print("")  # put some space between info above and start of menu
    return db_P, db_S

# from sql.py in proj1
def getNumber(message, maxLen = None, minLen = 0, maxValue = None, minValue = None):
    number = None
    while(True):
        try:
            number = eval(input(message))
        except:
            print("Invalid input, try again.")
            continue
        length = len(str(number))
        if maxLen is not None:
            if length > maxLen:
                print("Number length too long, try again.")
                continue
        if minLen is not None:
            if length < minLen:
                print("Number length too short, try again.")
                continue
        if maxValue is not None:
            if number > maxValue:
                print("Value too large, try again.")
                continue
        if minValue is not None:
            if number < minValue:
                print("Value too small, try again.")
                continue
        return number


# only want the main function called if this is the main file
if __name__ == "__main__":
    main()
