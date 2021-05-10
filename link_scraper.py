import datetime
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = 'https://www.nba.com/games?date='
final_base_url = 'https://www.nba.com'

# this is the real season start
curr_date = datetime.date(2018, 10, 16)  # october 16 2018
end_date = datetime.date(2019, 4, 10)  # april 10 2019
delta = datetime.timedelta(days=1)

# example link: https://www.nba.com/game/phi-vs-bos-0021800001
# match "/game/3 letters-vs-3 letters-10 numbers
regex = "/game/\D{3}-vs-\D{3}-\d{10}"
games = []

while curr_date <= end_date:
    print(curr_date)
    date_link = base_url + str(curr_date)
    page = requests.get(date_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    raw_regex_match_list = re.findall(regex, str(page.content))
    no_dups_list = [i for j, i in enumerate(raw_regex_match_list) if i not in raw_regex_match_list[:j]]

    for link in no_dups_list:
        games_dict = {"date": curr_date,
                      "game_link": final_base_url + link}
        print(games_dict)
        games.append(games_dict)

    curr_date += delta

df = pd.DataFrame(data=games)
df.to_csv(index=False, path_or_buf="games_with_links.csv")
print(df)
