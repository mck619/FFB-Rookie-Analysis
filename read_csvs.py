'''
This is a script to read in the csvs from www.pro-football-reference.com so I can create a table of draft results from
2010 on
'''

import csv
import os
import psycopg2


row_tester = {str(x) for x in range(1,8)}


def read_rookie_by_year(csvfile, year):


    f = open('database_password.txt','r')
    pw = f.readlines()[0]
    f.close()
    conn = psycopg2.connect("dbname=nfldb user=postgres password="+pw)
    cur = conn.cursor()

    c = open(os.getcwd()+'\\raw_data\\'+csvfile, 'rb')
    cs = csv.reader(c)
    for row in cs:
        if row[0] in row_tester:

            if row[2] == 'TAM':
                team = 'TB'
            elif row[2] == 'KAN':
                team = 'KC'
            elif row[2] == 'JAX':
                team = 'JAC'
            elif row[2] == 'SFO':
                team = 'SF'
            elif row[2] == 'NWE':
                team = 'NE'
            elif row[2] == 'NOR':
                team = 'NO'
            elif row[2] == 'SDG':
                team = 'SD'
            elif row[2] == 'GNB':
                team = 'GB'
            else:
                team = row[2]
            name = row[3]
            print (name)
            cur.execute('SELECT player_id FROM player WHERE full_name = %s;', (name,))
            player_id = cur.fetchall()

            if player_id == []:
                print("Player name does not match for row, ending script. Go fix it.")
                print(row)
                conn.commit()
                cur.close()
                conn.close()
                c.close()
                return
            if len(player_id)>1:
                print("Multiple players have this name, ending script. Go figure it out and enter row manually.")
                print(row)
                conn.commit()
                cur.close()
                conn.close()
                c.close()
                return
            conn.commit()
            try:
                cur.execute('INSERT INTO drafts (player_id, draft_year, draft_round, overall_pick, team_id) VALUES'
                            '(%s,%s,%s,%s,%s);',
                            (player_id[0], year, row[0], row[1],team))
            except psycopg2.Error as e:
                conn.rollback()
                print (e.pgerror)
    conn.commit()
    cur.close()
    conn.close()
    c.close()

read_rookie_by_year('years_2010_draft_drafts.csv', 2010)

