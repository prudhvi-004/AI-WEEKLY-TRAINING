# We are writing Gradient Descent from scratch.
# The main goal of Gradient Descent is to reduce mistakes made by the model.
# Initially the model knows nothing, so it predicts badly.
# Then it slowly improves by learning from errors.

# Here we are taking a simple example where:
# x = input
# y = output
#
# If you observe carefully:
# when x = 1, y = 2
# when x = 2, y = 4
# when x = 3, y = 6
#
# So the pattern here is:
# y = 2x

x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]


# At the beginning the model does not know the correct weight and bias.
# So we initialize both with 0.
#
# Weight means how much importance should be given to input.
# Bias helps shift the prediction line up or down.

weight = 0
bias = 0


# Learning rate decides how fast the model should learn.
#
# If we keep this value too high,
# the model may jump too much and miss the correct answer.
#
# If we keep it too low,
# the model will learn very slowly.

learning_rate = 0.01


# Epochs means how many times the model should see the full dataset.
#
# If epochs = 1000,
# it means the model will learn from the same data 1000 times.

epochs = 1000


# Now training starts.
#
# Every epoch the model will:
# 1. Make predictions
# 2. Find mistakes
# 3. Understand in which direction to move
# 4. Update weight and bias
#
# This process repeats again and again.

for epoch in range(epochs):

    # We are resetting gradients every epoch.
    # Gradient simply means:
    # how much change is needed.
    #
    # dw = change needed for weight
    # db = change needed for bias

    dw = 0
    db = 0

    # This variable is used to calculate
    # total error in one epoch.

    total_loss = 0


    # Now we go through every training example one by one.

    for i in range(len(x)):

        current_x = x[i]
        actual_y = y[i]


        # Here the model tries to predict output.
        #
        # Formula:
        # prediction = (weight × input) + bias
        #
        # Initially:
        # weight = 0
        # bias = 0
        #
        # So prediction becomes wrong.
        # But that is okay because learning has just started.

        predicted_y = (weight * current_x) + bias


        # Now we calculate error.
        #
        # We compare predicted answer
        # with actual correct answer.
        #
        # Example:
        # predicted = 3
        # actual = 6
        #
        # error = -3
        #
        # This tells us how wrong the model is.

        error = predicted_y - actual_y


        # We calculate loss using squared error.
        #
        # Why square?
        #
        # Because negative values should not cancel positive values.
        # Also, bigger mistakes should get bigger punishment.
        #
        # Example:
        # error = -5
        # loss = 25

        loss = error ** 2

        # Add loss of every sample
        # to get total epoch loss.

        total_loss += loss


        # Now comes the most important part.
        #
        # We calculate gradients.
        #
        # Gradient tells:
        # "How much should I change?"
        # and
        # "In which direction should I move?"
        #
        # If mistake is large,
        # update will be larger.
        #
        # If mistake is small,
        # update will also be smaller.

        dw += 2 * error * current_x
        db += 2 * error


    # After processing all training examples,
    # we take average gradients.
    #
    # This gives stable learning instead of random updates.

    dw = dw / len(x)
    db = db / len(x)


    # Finally we update the model.
    #
    # This is the actual Gradient Descent step.
    #
    # Formula:
        #
    # We subtract because we want to reduce error.
    # Gradient points toward higher error,
    # so we move opposite to it.

    weight = weight - (learning_rate * dw)
    bias = bias - (learning_rate * db)


    # Printing progress every 100 epochs
    # so we can observe learning.

    if epoch % 100 == 0:
        print("Epoch:", epoch)
        print("Loss:", total_loss)
        print("Weight:", weight)
        print("Bias:", bias)
        print("------------------------")


# Training completed.

print("\nTraining Finished")
print("Final Weight:", weight)
print("Final Bias:", bias)


# Let us test the model with a new value.
#
# Since pattern is y = 2x,
# for x = 6 answer should be near 12.

new_x = 6

prediction = (weight * new_x) + bias

print("Prediction for x = 6:", prediction)
