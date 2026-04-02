# ============================================================
#   ZOMATO BUSINESS ANALYTICS — Data Cleaning
#   File: 01_data_cleaning.py
#   Libraries: pandas, numpy, sqlalchemy
# ============================================================

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# ------------------------------------------------------------
# STEP 1: LOAD DATA (from CSV or MySQL)
# ------------------------------------------------------------
# Option A: Load from CSV (download from Kaggle Zomato dataset)
# df = pd.read_csv('zomato.csv', encoding='latin-1')

# Option B: Load from MySQL
# from sqlalchemy import create_engine
# engine = create_engine('mysql+pymysql://root:password@localhost/zomato_db')
# df = pd.read_sql('SELECT * FROM vw_restaurant_profile', engine)

# For demonstration — create a synthetic dataset
np.random.seed(42)
n = 500

cities = ['Mumbai','Delhi','Bangalore','Hyderabad','Chennai',
          'Kolkata','Pune','Ahmedabad','Jaipur','Lucknow']
cuisines_list = ['North Indian','South Indian','Chinese','Italian',
                 'Fast Food','Biryani','Pizza','Continental','Mughlai']
rating_labels = {
    (4.5, 5.0): 'Excellent',
    (4.0, 4.5): 'Very Good',
    (3.5, 4.0): 'Good',
    (2.5, 3.5): 'Average',
    (0.0, 2.5): 'Poor'
}

df = pd.DataFrame({
    'restaurant_id':   range(1, n+1),
    'restaurant_name': [f'Restaurant_{i}' for i in range(1, n+1)],
    'city':            np.random.choice(cities, n),
    'cuisines':        np.random.choice(cuisines_list, n),
    'avg_cost_for_two':np.random.choice([np.nan, 200, 400, 600, 800, 1000, 1500, 2000], n,
                                         p=[0.05,0.05,0.15,0.25,0.20,0.15,0.10,0.05]),
    'has_table_booking':   np.random.choice(['Yes','No'], n),
    'has_online_delivery': np.random.choice(['Yes','No'], n),
    'aggregate_rating': np.random.choice([0.0, 2.5, 3.0, 3.5, 3.8, 4.0, 4.2, 4.5, 4.8], n,
                                          p=[0.05,0.03,0.07,0.15,0.20,0.25,0.15,0.07,0.03]),
    'votes': np.random.randint(0, 10000, n),
    'price_range': np.random.choice([1,2,3,4], n, p=[0.2,0.4,0.3,0.1])
})

# Introduce some messiness for cleaning practice
df.loc[np.random.choice(n, 20), 'avg_cost_for_two'] = np.nan
df.loc[np.random.choice(n, 10), 'aggregate_rating'] = 0.0  # unrated
df.loc[np.random.choice(n, 5),  'city'] = '  Mumbai  '  # whitespace

print("=" * 55)
print("  ZOMATO DATA CLEANING PIPELINE")
print("=" * 55)

# ------------------------------------------------------------
# STEP 2: INITIAL EXPLORATION
# ------------------------------------------------------------
print("\n[1] Dataset Shape:", df.shape)
print("\n[2] Data Types:\n", df.dtypes)
print("\n[3] First 3 rows:\n", df.head(3))
print("\n[4] Missing Values:\n", df.isnull().sum())
print("\n[5] Duplicate rows:", df.duplicated().sum())

# ------------------------------------------------------------
# STEP 3: CLEANING
# ------------------------------------------------------------
df_clean = df.copy()

# 3a. Strip whitespace from string columns
string_cols = df_clean.select_dtypes(include='object').columns
for col in string_cols:
    df_clean[col] = df_clean[col].str.strip()

# 3b. Handle missing avg_cost_for_two — fill with city median
df_clean['avg_cost_for_two'] = df_clean.groupby('city')['avg_cost_for_two']\
    .transform(lambda x: x.fillna(x.median()))

# 3c. Unrated restaurants (rating = 0) → NaN then fill with cuisine avg
df_clean['aggregate_rating'] = df_clean['aggregate_rating'].replace(0.0, np.nan)
df_clean['aggregate_rating'] = df_clean.groupby('cuisines')['aggregate_rating']\
    .transform(lambda x: x.fillna(x.median()))

# 3d. Convert Yes/No to boolean int
df_clean['has_table_booking']   = (df_clean['has_table_booking'] == 'Yes').astype(int)
df_clean['has_online_delivery'] = (df_clean['has_online_delivery'] == 'Yes').astype(int)

# 3e. Drop duplicates
df_clean.drop_duplicates(inplace=True)

# 3f. Add derived columns
df_clean['rating_category'] = pd.cut(
    df_clean['aggregate_rating'],
    bins=[0, 2.5, 3.5, 4.0, 4.5, 5.0],
    labels=['Poor','Average','Good','Very Good','Excellent'],
    right=True
)

df_clean['cost_tier'] = pd.cut(
    df_clean['avg_cost_for_two'],
    bins=[0, 300, 600, 1000, 5000],
    labels=['Budget','Mid Range','Premium','Luxury']
)

df_clean['is_popular'] = (df_clean['votes'] > df_clean['votes'].quantile(0.75)).astype(int)

# ------------------------------------------------------------
# STEP 4: VALIDATION
# ------------------------------------------------------------
print("\n[6] After Cleaning — Missing Values:\n", df_clean.isnull().sum())
print("\n[7] Rating Categories:\n", df_clean['rating_category'].value_counts())
print("\n[8] Cost Tiers:\n", df_clean['cost_tier'].value_counts())
print("\n[9] Cities (cleaned):\n", df_clean['city'].value_counts())

# ------------------------------------------------------------
# STEP 5: EXPORT CLEAN DATA
# ------------------------------------------------------------
df_clean.to_csv('zomato_clean.csv', index=False)
print("\n✅ Clean data saved to: zomato_clean.csv")
print(f"   Final shape: {df_clean.shape}")

# Export to Excel with multiple sheets
with pd.ExcelWriter('zomato_analysis.xlsx', engine='openpyxl') as writer:
    df_clean.to_excel(writer, sheet_name='Clean_Data',  index=False)
    df_clean.groupby('city').agg(
        restaurants=('restaurant_id','count'),
        avg_rating=('aggregate_rating','mean'),
        avg_cost=('avg_cost_for_two','mean')
    ).round(2).to_excel(writer, sheet_name='City_Summary')
    df_clean['rating_category'].value_counts().to_excel(writer, sheet_name='Rating_Distribution')

print("✅ Excel file saved: zomato_analysis.xlsx")
print("\n" + "=" * 55)