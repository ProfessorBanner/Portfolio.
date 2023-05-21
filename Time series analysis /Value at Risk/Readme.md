
## Task

 to develop and implement a market risk assessment model for this portfolio. The following steps should be taken:

1. Identify and discuss the relevant risk factors:
   a. If there are missing data for selected risk factors, obtain or calculate the necessary data.
   b. Visualize the historical values of risk factors and analyze descriptive statistics, including correlations, tail heaviness of distributions, and trends.
   c. Utilize principal component analysis or factor analysis to reduce the number of factors.

2. Select appropriate dynamics models for all risk factors:
   a. Consider the descriptive statistics obtained in the previous step when choosing the models.
   b. Estimate model parameters using available historical data if needed.

3. Evaluate the fair value and cost of instruments in the portfolio based on the risk factors:
   a. Critically discuss the chosen valuation model.
   b. Validate the accuracy of the model.

4. Estimate portfolio risk for each trading day using the available historical data, considering 1-day and 10-day horizons:
   a. Choose risk measures such as Value-at-Risk (VaR) at 99% and Expected Shortfall at 97.5%.
   b. Generate a sample from the distribution of risk factors based on the selected dynamics models.
   c. Construct a sample of portfolio values using the previous day's instrument prices, assuming daily rebalancing.
   d. Calculate the necessary risk measures based on the constructed sample.

5. Perform quantitative validation (backtesting) of the VaR:
   a. Calculate risk measures for each trading day of the year.
   b. Count the number of breaches.
   c. Test the hypothesis of accurate estimation.
   d. Critically discuss the results of the validation for the overall portfolio and the sub-portfolios (stocks, bonds, currency).

By following these steps and conducting thorough analysis and validation, we can build and implement an effective market risk assessment model for the portfolio.

EDA. ipynb - exploring time series and VaR models

Modeling.ipynb  - VaR (cVaR) calculation for the whole investment portfolio using different models 
