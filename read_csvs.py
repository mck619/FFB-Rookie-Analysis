'''
This is a script to read in the csvs from www.pro-football-reference.com so I can create a table of draft results from
2010 on
'''

import csv
import os
import psycopg2


row_tester = {str(x) for x in range(1,8)}


def read_rookie_by_year(csvfile):

    f = open('database_password.txt','r')
    pw = f.readlines()[0]
    f.close()
    conn = psycopg2.connect("dbname=nfldb user=postgres password="+pw)
    cur = conn.cursor()

    c = open(os.getcwd()+'\\raw_data\\'+csvfile, 'rb')
    cs = csv.reader(c)

    c.close()

#read_rookie_by_year('years_2010_draft_drafts.csv')

