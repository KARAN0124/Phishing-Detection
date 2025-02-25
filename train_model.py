import pickle
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier

# Generate random dataset (for testing purposes)
np.random.seed(42)  # Ensures reproducibility
X_train = np.random.rand(100, 10)
y_train = np.random.randint(0, 2, 100)

# Train model
gbc = GradientBoostingClassifier()
gbc.fit(X_train, y_train)

# Save model using pickle
model_filename = "newmodel.pkl"
try:
    with open(model_filename, "wb") as file:
        pickle.dump(gbc, file)
    print(f"Model trained and saved as {model_filename}")
except Exception as e:
    print(f"Error saving the model: {e}")
