from init import session
import csv

response = session.get("https://www.transfermarkt.com.mt/sir-alex-ferguson/eingesetzteSpieler/trainer/4/plus/1?saison_id=&verein_id=985&liga=&wettbewerb_id=GB1")

with open("most_players_stats.csv", "w", newline="") as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['Name', 'Appearances', 'Goals', 'Assists'])

items = response.html.find("table.items", first=True)

odd_items = items.find("tr.odd")
even_items = items.find("tr.even")

for i in range(12):
    odd_item = odd_items[i]
    table_rows = odd_item.find("td")
    odd_name = table_rows[2].find("a", first=True).text
    odd_appearances = table_rows[8].find("a", first=True).text
    odd_goals = table_rows[11].text
    odd_assists = table_rows[12].text
    print(odd_name, odd_appearances, odd_goals, odd_assists)

    even_item = even_items[i]
    table_rows = even_item.find("td")
    even_name = table_rows[2].find("a", first=True).text
    even_appearances = table_rows[8].find("a", first=True).text
    even_goals = table_rows[11].text
    even_assists = table_rows[12].text
    print(even_name, even_appearances, even_goals, even_assists)

    with open('most_players_stats.csv', 'a+', newline='', encoding="utf-8") as new_file:
        csv_writer = csv.writer(new_file)
        csv_writer.writerow([odd_name, odd_appearances, odd_goals, odd_assists])
        csv_writer.writerow([even_name, even_appearances, even_goals, even_assists])


# github.com/arutselvanManivannan
