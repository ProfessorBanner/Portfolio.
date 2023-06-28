from metaflow import FlowSpec, step

class DataProcessingFlow(FlowSpec):

    @step
    def start(self):
        import yfinance as yf
        
        self.data = yf.download("SPY AAPL CHF=X ^TNX ^VIX EURUSD=X", start="2005-01-01", end="2023-04-30")
        self.next(self.select_features)
    
    @step
    def select_features(self):
        selected_col = [('Open', 'AAPL'),
                        ('High', 'AAPL'),
                        ('Low', 'AAPL'),
                        ('Volume', 'AAPL'),
                        ('Adj Close', 'AAPL'),
                        ('Adj Close', 'SPY'),
                        ('Adj Close', '^VIX'),
                        ('Adj Close', '^TNX'),
                        ('Adj Close', 'CHF=X'),
                        ('Adj Close', 'EURUSD=X')
                       ]
        self.df = self.data[selected_col]
        self.next(self.drop_multiindex)
    
    @step
    def drop_multiindex(self):
        self.df.columns = self.df.columns.map(''.join)
        self.next(self.reset_date_index)
    
    @step
    def reset_date_index(self):
        self.df.index = self.data.index
        self.next(self.end)
    
    @step
    def end(self):
        pass

if __name__ == '__main__':
    DataProcessingFlow()
