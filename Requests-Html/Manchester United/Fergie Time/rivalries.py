from init import session
import csv

with open("rivalries.csv", "w", newline="") as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['team', 'm', 'w', 'd', 'l'])

response = session.get("https://www.transfermarkt.co.in/sir-alex-ferguson/bilanz/trainer/4")

wanted = ['Chelsea FC', 'Liverpool FC', 'Arsenal FC', 'Manchester City', 'Leeds United']

table = response.html.find("table.items", first=True)

odd_items = table.find("tr.odd")
even_items = table.find("tr.even")

for item in odd_items:
    team_name = item.find("td.hauptlink.links.no-border-links a", first=True).text
    if team_name in wanted:
        stats = item.find("td.zentriert")
        matches = stats[1].text
        win = stats[2].text
        draw = stats[3].text
        lose = stats[4].text
        print(team_name, matches, win, draw, lose)

        with open("rivalries.csv", 'a+', newline='') as new_file:
            csv_writer = csv.writer(new_file)
            csv_writer.writerow([team_name, matches, win, draw, lose])

for item in even_items:
    team_name = item.find("td.hauptlink.links.no-border-links a", first=True).text
    if team_name in wanted:
        stats = item.find("td.zentriert")
        matches = stats[1].text
        win = stats[2].text
        draw = stats[3].text
        lose = stats[4].text
        print(team_name, matches, win, draw, lose)

        with open("rivalries.csv", 'a+', newline='') as new_file:
            csv_writer = csv.writer(new_file)
            csv_writer.writerow([team_name, matches, win, draw, lose])


# github.com/arutselvanManivannan
