from init import session
import csv

with open("purchased_players.csv", "w") as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['name', 'position', 'club_from', 'date', 'fee'])

response = session.get("https://www.transfermarkt.co.uk/sir-alex-ferguson/spielertransfers/trainer/4")

table = response.html.find("div.grid-view", first=True)

players = table.find("table tbody tr")

for player in players:
    try:
        temp = player.find("table.inline-table")
        name = temp[0].find("tr")[0].find("td")[1].find("a", first=True).text
        # print(name)
        position = temp[0].find("tr")[1].find("td", first=True).text
        # print(position)

        club_from = temp[1].find("tr")[0].find("td")[1].find("a", first=True).text
        # print(club_from)

        date = player.find("td.zentriert")[2].text
        # print(date)

        fee = player.find("td.rechts.hauptlink a", first=True).text
        if "Loan fee" in fee:
            fee = fee.split(":")[1].strip()
        fee = fee[1:-1]
        # print(fee)

        print(name, position, club_from, date, fee)

        with open("purchased_players.csv", "a+", newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([name, position, club_from, date, fee])
    except Exception as e:
        pass


# github.com/arutselvanManivannan
