#include <iostream>
#include <tuple>
#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <map>

std::string finalstring = "";


struct team
{
    std::string team_name;
    float three_point_attempts_per_game;
};
// class to keep track of all the years in order and all the teams in them
class Years
{
public:
    Years(std::vector<team> teams_vector, int currentyear)
    {
        teams = teams_vector; // vector of teams for this current year
        year = currentyear;   // is current year of season that object was made
    }
    int get_year()
    {
        return year;
    }
    void print_stats()
    {
        for (int i = 0; i < teams.size(); ++i)
        {
            std::ostringstream append_to_final_string;
            append_to_final_string << teams[i].team_name <<","<< teams[i].three_point_attempts_per_game<<std::endl;
            finalstring=finalstring+append_to_final_string.str();

        }
    }
    void print_team(std::string tm)
    {
        for (int i = 0; i < teams.size(); ++i)
        {
            
            if (tm == teams[i].team_name)
            {
                std::ostringstream append_to_final_string;
                append_to_final_string<< get_year() << "," << teams[i].three_point_attempts_per_game <<std::endl;
                finalstring=finalstring+append_to_final_string.str();
                return;
            }
        }
        std::ostringstream append_to_final_string;
        append_to_final_string<<get_year()<<0<<std::endl;
        finalstring=finalstring+append_to_final_string.str();
    }
    void print_leauge_avg()
    {
        float total;
        for (int i = 0; i < teams.size(); ++i)
        {
            total = total + teams[i].three_point_attempts_per_game;
        }
        std::ostringstream append_to_final_string;
        append_to_final_string<<get_year() << "," << total / teams.size() << std::endl;
        finalstring=finalstring+append_to_final_string.str();
        
    }
    int get_rank(std::string tm, std::string yr,int print)
    {
        if (get_year() != std::stoi(yr))
        {
            return -1;
        }
        std::vector<float> attempts;
        float team_attempts;
        for (int i = 0; i < teams.size(); ++i)
        {
            attempts.push_back(teams[i].three_point_attempts_per_game);
            if (teams[i].team_name == tm)
            {
               
                team_attempts = teams[i].three_point_attempts_per_game;
            }
        }
        std::sort(attempts.begin(), attempts.end());
        std::reverse(attempts.begin(), attempts.end());

        for (int i = 0; i < attempts.size(); ++i)
        {
            if (team_attempts == attempts[i])
            {
                if(print==1){
                std::ostringstream append_to_final_string;
                append_to_final_string<< get_year() << " Champion " << tm << " Rank:" << i + 1 << std::endl;
                        finalstring=finalstring+append_to_final_string.str();

                
                }
                return i + 1;
            }
        }
    }
    std::string does_this_team_have_top_ten_record(int yr,std::string tm)
    {
        std::ifstream records("all_teams_records_since_2014.csv");
        std::string line;
        std::vector<int> team_records;
        std::vector<std::string> team_names;
        while (std::getline(records, line))
        {
            std::istringstream team(line);

            std::string team_1;
            std::string wins;
            std::string current_year;
            std::getline(team, team_1, ',');
            std::getline(team, wins, ',');
            std::getline(team, current_year, ',');
            if (std::stoi(current_year) == yr)
            {
                //team_tuple = std::make_tuple(std::stoi(wins), team_1);
                std::pair<std::string,int> temp_team(team_1, std::stoi(wins));
                team_records.push_back(std::stoi(wins));
                team_names.push_back(team_1);
            }
        }
        int exit=0;
        while(exit==0){
            int change=0;
            for(int i=0;i<team_records.size();++i){
            if(i==team_records.size()-1){
                break;
            }
            else{
                int current=team_records[i];
                std::string current_team=team_names[i];
                int next=team_records[i+1];
                std::string next_team=team_names[i+1];
                if(current<next){
                    change=1;
                    team_records[i]=next;
                    team_records[i+1]=current;
                    team_names[i]=next_team;
                    team_names[i+1]=current_team;

                }


            }
        }
        if(change==0){
            exit=1;
        }
        
    };
    for(int i=0;i<10;++i){
        if(tm==team_names[i]){
            return "yes";
        }
    }
    return "no";
    

    // Sorting the vector using the custom comparator
    
  
     
        
    }
    int get_top_ten_teams_top_ten_in_tpa()
    {
        if(get_year()<2015){
            return -1;
        }
        std::string current_year = std::to_string(get_year());
        int counter=0;
        int counted=0;
        for (int i = 0; i < teams.size(); ++i)
        {   
            //int current_rank = get_rank(teams[i].team_name, current_year);
            std::string yes_or_no=does_this_team_have_top_ten_record(get_year(),teams[i].team_name);
           if(yes_or_no=="yes"){
              if (get_rank(teams[i].team_name,current_year,2)<=10){
                   counter=counter+1;
                    
               }
               counted=counted+1;

           }

        }
        
        return counter;
    }
    int number_of_playoff_teams_in_top_ten(int round){
        if(get_year()<2015){
            return -1;
        }
        std::string csv_name;
        std::string written_file_name;
        if(round==1){
            csv_name="first_round.csv";
            written_file_name="top_10_first_round_teams.csv";
        }
        if(round==2){
            csv_name="second_round.csv";
            written_file_name="top_10_second_round_teams.csv";

        }
        if(round==3){
            csv_name="third_round.csv";
            written_file_name="top_10_third_round_teams.csv";

        }
        if(round==4){
            csv_name="fourth_round.csv";
            written_file_name="top_10_fourth_round_teams.csv";

        }
        std::ifstream records(csv_name);
        std::string line;
        int counter=0;
        while (std::getline(records, line))
        {
            std::istringstream team(line);

            std::string year1;
            std::string team_name;
            std::getline(team,year1, ',');
            std::getline(team,team_name, ',');
            if(std::stoi(year1)==get_year()){
                team_name.pop_back();
                int rnk=get_rank(team_name,year1,2);
                std::cout<<rnk<<std::endl;
                if(rnk<=10){
                    counter=counter+1;

                }

            }
        }
        std::ofstream writefile(written_file_name, std::ios::app);
        writefile<<get_year()<<","<<counter<<std::endl;
        return counter;


    }
    float threes_attempted_by_team_2015_to_2024(std::string tm){

        if(get_year()<2015){
            return -1;
        }
        std::ofstream writefile("teamtpa.csv", std::ios::app);
        
        for(int i=0;i<teams.size();++i){
            if(teams[i].team_name==tm){
                writefile<<get_year()<<","<<teams[i].three_point_attempts_per_game<<std::endl;
                return teams[i].three_point_attempts_per_game;
            }
        }

    }
    float average_increase_per_season(std::string tm){
        if(get_year()<2015){
            return -1;
        }
        for(int i=0;i<teams.size();++i){
        if(tm==teams[i].team_name){
            return teams[i].three_point_attempts_per_game;
        }
        }
    }
private:
    std::vector<team> teams;
    int year;
};

int main()
{
    std::vector<std::string> nba_teams;
    nba_teams.push_back("Hawks");
    nba_teams.push_back("Celtics");
    nba_teams.push_back("Nets");
    nba_teams.push_back("Hornets");
    nba_teams.push_back("Bulls");
    nba_teams.push_back("Cavaliers");
    nba_teams.push_back("Mavericks");
    nba_teams.push_back("Nuggets");
    nba_teams.push_back("Pistons");
    nba_teams.push_back("Warriors");
    nba_teams.push_back("Rockets");
    nba_teams.push_back("Pacers");
    nba_teams.push_back("Clippers");
    nba_teams.push_back("Lakers");
    nba_teams.push_back("Grizzlies");
    nba_teams.push_back("Heat");
    nba_teams.push_back("Bucks");
    nba_teams.push_back("Timberwolves");
    nba_teams.push_back("Pelicans");
    nba_teams.push_back("Knicks");
    nba_teams.push_back("Thunder");
    nba_teams.push_back("Magic");
    nba_teams.push_back("76ers");
    nba_teams.push_back("Suns");
    nba_teams.push_back("Trail Blazers");
    nba_teams.push_back("Kings");
    nba_teams.push_back("Spurs");
    nba_teams.push_back("Raptors");
    nba_teams.push_back("Jazz");
    nba_teams.push_back("Wizards");
    std::map<std::string, std::string> cityToTeam;

    // Populate the map with city to team mappings
    cityToTeam["San Antonio"] = "Spurs";
    cityToTeam["L.A. Lakers"] = "Lakers";
    cityToTeam["Cleveland"] = "Cavaliers";
    cityToTeam["New York"] = "Knicks";
    cityToTeam["Boston"] = "Celtics";
    cityToTeam["Indiana"] = "Pacers";
    cityToTeam["Phoenix"] = "Suns";
    cityToTeam["Houston"] = "Rockets";
    cityToTeam["Milwaukee"] = "Bucks";
    cityToTeam["Philadelphia"] = "76ers";
    cityToTeam["Detroit"] = "Pistons";
    cityToTeam["Seattle"] = "Thunder";
    cityToTeam["New Jersey"] = "Nets";
    cityToTeam["Denver"] = "Nuggets";
    cityToTeam["Kansas City"] = "Kings";
    cityToTeam["San Diego"] = "Clippers";
    cityToTeam["Chicago"] = "Bulls";
    cityToTeam["Washington"] = "Wizards";
    cityToTeam["Atlanta"] = "Hawks";
    cityToTeam["Golden State"] = "Warriors";
    cityToTeam["Portland"] = "Trail Blazers";
    cityToTeam["Utah"] = "Jazz";
    cityToTeam["Dallas"] = "Mavericks";
    cityToTeam["L.A. Clippers"] = "Clippers";
    cityToTeam["Sacramento"] = "Kings";
    cityToTeam["Charlotte"] = "Hornets";
    cityToTeam["Miami"] = "Heat";
    cityToTeam["Orlando"] = "Magic";
    cityToTeam["Minnesota"] = "Timberwolves";
    cityToTeam["Toronto"] = "Raptors";
    cityToTeam["Vancouver"] = "Grizzlies";
    cityToTeam["Memphis"] = "Grizzlies";
    cityToTeam["New Orleans"] = "Pelicans";
    cityToTeam["Oklahoma City"] = "Thunder";
    cityToTeam["Brooklyn"] = "Nets";

    int years[] = {1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989,
                   1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999,
                   2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009,
                   2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019,
                   2020, 2021, 2022, 2023, 2024};
    int numYears = sizeof(years) / sizeof(years[0]); // get number of elements in arrat
    std::vector<Years> all_seasons;                  // this is a vector to organize each season
    for (int i = 0; i < numYears; ++i)
    {
        std::ifstream currentyear("NBA_3PT_BY_TEAM_" + std::to_string(years[i]) + ".csv");
        std::string line;
        std::vector<team> teams; // this an array to store the teams for the current year in the loop
        while (std::getline(currentyear, line))
        {
            std::istringstream current_team_and_stats(line);
            std::string delimited_result;
            team add_team;
            std::getline(current_team_and_stats, delimited_result, ',');
            add_team.team_name = delimited_result; // this gets team name
            auto it = cityToTeam.find(delimited_result);
            std::string team_name;
            if (it != cityToTeam.end())
            {
                team_name = it->second; // NBA team name if city is found
            }
            add_team.team_name = team_name;
            std::getline(current_team_and_stats, delimited_result, ',');
            add_team.three_point_attempts_per_game = std::stof(delimited_result); // this gets three point attempts
            teams.push_back(add_team);
        }

        Years year_object(teams, years[i]); // add all teams to the current year and make year object
        all_seasons.push_back(year_object);

        currentyear.close();
    }
    int exit = 0;
    while (exit == 0)
    {
        int option = 0; // this stores the user input;
        std::cout << "Press 1 to View three point attempts by each team per year" << std::endl;
        std::cout << "Press 2 to View three point attempts by a individual team per year" << std::endl;
        std::cout << "Press 3 to View the leauge average by year" << std::endl;
        std::cout << "Press 4 to view the champions rank in 3pt attempts for that season" << std::endl;
        std::cout << "Press 5 to view the amount of teams with a top 10 record that are also top 10 in three point attempts since 2015" << std::endl;
        std::cout << "Press 6 to view the number of teams per playoff round top 10 in 3pt shooting since 2015" << std::endl;
        std::cout << "Press 7 to view TPA by year for a particular team since 2015" << std::endl;
        std::cout << "Press 8 to view average TPA for team since 2015" << std::endl;



        std::cin >> option;
        if (option == 1)
        { // this option is for viewing three point attempts for a entered year
            int year = 0;
            std::cout << "Enter a year from 1980 to 2024" << std::endl;
            std::cin >> year;
            for (int i = 0; i < all_seasons.size(); ++i)
            {
                if (all_seasons[i].get_year() == year)
                {
                    all_seasons[i].print_stats();
                }
            }
            std::ofstream writefile("option_1.csv");
            writefile<<finalstring;
            finalstring="";
        }
        else if (option == 2) // gets a teams 3pt stats every year
        {
            std::string team;
            std::cout << "Enter team name" << std::endl;
            std::cin >> team;
            for (int i = 0; i < all_seasons.size(); ++i)
            {
                all_seasons[i].print_team(team);
            }
            std::ofstream writefile("option_2.csv");
            writefile<<finalstring;
            finalstring="";
        }

        else if (option == 3)
        {
            for (int i = 0; i < all_seasons.size(); ++i)
            {
                all_seasons[i].print_leauge_avg();
            }
            std::ofstream writefile("option_3.csv");
            writefile<<finalstring;
            finalstring="";
        }
        else if (option == 4)
        {
            std::ifstream champions("champs.csv");
            std::string line;
            while (std::getline(champions, line))
            {
                std::istringstream champ(line);
                std::string delimited_result;
                std::getline(champ, delimited_result, ',');
                std::string yr;
                std::getline(champ, yr, ',');

                for (int i = 0; i < all_seasons.size(); ++i)
                {
                    all_seasons[i].get_rank(delimited_result, yr,1);
                }
            }
            std::ofstream writefile("option_4.csv");
            writefile<<finalstring;
            finalstring="";

        }
        else if (option == 5)
        {
            std::vector<int> teams_by_year;
            for (int i = 0; i < all_seasons.size(); ++i)
            {
                //all_seasons[i].get_top_ten_teams_top_ten_in_tpa();
                int teams=all_seasons[i].get_top_ten_teams_top_ten_in_tpa();
                if(teams!=-1){
                    teams_by_year.push_back(teams);
                    }
                
            }
            int temp_year=2015;
            for(int i = 0; i<teams_by_year.size();++i){
              
               std::ostringstream append_to_final_string;
            append_to_final_string<<"Year: "<<temp_year<<" Number of teams with top 10 record in top 10 of tpa: "<<teams_by_year[i]<<std::endl;
            finalstring=finalstring+append_to_final_string.str();

               temp_year=temp_year+1;
            }
             std::ofstream writefile("option_5.csv");
            writefile<<finalstring;
            finalstring="";

        }
        else if (option==6){
            int round=0;
            std::cout << "Enter a round 1-4(First,second,WCF AND ECF,finals)" << std::endl;
            std::cin >> round;
            std::vector<int> count;
            if(round==1){
            for(int i=0;i<all_seasons.size();++i){
                int teams=all_seasons[i].number_of_playoff_teams_in_top_ten(1);
                if(teams!=-1){
                    count.push_back(teams);
                }
               
            }
            int year=2015;
            for(int i = 0;i<count.size();++i){
                std::ostringstream append_to_final_string;
                append_to_final_string<<"Number of teams in top 10 tpa round 1 "<<count[i]<<" in the year "<<year<<std::endl;
                finalstring=finalstring+append_to_final_string.str();
                 std::ofstream writefile("option_6.csv");
            writefile<<finalstring;
               // std::cout<<"Number of teams in top 10 tpa round 1 "<<count[i]<<" in the year "<<year<<std::endl;
                year=year+1;
            }
            }
            if(round==2){
            for(int i=0;i<all_seasons.size();++i){
                int teams=all_seasons[i].number_of_playoff_teams_in_top_ten(2);
                if(teams!=-1){
                    count.push_back(teams);
                }
            }
            int year=2015;
            for(int i = 0;i<count.size();++i){
                std::ostringstream append_to_final_string;
                append_to_final_string<<"Number of teams in top 10 tpa round 2 "<<count[i]<<" in the year "<<year<<std::endl;
                finalstring=finalstring+append_to_final_string.str();
                 std::ofstream writefile("option_6.csv");
            writefile<<finalstring;
                year=year+1;
            }
            }
            if(round==3){
            for(int i=0;i<all_seasons.size();++i){
                int teams=all_seasons[i].number_of_playoff_teams_in_top_ten(3);
                if(teams!=-1){
                    count.push_back(teams);
                }
            }
            int year=2015;
            for(int i = 0;i<count.size();++i){
                std::ostringstream append_to_final_string;
                append_to_final_string<<"Number of teams in top 10 tpa round 3 "<<count[i]<<" in the year "<<year<<std::endl;
                finalstring=finalstring+append_to_final_string.str();
                 std::ofstream writefile("option_6.csv");
            writefile<<finalstring;
                year=year+1;
            }
            }
            if(round==4){
            for(int i=0;i<all_seasons.size();++i){
                int teams=all_seasons[i].number_of_playoff_teams_in_top_ten(4);
                if(teams!=-1){
                    count.push_back(teams);
                }
                
            }
            int year=2015;
            for(int i = 0;i<count.size();++i){
                std::ostringstream append_to_final_string;
                append_to_final_string<<"Number of teams in top 10 tpa round 4 "<<count[i]<<" in the year "<<year<<std::endl;
                finalstring=finalstring+append_to_final_string.str();
                 std::ofstream writefile("option_6.csv");
            writefile<<finalstring;
                year=year+1;
            }
            }

            finalstring="";

        }
        else if(option==7){
            std::string teamname;
            std::cout << "Enter A Team Name" << std::endl;
            std::cin >> teamname;
            std::vector<float> count;
            for(int i=0;i<all_seasons.size();++i){
                int attempts=all_seasons[i].threes_attempted_by_team_2015_to_2024(teamname);
                if(attempts!=-1){
                    count.push_back(attempts);
                }
            }
            int year=2015;
            
            for(int i = 0;i<count.size();++i){
                std::ostringstream append_to_final_string;
                append_to_final_string<<"TPA by "<<teamname<<" was "<<count[i]<<" in the year "<<year<<std::endl;
                finalstring=finalstring+append_to_final_string.str();
                year=year+1;
            }
            std::ofstream writefile("option_7.csv");
            writefile<<finalstring;
            finalstring="";

        }
        else if(option==8){
            std::vector<float> averages;
           
            
                for(int j=0;j<nba_teams.size();j++){
                    float counter=0;
                for(int i=0;i<all_seasons.size();++i){
                    float temp=all_seasons[i].average_increase_per_season(nba_teams[j]);
                    if(temp!=-1){
                        counter=counter+temp;
                    }
                }
                counter=counter/10;
                averages.push_back(counter);

                }
                
                for(int i = 0;i<nba_teams.size();++i){
                    std::ostringstream append_to_final_string;
                append_to_final_string<<"Since 2015 the "<<nba_teams[i]<<" have an average of "<<averages[i]<<" per year "<<std::endl;
                finalstring=finalstring+append_to_final_string.str();
                //std::cout<<"Since 2015 the "<<nba_teams[i]<<" have an average of "<<averages[i]<<" per year "<<std::endl;
                
                }
                std::ofstream writefile("option_8.csv");
                writefile<<finalstring;
            
                finalstring="";



        }
    }
}
