# Program as part of project relating to Applied Databases
# Manipulation of SQL and neo4j databases 

# Author: Katie O'Brien G00398250

# Importing packages required for program

from neo4j import GraphDatabase
from neo4j import exceptions
import db_module
import pymysql
import time

# NEO4J Drivers
driver = None
def connect():
    global driver
    uri= "neo4j://localhost:7687"
    driver = GraphDatabase.driver(uri, auth = ("neo4j","neo4j"),max_connection_lifetime = 1000)

# Main Program code

def main():
    connect()
 

# Main Menu and user input

    while True:
        db_module.user_menu()
        choice = input("Choice: ")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Code section returns list of employees via db_module
        if (choice == "1"):
            employees = db_module.employee()
            for employee in employees:
                print(employee["name"], "|", employee["d.name"])
            
 # Made multiple attempts with "keyboard" and using limit and offset with a while loop
 #  iterating + 2 on each pass but was unable to get it working    
            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#  
#  Asks for input then displays min max avg salary for employee via db_module function                         
        elif (choice == "2"):
            e_id= input("Enter EID: ")
            salary= db_module.choice_2(e_id)
            print("Salary Details For Employee:  ", e_id)
            print("Minimum   |  Average  |   Maximum   ")
            for salary in salary:
                print(salary["Minimum"],"|",salary["Average"],"|",salary["Maximum"])
  
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Asks for input, converts various month responses to correct format and sends to db_module function
        elif (choice == "3"):
          
            month = (input("Enter Month: ").lower)
            
            if month == "apr" or "4":
                month = 4
            elif month == "may" or "5": 
                month = 5
            elif month == "jun" or "6":
                month = 6
            elif month =="jul" or "7":  
                month = 7
            elif month == "aug" or "8":
                month = 8
            elif month == "sep" or "9":
                month = 9
            elif month == "oct" or "10":
                month = 10
            elif month == "nov" or "11":
                month = 11
            elif month == "dec" or "12":
                month = 12
            elif month == "jan" or "1":
                month = 1
            elif  month == "feb" or "2":
                month = 2
            elif  month == "mar" or "3":
                month = 3
            
            dob = db_module.choice_3(month)
            for month in dob:
                print(month["eid"],"|", month["name"], "|", month["dob"])
                        
#  invalid months still showing active- suspect a while loop could solve but
# using one was throwing an error

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Asks for a series of inputs, and sends to db_module. when returned, try/except catches potential errors
        elif (choice == "4"):
            emp_id = input("EID : ")
            name = input("Name : ")
            dob = input("DOB (in format YYYY-MM-DD) : ")
            dept_id = input("Dept ID : ")
            try:
                db_module.choice_4(emp_id,name,dob,dept_id)
                print ("Employee successfully added")
            except pymysql.err.IntegrityError as e:
                   print("***Error***",emp_id, "already exists or ", dept_id, "does not exist. please try again")   
            except pymysql.err.OperationalError as e:
                print("*** Error***: Invalid DOB:",dob)
            except Exception as e:
                print("Error: ", e)
# Tried to split the integrity error up into 2 possible returns however, was still getting only one error message back

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#  
# db_module returns answer from neo4j query, then feeds output from returned array into sql query and prints output
        elif (choice == "5"):
            n = db_module.choice_5()
            print("Department  |   Budget")
            for i in n:
                x = db_module.choice_5_sql(i)
                for a in x:
                    print(i,"|",a["budget"])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#  
# first 2 functions are checking sql to see if the inputs exist, then printing error messages
# if non-existent returns messages. else sends sql outputs to neo4j to create relationship                   
        elif (choice == "6"):
                while True: 
                    eid = db_module.choice_6_1_sql()
                    for id in eid:
                        e_id = (id["eid"])
                    did = db_module.choice_6_2_sql()
                    for id in did:
                        d_id = (id["did"])
                    break
                print("ID/DEPT error, please try again")
                try:      
                    add_user= db_module.choice_6_1_neo4j(e_id,d_id)
                    print("Employee ",e_id, " now manages Department ", d_id)
                except:
                    print(" relationship error, please try again")
                                    
# Was unable to create error message if department is already managed
#Invalid dept error is not allowing user to input new info,instead sending them back to user menu

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Returns list of departments, with budgets etc.
# first time inserts result into array and calls from that on subsequent running 
                        
        elif (choice == "7"):
            depts = db_module.choice_7()
            print ("Did  |  Name  |   Location   |   Budget   ")
            for dept in depts:
                print (dept[0], "|", dept[1], "|", dept[2],"|", dept[3])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# 
# Quits Program      
        elif (choice == "x"):
            break

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# For all other input, returns to user menu
        else:
            db_module.user_menu()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if __name__ == "__main__":
    main()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
