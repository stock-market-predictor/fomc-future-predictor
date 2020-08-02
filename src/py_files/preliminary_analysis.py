import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

sns.set_style('darkgrid')

def differenceBeforeAfterFOMC(massivechanges):
    x = massivechanges['Rate Changes']
    y = massivechanges['difference']

    x_np = (massivechanges['Rate Changes']).to_numpy()
    y_np = massivechanges['difference'].to_numpy()
    m, b = np.polyfit(x_np, y_np, 1)

    plt.scatter(x, y)
    plt.plot(x, m * x + b, 'r-', label='y = {0:.{1}f}'.format(m, 6) + 'x + {0:.{1}f}'.format(b, 6))
    plt.xlabel("Rate Hike/Cut")
    plt.ylabel("Change in price of 30 day Fed Funds Future")
    plt.title("Effect of Rate Hike/Cut on Price of 30 day Fed Funds Future")
    plt.legend()

    plt.savefig('../figures/rate_change_on_FFF.png', dpi=800)

def differenceBeforeBeforeFOMC(massivechanges):
    x = massivechanges['difference type 2']
    y = massivechanges['Rate Changes']
    x_np = (massivechanges['difference type 2']).to_numpy()
    y_np = massivechanges['Rate Changes'].to_numpy()

    m, b = np.polyfit(x_np, y_np, 1)

    fig = plt.figure(figsize=(10, 10))
    sns.scatterplot(x='difference type 2', y='Rate Changes', data=massivechanges)
    plt.plot(x, m * x + b, 'r-',
             label='y = {0:.{1}f}'.format(m, 6) + 'x + {0:.{1}f}'.format(b, 6) + '\nr^2 = {0:.{1}f}'.format(
                 0.6635572131965038, 3))
    plt.xlabel("Change in Fed Funds Future between the day before the last cut/hike and the day before the FOMC")
    plt.ylabel("Rate Hike/Cut")
    plt.title("Effectiveness of Fed Funds future in predicting Fed Rate/Hike")
    plt.legend()

    plt.savefig('../figures/FFF_on_rate_change.png', dpi=800)

    slope, intercept, r_value, p_value, std_err = stats.linregress(x_np, y_np)
    print(slope)
    print(intercept)
    print(r_value ** 2)
    print(p_value)

def differenceAfterAfterFOMC(massivechanges):
    x = massivechanges['Rate Changes']
    y = massivechanges['difference type 3']
    x_np = massivechanges['Rate Changes'].to_numpy()
    y_np = (massivechanges['difference type 3']).to_numpy()
    m, b = np.polyfit(x_np, y_np, 1)

    fig = plt.figure(figsize=(10, 10))
    sns.scatterplot(x='Rate Changes', y='difference type 3', data=massivechanges)
    plt.plot(x, m * x + b, 'r-',
             label='y = {0:.{1}f}'.format(m, 6) + 'x + {0:.{1}f}'.format(b, 6) + '\nr^2 = {0:.{1}f}'.format(
                 0.5645045838882956, 3))
    plt.ylabel("Change in Fed Funds Future between the day after the last cut/hike and the day after the FOMC meeting")
    plt.xlabel("Rate Hike/Cut")
    plt.title("Effectiveness of Fed Rate/Hike in predicting Fed Funds Future one day after meeting")
    plt.legend()

    plt.savefig('../figures/rate_change_on_FFF_2.png', dpi=800)

    slope, intercept, r_value, p_value, std_err = stats.linregress(x_np, y_np)
    print(slope)
    print(intercept)
    print(r_value ** 2)
    print(p_value)

if __name__ == "__main__":
    massivechanges = pd.read_csv("../data/meeting_future_combined_data.csv")
    differenceBeforeAfterFOMC(massivechanges)
    differenceBeforeBeforeFOMC(massivechanges)
    differenceAfterAfterFOMC(massivechanges)