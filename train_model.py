import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

rng = np.random.default_rng(42)
n = 2000
df = pd.DataFrame({
    "weight_kg":    rng.uniform(20000, 30000, n),
    "is_40ft":      rng.integers(0, 2, n),
    "arrival_hour": rng.integers(0, 24, n),
    "day_of_week":  rng.integers(0, 7, n)
})
df["dwell_days"]   = (2 + df["weight_kg"] / 1000) + (df["is_40ft"] * 0.8) 
+ (df["day_of_week"] >= 5) *1.5 + rng.normal(0, 0.7, n) 

X, y = df.drop(columns="dwell_days"), df["dwell_days"]
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print("Test MAE(days):", round(mean_absolute_error(y_test, model.predict(X_test)), 2))

joblib.dump(model, "models/dwell_model.pkl")

