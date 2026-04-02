# ============================================================
#   ZOMATO BUSINESS ANALYTICS — Exploratory Data Analysis
#   File: 02_eda_analysis.py
#   Libraries: pandas, numpy, scipy
# ============================================================

import pandas as pd
import numpy as np
from scipy import stats

# Load clean data (run 01_data_cleaning.py first)
try:
    df = pd.read_csv('zomato_clean.csv')
except FileNotFoundError:
    # Generate synthetic data if file not found
    np.random.seed(42)
    n = 500
    cities = ['Mumbai','Delhi','Bangalore','Hyderabad','Chennai',
              'Kolkata','Pune','Ahmedabad','Jaipur','Lucknow']
    cuisines_list = ['North Indian','South Indian','Chinese','Italian',
                     'Fast Food','Biryani','Pizza','Continental','Mughlai']
    df = pd.DataFrame({
        'restaurant_id':   range(1, n+1),
        'city':            np.random.choice(cities, n),
        'cuisines':        np.random.choice(cuisines_list, n),
        'avg_cost_for_two':np.random.randint(200, 2000, n).astype(float),
        'has_table_booking':   np.random.randint(0, 2, n),
        'has_online_delivery': np.random.randint(0, 2, n),
        'aggregate_rating':    np.round(np.random.uniform(2.5, 5.0, n), 1),
        'votes':               np.random.randint(10, 10000, n),
        'price_range':         np.random.choice([1,2,3,4], n),
        'rating_category':     np.random.choice(
            ['Poor','Average','Good','Very Good','Excellent'], n),
        'cost_tier':           np.random.choice(
            ['Budget','Mid Range','Premium','Luxury'], n),
        'is_popular':          np.random.randint(0, 2, n)
    })

print("=" * 60)
print("  ZOMATO EDA — EXPLORATORY DATA ANALYSIS")
print("=" * 60)

# ============================================================
# MODULE 1: UNIVARIATE ANALYSIS
# ============================================================
print("\n[1] UNIVARIATE ANALYSIS")
print("-" * 40)

# Numeric summaries
numeric_cols = ['aggregate_rating','avg_cost_for_two','votes']
print("\nDescriptive Statistics:")
print(df[numeric_cols].describe().round(2))

# Skewness and Kurtosis
for col in numeric_cols:
    skew = df[col].skew()
    kurt = df[col].kurtosis()
    print(f"\n  {col}: skewness={skew:.3f}, kurtosis={kurt:.3f}")

# ============================================================
# MODULE 2: BIVARIATE ANALYSIS
# ============================================================
print("\n\n[2] BIVARIATE ANALYSIS")
print("-" * 40)

# 2a. Cost vs Rating correlation
corr, pvalue = stats.pearsonr(df['avg_cost_for_two'], df['aggregate_rating'])
print(f"\nCost vs Rating Pearson r = {corr:.3f}, p-value = {pvalue:.4f}")
interpretation = "significant" if pvalue < 0.05 else "not significant"
print(f"  → Correlation is {interpretation} at α=0.05")

# 2b. Votes vs Rating
corr2, pv2 = stats.pearsonr(df['votes'], df['aggregate_rating'])
print(f"\nVotes vs Rating Pearson r = {corr2:.3f}, p-value = {pv2:.4f}")

# 2c. Online delivery vs Rating
online = df[df['has_online_delivery']==1]['aggregate_rating']
no_online = df[df['has_online_delivery']==0]['aggregate_rating']
t_stat, t_pval = stats.ttest_ind(online, no_online)
print(f"\nOnline Delivery Effect on Rating:")
print(f"  With delivery: mean={online.mean():.2f}, Without: mean={no_online.mean():.2f}")
print(f"  t-test: t={t_stat:.3f}, p={t_pval:.4f}")

# 2d. Table booking vs Rating
tbl = df[df['has_table_booking']==1]['aggregate_rating']
no_tbl = df[df['has_table_booking']==0]['aggregate_rating']
t2, p2 = stats.ttest_ind(tbl, no_tbl)
print(f"\nTable Booking Effect on Rating:")
print(f"  With booking: mean={tbl.mean():.2f}, Without: mean={no_tbl.mean():.2f}")
print(f"  t-test: t={t2:.3f}, p={p2:.4f}")

# ============================================================
# MODULE 3: GROUP ANALYSIS
# ============================================================
print("\n\n[3] GROUP ANALYSIS")
print("-" * 40)

# 3a. City-wise analysis
city_analysis = df.groupby('city').agg(
    count=('restaurant_id','count'),
    avg_rating=('aggregate_rating','mean'),
    avg_cost=('avg_cost_for_two','mean'),
    avg_votes=('votes','mean'),
    online_pct=('has_online_delivery','mean')
).round(2).sort_values('avg_rating', ascending=False)
print("\nCity-wise Restaurant Analysis:")
print(city_analysis.to_string())

# 3b. Cuisine analysis
cuisine_analysis = df.groupby('cuisines').agg(
    count=('restaurant_id','count'),
    avg_rating=('aggregate_rating','mean'),
    avg_cost=('avg_cost_for_two','mean')
).round(2).sort_values('avg_rating', ascending=False)
print("\nCuisine-wise Analysis:")
print(cuisine_analysis.to_string())

# 3c. Price range analysis
price_analysis = df.groupby('price_range').agg(
    count=('restaurant_id','count'),
    avg_rating=('aggregate_rating','mean'),
    avg_cost=('avg_cost_for_two','mean'),
    online_pct=('has_online_delivery','mean')
).round(2)
price_analysis.index = price_analysis.index.map(
    {1:'Budget',2:'Mid Range',3:'Premium',4:'Luxury'})
print("\nPrice Range Analysis:")
print(price_analysis.to_string())

# ============================================================
# MODULE 4: ANOVA TEST
# ============================================================
print("\n\n[4] ONE-WAY ANOVA — Rating across cuisines")
print("-" * 40)
groups = [group['aggregate_rating'].values
          for _, group in df.groupby('cuisines')]
f_stat, anova_p = stats.f_oneway(*groups)
print(f"F-statistic = {f_stat:.3f}, p-value = {anova_p:.4f}")
if anova_p < 0.05:
    print("→ Significant differences in ratings across cuisines (p < 0.05)")
else:
    print("→ No significant difference in ratings across cuisines")

# ============================================================
# MODULE 5: OUTLIER DETECTION
# ============================================================
print("\n\n[5] OUTLIER DETECTION (IQR Method)")
print("-" * 40)
for col in ['aggregate_rating', 'avg_cost_for_two', 'votes']:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower) | (df[col] > upper)]
    print(f"\n  {col}: {len(outliers)} outliers"
          f"  (bounds: [{lower:.1f}, {upper:.1f}])")

# ============================================================
# MODULE 6: KEY BUSINESS INSIGHTS
# ============================================================
print("\n\n[6] KEY BUSINESS INSIGHTS")
print("=" * 60)

best_city = city_analysis['avg_rating'].idxmax()
print(f"\n✅ Best rated city: {best_city} "
      f"(avg rating: {city_analysis.loc[best_city,'avg_rating']:.2f})")

best_cuisine = cuisine_analysis['avg_rating'].idxmax()
print(f"✅ Best rated cuisine: {best_cuisine} "
      f"(avg rating: {cuisine_analysis.loc[best_cuisine,'avg_rating']:.2f})")

high_cost_high_rating = df[
    (df['avg_cost_for_two'] > df['avg_cost_for_two'].median()) &
    (df['aggregate_rating'] >= 4.0)
]
print(f"✅ Premium & high-rated restaurants: {len(high_cost_high_rating)}")

popular_not_great = df[
    (df['is_popular'] == 1) &
    (df['aggregate_rating'] < 3.5)
]
print(f"✅ Popular but avg-rated (improvement opp): {len(popular_not_great)}")

print("\n" + "=" * 60)
print("✅ EDA complete! Use 03_visualization.py for charts.")