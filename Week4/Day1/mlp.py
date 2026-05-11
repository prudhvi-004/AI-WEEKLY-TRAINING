# Import MLP classifier
from sklearn.neural_network import MLPClassifier

# Training input data
X = [
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
]

# XOR output
y = [0, 1, 1, 0]

# Create MLP model
model = MLPClassifier(

    # Hidden layer with 4 neurons
    hidden_layer_sizes=(4,),

    # Activation function
    activation='relu',

    # Training iterations
    max_iter=1000,

    # Random seed (same output every run)
    random_state=42
)

# Train the model
model.fit(X, y)

# Predict new input
prediction = model.predict([[1, 0]])

#result
print("Prediction:", prediction)
