## Liquidity prediction 2021

The objective of the project is to implement an automated pipeline for predicting the values of time series for the next day. The time series data consists of slices at specific times, including inflows, outflows, and the balance of an indicator related to the Bank's liquidity flows. The forecast should be focused on predicting the balance value, which is the difference between inflows and outflows. The model's customer has specified a requirement that the forecast error should not exceed 0.42 in absolute value.

By analyzing the provided data and utilizing the functionalities of the tslib library and associated notebooks, the project aims to accurately predict the next day's time series values, ultimately meeting the customer's requirement for forecast accuracy.

## The project includes the following files and folders:

tslib: This is a developed library specifically for this project. It contains the following modules:

calibrate.py: A module for model calibration.
cusum_finder.py and shiryaev_roberts_finder.py: Modules for detecting mean discord using cumulative sums and variances through Shiryaev-Roberts statistics.
scoring.py: A module for calculating main metrics.
feature_selection.py: A module for feature rejection.
notebooks: This folder contains notebooks demonstrating the functionality of the library and pipeline:

Breakpoint-finding.ipynb: Demonstrates the breakpoint search method.
Feature-selection.ipynb: Illustrates the feature rejection method.
Profit.ipynb: Demonstrates the algorithm for calculating profits.
Summary.ipynb: Shows the operation of the pipeline.
parsing_notebook.ipynb: Demonstrates the parsing of data to extract features.
data: This folder contains the data obtained through parsing.




### Model Requirements:

To meet the objectives of the project, the model must satisfy the following requirements:

1. **Metric Selection**: The choice of the metric to be optimized should align with the business needs and goals. It should be selected carefully to ensure it captures the desired performance of the model.

2. **Incorporation of External Factors**: The model can utilize external factors, as indicated by the provided hints, to enhance its predictive capabilities. These factors should be identified and integrated appropriately into the model.

3. **Feature Selection Module**: The model must include a feature selection module. The selection method should demonstrate stability compared to alternative methods. At least one method from each category - inline, wrapper, and filter - should be compared. Additionally, one of the alternatives should explore non-linear dependencies in the data.

4. **Automatic Hyperparameter Selection**: The model should automatically select hyperparameters to optimize the target metric. This ensures efficient parameter tuning and improved model performance.

5. **Calibration Frequency**: If the model requires calibration over an extended period, the frequency of calibration should be determined. It is essential to assess the sufficiency of calibration to maintain optimal model performance.

6. **Documentation of Blocks**: All blocks within the model should be appropriately labeled and accompanied by concise descriptions. These descriptions should outline the implementation rationale and provide an overview of how each block functions.

7. **Automatic Retraining**: The model should be designed for automatic retraining. All modules should operate without manual adjustments. The choice of the retraining period must be justified based on the specific needs of the project.

8. **Discord Detection Module**: The model must include a discord detection module to identify potential anomalies or deviations. This module should provide alerts for the need to switch to manual process control or unscheduled retraining when necessary.

By fulfilling these requirements, the model will be capable of optimizing performance metrics, incorporating external factors, selecting relevant features, automatically adjusting hyperparameters, providing calibrated predictions, and signaling any abnormalities or issues that require manual intervention or retraining.