import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def getFOMCChanges():
    url = 'https://en.wikipedia.org/wiki/History_of_Federal_Open_Market_Committee_actions'
    html = requests.get(url).content
    df_list = pd.read_html(html)
    massivechanges = df_list[1]
    return massivechanges

def getFOMCDates(decade):
    url = f'https://fraser.stlouisfed.org/title/federal-open-market-committee-meeting-minutes-transcripts-documents-677?browse={decade}s'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    dateList = soup.find_all('span', {'class': 'list-item-title'})
    dList = []

    def parseString():
        for i in range(len(dateList)):
            s = dateList[i].text
            ind = s.find('Meeting, ')
            if ind != None and ind != -1:
                dateStr = s[ind + 9:]
                dateStr = dateStr[:dateStr.find(',') + 6]
                if dateStr.find('-') != -1:
                    dateStr = dateStr[:dateStr.find('-')] + dateStr[dateStr.find(','):]
                dList.append(dateStr)

    parseString()
    return dList

def fullFOMCDatesRates():
    massivechanges = getFOMCChanges()

    dateList = getFOMCDates(2000) + getFOMCDates(2010) + [getFOMCDates(2020)[0]]
    def strToCal(s):
        return datetime.strptime(s, '%B %d, %Y')
    dateTimeList = list(map(strToCal, dateList))

    dfList = []
    d = datetime(2002, 12, 10)
    for elem in dateTimeList:
        if elem > d:
            dfList.append([None, elem])
    df = pd.DataFrame(dfList, columns=['Fed. Funds Rate', 'Converted_Datetime'])

    massivechanges['Converted_Datetime'] = massivechanges['Date'].apply(lambda x: datetime.strptime(x, '%B %d, %Y'))
    del massivechanges['Votes']
    del massivechanges['Date']
    del massivechanges['Notes']
    del massivechanges['Discount Rate']

    massivechanges = massivechanges.append(df, ignore_index=True)
    massivechanges.sort_values(by='Converted_Datetime', ascending=False, inplace=True, ignore_index=True)

    bigChanges = massivechanges.sort_values(by='Converted_Datetime', ignore_index=True)
    for index, row in bigChanges.iterrows():
        if pd.isnull(row['Fed. Funds Rate']):
            if row['Converted_Datetime'] == bigChanges.iloc[index + 1, 1] or row['Converted_Datetime'] == bigChanges.iloc[index + 1, 1] + timedelta(days=-1):
                continue
            else:
                bigChanges.iloc[index, 0] = bigChanges.iloc[index - 1, 0]
    bigChanges.dropna(inplace=True)
    bigChanges.drop_duplicates(inplace=True, ignore_index=True)

    massivechanges = bigChanges.sort_values(by='Converted_Datetime', ascending=False, ignore_index=True)
    return massivechanges

def cleanFOMC():
    massivechanges = fullFOMCDatesRates()

    def parsestring(s):
        if chr(8211) in s:
            w = s.split(chr(8211))
            s1 = w[0][:-1]
            s2 = w[1][:-1]
            return (float(s1) + float(s2)) / 2
        else:
            return float(s[:-1])

    massivechanges['Rate'] = massivechanges['Fed. Funds Rate'].apply(parsestring)
    del massivechanges['Fed. Funds Rate']

    return massivechanges

def futurePrices():
    priceoffutures = pd.read_csv('../data/30-day-fed-funds-futures.csv')
    priceoffutures['Date'] = priceoffutures['date'].apply(lambda x: datetime.strptime(x, '%m/%d/%Y'))
    del priceoffutures['date']

    priceoffutures_dict = {}
    for i in range(priceoffutures.shape[0]):
        priceoffutures_dict[priceoffutures['Date'][i]] = priceoffutures[' value'][i]

    return priceoffutures, priceoffutures_dict

def combineTables():
    massivechanges = cleanFOMC()
    priceoffutures, priceoffutures_dict = futurePrices()

    massivechanges['DayofWeek'] = massivechanges['Converted_Datetime'].apply(lambda x: datetime.weekday(x))
    def rowinpriceoffutures(i):
        for j in range(len(priceoffutures['Date'])):
            if priceoffutures['Date'][j] > i:
                return j - 1
        return -1

    massivechanges['rowinpriceoffutures'] = massivechanges['Converted_Datetime'].apply(lambda x: rowinpriceoffutures(x))
    returnlist = []
    for i in range(len(massivechanges['rowinpriceoffutures'])):
        if massivechanges['DayofWeek'][i] == 5 or massivechanges['DayofWeek'][i] == 6:
            returnlist.append(priceoffutures['Date'][massivechanges['rowinpriceoffutures'][i]])
        else:
            returnlist.append(priceoffutures['Date'][massivechanges['rowinpriceoffutures'][i] - 1])
    massivechanges['Day before'] = pd.Series(returnlist)

    returnlist = []
    for i in range(len(massivechanges['rowinpriceoffutures'])):
        returnlist.append(priceoffutures['Date'][massivechanges['rowinpriceoffutures'][i] + 1])

    massivechanges['Day after'] = pd.Series(returnlist)

    massivechanges['Ratedaybefore'] = massivechanges['Day before'].apply(lambda x: priceoffutures_dict[x])
    massivechanges['Ratedayafter'] = massivechanges['Day after'].apply(lambda x: priceoffutures_dict[x])

    returnlist = []
    for i in range(len(massivechanges['Rate'])):
        if i == len(massivechanges['Rate']) - 1:
            returnlist.append(0)
        else:
            returnlist.append(massivechanges['Rate'][i] - massivechanges['Rate'][i + 1])
    massivechanges['Rate Changes'] = pd.Series(returnlist)

    massivechanges['difference'] = massivechanges['Ratedayafter'] - massivechanges['Ratedaybefore']

    retList = []
    for i in range(len(massivechanges['Ratedaybefore'])):
        if i == len(massivechanges['Ratedaybefore']) - 1:
            retList.append(0)
        else:
            retList.append(massivechanges['Ratedaybefore'][i + 1] - massivechanges['Ratedaybefore'][i])
    massivechanges['difference type 2'] = pd.Series(retList)

    retList = []
    for i in range(len(massivechanges['Ratedayafter'])):
        if i == len(massivechanges['Ratedayafter']) - 1:
            retList.append(0)
        else:
            retList.append(massivechanges['Ratedayafter'][i + 1] - massivechanges['Ratedayafter'][i])
    massivechanges['difference type 3'] = pd.Series(retList)

    massivechanges.to_csv("../data/meeting_future_combined_data.csv")

    return massivechanges


if __name__ == "__main__":
    combineTables()