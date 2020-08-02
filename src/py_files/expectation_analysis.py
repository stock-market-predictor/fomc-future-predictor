import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from calendar import monthrange

sns.set_style('darkgrid')

def calculateDataPredictors(massivechanges):
    expectation_df = massivechanges[
        ['Converted_Datetime', 'Rate', 'Ratedaybefore', 'Ratedayafter', 'Rate Changes', 'difference']].copy()

    expectation_df['Converted_Datetime'] = expectation_df['Converted_Datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

    returnlist = []
    for i in range(len(expectation_df['Converted_Datetime'])):
        if i == len(expectation_df['Converted_Datetime']) - 1:
            returnlist.append(1)
        else:
            value = (expectation_df['Converted_Datetime'][i].month - expectation_df['Converted_Datetime'][i + 1].month) % 12
            if value <= 1:
                returnlist.append(1)
            else:
                returnlist.append(2)
    expectation_df['Month Type'] = pd.Series(returnlist)

    expectation_df['N'] = expectation_df['Converted_Datetime'].apply(lambda x: monthrange(x.year, x.month)[1])
    expectation_df['M'] = expectation_df['Converted_Datetime'].apply(lambda x: x.day - 1)
    expectation_df['ImpliedRate'] = expectation_df['Ratedaybefore'].apply(lambda x: 100 - x)

    def averageoverspan(datetime1, datetime2, price_dict):
        change = datetime1
        total = 0
        count = 0
        while change < datetime2:
            if change in price_dict:
                total += price_dict[change]
                count += 1
            change += timedelta(1)
        return total / count

    priceoffutures = pd.read_csv('../data/30-day-fed-funds-futures.csv')
    priceoffutures['Date'] = priceoffutures['date'].apply(lambda x: datetime.strptime(x, '%m/%d/%Y'))
    del priceoffutures['date']

    priceoffutures_dict = {}
    for i in range(priceoffutures.shape[0]):
        priceoffutures_dict[priceoffutures['Date'][i]] = priceoffutures[' value'][i]

    returnlist = []
    for i in range(len(expectation_df['Converted_Datetime'])):
        end_dt = datetime(expectation_df['Converted_Datetime'][i].year, expectation_df['Converted_Datetime'][i].month, 1) - timedelta(1)
        beginning_dt = datetime(end_dt.year, end_dt.month, 1)
        returnlist.append(100 - averageoverspan(beginning_dt, end_dt, priceoffutures_dict))

    expectation_df['FFER.Start'] = pd.Series(returnlist)

    returnlist = []
    for i in range(len(expectation_df['Converted_Datetime'])):
        N = expectation_df['N'][i]
        M = expectation_df['M'][i]

        value = N / (N - M) * (expectation_df['ImpliedRate'][i] - (M / N) * expectation_df['FFER.Start'][i])

        returnlist.append(value)
    expectation_df['FFER.End'] = pd.Series(returnlist)

    P_Hikelist = []
    for i in range(len(expectation_df['FFER.Start'])):
        value = (expectation_df['FFER.End'][i] - expectation_df['FFER.Start'][i]) / .25
        P_Hikelist.append(value)
    expectation_df['P_Hike'] = pd.Series(P_Hikelist)

    expectation_df['P_Hike_Normalized_Index'] = (expectation_df['P_Hike'] - np.mean(expectation_df['P_Hike'])) / np.std(
        expectation_df['P_Hike'])
    expectation_df['Rate_Change_Normalized'] = (expectation_df['Rate Changes'] - np.mean(
        expectation_df['Rate Changes'])) / np.std(expectation_df['Rate Changes'])
    expectation_df['Shock_Index'] = abs(
        expectation_df['P_Hike_Normalized_Index'] - expectation_df['Rate_Change_Normalized'])

    # Taking the absolute value of the shock will produce a better linear regression
    # expectation_df['difference'] = abs(expectation_df['difference'])

    return expectation_df

def generateFigure(expectation_df):
    x = expectation_df['Shock_Index']
    y = expectation_df['difference']
    x_np = expectation_df['Shock_Index'].to_numpy()
    y_np = (expectation_df['difference']).to_numpy()
    m, b = np.polyfit(x_np, y_np, 1)

    fig = plt.figure(figsize=(10, 10))
    sns.scatterplot(x='Shock_Index', y='difference', data=expectation_df)
    plt.xlabel('Deviance from expectations')
    plt.ylabel("Difference before and after FOMC decision")
    plt.title('Effect of shocking FOMC decisions on Federal Funds Future')
    plt.plot(x, m * x + b, 'r-',
             label='y = {0:.{1}f}'.format(m, 6) + 'x + {0:.{1}f}'.format(b, 6) + '\nr^2 = {0:.{1}f}'.format(
                 0.14164875417905126, 3))
    plt.legend()

    plt.savefig('../figures/expectations_on_FFF.png', dpi=800)

    slope, intercept, r_value, p_value, std_err = stats.linregress(x_np, y_np)
    print(slope)
    print(intercept)
    print(r_value ** 2)
    print(p_value)

if __name__ == "__main__":
    massivechanges = pd.read_csv("../data/meeting_future_combined_data.csv")
    expectation_df = calculateDataPredictors(massivechanges)
    generateFigure(expectation_df)
