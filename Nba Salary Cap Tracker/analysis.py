import tkinter as tk
import psycopg2
import matplotlib.pyplot as plt
import math
from PIL import Image, ImageTk
conn = psycopg2.connect(
    dbname="salaries",
    user="postgres",
    host="localhost",
    port="5432"
        )
cur = conn.cursor()
nba_teams = ["Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets", "Chicago Bulls", "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets", "Detroit Pistons", "Golden State Warriors", "Houston Rockets", "Indiana Pacers", "LA Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat", "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks", "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns", "Portland Trail Blazers", "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors", "Utah Jazz", "Washington Wizards"]
nba_teams_dictionary = {"Atlanta Hawks": "ATL", "Boston Celtics": "BOS", "Brooklyn Nets": "BRK", "Charlotte Hornets": "CHO", "Chicago Bulls": "CHI", "Cleveland Cavaliers": "CLE", "Dallas Mavericks": "DAL", "Denver Nuggets": "DEN", "Detroit Pistons": "DET", "Golden State Warriors": "GSW", "Houston Rockets": "HOU", "Indiana Pacers": "IND", "LA Clippers": "LAC", "Los Angeles Lakers": "LAL", "Memphis Grizzlies": "MEM", "Miami Heat": "MIA", "Milwaukee Bucks": "MIL", "Minnesota Timberwolves": "MIN", "New Orleans Pelicans": "NOP", "New York Knicks": "NYK", "Oklahoma City Thunder": "OKC", "Orlando Magic": "ORL", "Philadelphia 76ers": "PHI", "Phoenix Suns": "PHO", "Portland Trail Blazers": "POR", "Sacramento Kings": "SAC", "San Antonio Spurs": "SAS", "Toronto Raptors": "TOR", "Utah Jazz": "UTA", "Washington Wizards": "WAS"}
reversed_nba_teams_dictionary = {"ATL": "Atlanta Hawks", "BOS": "Boston Celtics", "BRK": "Brooklyn Nets", "CHO": "Charlotte Hornets", "CHI": "Chicago Bulls", "CLE": "Cleveland Cavaliers", "DAL": "Dallas Mavericks", "DEN": "Denver Nuggets", "DET": "Detroit Pistons", "GSW": "Golden State Warriors", "HOU": "Houston Rockets", "IND": "Indiana Pacers", "LAC": "LA Clippers", "LAL": "Los Angeles Lakers", "MEM": "Memphis Grizzlies", "MIA": "Miami Heat", "MIL": "Milwaukee Bucks", "MIN": "Minnesota Timberwolves", "NOP": "New Orleans Pelicans", "NYK": "New York Knicks", "OKC": "Oklahoma City Thunder", "ORL": "Orlando Magic", "PHI": "Philadelphia 76ers", "PHO": "Phoenix Suns", "POR": "Portland Trail Blazers", "SAC": "Sacramento Kings", "SAS": "San Antonio Spurs", "TOR": "Toronto Raptors", "UTA": "Utah Jazz", "WAS": "Washington Wizards"}
current_team=""

def team_analysis():
    global current_team
    def view_team():
        global current_team
        nonlocal current
        team_players = []
        selected_team = nba_teams_dictionary[team_var.get()]
        cur.execute(
            "SELECT name,salary FROM player_salaries WHERE team = %s", (selected_team,)
        )
        result = cur.fetchall()
        for player in result:
            team_players.append((player[0], player[1]))
        team_length = len(team_players)
        #formatted_number = "{:,}".format(team_players[current][1])
        #current_player_label.config(text=team_players[current][0] + " Makes $" + formatted_number)

        current=0
        selected_team=nba_teams_dictionary[team_var.get()]
        current_team=team_var.get()
        cur.execute(
            "SELECT sum(salary) FROM player_salaries WHERE team = %s", (selected_team,)
        )
        result = cur.fetchone()
        team_salary=str(result[0])
        team_salary_text = "{:,}".format(result[0])
        team_salary_label.pack()
        team_salary_label.config(text="Team Salary is $"+team_salary_text)
        cur.execute(
            "select team from player_salaries group by team order by sum(salary) desc"
        )
        result = cur.fetchall()
        counter=1
        for team in result:
            if team[0] == selected_team:
                break
            counter=counter+1
        team_rank_label.config(text=team_var.get()+" ranks "+str(counter)+"/30 in salary cap for the 23-24 season")
        team_salary=int(team_salary)
        if(team_salary>first_apron):
            first_apron_label.config(text="First apron? YES")
        else:
            first_apron_label.config(text="First apron? NO")
        if (team_salary > second_apron):
            second_apron_label.config(text="Second apron? YES")
        else:
            second_apron_label.config(text="Second apron? NO")
        cur.execute(
            "SELECT name,salary FROM player_salaries WHERE team = %s", (selected_team,)
        )
        result = cur.fetchall()

        team_players = []
        for player in result:

            team_players.append((player[0],player[1]))
        x_graph=[]
        y_graph=[]
        color_names = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'g', 'tab:blue', 'tab:orange', 'tab:green', 'tab:red',
                       'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']

        for player in team_players:
            x_graph.append(player[0])
            y_graph.append(player[1])
        print(x_graph,"xgra")
        print(y_graph)
        plt.bar(x_graph, y_graph,width=.5,color=color_names)
        plt.xticks(fontsize=10,rotation=90)
        plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x/1e6)) + 'M'))
        plt.xlabel('Players')
        plt.ylabel('Salary')
        plt.title('Player Salary')

        #plt.show()  # Display the graph
        plt.savefig('player_salaries.png', format='png',dpi=300, bbox_inches='tight')
        plt.clf()
        new_image = Image.open("player_salaries.png")
        resized_new_image = new_image.resize((400, 400), Image.LANCZOS)
        new_photo = ImageTk.PhotoImage(resized_new_image)
        image_label.config(image=new_photo)
        image_label.image = new_photo









    for widget in root.winfo_children():
        widget.destroy()
    team_var = tk.StringVar(value="Atlanta Hawks")
    team_combo = tk.OptionMenu(root, team_var, *nba_teams)
    team_combo.pack()
    select_button=tk.Button(root,text="Select",command=view_team)
    select_button.pack()
    team_salary_label = tk.Label(root, text="")
    team_salary_label.pack()
    team_rank_label=tk.Label(root,text="")
    team_rank_label.pack()
    first_apron_label = tk.Label(root,text="")
    first_apron_label.pack()
    second_apron_label = tk.Label(root, text="")
    second_apron_label.pack()
    selected_team = nba_teams_dictionary[team_var.get()]


    current = 0

    def prev():
        team_players=[]
        selected_team = nba_teams_dictionary[team_var.get()]
        cur.execute(
            "SELECT name,salary FROM player_salaries WHERE team = %s", (selected_team,)
        )
        result = cur.fetchall()
        for player in result:
            team_players.append((player[0], player[1]))
        team_length = len(team_players)
        nonlocal current
        print(current)
        if (current == 0):
            current = team_length-1
        else:
            current = current - 1
        number = team_players[current][1]
        formatted_number = "{:,}".format(number)
        current_player_label.config(text=team_players[current][0] + " Makes $" + formatted_number)
        cur.execute(
            "select name from player_salaries order by salary desc"
        )
        result = cur.fetchall()
        counter=1
        for player in result:
            if player[0]==team_players[current][0]:
                print(player[0])
                break
            counter=counter+1
        player_rank_label.config(text="This player is "+str(counter)+"/562 in salary")


    def next():
        team_players = []
        selected_team = nba_teams_dictionary[team_var.get()]
        cur.execute(
            "SELECT name,salary FROM player_salaries WHERE team = %s", (selected_team,)
        )
        result = cur.fetchall()
        for player in result:
            team_players.append((player[0], player[1]))
        nonlocal current
        team_length = len(team_players)
        if (current == team_length - 1):
            current = 0
        else:
            current = current + 1
        number=team_players[current][1]
        formatted_number = "{:,}".format(number)
        current_player_label.config(text=team_players[current][0] + " Makes $" + formatted_number)
        cur.execute(
            "select name from player_salaries order by salary desc"
        )
        result = cur.fetchall()
        counter = 1
        for player in result:
            if player[0] == team_players[current][0]:
                print(player[0])
                break
            counter = counter + 1
        player_rank_label.config(text="This player is " + str(counter) + "/562 in salary")

    image = Image.open("white.png")
    resized_image = image.resize((200, 200), Image.LANCZOS)
    photo = ImageTk.PhotoImage(resized_image)
    image_label = tk.Label(root, image=photo)
    image_label.image = photo
    image_label.pack()
    current_player_label = tk.Label(root, text="Click Next or Previous to view players salaries")
    current_player_label.pack()
    prev_next_frame = tk.Frame(root)
    prev_next_frame.pack()
    previous_player_button = tk.Button(prev_next_frame, text="Previous Player", command=prev)
    previous_player_button.pack(side=tk.LEFT)
    next_player_button = tk.Button(prev_next_frame, text="Next Player", command=next)
    next_player_button.pack(side=tk.LEFT)
    player_rank_label=tk.Label(root,text="")
    player_rank_label.pack()
    go_home_button=tk.Button(root,text="Go back to home screen",command=go_home)
    go_home_button.pack()


    #view_team()

def leauge_analysis():
    for widget in root.winfo_children():
        widget.destroy()
    go_home_button = tk.Button(root, text="Go back to home screen", command=go_home)
    go_home_button.pack()
    cur.execute(
        "select team,sum(salary) from player_salaries group by team order by sum(salary) desc")
    result = cur.fetchall()
    salary_cap_teams_in_order=[]
    salary_cap_sum_in_order=[]
    for team in result:
        print(team)
        salary_cap_teams_in_order.append(reversed_nba_teams_dictionary[team[0]])
        salary_cap_sum_in_order.append(team[1])
    print(salary_cap_teams_in_order)
    teams_text="Highest Salary cap in order:\n"
    counter=1
    counter1=0
    for a in salary_cap_teams_in_order:
        formatted_number = "{:,}".format(salary_cap_sum_in_order[counter1])
        teams_text=teams_text+"Rank"+" "+str(counter)+": "+a+"         Total Salary: $"+formatted_number+"\n"
        counter=counter+1
        counter1=counter1+1
    salary_Cap_order=tk.Label(root,text=teams_text)
    salary_Cap_order.pack()
    def Apron(param):
        if param==1:
            cur.execute(
                "select team from player_salaries group by team having sum(salary)>172346000 order by sum(salary) desc")
        else:
            cur.execute(
                "select team from player_salaries group by team having sum(salary)>182794000 order by sum(salary) desc")
        result = cur.fetchall()
        final_string=""
        for team in result:
            final_string=final_string+reversed_nba_teams_dictionary[team[0]]+"\n"
        salary_Cap_order.config(text=final_string)

    def show_All():
        cur.execute(
            "select team,sum(salary) from player_salaries group by team order by sum(salary) desc")
        result = cur.fetchall()
        salary_cap_teams_in_order = []
        salary_cap_sum_in_order = []
        for team in result:
            print(team)
            salary_cap_teams_in_order.append(reversed_nba_teams_dictionary[team[0]])
            salary_cap_sum_in_order.append(team[1])
        print(salary_cap_teams_in_order)
        teams_text = "Highest Salary cap in order:\n"
        counter = 1
        counter1 = 0
        for a in salary_cap_teams_in_order:
            formatted_number = "{:,}".format(salary_cap_sum_in_order[counter1])
            teams_text = teams_text + "Rank" + " " + str(
                counter) + ": " + a + "         Total Salary: $" + formatted_number + "\n"
            counter = counter + 1
            counter1 = counter1 + 1
        salary_Cap_order.config(text=teams_text)
    def avg_sal():
        cur.execute(
            "select team,sum(salary),count(name) from player_salaries group by team order by sum(salary) desc")
        result = cur.fetchall()
        final_string=""
        for team in result:
            formatted_number = "{:,}".format(round(team[1]/team[2],2))
            final_string=final_string+reversed_nba_teams_dictionary[team[0]]+"         Avg salary per player: $"+str(formatted_number)+"\n"
        salary_Cap_order.config(text=final_string)

    show_all_teams_button=tk.Button(root,text="Show All teams",command=show_All)
    show_all_teams_button.pack()
    first_apron_button=tk.Button(root,text="Show First Apron teams",command=lambda: Apron(1))
    first_apron_button.pack()
    second_apron_button = tk.Button(root, text="Show Second Apron teams", command=lambda: Apron(2))
    second_apron_button.pack()
    avg_player_salary_by_team_button=tk.Button(root,text="Average player Salary by Team",command=avg_sal)
    avg_player_salary_by_team_button.pack()



def player_database():
    for widget in root.winfo_children():
        widget.destroy()
    go_home_button = tk.Button(root, text="Go back to home screen", command=go_home)
    go_home_button.pack()
    pick_text = tk.Text(root, wrap="word", height=50, width=100)
    cur.execute(
        "select name from player_salaries")
    result = cur.fetchall()
    players=""
    for player in result:
        players=players+player[0]+"\n"
    pick_text.pack()
    pick_text.insert(tk.END, players)
    by_team_fram=tk.Frame(root)
    by_team_fram.pack()
    by_team_Label=tk.Label(by_team_fram,text="Players who make more than $64,343")
    by_team_Label.pack(side=tk.LEFT)
    #by_team_entry=tk.Entry(by_team_fram)
   #by_team_entry.pack()
    def update_slider(value):
        formatted_number = "{:,}".format(int(value))
        by_team_Label.config(text="Players who make more than $"+formatted_number)
        print(value)
        cur.execute(
            "select name from player_salaries where salary>%s",(value,))
        result = cur.fetchall()
        print(result)
        final_string=""
        for player in result:
            final_string=final_string+player[0]+"\n"
        pick_text.delete("1.0", tk.END)
        pick_text.insert(tk.END, final_string)


    by_team_slider = tk.Scale(by_team_fram, from_=64342, to=51915614, orient=tk.HORIZONTAL,command=update_slider,length=600,showvalue=False,resolution=1)
    by_team_slider.pack(side=tk.LEFT)




def go_home():
    for widget in root.winfo_children():
        widget.destroy()
    team_analysis_button = tk.Button(root, text="Team Analysis", command=team_analysis)
    team_analysis_button.pack()
    leauge_analysis_button = tk.Button(root,text="Leauge Analysis",command=leauge_analysis)
    leauge_analysis_button.pack()
    player_database_button = tk.Button(root, text="Player Database Button", command=player_database)
    player_database_button.pack()

first_apron = 172346000
second_apron = 182794000
root = tk.Tk()
root.title("Salary Analysis")
root.geometry("900x900")
team_analysis_button=tk.Button(root,text="Team Analysis",command=team_analysis)
team_analysis_button.pack()
leauge_analysis_button = tk.Button(root,text="Leauge Analysis",command=leauge_analysis)
leauge_analysis_button.pack()
player_database_button=tk.Button(root,text="Player Database Button",command=player_database)
player_database_button.pack()
root.mainloop()