import tensorflow as tf
from keras import layers, models
from keras.datasets import mnist
from keras.utils import to_categorical
import matplotlib.pyplot as plt

tf.config.experimental.set_visible_devices([], 'GPU')


# Load and preprocess the MNIST dataset
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# Reshape and normalize the input data
# Reshape the images to have a single channel (since MNIST images are grayscale)
# Normalize pixel values to be in the range [0, 1]
train_images = train_images.reshape((60000, 28, 28, 1)).astype('float32') / 255
test_images = test_images.reshape((10000, 28, 28, 1)).astype('float32') / 255

# One-hot encode the labels
# Convert labels to one-hot encoding for categorical classification
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

# Build the neural network model
model = models.Sequential()

# Add a 2D convolutional layer with 32 filters, each of size (3, 3)
# Use ReLU activation function for non-linearity
# Specify input shape for the first layer
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))

# Add a 2x2 max-pooling layer to reduce spatial dimensions
model.add(layers.MaxPooling2D((2, 2)))

# Flatten the 2D output to 1D array for input to a densely connected layer
model.add(layers.Flatten())

# Add a densely connected layer with 10 neurons for the 10 output classes
# Use softmax activation for multi-class classification
model.add(layers.Dense(10, activation='softmax'))

# Compile the model
# Specify the Adam optimizer, categorical crossentropy loss, and accuracy metric
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
# Use training data, run for 10 epochs, with a batch size of 64
# Validate the model on 20% of the training data
history = model.fit(train_images, train_labels, epochs=10, batch_size=64, validation_split=0.2)

# Evaluate the model on the test set
test_loss, test_acc = model.evaluate(test_images, test_labels)

# Print test accuracy and loss
print(f'Test accuracy: {test_acc}')
print(f'Test loss: {test_loss}')

# Plot the training history (loss and accuracy)
plt.figure(figsize=(12, 4))

# Plot training & validation accuracy values
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(['Train', 'Validation'], loc='upper left')

# Plot training & validation loss values
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend(['Train', 'Validation'], loc='upper left')

# Show the plots
plt.tight_layout()
plt.show()



