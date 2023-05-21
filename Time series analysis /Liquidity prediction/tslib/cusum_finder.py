import numpy as np
from scipy.stats import norm

# Neyman–Pearson test for the mean
def normal_likelihood(value, mean_0, mean_8, std):
    return np.log(norm.pdf(value, mean_0, std) / 
                  norm.pdf(value, mean_8, std))

class CusumFinder():
    
    def __init__(self, alpha, beta, mean_diff, trsh=2, breaks_max=5,
                slice_length=15):
        
        self.mean_hat = 0
        self.std_hat = 1
        
        self.alpha = alpha
        self.beta = beta
        
        self.metric = 0
        
        #Hyperparameter for alternative hypothesis
        self.mean_diff = mean_diff 
        #Threshold
        self.trsh = trsh
        # Hyperparameter for the max number of breaks
        self.breaks_max = breaks_max
        
        self.states = []
        self.breakpoints = []
        # Additional hyperparameter for the depth of slice
        self.slice_length = slice_length
        self.colors=['blue', 'red']
        
    def get_values(self):
        # Mean and std esimation
        try:
            self.mean_hat = self.mean_values_sum / self.mean_weights_sum
            self.var_hat = self.var_values_sum / self.var_weights_sum
        except AttributeError:
            self.mean_hat = 0
            self.var_hat = 1
    
    def update(self, new_value):

        self.get_values()
        
        # Normalisation and stadartisation
        self.new_value_normalized = (new_value - self.mean_hat) / np.sqrt(self.std_hat)
        
        # Update mean and std^2
        try:
            self.mean_values_sum = (1 - self.alpha) * self.mean_values_sum + new_value
            self.mean_weights_sum = (1 - self.alpha) * self.mean_weights_sum + 1.0
        except AttributeError:
            self.mean_values_sum = new_value
            self.mean_weights_sum = 1.0 
        
        # New std^2 value
        new_value_var = (self.new_value_normalized - self.mean_hat)**2
        
        try:
            self.var_values_sum = (1 - self.beta) * self.var_values_sum + new_value_var
            self.var_weights_sum = (1 - self.beta) * self.var_weights_sum + 1.0
        except:
            self.var_values_sum = new_value_var
            self.var_weights_sum = 1.0      

    def count_metric(self):
        # Chech the hypothesis that the mean = 0
        zeta_k = normal_likelihood(self.new_value_normalized, self.mean_diff, 0., 1)
        self.metric = max(0, self.metric + zeta_k)

        if self.metric > self.trsh:            
            self.states.append(1)
        else:
            self.states.append(0)
            
        if (np.array(self.states[-self.slice_length:]) == 1).sum() > self.breaks_max:
            self.breakpoints.append('red')
        else:
            self.breakpoints.append('blue')
            
