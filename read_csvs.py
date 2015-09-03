'''
This is a script to read in the csvs from www.pro-football-reference.com so I can create a table of draft results from
2010 on
'''

import csv
import os
import psycopg2





def read_rookie_by_year(csvfile, year):

    row_tester = {str(x) for x in range(1,8)}
    f = open('database_password.txt','r')
    pw = f.readlines()[0]
    f.close()
    conn = psycopg2.connect("dbname=nfldb user=postgres password="+pw)
    cur = conn.cursor()

    c = open(os.getcwd()+'\\raw_data\\'+csvfile, 'rb')
    cs = csv.reader(c)
    for row in cs:
        if row[0] in row_tester:
            cur.execute ('SELECT * FROM drafts WHERE draft_year = %s AND draft_round = %s AND overall_pick= %s;',
                        (year,row[0],row[1]))
            duplicate_checker = cur.fetchall()
            if duplicate_checker:
                print('An entry for this draft pick('+str(year)+', Round: '+str(row[0])+', Overall Pick: '
                      +str(row[1])+') already exists, moving to next row of csv')
                continue

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
            split_name = name.split()
            gsis_name = split_name[0][0]+'.'+split_name[1]
            cur.execute('SELECT player_id FROM player WHERE full_name = %s;', (name,))
            player_id = cur.fetchall()
            print(player_id)
            while player_id == []:
                print(row)
                print('Player name from row above does not match nfldb, lets try and find him.')
                split_name = name.split()
                gsis_name = split_name[0][0]+'.'+split_name[1]
                print('searching for players with gsis_name: '+gsis_name+'.')
                cur.execute('SELECT player_id FROM player WHERE gsis_name = %s;',(gsis_name,))
                player_id = cur.fetchall()
                print(player_id)

                while player_id ==[]:
                    z = raw_input('Couldn''t find any players with that name,'
                                  ' would you like to enter a[nother] full name manually? (Y/N)')
                    if z == 'Y':
                        name = raw_input('Enter alternate spelling: ')
                        cur.execute('SELECT player_id FROM player WHERE full_name = %s;', (name,))
                        player_id = cur.fetchall()
                    else:
                        print("okay, fix it yourself")
                        print("here is a start")
                        print('INSERT INTO player('
                              'player_id, gsis_name, full_name, first_name, last_name, team,'
                              '"position", profile_id, profile_url,birthdate,'
                              'college, height, weight, years_pro, status)'
                              'VALUES'
                              '(\'NS-00000XX\',\''+gsis_name+'\',\''+name+'\',\''+split_name[0]+'\',\''+split_name[1]+'\',\'team\','
                              '\''+row[4]+'\',profile_id,\'profile_url\',\'birthdate\',\''+row[27]+'\',height,weight,years_pro,\'Unknown\'')
                        cur.close()
                        conn.close()
                        c.close()
                        return False
                if len(player_id)==1:
                    cur.execute('SELECT * FROM player WHERE player_id = %s;',(player_id[0],))
                    temp_player = cur.fetchall()
                    print(temp_player[0])
                    player_checker = raw_input('We found 1 match, does this look like the correct player for draft year: '
                                      +str(year)+ ', round: '+str(row[0])+', Overall pick: '+str(row[1])+
                                      ', College: '+row[27]+'? (Y/N)')


                    if player_checker == 'Y':
                        break
                    else:
                        print('gsis name or alternate spelling did not match, player might be missing from DB,'
                              ' good luck')
                        cur.close()
                        conn.close()
                        c.close()
                        return False


            if len(player_id)>1:
                try:
                    '''for player in player_id:
                        cur.execute('INSERT INTO drafts (player_id, draft_year, draft_round, overall_pick, team_id) VALUES'
                            '(%s,%s,%s,%s,%s);',
                            (player, year, row[0], row[1],team))'''
                    print("Multiple players have this name. Lets try and figure it out.")
                    '''conn.rollback()'''
                    fixed = False
                    cur.execute('SELECT * FROM player WHERE gsis_name = %s OR full_name = %s;',(gsis_name,name))
                    dpn = cur.fetchall()

                    for item in dpn:
                        print(item)
                        x = raw_input("Does this look like the correct player for draft year: "
                                      +str(year)+", round: "+str(row[0])+", Overall pick: "+str(row[1])+
                                      " College: "+row[27]+"? (Y/N)")
                        if x == 'Y':
                            player_id[0] = item[0]
                            fixed = True
                            break
                        else:
                            print("trying next name..")

                    if fixed == False:
                        print("couldn't find a good match player , please fix manually for:")
                        print(row)
                        print("here is a start")
                        print('INSERT INTO player('
                              'player_id, gsis_name, full_name, first_name, last_name, team,'
                              '"position", profile_id, profile_url,birthdate,'
                              'college, height, weight, years_pro, status)'
                              'VALUES'
                              '(NS-00000XX,'+gsis_name+','+name+','+split_name[0]+','+split_name[1]+',team,'
                              +row[4]+',profile_id,profile_url,birthdate,'+row[27]+',height,weight,years_pro,status')
                        cur.close()
                        conn.close()
                        c.close()
                        return False
                except psycopg2.Error as e:
                    conn.rollback()
                    print('Uh oh, something is wrong')
                    print(e.pgerror)
                    return False
            try:
                cur.execute('INSERT INTO drafts (player_id, draft_year, draft_round, overall_pick, team_id) VALUES'
                            '(%s,%s,%s,%s,%s);',
                            (player_id[0], year, row[0], row[1],team))
            except psycopg2.Error as e:

                conn.rollback()

                print('Uh oh, something is wrong')
                print(e.pgerror)
                return False

            conn.commit()
    cur.close()
    conn.close()
    c.close()
    return True


year_str = raw_input('What year are we working on now? ')
while read_rookie_by_year('years_'+year_str+'_draft_drafts.csv', int(year_str)):
    year_str = raw_input('What year are we working on next? ')
