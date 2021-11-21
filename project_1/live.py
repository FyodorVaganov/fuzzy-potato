import requests
from requests.api import request

point = "https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json"

response = requests.request("GET", point)


def get_score(game):
    return{
        "home_score": game["homeTeam"]["score"],
        "away_score": game["awayTeam"]["score"],
        "home_team": game["homeTeam"]["teamTricode"],
        "away_team": game["awayTeam"]["teamTricode"]}


def get_live_games(data):
    all_live_games = []
    live_games = data["scoreboard"]["games"]
    for game in range(len(live_games)):
        if live_games[game]["gameStatus"] == 2:
            all_live_games.append(get_score(live_games[game]))
    return(all_live_games)


if response.status_code == 200:
    data = response.json()
    test_get = get_live_games(data)
