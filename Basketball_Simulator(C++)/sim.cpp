#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <thread>
#include <chrono>
#include <fstream>
#include <tuple>
#include <sstream>
#include <random>
#include <algorithm>
std::string team1;
std::string team2;
int team1_score = 0;
int team2_score = 0;
int whosball = 1;
int itwasamake = 0;
struct player //use to keep track of each player on a team
{
    std::string name;
    std::string position;
    int three;
    int two;
    int stl;
    int blk;
    int reb;
    int pass;
};

struct stats //used for keeping track of each players stats
{
    std::string name;
    int fg = 0;
    int fgm = 0;
    int tpa = 0;
    int tpm = 0;
    int reb = 0;
    int ast = 0;
    int blk = 0;
    int stl = 0;
    int to = 0;
};
//vectors to keep track of player stats for team1  and team 2 
std::vector<stats> team1_boxscore; 
std::vector<stats> team2_boxscore; 

void chooseteams() //function to pick teams to play eachother
{
    std::ifstream inputFile("Teams.txt");
    std::string line;
    std::vector<std::string> teams;
    int counter = 1;
    while (std::getline(inputFile, line)) //goes through each line of teams file
    {
        if (counter == 0) //if line =="TEAM" add it to the team array
        {
            teams.push_back(line); 
        }
        if (line == "TEAM")
        {
            counter = 0;
        }
        else
        {
            counter = 1;
        }
    }

    int exit = 0;
    int team1chosen = 0;
    std::string tea1;
    while (exit == 0)
    {
        if (team1chosen == 1) //if a first team is picked already
        {
            std::cout << "Enter Name of the second Team you want to choose!" << std::endl
                      << "List of teams: " << std::endl;
        }
        else
        {
            std::cout << "Enter Name of Team you want to choose!" << std::endl
                      << "List of teams: " << std::endl;
        }
        for (int i = 0; i < teams.size(); ++i) //display the teams
        {
            std::cout << teams[i] << std::endl;
        }
        std::cin >> tea1;
        if (team1chosen == 0) //if team isnt chosen yet
        {
            int found = 0;
            for (int i = 0; i < teams.size(); ++i)
            {
                if (teams[i] == tea1)
                {
                    team1 = tea1;
                    found = 1;
                }
            }
            if (found == 1)
            {
                team1chosen = 1;
            }
            else
            {
                std::cout << std::endl
                          << "Error invalid team name" << std::endl;
            }
        }
        else
        {
            int found = 0;
            for (int i = 0; i < teams.size(); ++i)
            {
                if (teams[i] == tea1)
                {
                    team2 = tea1;
                    found = 1;
                }
            }
            if (found == 1)
            {
                exit = 1;
            }
            else
            {
                std::cout << std::endl
                          << "Error invalid team name" << std::endl;
            }
        }
    }
}

std::vector<player> getplayers(std::string t1)
{
    std::ifstream inputFile("Teams.txt");
    std::string line;
    int playerline = 0;
    int counter = 1;
    std::vector<std::string> player_line;
    while (std::getline(inputFile, line))
    {
        if (line == t1)
        {
            playerline = 1;
        }
        if (playerline == 1)
        {
            player_line.push_back(line);

            counter = counter + 1;
            if (counter == 7)
            {
                break;
            }
        }
    }
    std::vector<player> team;
    for (int i = 1; i < player_line.size(); ++i)
    {
        std::stringstream playe(player_line[i]);
        std::string attribute;
        player player1;
        int count = 1;
        while (std::getline(playe, attribute, ','))
        {
            if (count == 1)
            {
                player1.name = attribute;
            }
            if (count == 2)
            {
                player1.position = attribute;
            }
            if (count == 3)
            {
                player1.three = std::stoi(attribute);
            }
            if (count == 4)
            {
                player1.two = std::stoi(attribute);
            }
            if (count == 5)
            {
                player1.stl = std::stoi(attribute);
            }
            if (count == 6)
            {
                player1.blk = std::stoi(attribute);
            }
            if (count == 7)
            {
                player1.reb = std::stoi(attribute);
            }
            if (count == 8)
            {
                player1.pass = std::stoi(attribute);
            }
            count = count + 1;
        }
        team.push_back(player1);
    }
    return team;
}

int whosassist(std::vector<player> tm1)
{
    std::vector<int> player;
    for (int i = 0; i < tm1.size(); ++i)
    {
        if (tm1[i].pass >= 90)
        {
            player.insert(player.end(), 100, i);
        }
        else if (tm1[i].pass >= 80)
        {
            player.insert(player.end(), 60, i);
        }
        else if (tm1[i].pass >= 70)
        {
            player.insert(player.end(), 40, i);
        }
        else if (tm1[i].pass >= 60)
        {
            player.insert(player.end(), 20, i);
        }
        else
        {
            player.insert(player.end(), 10, i);
        }
    }
    std::random_device rd;
    std::shuffle(std::begin(player), std::end(player), rd);
    return player[0];
}

int whosrebound(std::vector<player> tm1)
{
    std::vector<int> player;
    for (int i = 0; i < tm1.size(); ++i)
    {
        if (tm1[i].reb >= 90)
        {
            player.insert(player.end(), 100, i);
        }
        else if (tm1[i].reb >= 80)
        {
            player.insert(player.end(), 80, i);
        }
        else if (tm1[i].reb >= 70)
        {
            player.insert(player.end(), 60, i);
        }
        else if (tm1[i].reb >= 60)
        {
            player.insert(player.end(), 40, i);
        }
        else
        {
            player.insert(player.end(), 20, i);
        }
    }
    std::random_device rd;
    std::shuffle(std::begin(player), std::end(player), rd);
    return player[0];
}
std::string gettime(int value)
{
    int minutes = value / 60;
    int seconds = value % 60;
    std::stringstream ss;
    ss << minutes << ":" << std::setw(2) << std::setfill('0') << seconds;

    return ss.str();
}

std::string assist()
{
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> distr(0, 1);
    int yesorno = distr(gen);

    if (yesorno == 1)
    {
        return "yes";
    }
    else
    {
        return "no";
    }
}

void random_event_call(std::vector<player> tm1, int ball, std::vector<player> tm2)
{
    int i = 0;
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> distr(0, 10);
    int event = distr(gen);
    if (event >= 0 && event <= 7)
    { // shot
        // 3pt
        std::vector<std::string> tpa;
        if (event >= 0 && event <= 2)
        {
            if (tm1[i].three >= 90)
            {
                tpa.insert(tpa.end(), 90, tm1[i].name);
            }
            else if (tm1[i].three >= 80)
            {
                tpa.insert(tpa.end(), 60, tm1[i].name);
            }
            else if (tm1[i].three >= 70)
            {
                tpa.insert(tpa.end(), 30, tm1[i].name);
            }
            else if (tm1[i].three >= 60)
            {
                tpa.insert(tpa.end(), 15, tm1[i].name);
            }
            else
            {
                tpa.insert(tpa.end(), 3, tm1[i].name);
            }
        }
        else
        {
            for (int i = 0; i < tm1.size(); ++i)
            {
                if (tm1[i].two >= 90)
                {
                    tpa.insert(tpa.end(), 90, tm1[i].name);
                }
                else if (tm1[i].two >= 80)
                {
                    tpa.insert(tpa.end(), 60, tm1[i].name);
                }
                else if (tm1[i].two >= 70)
                {
                    tpa.insert(tpa.end(), 30, tm1[i].name);
                }
                else if (tm1[i].two >= 60)
                {
                    tpa.insert(tpa.end(), 15, tm1[i].name);
                }
                else
                {
                    tpa.insert(tpa.end(), 3, tm1[i].name);
                }
            }
        }
        
        std::random_device rd;
        std::shuffle(std::begin(tpa), std::end(tpa), rd);

        std::string whoshot = tpa[0];
        std::string yesorno = "no";
        std::vector<std::string> yorn;
        if (event >= 0 && event <= 2)
        {
            for (int i = 0; i < tm1.size(); ++i)
            {
                if (whoshot == tm1[i].name)
                {
                    if (tm1[i].three >= 90)
                    {
                        yorn.insert(yorn.end(), 50, "yes");
                        yorn.insert(yorn.end(), 50, "no");
                    }
                    else if (tm1[i].three >= 80)
                    {
                        yorn.insert(yorn.end(), 40, "yes");
                        yorn.insert(yorn.end(), 60, "no");
                    }
                    else if (tm1[i].three >= 70)
                    {
                        yorn.insert(yorn.end(), 30, "yes");
                        yorn.insert(yorn.end(), 70, "no");
                    }
                    else if (tm1[i].three >= 60)
                    {
                        yorn.insert(yorn.end(), 20, "yes");
                        yorn.insert(yorn.end(), 80, "no");
                    }
                    else
                    {
                        yorn.insert(yorn.end(), 10, "yes");
                        yorn.insert(yorn.end(), 90, "no");
                    }
                }
            }
        }
        else
        { // 2pter
            for (int i = 0; i < tm1.size(); ++i)
            {
                if (whoshot == tm1[i].name)
                {
                    if (tm1[i].three >= 90)
                    {
                        yorn.insert(yorn.end(), 70, "yes");
                        yorn.insert(yorn.end(), 30, "no");
                    }
                    else if (tm1[i].three >= 80)
                    {
                        yorn.insert(yorn.end(), 60, "yes");
                        yorn.insert(yorn.end(), 40, "no");
                    }
                    else if (tm1[i].three >= 70)
                    {
                        yorn.insert(yorn.end(), 55, "yes");
                        yorn.insert(yorn.end(), 45, "no");
                    }
                    else if (tm1[i].three >= 60)
                    {
                        yorn.insert(yorn.end(), 45, "yes");
                        yorn.insert(yorn.end(), 65, "no");
                    }
                    else
                    {
                        yorn.insert(yorn.end(), 40, "yes");
                        yorn.insert(yorn.end(), 60, "no");
                    }
                }
            }
        }
        std::random_device rd1;
        std::shuffle(std::begin(yorn), std::end(yorn), rd1);
        yesorno = yorn[0];
        if (ball == 1)
        {
            for (int i = 0; i < team1_boxscore.size(); ++i)
            {
                if (team1_boxscore[i].name == whoshot)
                {
                    if (yesorno == "yes")
                    {
                        itwasamake = 1;
                        if (event >= 0 && event <= 2)
                        {
                            team1_boxscore[i].tpa = team1_boxscore[i].tpa + 1;
                            team1_boxscore[i].tpm = team1_boxscore[i].tpm + 1;
                            team1_score = team1_score + 3;
                            std::string was_it_assist = assist();
                            if (was_it_assist == "yes")
                            {
                                int whosast = whosassist(tm1);
                                team1_boxscore[whosast].ast = team1_boxscore[whosast].ast + 1;
                                std::cout << "THREE Pointer by " << team1_boxscore[i].name << " Assisted By " << team1_boxscore[whosast].name << std::endl;
                            }
                            else
                            {
                                std::cout << "THREE Pointer by " << team1_boxscore[i].name << std::endl;
                            }
                        }
                        else
                        {
                            team1_boxscore[i].fg = team1_boxscore[i].fg + 1;
                            team1_boxscore[i].fgm = team1_boxscore[i].fgm + 1;
                            team1_score = team1_score + 2;
                            std::string was_it_assist = assist();
                            if (was_it_assist == "yes")
                            {
                                int whosast = whosassist(tm1);
                                team1_boxscore[whosast].ast = team1_boxscore[whosast].ast + 1;
                                std::cout << "TWO Pointer by " << team1_boxscore[i].name << " Assisted By " << team1_boxscore[whosast].name << std::endl;
                            }
                            else
                            {
                                std::cout << "TWO Pointer by " << team1_boxscore[i].name << std::endl;
                            }
                        }
                        whosball = 2;
                    }
                    else
                    {
                        if (event >= 0 && event <= 2)
                        {
                            team1_boxscore[i].tpa = team1_boxscore[i].tpa + 1;
                        }
                        else
                        {
                            team1_boxscore[i].fg = team1_boxscore[i].fg + 1;
                        }

                        std::random_device rd;
                        std::mt19937 gen(rd());
                        std::uniform_int_distribution<> distr(0, 10);
                        int rebound = distr(gen);
                        if (rebound >= 0 && rebound < 9)
                        {
                            whosball = 2;

                            int rebound = whosrebound(tm2);
                            team2_boxscore[rebound].reb = team2_boxscore[rebound].reb + 1;
                            std::cout << std::endl
                                      << "Missed Shot by " << whoshot << " Defesnive rebound by " << team2_boxscore[rebound].name << std::endl;
                        }
                        else
                        {
                            whosball = 1;
                            int rebound = whosrebound(tm1);

                            team1_boxscore[rebound].reb = team1_boxscore[rebound].reb + 1;
                            std::cout << std::endl
                                      << "Missed Shot by " << whoshot << " Offensive rebound by " << team1_boxscore[rebound].name << std::endl;
                        }
                    }
                }
            }
        }
        else
        {

            for (int i = 0; i < team2_boxscore.size(); ++i)
            {
                if (team2_boxscore[i].name == whoshot)
                {
                    if (yesorno == "yes")
                    {
                        itwasamake = 1;
                        if (event >= 0 && event <= 2)
                        {
                            team2_boxscore[i].tpa = team2_boxscore[i].tpa + 1;
                            team2_boxscore[i].tpm = team2_boxscore[i].tpm + 1;
                            team2_score = team2_score + 3;
                            std::string was_it_assist = assist();
                            if (was_it_assist == "yes")
                            {
                                int whosast = whosassist(tm1);
                                team2_boxscore[whosast].ast = team2_boxscore[whosast].ast + 1;
                                std::cout << "THREE Pointer by " << team2_boxscore[i].name << " Assisted By " << team2_boxscore[whosast].name << std::endl;
                            }
                            else
                            {
                                std::cout << "THREE Pointer by " << team2_boxscore[i].name << std::endl;
                            }
                        }
                        else
                        {
                            team2_boxscore[i].fg = team2_boxscore[i].fg + 1;
                            team2_boxscore[i].fgm = team2_boxscore[i].fgm + 1;
                            team2_score = team2_score + 2;
                            std::string was_it_assist = assist();
                            if (was_it_assist == "yes")
                            {
                                int whosast = whosassist(tm1);
                                team2_boxscore[whosast].ast = team2_boxscore[whosast].ast + 1;
                                std::cout << "TWO Pointer by " << team2_boxscore[i].name << " Assisted By " << team2_boxscore[whosast].name << std::endl;
                            }
                            else
                            {
                                std::cout << "TWO Pointer by " << team2_boxscore[i].name << std::endl;
                            }
                        }
                        whosball = 1;
                    }
                    else
                    {
                        if (event >= 0 && event <= 2)
                        {
                            team2_boxscore[i].tpa = team2_boxscore[i].tpa + 1;
                        }
                        else
                        {

                            team2_boxscore[i].fg = team2_boxscore[i].fg + 1;
                        }
                        std::random_device rd;
                        std::mt19937 gen(rd());
                        std::uniform_int_distribution<> distr(0, 10);
                        int rebound = distr(gen);
                        if (rebound >= 0 && rebound < 9)
                        {
                            whosball = 1;
                            int rebound = whosrebound(tm1);

                            team1_boxscore[rebound].reb = team1_boxscore[rebound].reb + 1;
                            std::cout << std::endl
                                      << "Missed Shot by " << whoshot << " Defesnive rebound by " << team1_boxscore[rebound].name << std::endl;
                        }
                        else
                        {
                            whosball = 2;
                            int rebound = whosrebound(tm2);

                            team2_boxscore[rebound].reb = team2_boxscore[rebound].reb + 1;
                            std::cout << std::endl
                                      << "Missed Shot by " << whoshot << " Offensive rebound by " << team2_boxscore[rebound].name << std::endl;
                        }
                    }
                }
            }
        }
    }
    else if (event == 8)
    {
        if (whosball == 1)
        {
            whosball = 2;
        }
        else
        {
            whosball = 1;
        }
        // turnover
    }
    else if (event == 9)
    {
        // stl
        if (whosball == 1)
        {
            whosball = 2;
            std::random_device rd;
            std::mt19937 gen(rd());
            std::uniform_int_distribution<> distr(0, 4);
            int steal = distr(gen);
            std::random_device rd1;
            std::mt19937 gen1(rd1());
            std::uniform_int_distribution<> distr1(0, 4);
            int turnover = distr1(gen);
            team2_boxscore[steal].stl = team2_boxscore[steal].stl + 1;
            team1_boxscore[turnover].to = team1_boxscore[turnover].to + 1;
            std::cout << "Stolen by " << team2_boxscore[steal].name << " " << "Turnover by " << team1_boxscore[turnover].name << std::endl;
        }
        else
        {
            whosball = 1;
            std::random_device rd;
            std::mt19937 gen(rd());
            std::uniform_int_distribution<> distr(0, 4);
            int steal = distr(gen);
            std::random_device rd1;
            std::mt19937 gen1(rd1());
            std::uniform_int_distribution<> distr1(0, 4);
            int turnover = distr1(gen);
            team1_boxscore[steal].stl = team1_boxscore[steal].stl + 1;
            team2_boxscore[turnover].to = team2_boxscore[turnover].to + 1;
            std::cout << "Stolen by " << team1_boxscore[steal].name << " " << "Turnover by " << team2_boxscore[turnover].name << std::endl;
        }
    }
    else if (event == 10)
    {
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<> distr(0, 4);
        int block = distr(gen);
        if (whosball == 1)
        {
            team2_boxscore[block].blk = team2_boxscore[block].blk + 1;
            std::cout << "BLOCKED by " << team2_boxscore[block].name << std::endl;
            whosball = 2;
        }
        else
        {
            team1_boxscore[block].blk = team1_boxscore[block].blk + 1;
            std::cout << "BLOCKED by " << team1_boxscore[block].name << std::endl;
            whosball = 1;
        }
    }
}

void create_boxscore_team1(std::vector<player> team)
{

    for (int i = 0; i < team.size(); ++i)
    {
        stats player;
        player.name = team[i].name;
        team1_boxscore.push_back(player);
    }
}
void create_boxscore_team2(std::vector<player> team)
{

    for (int i = 0; i < team.size(); ++i)
    {
        stats player;
        player.name = team[i].name;
        team2_boxscore.push_back(player);
       
    }
}

void startgame(std::vector<player> tm1, std::vector<player> tm2)
{
    int quarter_time = 300;
    int quarter_length = 4;
    int quarter = 1;
    int exit = 0;
    int random_event = 0;
    int event_value = 0;
    int shotclock=24;

    create_boxscore_team1(tm1);
    create_boxscore_team2(tm2);

    while (exit == 0)
    {
        std::cout <<"Quarter: "<<quarter<<" Time: " <<gettime(quarter_time) <<" Shot Clock: "<<shotclock <<std::endl;
        quarter_time = quarter_time - 1;
        if(quarter_time<=24&&shotclock==0){
            
        }
        else{
            shotclock=shotclock-1;
        }
        
        if (quarter_time == event_value)
        {
            random_event = 0;
            if (whosball == 1)
            {
                random_event_call(tm1, whosball, tm2);
            }
            else
            {
                random_event_call(tm2, whosball, tm1);
            }

            if (itwasamake == 1)
            {
                itwasamake = 0;
                std::cout << "Score: " << team1 << " " << team1_score << " " << team2 << " " << team2_score << std::endl;
            }
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
        if (random_event == 0)
        {
            if(quarter_time<=24){
                shotclock=0;
            }
            else{
                shotclock=24;
            }
            std::random_device rd;
            std::mt19937 gen(rd());
            std::uniform_int_distribution<> distr(4, 24);
            int shotclock1 = distr(gen);
            event_value = quarter_time - shotclock1;
            random_event = 1;
        }
        if (quarter_time == 0)
        {
            quarter_time = 300;
            quarter = quarter + 1;
            random_event = 0;
            if (quarter > 4)
            {
                if (team1_score == team2_score)
                {
                    std::cout << "OVERTIME!!!!!!" << std::endl;
                }
                else
                {
                    exit = 1;
                }
            }
        }
    }
    int exit1 = 0;
    while (exit1 == 0)
    {
        std::cout << "Final Score: " << team1 << " " << team1_score << " " << team2 << " " << team2_score << std::endl;

        int input = 0;
        std::cout << "Press 1 to view " << team1 << " boxscore," << "press 2 to view " << team2 << " boxscore," << " press 3 to view team stats for " << team1 << ", press 4 to view team stats for " << team2 << " press 5 to exit" << std::endl;
        std::cin >> input;
        if (input == 1)
        {
            std::cout << team1 << " BOXSCORE" << std::endl;
            for (int i = 0; i < team1_boxscore.size(); ++i)
            {
                int pts = 0;
                pts = (team1_boxscore[i].fgm * 2) + (team1_boxscore[i].tpm * 3);

                std::cout << team1_boxscore[i].name << " PTS:" << pts << " RBS:" << team1_boxscore[i].reb << " ASTS:" << team1_boxscore[i].ast << " STL:" << team1_boxscore[i].stl << " BLK:" << team1_boxscore[i].blk << " TOS:" << team1_boxscore[i].to << std::endl;
            }
        }
        else if (input == 2)
        {
            std::cout << team2 << " BOXSCORE" << std::endl;
            for (int i = 0; i < team2_boxscore.size(); ++i)
            {
                int pts = 0;
                pts = (team2_boxscore[i].fgm * 2) + (team2_boxscore[i].tpm * 3);

                std::cout << team2_boxscore[i].name << " PTS:" << pts << " RBS:" << team2_boxscore[i].reb << " ASTS:" << team2_boxscore[i].ast << " STL:" << team2_boxscore[i].stl << " BLK:" << team2_boxscore[i].blk << " TOS:" << team2_boxscore[i].to << std::endl;
            }
        }
        else if (input == 3)
        {
            int fgm = 0;
            int fga = 0;
            int tpm = 0;
            int tpa = 0;
            int to = 0;
            int ast = 0;
            int blks = 0;
            int stls = 0;
            int rebs = 0;
            for (int i = 0; i < tm1.size(); ++i)
            {
                fgm = fgm + team1_boxscore[i].fgm + team1_boxscore[i].tpm;
                fga = fga + team1_boxscore[i].fg + team1_boxscore[i].tpa;
                tpm = tpm + team1_boxscore[i].tpm;
                tpa = tpa + team1_boxscore[i].tpa;
                to = to + team1_boxscore[i].to;
                ast = ast + team1_boxscore[i].ast;
                blks = blks + team1_boxscore[i].blk;
                stls = stls + team1_boxscore[i].stl;
                rebs = rebs + team1_boxscore[i].reb;
            }
            std::cout << "FGS: " << fgm << "/" << fga << std::endl
                      << "Threes: " << tpm << "/" << tpa << std::endl
                      << "Turnovers: " << to << std::endl
                      << "Assists: " << ast << std::endl
                      << "Blocks: " << blks << std::endl
                      << "Steals: " << stls << std::endl
                      << "Rebounds: " << rebs << std::endl;
        }
        else if (input == 4)
        {
            int fgm = 0;
            int fga = 0;
            int tpm = 0;
            int tpa = 0;
            int to = 0;
            int ast = 0;
            int blks = 0;
            int stls = 0;
            int rebs = 0;
            for (int i = 0; i < tm1.size(); ++i)
            {
                fgm = fgm + team2_boxscore[i].fgm + team2_boxscore[i].tpm;
                fga = fga + team2_boxscore[i].fg + team2_boxscore[i].tpa;
                tpm = tpm + team2_boxscore[i].tpm;
                tpa = tpa + team2_boxscore[i].tpa;
                to = to + team2_boxscore[i].to;
                ast = ast + team2_boxscore[i].ast;
                blks = blks + team2_boxscore[i].blk;
                stls = stls + team2_boxscore[i].stl;
                rebs = rebs + team2_boxscore[i].reb;
            }
            std::cout << "FGS: " << fgm << "/" << fga << std::endl
                      << "Threes: " << tpm << "/" << tpa << std::endl
                      << "Turnovers: " << to << std::endl
                      << "Assists: " << ast << std::endl
                      << "Blocks: " << blks << std::endl
                      << "Steals: " << stls << std::endl
                      << "Rebounds: " << rebs << std::endl;
        }
        else
        {
            exit1 = 1;
        }
    }
}

int main()
{
    chooseteams();
    std::vector<player> tm1;
    std::vector<player> tm2;
    tm1 = getplayers(team1);

    tm2 = getplayers(team2);
    startgame(tm1, tm2);
}
