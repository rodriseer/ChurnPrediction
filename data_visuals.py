import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import time

# connecting to the sql db via sqlalchemy instead of mysql conn, due to pandas conflict
engine = create_engine('mysql+pymysql://root:(password)@localhost/churn_db')

interactions = pd.read_sql_query("SELECT * FROM interactions", engine)

class DataVisualization:
    def __init__(self):

        self.basic = 0
        self.pro = 0
        self.premium = 0
        
    def customer_counter(self):
        """
        method to pull total # of customers from the table
        
        """
        customer_count_df = pd.read_sql_query("SELECT COUNT(*) as total_customers FROM customers", engine)
        # extracting numbers
        # starting from table 0 through iloc[0]
        customer_count = customer_count_df['total_customers'].iloc[0]
        return customer_count
    
    def subs_counter(self):
        """
        method to pull subscriptions vs non subscriptions data
        """
        subs_count_df = pd.read_sql_query("SELECT COUNT(*) as total_subs FROM subscriptions", engine)
        subs_count = subs_count_df['total_subs'].iloc[0]

        # count how many subs have 'basic' as plan_type
        basic_count_df = pd.read_sql_query("SELECT COUNT(*) as basic_subs FROM subscriptions WHERE plan_type = 'basic'", engine)
        basic_subs = basic_count_df['basic_subs'].iloc[0]

        # count how many subs have 'pro'
        pro_count_df = pd.read_sql_query("SELECT COUNT(*) as pro_subs FROM subscriptions WHERE plan_type = 'pro'", engine)
        pro_subs = pro_count_df['pro_subs'].iloc[0]

        # count how many subs are premium
        premium_count_df = pd.read_sql_query("SELECT COUNT(*) as premium_subs FROM subscriptions WHERE plan_type = 'premium'", engine)
        premium_subs = premium_count_df['premium_subs'].iloc[0]

        return subs_count, basic_subs, pro_subs, premium_subs

    def visualizations(self):
        # call method o get count
        customer_count = self.customer_counter()
        subs_count, basic_subs, pro_subs, premium_subs = self.subs_counter()
        
        # plot data visualizations for custoemers
        plt.bar(['customers'], [customer_count])
        plt.ylabel('number of customers')
        plt.title('customer count')
        plt.show()

        # plot data visualizations for subscriptions
        plt.bar(['subscriptions'], [subs_count])
        plt.ylabel('number of susbs')
        plt.title("subs count")
        plt.show()

        # pie chart for subs type
        labels = ['basic', 'pro', 'premium']
        sizes = [basic_subs, pro_subs, premium_subs]
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title('Subs Types')
        plt.show()

# instance of the class
data_visu = DataVisualization()
data_visu.visualizations()
