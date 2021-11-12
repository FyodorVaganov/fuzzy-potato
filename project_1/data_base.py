from sqlalchemy import *
import psycopg2
from datetime import datetime
import main


engine = create_engine(
    "postgresql+psycopg2://postgres:qwer123@localhost:5432/gms_n_tms")
conn = engine.connect()

print(engine, "done")

meta_data = MetaData(bind=engine)
meta_data.reflect(bind=engine)
games_table = meta_data.tables['games']


def get_today_date():
    today_date = datetime.today().timetuple()
    today_date = today_date[0:3]
    return(today_date)


def extract_last_date():
    s = select([games_table]).order_by(desc(games_table.c.date))
    r = conn.execute(s)
    extract = r.first()
    last_game_date = extract[5].timetuple()
    last_game_date = last_game_date[0:3]
    return(last_game_date)


def date_iteration():
    date = get_today_date()
    date_list = []
    last_game_date = extract_last_date()
    last_game_day = last_game_date[2]
    last_game_month = last_game_date[1]
    last_game_year = last_game_date[0]
    date_day = date[2]
    date_month = date[1]
    date_year = date[0]
    today_date = str(date_year)+"-"+str(date_month)+"-"+str(date_day)
    month_31_days = [1, 3, 5, 7, 8, 10, 12]
    month_30_days = [4, 6, 9, 11]
    month_feb = 2
    while date_day != last_game_day or date_month != last_game_month or date_year != last_game_year:
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
        if date_day < 10 and date_month < 10:
            date_list.append(str(date_year) + "-" + "0" +
                             str(date_month) + "-" + "0" + str(date_day))
        elif date_month < 10:
            date_list.append(str(date_year) + "-" + "0" +
                             str(date_month) + "-" + str(date_day))
        elif date_day < 10 and i != 1:
            date_list.append(str(date_year) + "-" +
                             str(date_month) + "-" + "0" + str(date_day))
        if date_day >= 10 and date_month >= 10:
            date_list.append(str(date_year) + "-" +
                             str(date_month) + "-" + str(date_day))
    date_list.reverse()
    return(date_list)


def insert_data(date_goal):
    data_for_insert = main.get_games_by_date(date_goal)
    if data_for_insert != "there is no games ":
        for game in data_for_insert:
            ins = games_table.insert().values(
                home_team_id=game.get('home_team'),
                away_team_id=game.get('away_team'),
                home_team_score=game.get('home_score'),
                away_team_score=game.get('away_score'),
                date=date_goal)
            print(ins.compile().params)
            r = conn.execute(ins)


dates_to_insert = date_iteration()
for i in range(1, len(dates_to_insert)):
    insert_data(dates_to_insert[i])
pass
