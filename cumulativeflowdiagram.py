#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vi:ts=4:et

# burndown.py
# Author: Marco Rubio
# Date  : 2/9/2018
# Desc  : Creates a burn down plot from the wekan mongodb data

# Install dependencies first
# pip install -r requirements.txt

from email import header
from operator import index
import os
import locale
from pickle import UNICODE
from unittest import skip
import schedule
import time
from datetime import datetime

from sqlalchemy import null

os.environ["PYTHONIOENCODING"] = "utf-8"
scriptLocale=locale.setlocale(category=locale.LC_ALL, locale="en_GB.UTF-8")

from pymongo import MongoClient
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import time                         # time.strptime # For datetime compairons
import pandas as pd
import csv

# Configuration Cariables
URL  = 'localhost'
PORT = 4001

def get_parenthesis(string):
    """Get number in parenthesis or return 0"""
    start = string.find("(") # Verify we have (
    end   = string.find(")") # Verify we have )
    value= 0
    if(start != -1):
        if(end != -1):
            value= int(string[start+1:end])
    return value

# field names 
fields = ['Backlog', 'To do', 'Doing', 'Blocked', 'Done', 'date']
# name of csv file 
filename = "cfd_top.csv"
# writing to csv file 
with open(filename, 'w') as csvfile: 
    # creating a csv dict writer object 
    writer = csv.DictWriter(csvfile, fieldnames = fields) 
        
    # writing headers (field names) 
    writer.writeheader() 


def job():
    # Set up database connection
    client = MongoClient(URL, PORT)
    db = client.wekan
    boardId = 'fC64YwSb7Ry4YrvNt'
    cards = db.cards.find({'boardId' : boardId}).sort("dateLastActivity")

    database = client["meteor"]

    datetime_1 = datetime.datetime.now()
    print("I'm working..."+ str(datetime_1))

    print("\n=== Board Lists START ===")
    colletion = database['lists']
    documents = colletion.find({'boardId' : boardId})
    boardLists = list(documents)
    print("=== Board Lists END ===\n")


    print("\n=== Cards per List START ===")
    colletion = database['cards']
    for boardList in boardLists:
        documents = colletion.find({'boardId' : boardId, 'listId' : boardList["_id"]})
        cardsPerList = list(documents)
    print("=== Cards per List END ===\n")

    print("\n=== Count Cards per List START ===")
    colletion = database['cards']
    items = []
    thisdict =	{
        'Backlog': '',
        'To do': '',
        'Doing': '',
        'Blocked': '',
        'Done': '',
        'date': null,
    }
    print(thisdict)

    for boardList in boardLists:
        items.append(boardList["title"])
    items.append("date")
    print("ITEMS")
    print(items)
    print(len(items))
    dateNow = datetime.date.today()


    for boardList in boardLists:
        documents = colletion.count_documents({'boardId' : boardId, 'listId' : boardList["_id"]})
        lista4 = documents

        print(boardList["title"])
        items.append(lista4)
        print(lista4)

        thisdict[boardList["title"]] = lista4

    thisdict["date"] = dateNow

    print("\n DICIONARIO")
    print(thisdict)
    print(len(thisdict))
    import pandas as pd
    df = pd.DataFrame.from_dict(thisdict, orient='index')
    print(df)
    print(df.transpose())

    trans = df.transpose()

    
    trans.to_csv(filename, mode='a', header=not os.path.exists(filename), index=False)

    print("=== Count Cards per List END ===\n")



    #Prepare for ploting
    dates  = [datetime.datetime(2000,1,1)]
    values = 0                          # Running Total
    total  = [0]

    print("\n=== Boards List START ===")
    colletion = database["boards"]
    documents = colletion.find().limit(15)
    boardsList = list(documents)

    for card in boardsList: #cards

        expected = get_parenthesis(card['title'])
        print("Title   : " + card['title'])
        # print("dateLastActivity   : " + card['dateLastActivity'].date())
        if(expected):
            #print("Expected: " + str(expected))
            if(card['dateLastActivity'].date() > dates[-1].date()):
                dates.append(card['dateLastActivity'])
                total.append(total[-1]+expected)
            else:
                total[-1] += expected
    print("=== Boards List END ===\n")


    print("\n=== All Cards START ===")
    colletion = database['cards']
    documents = colletion.find().limit(15)
    allCards = list(documents)

    for card in allCards: #cards

        expected = get_parenthesis(card['title'])
        # print("Expected: "+str(expected))
        print("Title   : " + card['title'] + " | " + "dateLastActivity   : " + str(card['dateLastActivity']))

        if(expected):
            #print("Expected: " + str(expected))
            if(card['dateLastActivity'].date() > dates[-1].date()):
                dates.append(card['dateLastActivity'])
                total.append(total[-1]+expected)
                
            else:
                total[-1] += expected
    print("=== All Cards END ===\n")

    print("\n=== Board Cards START ===")
    colletion = database['cards']
    documents = colletion.find({'boardId' : boardId})
    boardCards = list(documents)

    for card in boardCards: #cards

        expected = get_parenthesis(card['title'])
        print("Title   : " + card['title'])
        # print("dateLastActivity   : " + card['dateLastActivity'].date())
        if(expected):
            #print("Expected: " + str(expected))
            if(card['dateLastActivity'].date() > dates[-1].date()):
                dates.append(card['dateLastActivity'])
                total.append(total[-1]+expected)
            else:
                total[-1] += expected
    print("=== Board Cards END ===\n")


    print("\n=== Board Lists START ===")
    for card in boardLists: #cards

        expected = get_parenthesis(card['title'])
        print("Title   : " + card['title'])
        # print("dateLastActivity   : " + card['dateLastActivity'].date())
        if(expected):
            #print("Expected: " + str(expected))
            if(card['dateLastActivity'].date() > dates[-1].date()):
                dates.append(card['dateLastActivity'])
                total.append(total[-1]+expected)
            else:
                total[-1] += expected
    print("=== Board Lists END ===\n")


    print("\n=== Board Cards per List START ===")
    for card in cardsPerList: #cards

        print("Title   : " + card['title'])
        # print("dateLastActivity   : " + card['dateLastActivity'].date())
        
    print("=== Board Cards per List END ===\n")


def plot_cfd():
    print("\n=== Plot CFD START ===")
    df = pd.read_csv(filename, sep=",")
    print(df)
    dados = df[['To do', 'Doing', 'Done']]
    print(dados)


    # Stackplot with X, Y, colors value
    print(df['To do'])
    print(df[df.columns.difference(['date'])])
    print(df[df.columns.difference(['date'])].head())

    # iterating the columns
    colunas = []
    for col in df.columns:
        print(col)
        colunas.append(col)

    # colunas.remove('Unnamed: 0')
    print(colunas)

    # plt.stackplot(df['date'], df[df.columns.difference(['date', 'Unnamed: 0'])],
    fig = plt.figure(figsize=(8,5))
    plt.stackplot(df['date'], df['Backlog'], df['To do'], df['Doing'], df['Blocked'], df['Done'], 
    # colors =['r', 'c', 'b'],
    labels=colunas
    # labels=['Done', 'To do']
    )


    plt.xlabel('Days')
    plt.ylabel('No of Cards')
    plt.title('Cumulative Flow Diagram')
    plt.legend(loc = "lower center")
    plt.show()

    print("\n=== Plot CFD END ===")


# Schedules
boardId = 'fC64YwSb7Ry4YrvNt'
schedule.every(60).seconds.do(job)
# schedule.every().day.at("00:10").do(job)

schedule.every(70).seconds.do(plot_cfd)
# schedule.every().day.at("00:12").do(plot_cfd)


while True:
    schedule.run_pending()
    time.sleep(1)