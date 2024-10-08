from faker import Faker
import mysql.connector
from random import choice
from datetime import date

# initialize faker, using a seed so every time the faker is used the same is also generated
fake = Faker()
fake.seed_instance(9971)

# connecting to the sql db
conn = mysql.connector.connect(
    host="localhost",        
    user="root",            
    password="(password)",
    database="churn_db"
)

# cursor to the db
"""
cursor to allow us to interact with the database
so I can execute SQL commands like SELECT, INSERT, UPDATE
also manage the result sets returned by those queries.
"""
cursor = conn.cursor()


class SQLDataInserter:
    def __init__(self, conn, cursor):
        # initialize class with database connection
        self.conn = conn
        self.cursor = cursor

    def insert_customers(self, num_customers = 100):
        # insert data into customer table
        """
        iterate through customer_id first because that will tell how many customers are in the business
        description of loop: 1, 100. will create 100 instances of customers, this can be modified as will
        """
        for customer_id in range(1, num_customers +1):
            """
            sign_up_date = randomly generated date between 2 years ago (-2y) and 1 year ago (-1y).
            account_status = choice(['active', 'inactive']) works as active or inactive accounts
            last_login = random genearate date between sign up date and today, logic here is that the custoemr logged in after signing up....
            """
            sign_up_date = fake.date_between(start_date='-2y', end_date='-1y')
            account_status = choice(['active', 'inactive'])
            last_login = fake.date_between(start_date = sign_up_date, end_date='today')

            # burn it!
            self.cursor.execute("""
                INSERT INTO customers (sign_up_date, account_status, last_login)
                VALUES (%s, %s, %s)
            """, (sign_up_date, account_status, last_login))
        # committing customers
        self.conn.commit()
        print(f"{num_customers} have been inserted!")


    def insert_subs(self, num_subs = 100):
        """
        iterate through subscrptions_id first because that will tell how many subss are in the business
        description of loop: 1, 100. will create 100 instances of subs, this can be modified as will
        """
        for subscription_id in range(1, num_subs+1):
            """
            customer_id = using choice to random choose between 1, 100 customers that are subscriber
            start_date = random date between 1 yer ago and today for when the subscrition ended
            end_date = randomly generated end date between start_date and today, or None if the sub hasnt ended today
            plan_type = randomly selected plan type ('basic', 'premium', or 'pro')
            """
            customer_id = choice(range(1,101))
            start_date = fake.date_between(start_date='-1y', end_date = 'today')
            end_date = fake.date_between(start_date=start_date, end_date = 'today') if choice([True, False]) else None
            plan_type = choice(['basic', 'premium', 'pro'])

            # burn it!
            self.cursor.execute("""
            INSERT INTO subscriptions (customer_id, start_date, end_date, plan_type)                   
            VALUES (%s, %s, %s, %s)           
        """, (customer_id, start_date, end_date, plan_type))
        # subscriptions commiting
        self.conn.commit()
        print("Subs table populated.")


    def insert_interactions(self, num_interactions = 200):
        """
        interactions with the business
        in range of 1 to 500 interaction, can be changed at will
        """
        for interaction_id in range(1, num_interactions +1):
            """
            customer_id = random choice between 1, 100 - use your real number of customers for better precision
            interaction_date = random date between 1 year ago and today
            interaction_type = random "choice", what kind of interactions type?
            details = fake details, 200 chars max, can be modified for chars
            """
            customer_id = choice(range(1, 101))
            interaction_date = fake.date_between(start_date='-1y', end_date='today')
            interaction_type = choice(['email', 'call', 'in_person'])
            details = fake.text(max_nb_chars=200)

            self.cursor.execute("""
                INSERT INTO interactions (customer_id, interaction_date, interaction_type, details)
                VALUES (%s, %s, %s, %s)
            """, (customer_id, interaction_date, interaction_type, details))

        # Commit all interactions at once
        self.conn.commit()
        print("Interactions table populated.")

    def close_connection(self):
    
        self.cursor.close()
        self.conn.close()
        print("Database connection closed.")

# instance of the class
inserter = SQLDataInserter(conn, cursor)

# insert num of customers into the database
inserter.insert_customers(100)
inserter.insert_subs(100)
inserter.insert_interactions(200)

# close the connection after all data has been inserted
inserter.close_connection()
