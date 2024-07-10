import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score, roc_curve

# Example confusion matrix
conf_matrix = np.array([
    [30, 2, 1, 0, 1],
    [2, 28, 3, 1, 1],
    [1, 3, 25, 2, 2],
    [0, 2, 2, 27, 3],
    [1, 1, 3, 3, 24]
])

# True labels and predictions (flattened)
true_labels = np.repeat([1, 2, 3, 4, 5], [34, 35, 33, 34, 32])
predicted_labels = np.array([1]*30 + [2]*2 + [3]*1 + [5]*1 + [2]*2 + [2]*28 + [3]*3 + [4]*1 + [5]*1 + [3]*1 + [3]*3 + [3]*25 + [4]*2 + [5]*2 + [4]*27 + [5]*3 + [5]*1 + [5]*1 + [3]*3 + [4]*3 + [5]*24)

# Metrics
precision = precision_score(true_labels, predicted_labels, average=None)
recall = recall_score(true_labels, predicted_labels, average=None)
f1 = f1_score(true_labels, predicted_labels, average=None)
support = np.sum(conf_matrix, axis=1)
specificity = []
for i in range(len(conf_matrix)):
    tn = np.sum(np.delete(np.delete(conf_matrix, i, 0), i, 1))  # True Negatives
    fp = np.sum(conf_matrix[:, i]) - conf_matrix[i, i]  # False Positives
    specificity.append(tn / (tn + fp))

# Assuming we have binary class probabilities for AUC calculation
# y_true_binary and y_pred_prob would be your actual and predicted probabilities
# AUC calculation typically requires binary or probabilistic predictions
# Example:
# y_true_binary = [0, 1, 0, 1, ...]
# y_pred_prob = [0.1, 0.9, 0.2, 0.8, ...]

# Example for class 1
y_true_binary = (true_labels == 1).astype(int)
y_pred_prob = (predicted_labels == 1).astype(int)  # Replace with actual probabilities if available
fpr, tpr, _ = roc_curve(y_true_binary, y_pred_prob)
auc_class1 = roc_auc_score(y_true_binary, y_pred_prob)

# Print results
print("Class-wise Metrics:")
for i in range(len(precision)):
    print(f"Class {i+1}:")
    print(f"  Precision: {precision[i]:.2f}")
    print(f"  Recall: {recall[i]:.2f}")
    print(f"  F1 Score: {f1[i]:.2f}")
    print(f"  Specificity: {specificity[i]:.2f}")
    # Calculate AUC for each class similarly if probabilities are available
    # print(f"  AUC: {auc_class1:.2f}")
    print(f"  Support: {support[i]}")

# Example output
# Class 1:
#   Precision: 0.83
#   Recall: 0.88
#   F1 Score: 0.86
#   Specificity: 0.98
#   AUC: 0.90 (example, replace with actual calculation)
#   Support: 34
# and so on for other classes...
