# backend/federated/server.py

import os
import json
import flwr as fl
from typing import List, Tuple, Dict, Optional

def weighted_average(metrics: List[Tuple[int, Dict[str, fl.common.Scalar]]]) -> Dict[str, fl.common.Scalar]:
    # Multiply accuracy of each client by number of examples used
    accuracies = [num_examples * m["accuracy"] for num_examples, m in metrics]
    examples = [num_examples for num_examples, _ in metrics]
    
    # Aggregate and return custom metric (weighted average)
    if not examples or sum(examples) == 0:
        return {"accuracy": 0.0}
    return {"accuracy": sum(accuracies) / sum(examples)}

class LoggingStrategy(fl.server.strategy.FedAvg):
    def __init__(self, log_path: str, *args, **kwargs):
        # Set evaluation metrics aggregation function
        kwargs["evaluate_metrics_aggregation_fn"] = weighted_average
        super().__init__(*args, **kwargs)
        self.log_path = log_path
        self.accuracy_logs = []
        
        # Ensure results directory exists
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        # Clear/initialize the log file
        with open(self.log_path, "w") as f:
            json.dump([], f)

    def aggregate_evaluate(
        self,
        server_round: int,
        results,
        failures
    ):
        loss_aggregated, metrics_aggregated = super().aggregate_evaluate(server_round, results, failures)
        
        if metrics_aggregated is not None and "accuracy" in metrics_aggregated:
            accuracy = float(metrics_aggregated["accuracy"])
            print(f"[Server] Round {server_round} aggregated accuracy: {accuracy:.4f}")
            
            # Read existing logs if any (safety measure)
            if os.path.exists(self.log_path):
                try:
                    with open(self.log_path, "r") as f:
                        self.accuracy_logs = json.load(f)
                except Exception:
                    pass
            
            # Append new round result
            self.accuracy_logs.append({
                "round": server_round,
                "accuracy": round(accuracy, 4)
            })
            
            # Save updated logs
            with open(self.log_path, "w") as f:
                json.dump(self.accuracy_logs, f, indent=2)
                
        return loss_aggregated, metrics_aggregated

def main():
    print("=== Phase 6: Federated Threat Intelligence Mesh - Flower Server ===")
    
    log_path = "backend/federated/results/accuracy_log.json"
    
    # Create the strategy
    strategy = LoggingStrategy(
        log_path=log_path,
        min_fit_clients=2,
        min_evaluate_clients=2,
        min_available_clients=2,
    )
    
    # Start Flower server for 3 rounds
    num_rounds = 3
    print(f"[Server] Starting Flower server on port 8080 for {num_rounds} rounds...")
    fl.server.start_server(
        server_address="0.0.0.0:8080",
        config=fl.server.ServerConfig(num_rounds=num_rounds),
        strategy=strategy,
    )
    print("[Server] Server run complete.")

if __name__ == "__main__":
    main()
