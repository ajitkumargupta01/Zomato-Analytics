# ============================================================
#   ZOMATO BUSINESS ANALYTICS — ML: Rating Prediction
#   File: 04_ml_rating_prediction.py
#   Libraries: pandas, numpy, sklearn, matplotlib, seaborn
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

print("=" * 65)
print("  ZOMATO ML — RESTAURANT RATING PREDICTION")
print("=" * 65)

# ============================================================
# STEP 1: PREPARE DATA
# ============================================================
np.random.seed(42)
n = 800
cities = ['Mumbai','Delhi','Bangalore','Hyderabad','Chennai',
          'Kolkata','Pune','Ahmedabad','Jaipur','Lucknow']
cuisines_list = ['North Indian','South Indian','Chinese','Italian',
                 'Fast Food','Biryani','Pizza','Continental','Mughlai']

df = pd.DataFrame({
    'city':            np.random.choice(cities, n),
    'cuisines':        np.random.choice(cuisines_list, n),
    'avg_cost_for_two':np.random.randint(200, 2000, n).astype(float),
    'has_table_booking':   np.random.randint(0, 2, n),
    'has_online_delivery': np.random.randint(0, 2, n),
    'price_range':         np.random.choice([1,2,3,4], n, p=[0.2,0.4,0.3,0.1]),
    'votes':               np.random.randint(10, 10000, n),
})
# Synthetic rating (non-linear relationship for interesting ML)
df['aggregate_rating'] = (
    3.0
    + 0.0005 * df['avg_cost_for_two']
    + 0.00002 * df['votes']
    + 0.15 * df['has_online_delivery']
    + 0.10 * df['has_table_booking']
    + np.random.normal(0, 0.3, n)
).clip(1.0, 5.0).round(1)

# ============================================================
# STEP 2: FEATURE ENGINEERING
# ============================================================
le_city    = LabelEncoder()
le_cuisine = LabelEncoder()
df['city_encoded']    = le_city.fit_transform(df['city'])
df['cuisine_encoded'] = le_cuisine.fit_transform(df['cuisines'])

df['log_votes'] = np.log1p(df['votes'])
df['cost_per_person'] = df['avg_cost_for_two'] / 2
df['delivery_and_booking'] = df['has_online_delivery'] * df['has_table_booking']

features = [
    'avg_cost_for_two', 'has_table_booking', 'has_online_delivery',
    'price_range', 'log_votes', 'city_encoded', 'cuisine_encoded',
    'cost_per_person', 'delivery_and_booking'
]
target = 'aggregate_rating'

X = df[features]
y = df[target]

print(f"\n[1] Features used: {features}")
print(f"    Dataset size: {len(df)} rows")

# ============================================================
# STEP 3: TRAIN-TEST SPLIT
# ============================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

print(f"\n[2] Train: {len(X_train)}, Test: {len(X_test)}")

# ============================================================
# STEP 4: MODEL TRAINING & EVALUATION
# ============================================================
models = {
    'Linear Regression':      LinearRegression(),
    'Ridge Regression':       Ridge(alpha=1.0),
    'Decision Tree':          DecisionTreeRegressor(max_depth=6, random_state=42),
    'Random Forest':          RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
    'Gradient Boosting':      GradientBoostingRegressor(n_estimators=100, random_state=42),
}

results = {}
print("\n[3] MODEL COMPARISON")
print(f"{'Model':<25} {'RMSE':>8} {'MAE':>8} {'R²':>8} {'CV R²':>10}")
print("-" * 65)

for name, model in models.items():
    if 'Regression' in name:
        model.fit(X_train_sc, y_train)
        y_pred = model.predict(X_test_sc)
        cv_scores = cross_val_score(model, X_train_sc, y_train,
                                     cv=5, scoring='r2')
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        cv_scores = cross_val_score(model, X_train, y_train,
                                     cv=5, scoring='r2')

    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae  = mean_absolute_error(y_test, y_pred)
    r2   = r2_score(y_test, y_pred)

    results[name] = {
        'model': model, 'rmse': rmse, 'mae': mae,
        'r2': r2, 'cv_r2': cv_scores.mean(), 'y_pred': y_pred
    }
    print(f"{name:<25} {rmse:>8.4f} {mae:>8.4f} {r2:>8.4f} {cv_scores.mean():>10.4f}")

# ============================================================
# STEP 5: BEST MODEL — FEATURE IMPORTANCE
# ============================================================
best_model_name = max(results, key=lambda k: results[k]['r2'])
best_result     = results[best_model_name]
best_model      = best_result['model']

print(f"\n[4] Best Model: {best_model_name} (R² = {best_result['r2']:.4f})")

if hasattr(best_model, 'feature_importances_'):
    fi = pd.DataFrame({
        'feature': features,
        'importance': best_model.feature_importances_
    }).sort_values('importance', ascending=False)
    print("\nFeature Importances:")
    print(fi.to_string(index=False))

# ============================================================
# STEP 6: HYPERPARAMETER TUNING (Random Forest)
# ============================================================
print("\n[5] HYPERPARAMETER TUNING — Random Forest")
param_grid = {
    'n_estimators': [50, 100],
    'max_depth':    [None, 5, 10],
    'min_samples_split': [2, 5]
}
rf = RandomForestRegressor(random_state=42, n_jobs=-1)
grid = GridSearchCV(rf, param_grid, cv=3, scoring='r2', n_jobs=-1, verbose=0)
grid.fit(X_train, y_train)
print(f"Best params: {grid.best_params_}")
print(f"Best CV R²: {grid.best_score_:.4f}")
best_rf = grid.best_estimator_
y_pred_tuned = best_rf.predict(X_test)
print(f"Test R² (tuned): {r2_score(y_test, y_pred_tuned):.4f}")

# ============================================================
# STEP 7: RESIDUAL PLOT
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle(f'Model Evaluation — {best_model_name}',
             fontsize=14, fontweight='bold', color='#E23744')

y_pred_best = best_result['y_pred']
residuals = y_test - y_pred_best

# 7a. Actual vs Predicted
axes[0].scatter(y_test, y_pred_best, alpha=0.4, color='#E23744', s=20)
axes[0].plot([y_test.min(), y_test.max()],
             [y_test.min(), y_test.max()], 'k--', linewidth=1.5)
axes[0].set_xlabel('Actual Rating')
axes[0].set_ylabel('Predicted Rating')
axes[0].set_title(f'Actual vs Predicted (R²={best_result["r2"]:.3f})')

# 7b. Residuals distribution
axes[1].hist(residuals, bins=30, color='#E23744', alpha=0.7, edgecolor='white')
axes[1].axvline(0, color='black', linestyle='--')
axes[1].set_xlabel('Residual (Actual − Predicted)')
axes[1].set_ylabel('Frequency')
axes[1].set_title('Residuals Distribution')

# 7c. Feature importance
if hasattr(best_model, 'feature_importances_'):
    fi_sorted = pd.DataFrame({'feature': features,
                               'importance': best_model.feature_importances_})\
                  .sort_values('importance')
    axes[2].barh(fi_sorted['feature'], fi_sorted['importance'], color='#E23744')
    axes[2].set_title('Feature Importance')
    axes[2].set_xlabel('Importance Score')

plt.tight_layout()
plt.savefig('zomato_ml_results.png', dpi=150, bbox_inches='tight')
plt.show()
print("\n✅ Saved: zomato_ml_results.png")

# ============================================================
# STEP 8: PREDICTION FUNCTION
# ============================================================
def predict_rating(city, cuisine, avg_cost, has_table,
                   has_delivery, price_range, votes):
    """Predict restaurant rating given features."""
    city_enc    = le_city.transform([city])[0]    if city    in le_city.classes_    else 0
    cuisine_enc = le_cuisine.transform([cuisine])[0] if cuisine in le_cuisine.classes_ else 0
    input_data = pd.DataFrame([[
        avg_cost, has_table, has_delivery, price_range,
        np.log1p(votes), city_enc, cuisine_enc,
        avg_cost/2, has_delivery * has_table
    ]], columns=features)
    pred = best_rf.predict(input_data)[0]
    return round(np.clip(pred, 1.0, 5.0), 2)

# Test the predictor
test_cases = [
    ('Mumbai',    'North Indian', 800, 1, 1, 2, 3500),
    ('Delhi',     'Biryani',      500, 0, 1, 1, 1200),
    ('Bangalore', 'Italian',     1500, 1, 0, 3,  800),
    ('Chennai',   'South Indian', 300, 0, 1, 1, 5000),
]
print("\n[6] SAMPLE PREDICTIONS:")
print(f"{'City':<12}{'Cuisine':<16}{'Cost':>6}{'Delivery':>10}{'Votes':>7} → {'Pred Rating':>12}")
print("-" * 65)
for city, cuisine, cost, tbl, dlv, pr, votes in test_cases:
    pred = predict_rating(city, cuisine, cost, tbl, dlv, pr, votes)
    print(f"{city:<12}{cuisine:<16}{cost:>6}{('Yes' if dlv else 'No'):>10}{votes:>7} → {pred:>12.2f} ⭐")

print("\n" + "=" * 65)
print("✅ ML pipeline complete!")