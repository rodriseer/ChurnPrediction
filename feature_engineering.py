import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:47Nbm|}4B11=@localhost/churn_db')

class FeatEngineering:
    def __init__(self):
        pass
    
    def merge_and_churn(self):
        #fetching all data
        customers = pd.read_sql_query("SELECT * FROM customers", engine)
        subscriptions = pd.read_sql_query("SELECT * FROM subscriptions", engine)
        interactions = pd.read_sql_query("SELECT * FROM interactions", engine)
        
        # left merging
        data = customers.merge(subscriptions, on='customer_id', how ='left')
        data = data.merge(interactions, on='customer_id', how = 'left')

        # creating features
        data['account_age_days'] = (pd.to_datetime('today') - pd.to_datetime(data['sign_up_date'])).dt.days
        interaction_counts = interactions.groupby('customer_id').size().reset_index(name = 'interaction_count')
        data = data.merge(interaction_counts, on = 'customer_id', how = 'left')
        data['interaction_count'].fillna(0, inplace = True)
        # churning !!!
        """
        this 'apply' algorhithm return 1 or 0 using a temp var or: lambda
        
        """
        data['churn'] = data['account_status'].apply(lambda x: 1 if x == 'inactive' else 0)
        # Remove account_status from features to avoid data leakage
        data = data.drop(columns=['account_status'])

        # hot encodinggggg algorhithm
        """
        reason for hot encoding here is to turn textual (column) data into 1 and 0 
        ml algorithms generally don't work well with these textual data directly so hot encoding is neccessary
        converting categorical data into numerical data
        pandas can do that cool huh
        """
        data = pd.get_dummies(data, columns = ['plan_type', 'interaction_type'], drop_first = True)

        # save data to a csv just in case
        data.to_csv('churn_data.csv', index = False)
        print("Feature engineering completed and data prepared.")

feat = FeatEngineering()
feat.merge_and_churn()


















