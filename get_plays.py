import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
import multiprocessing

TAG_RE = re.compile(r'<[^>]+>')


def remove_tags(text):
    return TAG_RE.sub('', text)


def append_to_frames(row):
    series = (list(row)[1])
    link = series["game_link"]
    print("Processing row: " + str(list(row)[0]) + ", " + link)
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id="__NEXT_DATA__")
    json_data = remove_tags(str(results))
    raw_data = json.loads(json_data)
    # only interested in play by play
    curr_df = pd.DataFrame(raw_data["props"]["pageProps"]["playByPlay"]["actions"])
    print("Done with row " + str(list(row)[0]))
    return curr_df


def main():
    # open file with links to all of the games (generated by link_scraper.py)
    csv_links_df = pd.read_csv("games_with_links.csv")

    # Multiprocess pool.
    pool_size = multiprocessing.cpu_count() * 2
    pool = multiprocessing.Pool(processes=pool_size)
    frames = pool.map(append_to_frames, csv_links_df.iterrows())
    pool.close()
    pool.join()

    print(len(frames))
    actions_df = pd.concat(frames)
    print(actions_df)
    actions_df.to_csv(index=False, path_or_buf="actions.csv")


if __name__ == '__main__':
    main()
