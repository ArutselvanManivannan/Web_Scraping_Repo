from init import session
import csv

with open("premier_league_stats.csv", "w", newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(["match_id", "position", "year", "opponent", "ha", "scoreline", "diff", "attendance", "league_position", "result"])

match_id = 1

with open("all_season_urls.txt") as file:
    for _ in range(28):
        url = file.readline().strip()
        response = session.get(url)

        season = response.html.find("h1.firstHeading", first=True).text
        season = season.split(" ", 1)[0]
        print(season)

        container = response.html.find("div.mw-content-ltr", first=True)

        premier_league_table = container.find("table.wikitable")

        for table in premier_league_table:
            total_matches = len(table.find("tbody tr"))

            if total_matches >= 38:
                matches = table.find("tbody tr")
                matches = matches[1:]

                for match in matches:
                    match_stats = match.find("td")

                    match_date = match_stats[0].text
                    opponent = match_stats[1].find("a", first=True).text
                    ha = match_stats[2].text
                    scoreline = match_stats[3].text
                    attendance = match_stats[5].text
                    league_position = match_stats[6].text

                    result = ''
                    goals_scored, goals_conceded = scoreline.split(chr(8211))
                    diff = abs(int(goals_scored) - int(goals_conceded))
                    if goals_scored > goals_conceded:
                        result = 'win'
                    elif goals_scored < goals_conceded:
                        result = 'lose'
                    else:
                        result = 'draw'

                    print(match_id, match_date, opponent, ha, scoreline, diff, attendance, league_position, result)

                    with open("premier_league_stats.csv", "a+", newline='') as new_file:
                        csv_writer = csv.writer(new_file)
                        csv_writer.writerow([match_id, 0, season, opponent, ha, str(scoreline), diff, attendance, league_position, result])
                        csv_writer.writerow([match_id, 0.01, season, opponent, ha, str(scoreline), diff, attendance, league_position, result])
                        match_id += 1
                print()
                break


# github.com/arutselvanManivannan
