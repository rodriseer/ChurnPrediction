import pandas as pd
from sqlalchemy import create_engine
import time

# connecting to the sql db via sqlalchemy instead of mysql conn, due to pandas conflict
engine = create_engine('mysql+pymysql://root:47Nbm|}4B11=@localhost/churn_db')

customers = pd.read_sql_query("SELECT * FROM customers", engine)
subscriptions = pd.read_sql_query("SELECT * FROM subscriptions", engine)
interactions = pd.read_sql_query("SELECT * FROM interactions", engine)

"""
this will tell us if there any missing values on tables
if 1 or more, raises warning
"""
class ValuesChecker:

    def __init__(self, df):
        self.df = df

    def check_missing_values_customers(self):
        print("Checking customers table for empty values...")
        for column in self.df.columns:
            missing_count =  self.df[column].isnull().sum()
            if missing_count > 0:
                print(f"Warning! {column} has {missing_count} missing values!")
            else:
                print(f"Everything ok with {column}!")

        time.sleep(2)
        print("\n")

    def check_missing_values_subscriptions(self):
        print("Checking subscriptions for empty values...")
        for column in self.df.columns:
            if self.df[column].isnull().sum() > 0:
                if column == 'end_date':
                    print(f"{column} has missing values, but this is acceptable due to the fact that this indicates current subs")
                else:
                    pass
            else:
                print(f"Everything ok with {column}")
        time.sleep(2)
        print("\n")

    def check_missing_values_interactions(self):
        print("Checking interactions table...")
        for column in self.df.columns:
            if self.df[column].isnull().sum() > 0:
                print(f"{column} has missing values!")
            else:
                print(f"Everything ok with {column}")
        time.sleep(2)
        print("\n")

customer_checker = ValuesChecker(customers)
subs_checker = ValuesChecker(subscriptions)
interactions_checker = ValuesChecker(interactions)
customer_checker.check_missing_values_customers()
subs_checker.check_missing_values_subscriptions()
interactions_checker.check_missing_values_interactions()