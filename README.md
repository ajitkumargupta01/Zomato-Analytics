# 🍽️ Zomato Business Analytics Project

End-to-end data analytics project built on the Zomato restaurant dataset — covering relational database design, exploratory analysis, interactive dashboards, and machine learning for rating prediction.

**Python Dashboard**

**📌 Project Overview**
This project simulates a real-world business analytics workflow for a food-delivery platform like Zomato. It covers the full data pipeline — from raw data ingestion and SQL modelling to Python-based EDA, machine learning, and BI dashboarding.

**Business questions answered:**

Which cities and cuisines have the highest-rated restaurants?
What drives customer ratings — cost, delivery, bookings?
How does revenue trend month-over-month, and where does it come from?
Which customers are champions vs churning?
Can we predict a restaurant's rating from its features?
🗂️ Repository Structure
zomato-analytics/
│
├── sql/
│   ├── 01_create_database.sql       # Schema — 9 tables, indexes
│   ├── 02_insert_sample_data.sql    # Sample data — 10 cities, 15 restaurants, 20 orders
│   ├── 03_analytical_queries.sql    # 19 business queries (window functions, CTEs)
│   └── 04_stored_procedures.sql     # 3 stored procedures + 3 views for BI tools
│
├── python/
│   ├── 01_data_cleaning.py          # Missing values, encoding, feature engineering
│   ├── 02_eda_analysis.py           # Correlation, t-tests, ANOVA, outlier detection
│   ├── 03_visualization.py          # 4 chart sets — city dashboard, heatmap, correlation
│   └── 04_ml_rating_prediction.py   # 5 models, GridSearchCV, prediction function
│
├── excel_powerbi_guide.md           # Step-by-step Excel + Power BI connection guide
└── README.md
🛠️ Tech Stack
**Layer	Tools**
Database	MySQL 8.0 — schema design, joins, window functions, stored procedures
Data Analysis	Python — Pandas, NumPy, SciPy
Visualization	Matplotlib, Seaborn
Machine Learning	Scikit-learn — Linear Regression, Random Forest, Gradient Boosting
BI Dashboards	Power BI Desktop — DAX measures, 4-page report
Spreadsheet	Microsoft Excel — Pivot Tables, Slicers, Conditional Formatting
🗄️ Database Schema
The MySQL database (zomato_db) contains 9 normalized tables:

cities          ◄──── restaurants ────► restaurant_cuisines ────► cuisines
                            │
                     ┌──────┴──────┐
                  orders        reviews
                     │
              ┌──────┴──────┐
          customers    order_items
                            │
                    delivery_partners
Key design decisions:

Restaurant–Cuisine is many-to-many (a restaurant can serve multiple cuisines)
Orders hold both total_amount and final_amount to track discount impact
Views (vw_restaurant_profile, vw_order_details, vw_kpi_summary) are pre-built for Power BI / Excel direct connections
🐍 Python Modules
01_data_cleaning.py
Strips whitespace and standardises city names
Fills missing avg_cost_for_two with city-level median (grouped imputation)
Replaces unrated restaurants (rating = 0) with cuisine-level median
Derives rating_category, cost_tier, is_popular columns
Exports clean data to zomato_clean.csv and a multi-sheet Excel file
02_eda_analysis.py
Descriptive stats, skewness, kurtosis for numeric columns
Pearson correlation — cost vs rating, votes vs rating
Independent t-tests — delivery availability vs rating, table booking vs rating
One-way ANOVA — rating differences across cuisines
IQR outlier detection for all numeric features
City-wise and cuisine-wise group aggregations
03_visualization.py
Generates 4 publication-ready chart files:

File	Contents
zomato_city_dashboard.png	2×3 grid — count, rating, cost, pie, violin, scatter
zomato_cuisine_analysis.png	Bar chart + bubble chart (cost × rating × count)
zomato_heatmap.png	City × Cuisine average rating heatmap
zomato_correlation.png	Lower-triangle correlation matrix
04_ml_rating_prediction.py
Trains and compares 5 regression models to predict aggregate_rating:

Model	RMSE	R²
Linear Regression	~0.28	~0.71
Ridge Regression	~0.28	~0.71
Decision Tree	~0.24	~0.78
Random Forest	~0.20	~0.85
Gradient Boosting	~0.21	~0.84
Features used: avg_cost_for_two, has_table_booking, has_online_delivery, price_range, log_votes, city_encoded, cuisine_encoded, cost_per_person, delivery_and_booking

Includes a predict_rating() function for inference on new restaurants.

📊 SQL Highlights
The analytical queries file covers 6 modules:

Restaurant Performance — top 10 by rating, count by city, price range distribution
Order & Revenue — monthly revenue trend, payment method split, cancellation rate
Customer Behavior — RFM-style segmentation, retention (new vs repeat), LTV ranking
Review Analysis — platform vs review rating comparison, rating distribution
Delivery Performance — avg/min/max delivery time, late delivery count by city
Advanced Window Functions — RANK(), DENSE_RANK(), LAG(), running totals
📈 Power BI Report Pages
Page	Key Visuals
Executive Summary	KPI cards, top cities bar, rating donut, revenue line, map
Restaurant Analytics	Cost vs Rating scatter, City×Cuisine matrix, price range gauge
Order Analytics	Monthly orders line, payment pie, order status funnel
Customer Insights	New vs Repeat stacked bar, segments, delivery time by city
Key DAX measures included: Total Revenue, Avg Order Value, MoM Revenue Growth, Cancellation Rate, Excellent Restaurants %

🚀 Getting Started
Prerequisites
# Python packages
pip install pandas numpy matplotlib seaborn scikit-learn openpyxl pymysql sqlalchemy

# MySQL 8.0+ must be installed and running
1. Set up the Database
mysql -u root -p < sql/01_create_database.sql
mysql -u root -p < sql/02_insert_sample_data.sql
mysql -u root -p < sql/03_analytical_queries.sql
mysql -u root -p < sql/04_stored_procedures.sql
Or open each file in MySQL Workbench and run with Ctrl+Shift+Enter.

2. Run Python Analysis
cd python/

python 01_data_cleaning.py          # → zomato_clean.csv, zomato_analysis.xlsx
python 02_eda_analysis.py           # → prints stats to terminal
python 03_visualization.py          # → saves 4 PNG charts
python 04_ml_rating_prediction.py   # → model comparison table + zomato_ml_results.png
3. Connect Excel / Power BI
Follow the step-by-step instructions in excel_powerbi_guide.md.

Excel: Data → Get Data → MySQL → select vw_restaurant_profile
Power BI: Home → Get Data → MySQL → import views → build relationships
4. Use the Rating Predictor
from python.ml_rating_prediction import predict_rating

rating = predict_rating(
    city='Mumbai',
    cuisine='North Indian',
    avg_cost=800,
    has_table=1,
    has_delivery=1,
    price_range=2,
    votes=3500
)
print(f"Predicted Rating: {rating} ⭐")
# → Predicted Rating: 4.23 ⭐
🔑 Key Business Insights
Restaurants with online delivery score 0.15 points higher on average (statistically significant, p < 0.05)
Votes correlate more strongly with rating than cost — popularity builds credibility
The top 25% of customers by spend account for ~60% of total revenue (Pareto effect)
Peak ordering hours are 12–2 PM and 7–10 PM — ideal windows for promotions
Cities with higher avg cost do not always have higher ratings — value perception matters
📦 Dataset
This project uses a synthetic dataset generated to mirror the structure of the publicly available Zomato Restaurants Dataset on Kaggle. You can swap in the real CSV by replacing the data generation block in 01_data_cleaning.py with:

df = pd.read_csv('zomato.csv', encoding='latin-1')
🤝 Contributing
Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to change.

📄 License
This project is licensed under the MIT License — see the LICENSE file for details.

👤 Author
Built as a training project covering MySQL, Excel, Power BI, and Python data analysis libraries.

⭐ If this project helped you, consider starring the repository!
