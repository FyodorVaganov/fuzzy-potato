import requests

point = "https://ru.global.nba.com/stats2/season/conferencestanding.json?locale=ru"

response = requests.request("GET", point)

if response.status_code == 200:
    data = response.json()
