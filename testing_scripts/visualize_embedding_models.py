import matplotlib.pyplot as plt

evaluation_summary = {
    "ada-002": [
        {"threshold": 0.10, "accuracy": 0.575, "precision": 0.575, "recall": 1.000, "f1": 0.730},
        {"threshold": 0.15, "accuracy": 0.575, "precision": 0.575, "recall": 1.000, "f1": 0.730},
        {"threshold": 0.20, "accuracy": 0.575, "precision": 0.575, "recall": 1.000, "f1": 0.730},
        {"threshold": 0.25, "accuracy": 0.575, "precision": 0.575, "recall": 1.000, "f1": 0.730},
        {"threshold": 0.30, "accuracy": 0.575, "precision": 0.575, "recall": 1.000, "f1": 0.730},
        {"threshold": 0.35, "accuracy": 0.575, "precision": 0.575, "recall": 1.000, "f1": 0.730},
        {"threshold": 0.40, "accuracy": 0.575, "precision": 0.575, "recall": 1.000, "f1": 0.730},
        {"threshold": 0.45, "accuracy": 0.575, "precision": 0.575, "recall": 1.000, "f1": 0.730},
        {"threshold": 0.50, "accuracy": 0.575, "precision": 0.575, "recall": 1.000, "f1": 0.730},
        {"threshold": 0.55, "accuracy": 0.575, "precision": 0.575, "recall": 1.000, "f1": 0.730},
        {"threshold": 0.60, "accuracy": 0.575, "precision": 0.575, "recall": 1.000, "f1": 0.730},
        {"threshold": 0.65, "accuracy": 0.575, "precision": 0.575, "recall": 1.000, "f1": 0.730},
        {"threshold": 0.70, "accuracy": 0.575, "precision": 0.575, "recall": 1.000, "f1": 0.730},
        {"threshold": 0.75, "accuracy": 0.575, "precision": 0.575, "recall": 1.000, "f1": 0.730},
        {"threshold": 0.80, "accuracy": 0.825, "precision": 0.767, "recall": 1.000, "f1": 0.868},
        {"threshold": 0.85, "accuracy": 0.975, "precision": 1.000, "recall": 0.957, "f1": 0.978},
        {"threshold": 0.90, "accuracy": 0.950, "precision": 1.000, "recall": 0.913, "f1": 0.955}
    ],
    "3-small": [
        {"threshold": 0.10, "accuracy": 0.575, "precision": 0.575, "recall": 1.000, "f1": 0.730},
        {"threshold": 0.15, "accuracy": 0.575, "precision": 0.575, "recall": 1.000, "f1": 0.730},
        {"threshold": 0.20, "accuracy": 0.625, "precision": 0.605, "recall": 1.000, "f1": 0.754},
        {"threshold": 0.25, "accuracy": 0.675, "precision": 0.639, "recall": 1.000, "f1": 0.780},
        {"threshold": 0.30, "accuracy": 0.825, "precision": 0.767, "recall": 1.000, "f1": 0.868},
        {"threshold": 0.35, "accuracy": 0.925, "precision": 0.885, "recall": 1.000, "f1": 0.939},
        {"threshold": 0.40, "accuracy": 0.925, "precision": 0.885, "recall": 1.000, "f1": 0.939},
        {"threshold": 0.45, "accuracy": 0.950, "precision": 0.957, "recall": 0.957, "f1": 0.957},
        {"threshold": 0.50, "accuracy": 0.950, "precision": 0.957, "recall": 0.957, "f1": 0.957},
        {"threshold": 0.55, "accuracy": 0.950, "precision": 0.957, "recall": 0.957, "f1": 0.957},
        {"threshold": 0.60, "accuracy": 0.975, "precision": 1.000, "recall": 0.957, "f1": 0.978},
        {"threshold": 0.65, "accuracy": 0.950, "precision": 1.000, "recall": 0.913, "f1": 0.955},
        {"threshold": 0.70, "accuracy": 0.875, "precision": 1.000, "recall": 0.783, "f1": 0.878},
        {"threshold": 0.75, "accuracy": 0.825, "precision": 1.000, "recall": 0.696, "f1": 0.821},
        {"threshold": 0.80, "accuracy": 0.650, "precision": 1.000, "recall": 0.391, "f1": 0.562},
        {"threshold": 0.85, "accuracy": 0.450, "precision": 1.000, "recall": 0.043, "f1": 0.083},
        {"threshold": 0.90, "accuracy": 0.425, "precision": 0.000, "recall": 0.000, "f1": 0.000}
    ],
    "MiniLM": [
        {"threshold": 0.10, "accuracy": 0.575, "precision": 0.575, "recall": 1.000, "f1": 0.730},
        {"threshold": 0.15, "accuracy": 0.725, "precision": 0.676, "recall": 1.000, "f1": 0.807},
        {"threshold": 0.20, "accuracy": 0.875, "precision": 0.821, "recall": 1.000, "f1": 0.902},
        {"threshold": 0.25, "accuracy": 0.900, "precision": 0.852, "recall": 1.000, "f1": 0.920},
        {"threshold": 0.30, "accuracy": 0.975, "precision": 0.958, "recall": 1.000, "f1": 0.979},
        {"threshold": 0.35, "accuracy": 0.975, "precision": 0.958, "recall": 1.000, "f1": 0.979},
        {"threshold": 0.40, "accuracy": 1.000, "precision": 1.000, "recall": 1.000, "f1": 1.000},
        {"threshold": 0.45, "accuracy": 0.975, "precision": 1.000, "recall": 0.957, "f1": 0.978},
        {"threshold": 0.50, "accuracy": 0.925, "precision": 1.000, "recall": 0.870, "f1": 0.930},
        {"threshold": 0.55, "accuracy": 0.875, "precision": 1.000, "recall": 0.783, "f1": 0.878},
        {"threshold": 0.60, "accuracy": 0.850, "precision": 1.000, "recall": 0.739, "f1": 0.850},
        {"threshold": 0.65, "accuracy": 0.825, "precision": 1.000, "recall": 0.696, "f1": 0.821},
        {"threshold": 0.70, "accuracy": 0.800, "precision": 1.000, "recall": 0.652, "f1": 0.789},
        {"threshold": 0.75, "accuracy": 0.700, "precision": 1.000, "recall": 0.478, "f1": 0.647},
        {"threshold": 0.80, "accuracy": 0.525, "precision": 1.000, "recall": 0.174, "f1": 0.296},
        {"threshold": 0.85, "accuracy": 0.450, "precision": 1.000, "recall": 0.043, "f1": 0.083},
        {"threshold": 0.90, "accuracy": 0.450, "precision": 1.000, "recall": 0.043, "f1": 0.083}
    ],
    "FinLang": [
        {"threshold": 0.10, "accuracy": 0.600, "precision": 0.590, "recall": 1.000, "f1": 0.742},
        {"threshold": 0.15, "accuracy": 0.600, "precision": 0.590, "recall": 1.000, "f1": 0.742},
        {"threshold": 0.20, "accuracy": 0.625, "precision": 0.605, "recall": 1.000, "f1": 0.754},
        {"threshold": 0.25, "accuracy": 0.775, "precision": 0.719, "recall": 1.000, "f1": 0.836},
        {"threshold": 0.30, "accuracy": 0.800, "precision": 0.742, "recall": 1.000, "f1": 0.852},
        {"threshold": 0.35, "accuracy": 0.925, "precision": 0.885, "recall": 1.000, "f1": 0.939},
        {"threshold": 0.40, "accuracy": 0.950, "precision": 0.920, "recall": 1.000, "f1": 0.958},
        {"threshold": 0.45, "accuracy": 0.950, "precision": 0.920, "recall": 1.000, "f1": 0.958},
        {"threshold": 0.50, "accuracy": 0.925, "precision": 0.917, "recall": 0.957, "f1": 0.936},
        {"threshold": 0.55, "accuracy": 0.950, "precision": 0.957, "recall": 0.957, "f1": 0.957},
        {"threshold": 0.60, "accuracy": 0.925, "precision": 1.000, "recall": 0.870, "f1": 0.930},
        {"threshold": 0.65, "accuracy": 0.925, "precision": 1.000, "recall": 0.870, "f1": 0.930},
        {"threshold": 0.70, "accuracy": 0.850, "precision": 1.000, "recall": 0.739, "f1": 0.850},
        {"threshold": 0.75, "accuracy": 0.850, "precision": 1.000, "recall": 0.739, "f1": 0.850},
        {"threshold": 0.80, "accuracy": 0.775, "precision": 1.000, "recall": 0.609, "f1": 0.757},
        {"threshold": 0.85, "accuracy": 0.575, "precision": 1.000, "recall": 0.261, "f1": 0.414},
        {"threshold": 0.90, "accuracy": 0.500, "precision": 1.000, "recall": 0.130, "f1": 0.231}
    ]
}


models = evaluation_summary.keys()

plt.figure(figsize=(10, 6))
for model in models:
    thresholds = [entry["threshold"] for entry in evaluation_summary[model]]
    f1_scores = [entry["f1"] for entry in evaluation_summary[model]]
    plt.plot(thresholds, f1_scores, marker='o', label=model)

plt.xlabel("Threshold")
plt.ylabel("F1 Score")
plt.title("Performance Curves: F1 Score vs Threshold")
plt.legend()
plt.grid(True)
plt.show()
