import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap
import charts


def scatter(data):
    player1 = "K. Irving"
    player2 = "J. Tatum"
    subset = data[(data["playerNameI"] == player1) | (data["playerNameI"] == player2)]
    charts.draw_court()
    sns.scatterplot(x="xLegacy", y="yLegacy", hue="playerNameI", style="shotResult", alpha=1, data=subset)
    plt.xlim(-250, 250)
    plt.ylim(422.5, -47.5)
    plt.show()


def xyzplot(data):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x = shotActions['xLegacy']
    y = shotActions['yLegacy']
    z = shotActions['period']

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("period")

    ax.scatter(x, y, z, s=40, c=z, marker='o', alpha=0.4)

    plt.show()


actions = pd.read_csv("actions.csv").head(600000)
# only interested in play by play
# raw_data = json.load(open('game12018shots.json'))
# actions = pd.DataFrame(raw_data["props"]["pageProps"]["playByPlay"]["actions"]).head(1000)

shotActions = actions[actions["shotResult"] != ""]
scatter(shotActions)
