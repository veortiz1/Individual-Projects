import psycopg2
import csv
conn = psycopg2.connect(
    dbname="salaries",
    user="postgres",
    host="localhost",
    port="5432"
        )
cur = conn.cursor()
player_salaries=[]
with open("salaries.csv", mode='r', newline='') as file:
    csv_reader = csv.reader(file)

    for row in csv_reader:
        print(row)
        #current_player = ro.split(",")
        player_salaries.append((row[1],row[2],row[3]))

    print(player_salaries)
for player in player_salaries:
    temp = player[2]
    if temp == "":
        temp = "0"
    else:
        temp = temp[1:]
    cur.execute("INSERT INTO player_salaries (name,team,salary) VALUES (%s,%s,%s)", (player[0],player[1],temp))
    conn.commit()