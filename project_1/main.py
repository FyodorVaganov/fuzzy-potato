import requests
from requests.api import request
# ссылка, откуда можно брать сегодняшние игры
point = "https://ru.global.nba.com/stats2/scores/miniscoreboard.json?countryCode=RU&locale=ru&tz=%2B3"
# ссылка, откуда можно брать игры по дате, необходимо добавлять дату в формате "YYYY-MM-DD"
date_point = "https://ru.global.nba.com/stats2/scores/daily.json?countryCode=RU&gameDate="
# ссылка, по которой можно проверить, есть ли игры по дате, необходимо добавлять дату в формате "YYYY-MM-DD"
game_day_status_point = "https://ru.global.nba.com/stats2/scores/gamedaystatus.json?gameDate="
# для итерации по датам 17 строка:
date_start = "2021-09-10"
month_31_days = [1, 3, 5, 7, 8, 10, 12]
month_30_days = [4, 6, 9, 11]
month_feb = 2


# функция обратной итерации по дате
def reverse_date_iteration(date, num_of_days):
    date_list = []
    date_day = int(date[8:10])
    date_month = int(date[5:7])
    date_year = int(date[0:4])
    i = 0
    while i != num_of_days:
        date_day -= 1
        if date_day == 0:
            date_month -= 1
            if date_month in month_30_days:
                date_day = 30
            if date_month in month_31_days:
                date_day = 31
            if date_month == month_feb:
                if date_year % 4 == 0:
                    date_day = 29
                else:
                    date_day = 28
            if date_month == 0:
                date_month = 12
                date_day = 31
                date_year -= 1
        i += 1
        if date_day < 10 and date_month < 10:
            date_list.append(str(date_year) + "-" + "0" +
                             str(date_month) + "-" + "0" + str(date_day))
        elif date_month < 10:
            date_list.append(str(date_year) + "-" + "0" +
                             str(date_month) + "-" + str(date_day))
        elif date_day < 10:
            date_list.append(str(date_year) + "-" +
                             str(date_month) + "-" + "0" + str(date_day))
        if date_day >= 10 and date_month >= 10:
            date_list.append(str(date_year) + "-" +
                             str(date_month) + "-" + str(date_day))
    return(date_list)


# функция, берущая результаты конкретной игры
def get_score(game):
    return{
        "home_score": game["boxscore"]["homeScore"],
        "away_score": game["boxscore"]["awayScore"],
        "home_team": game["homeTeam"]["profile"]["abbr"],
        "away_team": game["awayTeam"]["profile"]["abbr"]}


# функция, получающая все игры по дате, если игр нет, возвращает строку "there is no games on " + date
def get_games_by_date(date):
    date_response = requests.request("GET", date_point+date)
    date_status = requests.request("GET", game_day_status_point+date)
    if (date_response.status_code == 200) and (date_status.status_code == 200):
        check = date_status.json()
        data = date_response.json()
        if check["payload"]["gameDates"][0]["games"] == []:
            return "there is no games "
        else:
            games = data["payload"]["date"]["games"]
            all_date_games = []
            for i in range(len(games)):
                all_date_games.append(get_score(games[i]))
        return all_date_games


# функция, берущая игры до сегодня, насколько глубоко работает пока не известно
def get_previous_games(data):
    games = data["payload"]["previous"]["games"]
    all_previous_games = []
    for i in range(len(games)):
        all_previous_games.append(get_score(games[i]))
    return all_previous_games


# функция, берущая сегоднящние игры
def get_today_games(data):
    games = data["payload"]["today"]["games"]
    all_today_games = []
    for i in range(len(games)):
        all_today_games.append(get_score(games[i]))
    return all_today_games


# функция, берущая будущие игры, скорее всего на неделю вперёд
def get_next_games(data):
    games = data["payload"]["next"]["games"]
    all_next_games = []
    for i in range(len(games)):
        all_next_games.append(get_score(games[i]))
    return all_next_games


response = requests.request("GET", point)
if response.status_code == 200:
    data = response.json()
    path = data["payload"]["previous"]["games"][0]  # путь к сегодняшним играм
    score_info = get_score(path)
    past_games_info = get_games_by_date("2021-10-20")
    today_games_info = get_today_games(data)
    next_games_info = get_next_games(data)
    date_games_info = get_games_by_date("2021-10-31")
    # сюда добавляется список дат, начиная с известной
    dates = reverse_date_iteration("2021-10-20", 4)
    past_games_list = []  # в этот список записываются игры за промежуток времени
    for i in range(len(dates)):
        past_games_list.append({dates[i]: get_games_by_date(dates[i])})
    print(past_games_list)
