
## Task

 to develop and implement a market risk assessment model for this portfolio. The following steps should be taken:

1. Identify and discuss the relevant risk factors:
   - If there are missing data for selected risk factors, obtain or calculate the necessary data.
   - Visualize the historical values of risk factors and analyze descriptive statistics, including correlations, tail heaviness of distributions, and trends.
   - Utilize principal component analysis or factor analysis to reduce the number of factors.

2. Select appropriate dynamics models for all risk factors:
   - Consider the descriptive statistics obtained in the previous step when choosing the models.
   - Estimate model parameters using available historical data if needed.

3. Evaluate the fair value and cost of instruments in the portfolio based on the risk factors:
   - Critically discuss the chosen valuation model.
   - Validate the accuracy of the model.

4. Estimate portfolio risk for each trading day using the available historical data, considering 1-day and 10-day horizons:
   - Choose risk measures such as Value-at-Risk (VaR) at 99% and Expected Shortfall at 97.5%.
   - Generate a sample from the distribution of risk factors based on the selected dynamics models.
   - Construct a sample of portfolio values using the previous day's instrument prices, assuming daily rebalancing.
   - Calculate the necessary risk measures based on the constructed sample.

5. Perform quantitative validation (backtesting) of the VaR:
   - Calculate risk measures for each trading day of the year.
   - Count the number of breaches.
   - Test the hypothesis of accurate estimation.
   - Critically discuss the results of the validation for the overall portfolio and the sub-portfolios (stocks, bonds, currency).

By following these steps and conducting thorough analysis and validation, we can build and implement an effective market risk assessment model for the portfolio.

EDA. ipynb - exploring time series and VaR models

Modeling.ipynb  - VaR (cVaR) calculation for the whole investment portfolio using different models 
