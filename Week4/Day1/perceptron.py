# Import Perceptron model
from sklearn.linear_model import Perceptron

# Training data (inputs)
# X = features/input
# Each row = one sample
X = [
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
]

# Output labels
# AND gate output
y = [0, 0, 0, 1]

# Create perceptron model
model = Perceptron()

# Train the model
# model learns weights and bias here
model.fit(X, y)

# Predict output for new data
prediction = model.predict([[1, 1]])

# Print result
print("Prediction:", prediction)