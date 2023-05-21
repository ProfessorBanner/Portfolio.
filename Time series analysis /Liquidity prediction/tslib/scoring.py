import numpy as np
import pandas as pd
from sklearn.metrics import make_scorer

key_rate = 0.07
day_deposit_rate = key_rate + 0.5 / 100
night_deposit_rate = key_rate - 0.9 / 100
night_loan_rate = key_rate + 1 / 100


def get_score(trues,
              preds,
              day_deposit_rate=day_deposit_rate,
              night_deposit_rate=night_deposit_rate,
              night_loan_rate=night_loan_rate,
              return_all_values=False):

    trues = trues.copy()
    profit = np.zeros(trues.shape)

    # Start of the day
    positive_pred_mask = (preds > 0)
    # Adding forecating 
    profit[positive_pred_mask] += day_deposit_rate * preds[positive_pred_mask]
    # Liquidity decrease
    trues[positive_pred_mask] -= preds[positive_pred_mask]
    # Cover the liquidity deficit if the score < 0
    trues[~positive_pred_mask] -= preds[~positive_pred_mask]

    # End of the day
    positive_balance_mask = (trues > 0)
    # If the liquidity is positive we invest 
    profit[positive_balance_mask] += night_deposit_rate * trues[positive_balance_mask]
    # In case of deficit we borrow
    profit[~positive_balance_mask] += night_loan_rate * trues[~positive_balance_mask]

    if return_all_values:
        return profit
    else:
        return profit.sum()


get_score_estimator = make_scorer(get_score)
