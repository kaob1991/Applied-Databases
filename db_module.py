# packages required for background modules

import pymysql
from neo4j import GraphDatabase
from neo4j import exceptions
import time

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# setting connection for mysql
conn = None

def connectsql():
    global conn
    conn = pymysql.connect(host= "localhost", user = "root", password = "root", db = "employees", cursorclass= pymysql.cursors.DictCursor)

#~~~~~~~~~~~~~~~~~~~
# neo4j connection

def connectneo4j():
    global driver
    uri = "neo4j://localhost:7687"
    driver = GraphDatabase.driver(uri, auth = ("neo4j","neo4j"),max_connection_lifetime = 1000)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# user menu- timer for 5 secs before loading/reloading for ease of user

def user_menu():
    time.sleep(5)
    print("Employees")
    print("---------")
    print("")
    print("")
    print("MENU")
    print("====")
    print("1 - View Employees & Departments")
    print("2 - View Salary Details")
    print("3 - View by Month of Birth")
    print("4 - Add New Employee")
    print("5 - View Departments managed by Employee")
    print("6 - Add Manager to Department")
    print("7 - View Departments")
    print("x - Exit application")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# section 1 code- sets connection, sql query then fetches all from sql database using cursor
# Then returns all to main program

def employee ():
    conn = pymysql.connect(host= "localhost", user = "root", password = "root", db = "employees", cursorclass= pymysql.cursors.DictCursor)
    query = "SELECT e.name, d.name from employee e inner join dept d on e.did = d.did order by e.name;"


    with conn:
        cursor = conn.cursor()
        cursor.execute(query)
        x = cursor.fetchall()
        return x

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# section 2 code- sets connection, sql query using input from main program and returns answer after formatting  

def choice_2(e_id):
    conn = pymysql.connect(host= "localhost", user = "root", password = "root", db = "employees", cursorclass= pymysql.cursors.DictCursor)
    query="select format(min(salary),2) as Minimum,format(avg(salary),2) as Average, format(max(salary),2) as Maximum from salary where EID = %s;"


    with conn:
        cursor = conn.cursor()
        cursor.execute(query,(e_id))
        x = cursor.fetchall()
        return x

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# section 3 code- sets connection, sql query using input from main program and returns answer back to main program       

def choice_3(month):
    conn = pymysql.connect(host= "localhost", user = "root", password = "root", db = "employees", cursorclass= pymysql.cursors.DictCursor)
    query= "select eid,name,dob from employee where (month(dob) = %s) ;"


    with conn:
        cursor = conn.cursor()
        cursor.execute(query,(month))
        x = cursor.fetchall()
        return x

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# section 4 code- sets connection, sql query using input from main program and returns answer back to main program

def choice_4(e,n,dob,did):
    conn = pymysql.connect(host= "localhost", user = "root", password = "root", db = "employees", cursorclass= pymysql.cursors.DictCursor)
    sql = "INSERT INTO employee(eid, name, dob,did) VALUES (%s,%s,%s,%s);"

    with conn:
        cursor = conn.cursor()
        x = cursor.execute(sql,(e,n,dob,did))
        return x

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# section 5 code- neo4j choice 5 asks for input, sends that to neo4j1 function, query is run, and appended to array
# sql function takes in elements from array and returns query based on each element, then returns to main program

#neo4j functions

def neo4j_1(tx,user_input):
    query = "match(:Employee{eid:$user})-[]-(s) return s.did as did"
    depts=[]
    results= tx.run(query,user = user_input)
    for result in results:
        depts.append(result["did"])
    return depts


def choice_5():
    connectneo4j()
    user_input = input("Enter EID : ")
    print("")
    print("Departments managed by:  ", user_input)
    print("----------------")
    with driver.session() as session:
        values = session.read_transaction(neo4j_1, user_input)
        #for value in values:
        return values

# sql function

def choice_5_sql(value):
    conn = pymysql.connect(host= "localhost", user = "root", password = "root", db = "employees", cursorclass= pymysql.cursors.DictCursor)
        
    query = "select format((budget),0) as budget from dept where (did = %s);" 

    with conn:
        cursor = conn.cursor()
        cursor.execute(query,(value))
        x = cursor.fetchall()
        return x

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Section 6 code-- both sql codes check the input to see if the input exists in sql
# neo4j code takes in the verified inputs, and creates a relationship with them in neo4j db

# Sql functions

def choice_6_1_sql():
    conn = pymysql.connect(host= "localhost", user = "root", password = "root", db = "employees", cursorclass= pymysql.cursors.DictCursor)
    eid= input("Enter EID: ")
    query= " select eid from employee where eid = %s;"


    with conn:
        cursor = conn.cursor()
        cursor.execute(query,(eid))
        x = cursor.fetchall()
        return x

def choice_6_2_sql():
    conn = pymysql.connect(host= "localhost", user = "root", password = "root", db = "employees", cursorclass= pymysql.cursors.DictCursor)
    did = input("Enter DID: ")
    if(not conn):
        connectsql()
    query= " select did from dept where did =  %s;"


    with conn:
        cursor = conn.cursor()
        cursor.execute(query,(did))
        x = cursor.fetchall()
        return x

# Neo4j functions

def choice_6_2_neo4j(tx, eid,did):
    query = "merge(e:Employee{eid:$eid})-[:MANAGES]->(d:Department{did:$did}) "
    tx.run(query, eid = eid, did = did)


def choice_6_1_neo4j(eid,did):
        connectneo4j()
        with driver.session() as session:
            node_id = session.write_transaction(choice_6_2_neo4j, eid,did)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Code for part 7- creates a array, code also checks to see if length of array is 0- if it is it runs onto next section of code which appends sql output to array
# and sends back to main program. if it isn't it just returns full array without contacting sql server

def choice_7():
    conn = pymysql.connect(host= "localhost", user = "root", password = "root", db = "employees", cursorclass= pymysql.cursors.DictCursor)
    depts1 = []
    length = len(depts1)
    if length == 0:
        if(not conn):
            connectsql()
        query="select * from dept;"

        
        with conn:
            cursor = conn.cursor()
            cursor.execute(query)
            depts = cursor.fetchall()
            for dept in depts:
                depts1.append([dept["did"], dept["name"], dept["lid"], dept["budget"]])
            return depts1
    else:
        return depts1

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            




