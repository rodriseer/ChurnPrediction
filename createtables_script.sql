/* customer table */
CREATE TABLE customers(
    customer_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    sign_up_date DATE NOT NULL,
    account_status TEXT CHECK (account_status IN ('active', 'inactive', 'suspended')) NOT NULL,
    last_login DATE
);


/* subscription table */
CREATE TABLE subscriptions(
    subscription_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    customer_id INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    plan_type TEXT CHECK (plan_type IN ('basic', 'premium', 'pro')) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
);

/* interactions table */
CREATE TABLE interactions(
    interaction_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    customer_id INTEGER NOT NULL,
    interaction_date DATE NOT NULL,
    interaction_type TEXT NOT NULL,
    details TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
);