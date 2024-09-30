import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression


class ModelTraining:
    def __init__(self):
        self.x_train = None
        self.x_test = None
        self.y_train = None
        self.y_test = None
        self.model = None

    def load_and_split_data(self):
        # load the prepared data
        data = pd.read_csv('churn_data.csv')

        # removed 'customer_id' as it's not useful for predictions in this model
        data = data.drop(columns=['customer_id'])

        # convert date columns to datetime format and extract year, month, and day
        date_columns = ['sign_up_date', 'last_login', 'start_date', 'interaction_date', 'end_date']
        for col in date_columns:
            if col in data.columns:
                data[col] = pd.to_datetime(data[col], errors='coerce')
                data[f'{col}_year'] = data[col].dt.year
                data[f'{col}_month'] = data[col].dt.month
                data[f'{col}_day'] = data[col].dt.day
                data = data.drop(columns=[col])

        # drop
        data = data.drop(columns=['details'])

        # check for remaining non-numeric columns (for debugging purposes)
        print("Non-numeric columns:\n", data.select_dtypes(include=['object']).columns)

        # define features (x) and target (y)
        x = data.drop(columns=['churn'])  # 'churn' is the target variable
        y = data['churn']

        # split the data into training (80%) and testing (20%)
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x, y, test_size=0.2, random_state=42)
        print("Data successfully split!")

    def train_model(self):
        # initialize and train the model

        """
        my model training:
        max_depth=5: Limits the depth of the decision tree to avoid overfitting
        min_samples_split=10: Sets the minimum number of samples needed to split a node
        min_samples_leaf=5: Ensures each leaf node has at least 5 samples
        """
        self.model = DecisionTreeClassifier(random_state=42, max_depth = 5, min_samples_split=10, min_samples_leaf=5)
        self.model.fit(self.x_train, self.y_train)
        print("Model training complete")

    def call_prediction(self):
        # make predictions
        y_pred = self.model.predict(self.x_test)
        print("Predictions made")
        return y_pred

    def evaluate_model(self, y_pred):
        # evaluate model accuracy
        accuracy = accuracy_score(self.y_test, y_pred)
        print(f"Accuracy: {accuracy * 100:.2f}%")
        # additional evaluation metrics
        report = classification_report(self.y_test, y_pred)
        print("Classification Report:\n", report)


trainer = ModelTraining()
trainer.load_and_split_data()
trainer.train_model()
predictions = trainer.call_prediction()
trainer.evaluate_model(predictions)