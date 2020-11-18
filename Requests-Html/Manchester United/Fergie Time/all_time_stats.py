from init import session
import csv

response = session.get("https://www.transfermarkt.co.in/sir-alex-ferguson/leistungsdatenDetail/trainer/4")

container = response.html.find("div.large-4.columns div.box")[0]
result = container.find("table tbody tr", first=True)

stats = []
table_data = result.find("td.zentriert")
for data in table_data:
    stats.append(data.text)

print(f'Matches {stats[0]}')
print(f'Won {stats[1]}')
print(f'Draw {stats[2]}')
print(f'Lost {stats[3]}')
print(f'Goals Scored {stats[4].split(":")[0]}')
print(f'Goals Conceded {stats[4].split(":")[1]}')


with open("all_time_stats.csv", "w", newline="") as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['Matches', 'Won', 'Draw', 'Lose', 'Goals Scored', 'Goals Conceded'])
    csv_writer.writerow([stats[0], stats[1], stats[2], stats[3], stats[4].split(":")[0], stats[4].split(":")[1]])


# github.com/arutselvanManivannan
