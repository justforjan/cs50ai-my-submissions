# 1. try
- Convolutional Layer (32 (3,3))
- Max Pooling 4x4
- Flatten
- Dense (128)
- Dropout (0.5)
- Dense (NUM_CATEGORIES)

Epochs = 10

Result:
333/333 - 1s - loss: 3.5026 - accuracy: 0.0565 - 1s/epoch - 4ms/step

# 2. try
- Convolutional Layer (32 (3,3))
- Max Pooling 4x4
- Flatten
- Dense (128)
- Dense (128)
- Dropout (0.5)
- Dense (NUM_CATEGORIES)

Epoch = 10

Result:
333/333 - 1s - loss: 0.8509 - accuracy: 0.7196 - 1s/epoch - 4ms/step

# 3. try
- Convolutional Layer (32 (3,3))
- Max Pooling 4x4
- Flatten
- Dense (128)
- Dropout (0.2)
- Dense (NUM_CATEGORIES)

Epoch = 10

Result:
333/333 - 1s - loss: 0.7505 - accuracy: 0.7589 - 1s/epoch - 3ms/step


# 4. try
- Convolutional Layer (32 (3,3))
- Max Pooling 2x2
- Flatten
- Dense (128)
- Dropout (0.5)
- Dense (NUM_CATEGORIES)

Epoch = 10

Result:
333/333 - 2s - loss: 3.4957 - accuracy: 0.0553 - 2s/epoch - 5ms/step

