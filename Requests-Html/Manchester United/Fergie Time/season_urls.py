from init import session
import csv

with open("all_season_stats.csv", "w", newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['Year', 'Matches', 'Win', 'Draw', 'Lose', 'Points', 'Position', 'FA Cup', 'EFL Cup', 'Community Shield', 'Top Scorer', 'Top Scorer Goals'])

response = session.get("https://en.wikipedia.org/wiki/List_of_Manchester_United_F.C._seasons")

container = response.html.find("div.mw-parser-output", first=True)
table = container.find("table")[2]

seasons = table.find("tbody tr")
# print(len(seasons))
all_season_urls = []
seasons = seasons[100:]
for prem in seasons:
    # prem = seasons[100]

    season_url = prem.find("th a", first=True)
    season_year = season_url.text
    season_url = season_url.attrs['href']
    season_url = f'https://en.wikipedia.org{season_url}'
    all_season_urls.append(season_url)
    print(season_year)

    season_stats = prem.find("td")

    matches = season_stats[1].text
    win = season_stats[2].text
    draw = season_stats[3].text
    try:
        lose = season_stats[4].find('span', first=True).text
    except:
        lose = season_stats[4].text

    points = season_stats[7].text

    try:
        position = season_stats[8].find('span', first=True).text
    except:
        position = season_stats[8].text

    fa_cup = season_stats[9].find('a', first=True).text
    efl_cup = season_stats[10].text
    community_shield = season_stats[11].text
    top_scorer_name = season_stats[13].find("a")
    if len(top_scorer_name) == 1:
        top_scorer_name = top_scorer_name[0].text
    else:
        top_scorer_name = f'{top_scorer_name[0].text} & {top_scorer_name[1].text}'
    top_scorer_goals = season_stats[14].text

    print(f'M-{matches} W-{win} D-{draw} L-{lose} P-{points} Pos-{position} FA_Cup-{fa_cup} EFL_Cup-{efl_cup} CS-{community_shield}')
    print(top_scorer_name, top_scorer_goals)
    print()

    with open("all_season_stats.csv", "a+", newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([season_year, matches, win, draw, lose, points, position, fa_cup, efl_cup, community_shield, top_scorer_name, top_scorer_goals])


with open("all_season_urls.txt", "a+") as file:
    for url in all_season_urls:
        file.write(url + "\n")


# github.com/arutselvanManivannan
