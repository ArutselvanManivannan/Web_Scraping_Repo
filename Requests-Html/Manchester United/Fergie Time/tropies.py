from init import session
import csv

with open("tropies.csv", "w", newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['cup', 'season'])

response = session.get("https://www.transfermarkt.co.in/sir-alex-ferguson/erfolge/trainer/4")

container = response.html.find("div.large-8.columns", first=True)

for row in container.find("div.row"):
    cups = row.find("div.large-6.columns")
    for cup in cups:
        header = cup.find("div.header h2", first=True).text.split(" ", 1)
        cup_title = header[1]
        if 'winner' in cup_title:
            cup_title = cup_title.replace('winner', '')
        cup_wins = header[0].split("x")[0]

        years = []

        table_rows = cup.find("div.erfolg_info_box table.auflistung tr")
        for tr in table_rows:
            year = tr.find("td.erfolg_table_saison", first=True).text
            years.append(year)

            with open("tropies.csv", "a+", newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow([cup_title, year])

        print(cup_title, *years)
        print(f'No.of times won: {cup_wins}')


# github.com/arutselvanManivannan
