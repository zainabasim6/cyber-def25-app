from sklearn.ensemble import RandomForestClassifier
import joblib
import numpy as np

print("Creating placeholder malware detection model...")
model = RandomForestClassifier(n_estimators=10)
X = np.random.rand(100, 5)
y = np.random.randint(0, 2, 100)
model.fit(X, y)
joblib.dump(model, 'model.pkl')
print("✅ Model created: model.pkl")
