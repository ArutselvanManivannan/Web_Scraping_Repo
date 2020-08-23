import time
from plyer import notification
from requests_html import HTMLSession

session = HTMLSession()

while True:
    res = session.get(
        "https://www.cricbuzz.com/live-cricket-scores/29079/eng-vs-pak-2nd-test-pakistan-tour-of-england-2020"
    )

    container = res.html
    # container.render()

    match = container.find("#matchCenter", first=True)

    title = match.find(
        "div.cb-nav-main.cb-col-100.cb-col.cb-bg-white h1", first=True
    ).text
    title = title.split(", Commentary")[0]
    print(title)
    print()

    match_complete = match.find(".cb-min-comp")
    if match_complete:
        match_complete = match_complete[0]
        scorecard = match_complete.find(".cb-col.cb-col-67.cb-scrs-wrp", first=True)

        teams = scorecard.find(".cb-col.cb-col-100.cb-min-tm")
        team1 = teams[0].text
        team2 = teams[1].text
        print(team1)
        print(team2)

        summary = match_complete.find(
            ".cb-col.cb-col-100.cb-min-stts.cb-text-complete", first=True
        ).text
        print(summary)
        print()

        mom = match_complete.find(".cb-col.cb-col-50.cb-mom-itm a")
        if mom:
            mom = mom[0].text
            print(f"Man of the Match: {mom}")

        notification.notify(
            title=f"{title}", message=f"{summary}\nMan of the Match: {mom}"
        )

        break

    score = match.find(".cb-col.cb-col-67.cb-scrs-wrp", first=True)

    opponentScore = score.find(".cb-text-gray.cb-font-16")
    if opponentScore:
        print(opponentScore[0].text)

    currentScore = score.find("div.cb-min-bat-rw", first=True)
    currentScore = currentScore.find(".cb-font-20.text-bold", first=True).text
    print(currentScore)

    try:
        stumps = score.find(".cb-text-stump")
        lunch = score.find(".cb-text-lunch")
        tea = score.find(".cb-text-tea")
        innings_break = score.find(".cb-text-innings.break")
        rain_break = score.find(".cb-text-rain")
        wet_outfield = score.find(".cb-text-wetoutfield")
    except Exception as e:
        print(e)
        break

    if stumps:
        status = stumps[0].text
        print(status)
        notification.notify(title=title, message=status)
        break
    elif lunch:
        status = lunch[0].text
        notification.notify(title=title, message=status)
        print(status)
        break
    elif tea:
        status = tea[0].text
        notification.notify(title=title, message=status)
        print(status)
        break
    elif innings_break:
        status = innings_break[0].text
        notification.notify(title=title, message=status)
        print(status)
        break
    elif rain_break:
        status = rain_break[0].text
        notification.notify(title=title, message=status)
        print(status)
        break
    elif wet_outfield:
        status = wet_outfield[0].text
        notification.notify(title=title, message=status)
        print(status)
        break
    else:
        status = score.find(".cb-text-inprogress", first=True).text

    print()

    scoreboard = match.find(".cb-col-scores+ .cb-col", first=True)

    batsmans = scoreboard.find(
        ".cb-min-inf:nth-child(1) div.cb-col.cb-col-100.cb-min-itm-rw"
    )

    striker = batsmans[0]

    striker_name = striker.find(".cb-col.cb-col-50 a", first=True).text
    stats = striker.find("div.cb-col.cb-col-10.ab.text-right")
    striker_runs = stats[0].text
    striker_balls = stats[1].text

    batsman1 = f"{striker_name} - {striker_runs} Runs {striker_balls} Balls"
    print(batsman1)
    batsman2 = None
    if len(batsmans) > 1:
        non_striker = batsmans[1]

        non_striker_name = non_striker.find(".cb-col.cb-col-50 a", first=True).text
        stats = non_striker.find("div.cb-col.cb-col-10.ab.text-right")
        non_striker_runs = stats[0].text
        non_striker_balls = stats[1].text

        batsman2 = (
            f"{non_striker_name} - {non_striker_runs} Runs {non_striker_balls} Balls"
        )
        print(batsman2)

    print()

    bowlers = scoreboard.find("div.cb-min-inf.cb-col-100")[1].find(
        ".cb-col.cb-col-100.cb-min-itm-rw"
    )

    bowler = bowlers[0]

    bowler_name = bowler.find("div.cb-col.cb-col-50 a", first=True).text
    bowler_overs = bowler.find("div.cb-col.cb-col-10.text-right", first=True).text
    bowler_wickets = bowler.find("div.cb-col.cb-col-8.text-right")[1].text

    bowler_stats = f"{bowler_name} - {bowler_overs} Overs {bowler_wickets} Wickets"
    print(bowler_stats)

    if batsman2:
        notification.notify(
            title=title,
            message=f"{currentScore}\n{batsman1}\n{bowler_stats}\n{status}",
        )
    else:
        notification.notify(
            title=title,
            message=f"{currentScore}\n{batsman1}\n{batsman2}\n{bowler_stats}\n{status}",
        )

    print("********************")
    time.sleep(300)
