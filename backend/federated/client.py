# backend/federated/client.py

import argparse
import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import flwr as fl

# Set random seed for reproducibility
np.random.seed(42)

class FlowClient(fl.client.NumPyClient):
    def __init__(self, model, X_train, y_train, X_test, y_test):
        self.model = model
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test

    def get_parameters(self, config):
        print("[Client] get_parameters called")
        if hasattr(self.model, "coef_"):
            return [self.model.coef_, self.model.intercept_]
        return []

    def fit(self, parameters, config):
        print("[Client] fit called - updating local model weights with global weights")
        self.model.coef_ = parameters[0]
        if len(parameters) > 1:
            self.model.intercept_ = parameters[1]
        
        # Train model locally
        self.model.fit(self.X_train, self.y_train)
        
        # Return updated parameters, training set size, and empty metrics
        return [self.model.coef_, self.model.intercept_], len(self.X_train), {}

    def evaluate(self, parameters, config):
        print("[Client] evaluate called - updating local model weights with global weights")
        self.model.coef_ = parameters[0]
        if len(parameters) > 1:
            self.model.intercept_ = parameters[1]
            
        preds = self.model.predict(self.X_test)
        loss = 0.0  # Dummy loss as scikit-learn does not expose iteration-wise loss directly
        accuracy = accuracy_score(self.y_test, preds)
        print(f"[Client] Local evaluation accuracy: {accuracy:.4f}")
        return loss, len(self.X_test), {"accuracy": accuracy}

def main():
    parser = argparse.ArgumentParser(description="Flower client for anomaly detection")
    parser.add_argument("--client-id", type=int, required=True, choices=[0, 1], help="Client ID (0 or 1)")
    parser.add_argument("--server-address", type=str, default="127.0.0.1:8080", help="Flower server address")
    args = parser.parse_args()

    csv_path = f"backend/federated/data/client_{args.client_id}.csv"
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Data shard not found: {csv_path}. Please run data_split.py first.")

    print(f"[Client {args.client_id}] Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Separate features and label
    X = df.drop(columns=["label"]).values
    y = df["label"].values

    # Train/test split locally
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Create Logistic Regression model
    # warm_start=True allows incremental training in federated rounds
    # saga is a fast solver for multi-class classification and large datasets
    model = LogisticRegression(
        max_iter=5,
        warm_start=True,
        solver="saga",
        random_state=42
    )

    # Pre-fit to initialize model parameters (coef_ and intercept_)
    print(f"[Client {args.client_id}] Initializing model parameters...")
    model.fit(X_train, y_train)

    # Start the client
    client = FlowClient(model, X_train, y_train, X_test, y_test)
    print(f"[Client {args.client_id}] Connecting to server at {args.server_address}...")
    fl.client.start_numpy_client(
        server_address=args.server_address,
        client=client
    )

if __name__ == "__main__":
    main()
