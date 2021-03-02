import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = 'https://www.nba.com/games?date='
final_base_url = 'https://www.nba.com'

# this is the real season start
curr_date = datetime.date(2018, 10, 16)  # october 16 2018
end_date = datetime.date(2019, 4, 10)  # april 10 2019
delta = datetime.timedelta(days=1)

games = []

while curr_date <= end_date:
    print(curr_date)
    date_link = base_url + str(curr_date)
    page = requests.get(date_link)
    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.findAll(class_='shadow-block bg-white flex md:rounded text-sm relative mb-4 GameCard_card__3jRUe')

    for game in results:
        link = game.find('a')['href']
        games_dict = {"date": curr_date,
                      "game_link": final_base_url + link}
        games.append(games_dict)

    curr_date += delta

df = pd.DataFrame(data=games)
df.to_csv(index=False, path_or_buf="games_with_links.csv")
print(df)
