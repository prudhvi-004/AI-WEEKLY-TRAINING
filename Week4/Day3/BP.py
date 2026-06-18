import numpy as np

# -------------------------------------------------------------
# BACKPROPAGATION (BP) + GRADIENT DESCENT (GD) FROM SCRATCH
# -------------------------------------------------------------
#
# In this code we will understand how a neural network learns.
#
# We are using a very simple example:
#
# x = input
# y = output
#
# Pattern in data:
#
# x = 1 → y = 2
# x = 2 → y = 4
# x = 3 → y = 6
#
# If you observe carefully,
# the pattern is:
#
# y = 2x
#
# Our model does not know this pattern initially.
# It has to learn it by making mistakes.
#
# Learning process:
#
# 1. Model predicts output
# 2. Compare prediction with actual answer
# 3. Find mistake (loss/error)
# 4. Backpropagation finds how much correction is needed
# 5. Gradient Descent updates weight and bias
# 6. Repeat again and again
#
# Slowly the model becomes better.


# -------------------------------------------------------------
# TRAINING DATA
# -------------------------------------------------------------
#
# X = input
# y = correct output

X = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 6, 8, 10])


# -------------------------------------------------------------
# INITIALIZE WEIGHT AND BIAS
# -------------------------------------------------------------
#
# Initially model knows nothing.
#
# So we start with random/small values.
#
# Weight:
# controls importance of input.
#
# Bias:
# helps shift prediction line
# up or down.

weight = 0.5
bias = 0.2


# -------------------------------------------------------------
# LEARNING RATE
# -------------------------------------------------------------
#
# Learning rate controls
# how fast the model learns.
#
# Example:
#
# If learning rate is too high:
# model may jump too much
# and miss correct answer.
#
# If learning rate is too low:
# learning becomes slow.

learning_rate = 0.01


# -------------------------------------------------------------
# EPOCHS
# -------------------------------------------------------------
#
# Epoch means:
# how many times model
# sees complete dataset.
#
# epochs = 1000 means
# model learns 1000 times.

epochs = 1000


# -------------------------------------------------------------
# TRAINING STARTS
# -------------------------------------------------------------
#
# Every epoch model will:
#
# Forward Pass
#      ↓
# Prediction
#      ↓
# Error/Loss
#      ↓
# Backpropagation
#      ↓
# Gradient Descent Update
#      ↓
# Repeat

for epoch in range(epochs):

    # Total loss for one epoch
    total_loss = 0


    # We train one sample at a time

    for i in range(len(X)):

        current_x = X[i]
        actual_y = y[i]


        # -----------------------------------------------------
        # STEP 1: FORWARD PASS
        # -----------------------------------------------------
        #
        # Here model predicts output.
        #
        # Formula:
                #
        # Initially prediction is bad
        # because model has not learned.

        predicted_y = (weight * current_x) + bias


        # -----------------------------------------------------
        # STEP 2: ERROR CALCULATION
        # -----------------------------------------------------
        #
        # We compare predicted value
        # with actual correct answer.
        #
        # Example:
        #
        # predicted = 4
        # actual = 8
        #
        # error = -4
        #
        # This tells how wrong model is.

        error = predicted_y - actual_y


        # -----------------------------------------------------
        # STEP 3: LOSS CALCULATION
        # -----------------------------------------------------
        #
        # We square error.
        #
        # Why squaring?
        #
        # Because negative mistakes
        # should not cancel positive mistakes.
        #
        # Also bigger mistakes
        # should get bigger punishment.

        loss = error ** 2

        # Add loss to total loss
        total_loss += loss


        # -----------------------------------------------------
        # STEP 4: BACKPROPAGATION (BP)
        # -----------------------------------------------------
        #
        # Now model asks:
        #
        # "Why mistake happened?"
        #
        # "How much should I change weight?"
        #
        # BP sends error backward
        # and calculates gradients.
        #
        # Gradient means:
        #
        # direction + amount of correction
        #
        # Large mistake → larger correction
        # Small mistake → smaller correction

        d_weight = 2 * error * current_x
        d_bias = 2 * error


        # -----------------------------------------------------
        # STEP 5: GRADIENT DESCENT (GD)
        # -----------------------------------------------------
        #
        # Now actual learning happens.
        #
        # GD updates weight and bias.
        #
        # Formula:
                #
        # eta = learning rate
        #
        # Why minus?
        #
        # Because we move opposite
        # direction of error
        # to reduce mistake.

        weight = weight - (learning_rate * d_weight)
        bias = bias - (learning_rate * d_bias)


    # ---------------------------------------------------------
    # PRINT PROGRESS
    # ---------------------------------------------------------
    #
    # Print every 100 epochs
    # so we can see learning progress.

    if epoch % 100 == 0:

        print("Epoch:", epoch)
        print("Loss:", total_loss)
        print("Weight:", weight)
        print("Bias:", bias)
        print("------------------------")


# -------------------------------------------------------------
# TRAINING FINISHED
# -------------------------------------------------------------
#
# By now model should have learned
# nearly y = 2x

print("\nTraining Finished")

print("Final Weight:", weight)
print("Final Bias:", bias)


# -------------------------------------------------------------
# TEST MODEL
# -------------------------------------------------------------
#
# Let us test new input.
#
# If x = 6
#
# Since pattern is y = 2x
# expected answer is near 12

new_x = 6

prediction = (weight * new_x) + bias

print("Prediction for x = 6:", prediction)