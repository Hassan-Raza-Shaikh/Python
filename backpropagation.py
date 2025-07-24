import numpy as np
import matplotlib.pyplot as plt

# --- Package Setup ---
# First load the workshhet dependencies.
# Here is the activation function and its derivative.
def sigma(z):
    return 1 / (1 + np.exp(-z))

def d_sigma(z):
    return sigma(z) * (1 - sigma(z)) # Correct derivative for logistic sigmoid

# This function initializes the network with its structure.
# It also resets any training already done.
def reset_network(n1=6, n2=7, random_mp=True):
    global W1, W2, W3, b1, b2, b3
    if random_mp:
        W1 = random.rand(n1, 1) / 2 # Weights for layer 1 (n1 neurons, 1 input)
        b1 = random.rand(n1, 1) / 2 # Biases for layer 1
        W2 = random.rand(n2, n1) / 2 # Weights for layer 2 (n2 neurons, n1 inputs)
        b2 = random.rand(n2, 1) / 2 # Biases for layer 2
        W3 = random.rand(2, n2) / 2 # Weights for layer 3 (2 output neurons, n2 inputs)
        b3 = random.rand(2, 1) / 2 # Biases for layer 3
    else:
        # Placeholder for non-random initialization if needed
        pass

# This function feeds forward each activation to the next layer.
# It returns all weighted sums and activations.
def network_function(a0):
    # Layer 1
    z1 = W1 @ a0 + b1
    a1 = sigma(z1)
    # Layer 2
    z2 = W2 @ a1 + b2
    a2 = sigma(z2)
    # Layer 3 (Output Layer)
    z3 = W3 @ a2 + b3
    a3 = sigma(z3)
    return a0, z1, a1, z2, a2, z3, a3

# This is the cost function of a neural network with respect to a training set.
def cost(x, y):
    # Calculate the output of the network
    a3 = network_function(x)[-1] # Get the final activation a3
    # Calculate the mean squared error
    return np.linalg.norm(a3 - y)**2 / x.size

# --- Backpropagation Functions ---

# GRADED FUNCTION
# Jacobian for the third layer weights.
def J_W3 (x, y) :
    # First get all the activations and weighted sums at each layer of the network.
    a0, z1, a1, z2, a2, z3, a3 = network_function(x)
    # We'll use the variable J to store parts of our result as we go along, updating it in each line.
    # Firstly, we calculate dC/da3, using the expressions above. This is the derivative of the cost
    # with respect to the output activation, (a3 - y)^2 derivative is 2 * (a3 - y).
    J = 2 * (a3 - y)
    # Next multiply the result we've calculated by the derivative of sigma, evaluated at z3.
    # This applies the chain rule for da3/dz3 = sigma'(z3).
    J = J * d_sigma(z3)
    # Then we take the dot product (along the axis that holds the training examples) with the final partial derivative,
    # i.e. dz3/dW3 = a2. This calculates the gradient with respect to W3.
    # The division by x.size averages the gradient over all training examples.
    J = J @ a2.T / x.size
    # Finally return the result out of the function.
    return J

# GRADED FUNCTION
# In this function, you will implement the jacobian for the bias.
# As you will see from the partial derivatives, only the last partial derivative is different.
# The first two partial derivatives are the same as previously.
def J_b3 (x, y) :
    # As last time, we'll first set up the activations.
    a0, z1, a1, z2, a2, z3, a3 = network_function(x)
    # Next you should implement the first two partial derivatives of the Jacobian.
    # dC/da3: Derivative of cost with respect to output activation.
    J = 2 * (a3 - y)
    # dC/dz3: Multiply by derivative of activation function.
    J = J * d_sigma(z3)
    # For the final line, we don't need to multiply by dz3/db3, because that is multiplying by 1.
    # We still need to sum over all training examples however, and then average.
    J = np.sum(J, axis=1, keepdims=True) / x.size
    return J

# GRADED FUNCTION
# Compare this function to J_W3 to see how it changes.
def J_W2 (x, y) :
    # The first two lines are identical to in J_W3, calculating dC/dz3.
    a0, z1, a1, z2, a2, z3, a3 = network_function(x)     
    J = 2 * (a3 - y)
    J = J * d_sigma(z3)
    # The next two lines implement da3/da2.
    # First, multiply by the transpose of W3, which represents the propagation of the error backwards
    # through the weights of the next layer (W3). Transpose is used for correct dimension matching.
    J = (J.T @ W3).T
    # Then the final lines are the same as in J_W3 but with the layer number bumped down.
    # Multiply by the derivative of sigma at z2 for da2/dz2.
    J = J * d_sigma(z2)
    # Multiply by a1.T for dz2/dW2 and average over training examples.
    J = J @ a1.T / x.size
    return J

# GRADED FUNCTION
# As previously, fill in all the incomplete lines.
def J_b2 (x, y) :
    a0, z1, a1, z2, a2, z3, a3 = network_function(x)
    # dC/da3
    J = 2 * (a3 - y)
    # dC/dz3
    J = J * d_sigma(z3)
    # dC/da2: Propagate error back through W3.
    J = (J.T @ W3).T
    # dC/dz2: Multiply by derivative of sigma at z2.
    J = J * d_sigma(z2)
    # Sum over training examples and average for the bias gradient.
    J = np.sum(J, axis=1, keepdims=True) / x.size
    return J

# GRADED FUNCTION
# Fill in all incomplete lines.
def J_W1 (x, y) :
    a0, z1, a1, z2, a2, z3, a3 = network_function(x)
    # dC/da3
    J = 2 * (a3 - y)
    # dC/dz3
    J = J * d_sigma(z3)
    # dC/da2
    J = (J.T @ W3).T
    # dC/dz2
    J = J * d_sigma(z2)
    # dC/da1: Propagate error back through W2.
    J = (J.T @ W2).T
    # dC/dz1: Multiply by derivative of sigma at z1.
    J = J * d_sigma(z1)
    # dC/dW1: Multiply by a0.T and average.
    J = J @ a0.T / x.size
    return J

# GRADED FUNCTION
# Fill in all incomplete lines.
def J_b1 (x, y) :
    a0, z1, a1, z2, a2, z3, a3 = network_function(x)
    # dC/da3
    J = 2 * (a3 - y)
    # dC/dz3
    J = J * d_sigma(z3)
    # dC/da2
    J = (J.T @ W3).T
    # dC/dz2
    J = J * d_sigma(z2)
    # dC/da1
    J = (J.T @ W2).T
    # dC/dz1
    J = J * d_sigma(z1)
    # dC/db1: Sum over training examples and average.
    J = np.sum(J, axis=1, keepdims=True) / x.size
    return J

# --- Example Usage (requires global W, b variables, which would be defined by reset_network) ---
# To make this code runnable independently for testing, we would need to call reset_network first
# and define some example x and y data.

# Example of how you might use these functions (not part of the submission, just for understanding):
if __name__ == "__main__":
    # Initialize the network (example parameters)
    np.random.seed(0) # for reproducibility
    reset_network(n1=6, n2=7, random_mp=True) # Sets W1, W2, W3, b1, b2, b3 globally

    # Create some dummy input and output data for testing
    # x represents input features (e.g., 1 feature for 10 training examples)
    # y represents target outputs (e.g., 2 output dimensions for 10 training examples)
    x_train = np.random.rand(1, 10) * 10 # 1 input feature, 10 training examples
    y_train = np.random.rand(2, 10) # 2 output features, 10 training examples

    print("--- Testing Jacobian Functions ---")
    print("J_W3 shape:", J_W3(x_train, y_train).shape)
    print("J_b3 shape:", J_b3(x_train, y_train).shape)
    print("J_W2 shape:", J_W2(x_train, y_train).shape)
    print("J_b2 shape:", J_b2(x_train, y_train).shape)
    print("J_W1 shape:", J_W1(x_train, y_train).shape)
    print("J_b1 shape:", J_b1(x_train, y_train).shape)

    # You would typically use these Jacobians in an optimization loop (e.g., gradient descent)
    # to update the weights and biases:
    learning_rate = 0.1
    # W3 -= learning_rate * J_W3(x_train, y_train)
    # b3 -= learning_rate * J_b3(x_train, y_train)
    # etc. for W2, b2, W1, b1