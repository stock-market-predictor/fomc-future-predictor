# fomc-future-predictor
### Necessary Technology
    Python v3.6
    Jupyter v1.0.0
### Python Libaries and Versions
    pandas v1.0.0
    numpy v1.18.1
    requests v2.22.0
    bs4 v0.0.1
    datetime v4.3
    matplotlib v3.1.2
    seaborn v0.9.0
    scipy v1.4.1


### Analysis

We scraped data from Wikipedia and the FOMC website on the various dates that the FOMC hosted a meeting to change the rate. Then we stored and graphed the various rate changes with corresponding Fed Funds prices to analyze the effects of FOMC meetings on the price of the 30 day Fed Funds Futures. We analyzed data from 2002 onwards. 
![Graph 1](/src/figures/rate_change_on_FFF.png)
The graph shows the immediate effect of the FOMC meeting decision (cut, unch, hike) on the price of the 30 day Fed Funds Future (price day after - price day before). We see a slight negative correlation between the variables. However, we believe that this analysis is incompelete for two reasons. First, most rate changes are 25 bps in size, and therefore our correlation is mostly due to outliers. Secondly, we believe that large changes in the price of the 30 day Fed Funds Future are mostly due to unexpected FOMC meeting decisions rather than shifts themselves. 

![Graph 2](/src/figures/FFF_on_rate_change.png)
Next is our attempt at predicting (or finding a correlation to) the proposed rate change at the next FOMC meeting. We plotted the difference in price between the 30 day Fed Funds Future before the previous meeting and the current meeting versus the rate change (hike, cut, unch) proposed by the FOMC. This data shows a strong positive correlation between the variables, and even holds relatively consistent for lower bound outliers (for reference, it holds consistent for the March 15 double cut FOMC meeting). 

![Graph 3](/src/figures/rate_change_on_FFF_2.png)
Next, in our attempt to reach profitability (or approach the beginnings of a trading strategy), we plotted the rate change versus the difference in price between the 30 day Fed Funds Future after the previous meeting and after the current meeting. This allows us to predict the immediate shift in the price of the 30 day Fed Funds Future after the FOMC meeting concludes (and the rates are announced). We see that there is a strong positive correlation between the two variables, however outliers vary wildly. 

![Graph 3](/src/figures/expectations_on_FFF.png)
Finally, this is our attempt at analyzing the effects of expectation on the price of the 30 Day Fed Funds future. We hypothesized that when market expectations were not in alignment with the resulting rate change from the FOMC meeting that the magnitude of the price difference would increase. That being said, we created a customized "shock" index in order to measure the difference between market expectation and rate change. We calculated market expectation using the formulas provided on CME's Fed Watch tool, and took the difference between the normalized market expectation and normalized rate change to arrive at our customized shock index. When graphed, we see a slight positive correlation between the two variables that seems to slightly suggest that our hypothesis is correct, however more refinement is necessary. 

### Future Steps
We want to create a better customized shock index. We saw many potential faults with the index, but the greatest of which was the method of calculating market expectation. We did not like CME's method of calculating market expectation, especially when the formulas on their website used the future price of the Fed Funds future to back-calculate the market expectation. This seemed problematic for a project that was attempting to predict the future price of the Fed Funds future, and as a result wouldn't have access to that information. We would like to find a better method of calculating market expectations, or generate our own. 

It would also be helpful to factor in market volatility and whether the FOMC press conference projected hawkish or dovish sentiment. As respect to the second point, we can see that recently (in the March 15th conference), that it wasn't necessarily the double cut that affected the price of the Fed Funds future, but the fact that the Fed projected dovish sentiments in the press conference. 
