import tkinter as tk
import csv
import matplotlib.pyplot as plt
class PlayerDataBase:
    def __init__(self, player_name, team_name, GP, MPG, PPG, FGM, FGA, FG_PERCENT,
                 TPM, TPA, TP_PERCENT, FTM, FTA, FT_PERCENT, ORB, DRB, RBG,
                 APG, SPG, BPG, TOV, PF, year):
        self.player_name = player_name
        self.team_name = team_name
        self.GP = GP
        self.MPG = MPG
        self.PPG = PPG
        self.FGM = FGM
        self.FGA = FGA
        self.FG_PERCENT = FG_PERCENT
        self.TPM = TPM
        self.TPA = TPA
        self.TP_PERCENT = TP_PERCENT
        self.FTM = FTM
        self.FTA = FTA
        self.FT_PERCENT = FT_PERCENT
        self.ORB = ORB
        self.DRB = DRB
        self.RBG = RBG
        self.APG = APG
        self.SPG = SPG
        self.BPG = BPG
        self.TOV = TOV
        self.PF = PF
        self.year = year
all_players=[]
players_who_fit_criteria=[]

root = tk.Tk()
root.title("My Tkinter Window")
root.geometry("800x800")


def get_stat_index(st, pl):
    if st == "Player":
        return pl.player_name
    if st == "Team":
        return pl.team_name
    if st == "GP":
        return pl.GP
    if st == "MPG":
        return pl.MPG
    if st == "PPG":
        return pl.PPG
    if st == "FGM":
        return pl.FGM
    if st == "FGA":
        return pl.FGA
    if st == "FG_PERCENT":
        return pl.FG_PERCENT
    if st == "3PM":
        return pl.TPM
    if st == "3PA":
        return pl.TPA
    if st == "FTM":
        return pl.FTM
    if st == "FTA":
        return pl.FTA
    if st == "FT_PERCENT":
        return pl.FT_PERCENT
    if st == "ORB":
        return pl.ORB
    if st == "DRB":
        return pl.DRB
    if st == "RBG":
        return pl.RBG
    if st == "APG":
        return pl.APG
    if st == "SPG":
        return pl.SPG
    if st == "BPG":
        return pl.BPG
    if st == "TOV":
        return pl.TOV
    if st == "PF":
        return pl.PF




def get_stat_between_two_years():
    def get_graph(option):
        global players_who_fit_criteria
        players_who_fit_criteria=[]
        start_year=selected_year.get()
        start_year=int(start_year)
        og_start_year=int(start_year)
        end_year=selected_year1.get()
        end_year=int(end_year)
        stat_sel=selected_stat.get()
        game_sel=selected_game.get()
        minutes_sel=selected_minutes.get()
        if minutes_sel=="None":
            minutes_sel=0
        if game_sel=="None":
            game_sel=0
        exit=0
        final_values=[]
        while exit == 0:
            temp_values=[]
            for player in all_players:
                if int(player.year)==start_year and float(minutes_sel)<=float(player.MPG) and float(game_sel)<=float(player.GP):
                    return_val=get_stat_index(stat_sel,player)
                    if return_val=="-":
                        return_val=0
                    temp_values.append(return_val)
                    temp_player = (player.player_name, player.year)
                    players_who_fit_criteria.append(temp_player)
            sum=0
            for value in temp_values:
                sum=sum+float(value)
            if len(temp_values) == 0:
                final_values.append(0)
            else:
                print(len(temp_values))
                sum = sum / len(temp_values)
                final_values.append(sum)

            start_year=start_year+1
            if start_year>end_year:
                exit = 1
        x_vals=list(range(og_start_year,end_year+1))
        y_vals=final_values
        print(len(x_vals),len(y_vals))


        if og_start_year==end_year:
            end_year=end_year+1
        if option!=2:
            plt.figure(figsize=(8, 5))
            plt.plot(x_vals, y_vals, marker='o', linestyle='-', color='b', label='Line 1')
            plt.xlabel('Year')
            plt.ylabel(stat_sel)
            plt.title(f"Average {stat_sel} between the years {og_start_year} and {end_year} per year")
            plt.xlim(og_start_year, end_year)
            plt.show()
        players_who_fit_criteria_text_box_string=""
        player_criteria_text_box.delete("1.0", tk.END)
        if len(players_who_fit_criteria)==0:
            players_who_fit_criteria_text_box_string="NO PLAYERS FIT CRITERIA"


        for player in players_who_fit_criteria:
            players_who_fit_criteria_text_box_string=players_who_fit_criteria_text_box_string+f"{player[0]} {player[1]} \n"
        player_criteria_text_box.insert(tk.END, players_who_fit_criteria_text_box_string)
        if option==2:
            exit=0
            year=og_start_year
            count_by_year=[]
            while exit==0:
                count_players_for_this_year=0
                for player in players_who_fit_criteria:
                    print(player[1])
                    if int(player[1])==year:
                        count_players_for_this_year=count_players_for_this_year+1
                count_by_year.append(count_players_for_this_year)
                year=year+1
                if year>end_year:
                    exit=1
            x_vals = list(range(og_start_year, end_year + 1))
            print(count_by_year)
            plt.figure(figsize=(10, 6))  # Optional: specify the figure size
            plt.bar(x_vals, count_by_year, color='blue')
            plt.xlabel('Year')
            plt.ylabel("Number of players who fit criteria")
            plt.title(f"Number of players per year who average more than {minutes_sel} minutes  and {game_sel} games played per year")
            plt.xlim(og_start_year, end_year)
            plt.show()





    for widget in root.winfo_children():
        widget.destroy()
    year_frame=tk.Frame(root)
    year_frame.pack()
    select_year_label=tk.Label(year_frame,text="Select A Start Year: ")
    select_year_label.pack(side=tk.LEFT)
    years = list(range(1947, 2025))
    selected_year = tk.StringVar(root)
    selected_year.set(years[0])
    year_dropdown = tk.OptionMenu(year_frame, selected_year, *years)
    year_dropdown.pack(side=tk.LEFT)


    year_frame1 = tk.Frame(root)
    year_frame1.pack()
    select_year_label1 = tk.Label(year_frame1, text="Select A End Year: ")
    select_year_label1.pack(side=tk.LEFT)
    years = list(range(1947, 2025))
    selected_year1 = tk.StringVar(root)
    selected_year1.set(years[0])
    year_dropdown1= tk.OptionMenu(year_frame1, selected_year1, *years)
    year_dropdown1.pack(side=tk.LEFT)


    stats = [ "GP", "MPG", "PPG", "FGM", "FGA", "FG_PERCENT", "3PM", "3PA", "3P_PERCENT", "FTM",
                   "FTA", "FT_PERCENT", "ORB", "DRB", "RBG", "APG", "SPG", "BPG", "TOV", "PF",]
    stat_frame=tk.Frame(root)
    stat_frame.pack()
    select_stat_label = tk.Label(stat_frame, text="Select A Stat")
    select_stat_label.pack(side=tk.LEFT)
    selected_stat = tk.StringVar(root)
    selected_stat.set(stats[0])
    stat_dropdown = tk.OptionMenu(stat_frame, selected_stat, *stats)
    stat_dropdown.pack(side=tk.LEFT)

    games_frame=tk.Frame(root)
    games_frame.pack()
    games=list(range(0,83))
    games_label=tk.Label(games_frame,text="Select Mininum Games")
    games_label.pack(side=tk.LEFT)
    selected_game = tk.StringVar(root)
    selected_game.set(games[0])
    game_dropdown = tk.OptionMenu(games_frame, selected_game, *games)
    game_dropdown.pack(side=tk.LEFT)

    minutes_frame = tk.Frame(root)
    minutes_frame.pack()
    minutes = list(range(0, 49))
    minutes_label = tk.Label(minutes_frame, text="Select Mininum Minutes")
    minutes_label.pack(side=tk.LEFT)
    selected_minutes = tk.StringVar(root)
    selected_minutes.set(minutes[0])
    minutes_dropdown = tk.OptionMenu(minutes_frame, selected_minutes, *minutes)
    minutes_dropdown.pack(side=tk.LEFT)



    confirm_button=tk.Button(root,text="Make Graph/Get Players who Meet Criteria",command=lambda: get_graph(1))
    confirm_button.pack()
    confirm_button1 = tk.Button(root, text="Get number of players per year who fit this criteria for GP OR MP OR BOTH/Get Players who Meet Criteria", command=lambda: get_graph(2))
    confirm_button1.pack()

    player_criteria_label=tk.Label(root,text="Players who meet this criteria(scroll to see all):")
    player_criteria_label.pack()
    player_criteria_text_box = tk.Text(root, height=30, width=50)  # Adjust height and width as needed
    player_criteria_text_box.pack()
    back_button = tk.Button(root, text="Go to main menu", command=home)
    back_button.pack()






with open("ALLRECORDS.csv", mode='r', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        player = PlayerDataBase(
            player_name=row[1],
            team_name=row[2],
            GP=row[3],
            MPG=row[4],
            PPG=row[5],
            FGM=row[6],
            FGA=row[7],
            FG_PERCENT=row[8],
            TPM=row[9],
            TPA=row[10],
            TP_PERCENT=row[11],
            FTM=row[12],
            FTA=row[13],
            FT_PERCENT=row[14],
            ORB=row[15],
            DRB=row[16],
            RBG=row[17],
            APG=row[18],
            SPG=row[19],
            BPG=row[20],
            TOV=row[21],
            PF=row[22],
            year=row[23]
        )
        all_players.append(player)
def get_selected_stats():
    for widget in root.winfo_children():
        widget.destroy()
    def players_who_meet_critera(option):
        f=0
        def get_number_of_players_for_year(yr):
            counter=0
            for player in all_players:
                if int(player.year)==yr:
                    counter=counter+1
            return counter

        start_year = selected_year.get()
        start_year = int(start_year)
        og_start_year = int(start_year)
        end_year = selected_year1.get()
        end_year = int(end_year)
        game_sel = selected_game.get()
        minutes_sel = selected_minutes.get()
        minutes_sel=int(minutes_sel)
        points_sel=selected_points.get()
        point_sel=int(points_sel)
        fgm_sel=selected_fgm.get()
        fgm_sel=int(fgm_sel)
        fga_sel=selected_fga.get()
        fga_sel=int(fga_sel)
        fgp_sel=selected_fgp.get()
        fgp_sel=float(fgp_sel)
        tpm_sel=selected_tpm.get()
        tpm_sel=int(tpm_sel)
        tpa_sel=selected_tpa.get()
        tpa_sel=int(tpa_sel)
        tpp_sel=selected_tpp.get()
        tpp_sel=float(tpp_sel)
        rb_sel=selected_rb.get()
        rb_sel=int(rb_sel)
        blk_sel=selected_blk.get()
        blk_sel=int(blk_sel)
        exit=0
        players_who_fit=[]
        y_arr=[]
        while exit==0:
            count=0
            for player in all_players:
                if player.MPG=="-":
                    player.MPG=0
                if player.GP=="-":
                    player.GP=0
                if player.FGM=="-":
                    player.FGM=0
                if player.FGA=="-":
                    player.FGA=0
                if player.FG_PERCENT=="-":
                    player.FG_PERCENT=0
                if player.TPM=="-":
                    player.TPM=0
                if player.TPA=="-":
                    player.TPA=0
                if player.TP_PERCENT=="-":
                    player.TP_PERCENT=0
                if player.RBG=="-":
                    player.RBG=0
                if player.BPG=="-":
                    player.BPG=0


                if float(player.MPG) >= float(minutes_sel) and float(player.GP) >= float(game_sel):
                    if float(player.FGM) >= float(fgm_sel) and float(player.FGA)>=float(fga_sel):
                        if float(player.FG_PERCENT)>=float(fgp_sel) and float(player.TPM)>=float(tpm_sel):
                            if float(player.TPA)>=float(tpa_sel) and float(player.TP_PERCENT)>=float(tpp_sel):
                                if float(player.RBG)>=float(rb_sel) and float(player.BPG)>=float(blk_sel):
                                    if int(start_year)==int(player.year) and float(player.PPG)>=float(point_sel):
                                        print("f")
                                        players_who_fit.append((player.player_name,start_year))
                                        count=count+1
            y_arr.append(count)
            start_year=start_year+1
            if start_year>end_year:
                exit=1
        x_arr = list(range(og_start_year, end_year+1))
        print(len(x_arr),len(y_arr))
        if option==1:
            plt.figure(figsize=(8, 5))
            plt.plot(x_arr, y_arr, marker='o', linestyle='-', color='b', label='Line 1')
            plt.xlabel('Year')
            plt.ylabel('Number of players who meet criteria')
            final_string=f"Players with mpg > {minutes_sel},gp > {game_sel},ppg > {point_sel}\n"
            final_string=final_string+f"fgm > {fgm_sel},fga > {fga_sel},fg % > {fgp_sel}\n"
            final_string=final_string+f"tpm > {tpm_sel},tpa > {tpa_sel},3pt% > {tpp_sel}\n"
            final_string=final_string+f"reb > {rb_sel},blk > {blk_sel}"
            plt.title(final_string)
            if og_start_year==end_year:
                end_year=end_year+1
            plt.xlim(og_start_year, end_year)
            plt.show()
        else:

            index=0
            for temp in range(og_start_year,end_year+1):
                total_players=get_number_of_players_for_year(temp)
                y_arr[index]=y_arr[index]/total_players
                index=index+1

            plt.figure(figsize=(10, 6))  # Optional: specify the figure size
            plt.bar(x_arr, y_arr, color='blue')
            plt.xlabel('Year')
            plt.ylabel("Percemt of players who fit criteria")
            final_string = f"Percent of players per year with mpg > {minutes_sel},gp > {game_sel},ppg > {point_sel}\n"
            final_string = final_string + f"fgm > {fgm_sel},fga > {fga_sel},fg % > {fgp_sel}\n"
            final_string = final_string + f"tpm > {tpm_sel},tpa > {tpa_sel},3pt% > {tpp_sel}\n"
            final_string = final_string + f"reb > {rb_sel},blk > {blk_sel}"
            plt.title(final_string)
            plt.xlim(og_start_year, end_year)
            plt.show()


        players_who_fit_string=""
        for player in players_who_fit:
            players_who_fit_string=players_who_fit_string+f"{player[0]} {player[1]}\n"
        if len(players_who_fit)==0:
            players_who_fit_string="NO PLAYER FITS CRITERIA"
        player_criteria_text_box.delete("1.0", tk.END)
        player_criteria_text_box.insert(tk.END, players_who_fit_string)




        #for player in players_who_fit:




    year_frame = tk.Frame(root)
    year_frame.pack()
    select_year_label = tk.Label(year_frame, text="Select A Start Year: ")
    select_year_label.pack(side=tk.LEFT)
    years = list(range(1947, 2025))
    selected_year = tk.StringVar(root)
    selected_year.set(years[0])
    year_dropdown = tk.OptionMenu(year_frame, selected_year, *years)
    year_dropdown.pack(side=tk.LEFT)

    year_frame1 = tk.Frame(root)
    year_frame1.pack()
    select_year_label1 = tk.Label(year_frame1, text="Select A End Year: ")
    select_year_label1.pack(side=tk.LEFT)
    years = list(range(1947, 2025))
    selected_year1 = tk.StringVar(root)
    selected_year1.set(years[0])
    year_dropdown1 = tk.OptionMenu(year_frame1, selected_year1, *years)
    year_dropdown1.pack(side=tk.LEFT)

    games_frame = tk.Frame(root)
    games_frame.pack()
    games = list(range(0, 83))
    games_label = tk.Label(games_frame, text="Select Mininum Games")
    games_label.pack(side=tk.LEFT)
    selected_game = tk.StringVar(root)
    selected_game.set(games[0])
    game_dropdown = tk.OptionMenu(games_frame, selected_game, *games)
    game_dropdown.pack(side=tk.LEFT)

    minutes_frame = tk.Frame(root)
    minutes_frame.pack()
    minutes = list(range(0, 49))
    minutes_label = tk.Label(minutes_frame, text="Select Mininum Minutes")
    minutes_label.pack(side=tk.LEFT)
    selected_minutes = tk.StringVar(root)
    selected_minutes.set(minutes[0])
    minutes_dropdown = tk.OptionMenu(minutes_frame, selected_minutes, *minutes)
    minutes_dropdown.pack(side=tk.LEFT)

    points_frame = tk.Frame(root)
    points_frame.pack()
    points = list(range(0, 49))
    points_label = tk.Label(points_frame, text="Select Mininum Points Per Game")
    points_label.pack(side=tk.LEFT)
    selected_points = tk.StringVar(root)
    selected_points.set(points[0])
    points_dropdown = tk.OptionMenu(points_frame, selected_points, *points)
    points_dropdown.pack(side=tk.LEFT)

    fgm_frame = tk.Frame(root)
    fgm_frame.pack()
    fgm = list(range(0, 49))
    fgm_label = tk.Label(fgm_frame, text="Select Mininum FGM Per Game")
    fgm_label.pack(side=tk.LEFT)
    selected_fgm = tk.StringVar(root)
    selected_fgm.set(fgm[0])
    fgm_dropdown = tk.OptionMenu(fgm_frame, selected_fgm, *fgm)
    fgm_dropdown.pack(side=tk.LEFT)

    fga_frame = tk.Frame(root)
    fga_frame.pack()
    fga = list(range(0, 49))
    fga_label = tk.Label(fga_frame, text="Select Mininum FGA Per Game")
    fga_label.pack(side=tk.LEFT)
    selected_fga = tk.StringVar(root)
    selected_fga.set(fga[0])
    fga_dropdown = tk.OptionMenu(fga_frame, selected_fga, *fga)
    fga_dropdown.pack(side=tk.LEFT)

    fgp_frame = tk.Frame(root)
    fgp_frame.pack()
    fgp = [i / 100.0 for i in range(0, 101)]
    fgp_label = tk.Label(fgp_frame, text="Select Mininum FG Percent Per Game")
    fgp_label.pack(side=tk.LEFT)
    selected_fgp = tk.StringVar(root)
    selected_fgp.set(fgp[0])
    fgp_dropdown = tk.OptionMenu(fgp_frame, selected_fgp, *fgp)
    fgp_dropdown.pack(side=tk.LEFT)

    tpm_frame = tk.Frame(root)
    tpm_frame.pack()
    tpm = list(range(0, 49))
    tpm_label = tk.Label(tpm_frame, text="Select Mininum TPM Per Game")
    tpm_label.pack(side=tk.LEFT)
    selected_tpm = tk.StringVar(root)
    selected_tpm.set(tpm[0])
    tpm_dropdown = tk.OptionMenu(tpm_frame, selected_tpm, *tpm)
    tpm_dropdown.pack(side=tk.LEFT)

    tpa_frame = tk.Frame(root)
    tpa_frame.pack()
    tpa = list(range(0, 49))
    tpa_label = tk.Label(tpa_frame, text="Select Mininum TPA Per Game")
    tpa_label.pack(side=tk.LEFT)
    selected_tpa = tk.StringVar(root)
    selected_tpa.set(tpa[0])
    tpa_dropdown = tk.OptionMenu(tpa_frame, selected_tpa, *tpa)
    tpa_dropdown.pack(side=tk.LEFT)

    tpp_frame = tk.Frame(root)
    tpp_frame.pack()
    tpp = [i / 100.0 for i in range(0, 101)]
    tpp_label = tk.Label(tpp_frame, text="Select Mininum Three Point Percentage Per Game")
    tpp_label.pack(side=tk.LEFT)
    selected_tpp = tk.StringVar(root)
    selected_tpp.set(tpp[0])
    tpp_dropdown = tk.OptionMenu(tpp_frame, selected_tpp, *tpp)
    tpp_dropdown.pack(side=tk.LEFT)

    rb_frame = tk.Frame(root)
    rb_frame.pack()
    rb = list(range(0, 49))
    rb_label = tk.Label(rb_frame, text="Select Mininum Rebounds Per Game")
    rb_label.pack(side=tk.LEFT)
    selected_rb = tk.StringVar(root)
    selected_rb.set(rb[0])
    rb_dropdown = tk.OptionMenu(rb_frame, selected_rb, *rb)
    rb_dropdown.pack(side=tk.LEFT)

    blk_frame = tk.Frame(root)
    blk_frame.pack()
    blk = list(range(0, 49))
    blk_label = tk.Label(blk_frame, text="Select Mininum Blocks Per Game")
    blk_label.pack(side=tk.LEFT)
    selected_blk = tk.StringVar(root)
    selected_blk.set(blk[0])
    blk_dropdown = tk.OptionMenu(blk_frame, selected_blk, *blk)
    blk_dropdown.pack(side=tk.LEFT)

    graph_players_who_meet_criteria_button=tk.Button(root,text="Players who meet criteria",command=lambda: players_who_meet_critera(1))
    graph_players_who_meet_criteria_button.pack()

    graph_get_percent_button=tk.Button(root,text="Get percent of players per year who meet criteria",command=lambda: players_who_meet_critera(2))
    graph_get_percent_button.pack()

    player_criteria_text_box = tk.Text(root, height=30, width=50)  # Adjust height and width as needed
    player_criteria_text_box.pack()
    back_button=tk.Button(root,text="Go to main menu",command=home)
    back_button.pack()
def home():
    for widget in root.winfo_children():
        widget.destroy()
    get_stat_button = tk.Button(root, text="Get average stat per year between two selected years",
                                command=get_stat_between_two_years)
    get_stat_button.pack()
    get_selected_stats_button = tk.Button(root, text="Get players selected stats between two years",
                                          command=get_selected_stats)
    get_selected_stats_button.pack()



get_stat_button=tk.Button(root,text="Get average stat per year between two selected years",command=get_stat_between_two_years)
get_stat_button.pack()
get_selected_stats_button=tk.Button(root,text="Get players selected stats between two years",command=get_selected_stats)
get_selected_stats_button.pack()

root.mainloop()