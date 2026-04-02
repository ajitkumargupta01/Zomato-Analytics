# ============================================================
#   ZOMATO BUSINESS ANALYTICS — Visualizations
#   File: 03_visualization.py
#   Libraries: matplotlib, seaborn
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Zomato color palette
ZOMATO_RED   = '#E23744'
ZOMATO_DARK  = '#1C1C1C'
ZOMATO_GRAY  = '#F5F5F5'
PALETTE = [ZOMATO_RED, '#FF8C00', '#2ECC71', '#3498DB',
           '#9B59B6', '#1ABC9C', '#E74C3C', '#F39C12']

sns.set_style("whitegrid")
sns.set_palette(PALETTE)
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'figure.facecolor': 'white'
})

# Generate data (or load from zomato_clean.csv)
np.random.seed(42)
n = 500
cities = ['Mumbai','Delhi','Bangalore','Hyderabad','Chennai',
          'Kolkata','Pune','Ahmedabad','Jaipur','Lucknow']
cuisines_list = ['North Indian','South Indian','Chinese','Italian',
                 'Fast Food','Biryani','Pizza','Continental','Mughlai']

df = pd.DataFrame({
    'city':            np.random.choice(cities, n),
    'cuisines':        np.random.choice(cuisines_list, n),
    'avg_cost_for_two':np.random.randint(200, 2000, n).astype(float),
    'has_online_delivery': np.random.randint(0, 2, n),
    'has_table_booking':   np.random.randint(0, 2, n),
    'aggregate_rating':    np.round(np.random.uniform(2.5, 5.0, n), 1),
    'votes':               np.random.randint(10, 10000, n),
    'price_range':         np.random.choice([1,2,3,4], n)
})
df['rating_category'] = pd.cut(df['aggregate_rating'],
    bins=[0,2.5,3.5,4.0,4.5,5.01],
    labels=['Poor','Average','Good','Very Good','Excellent'])

# ============================================================
# FIGURE 1: CITY PERFORMANCE DASHBOARD (2x3 grid)
# ============================================================
fig1, axes = plt.subplots(2, 3, figsize=(18, 11))
fig1.suptitle('Zomato — City Performance Dashboard', fontsize=18, fontweight='bold',
               color=ZOMATO_RED, y=0.98)

city_data = df.groupby('city').agg(
    count=('city','count'),
    avg_rating=('aggregate_rating','mean'),
    avg_cost=('avg_cost_for_two','mean')
).sort_values('count', ascending=False).reset_index()

# 1a. Restaurant count by city
ax = axes[0,0]
bars = ax.bar(city_data['city'], city_data['count'],
              color=[ZOMATO_RED if i==0 else '#CCCCCC' for i in range(len(city_data))])
ax.set_title('Restaurants by City')
ax.set_xlabel('City')
ax.set_ylabel('Count')
ax.tick_params(axis='x', rotation=45)
for bar, val in zip(bars, city_data['count']):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1,
            str(val), ha='center', va='bottom', fontsize=9)

# 1b. Avg rating by city (horizontal bar)
ax = axes[0,1]
city_rating = city_data.sort_values('avg_rating')
colors = [ZOMATO_RED if r >= 3.8 else '#AAAAAA' for r in city_rating['avg_rating']]
ax.barh(city_rating['city'], city_rating['avg_rating'], color=colors)
ax.set_title('Average Rating by City')
ax.set_xlabel('Average Rating')
ax.axvline(3.5, color='orange', linestyle='--', alpha=0.7, label='3.5 threshold')
ax.legend(fontsize=9)
for i, (val, city) in enumerate(zip(city_rating['avg_rating'], city_rating['city'])):
    ax.text(val+0.02, i, f'{val:.2f}', va='center', fontsize=9)

# 1c. Avg cost by city
ax = axes[0,2]
city_cost = city_data.sort_values('avg_cost', ascending=False)
bars = ax.bar(city_cost['city'], city_cost['avg_cost'],
              color=sns.color_palette('YlOrRd', len(city_cost)))
ax.set_title('Avg Cost for Two (₹)')
ax.set_xlabel('City')
ax.set_ylabel('INR')
ax.tick_params(axis='x', rotation=45)

# 1d. Rating distribution pie
ax = axes[1,0]
rating_counts = df['rating_category'].value_counts()
colors_pie = [ZOMATO_RED,'#FF8C00','#F5C518','#2ECC71','#27AE60']
wedges, texts, autotexts = ax.pie(rating_counts, labels=rating_counts.index,
    autopct='%1.1f%%', colors=colors_pie, startangle=140,
    wedgeprops=dict(edgecolor='white',linewidth=2))
ax.set_title('Rating Distribution')

# 1e. Online delivery vs rating violin
ax = axes[1,1]
delivery_groups = [
    df[df['has_online_delivery']==0]['aggregate_rating'],
    df[df['has_online_delivery']==1]['aggregate_rating']
]
vp = ax.violinplot(delivery_groups, positions=[0,1], showmedians=True, showmeans=False)
for pc in vp['bodies']:
    pc.set_facecolor(ZOMATO_RED)
    pc.set_alpha(0.7)
vp['cmedians'].set_color('white')
ax.set_xticks([0,1])
ax.set_xticklabels(['No Online\nDelivery','Has Online\nDelivery'])
ax.set_title('Rating vs Delivery Availability')
ax.set_ylabel('Rating')

# 1f. Cost vs rating scatter
ax = axes[1,2]
scatter = ax.scatter(df['avg_cost_for_two'], df['aggregate_rating'],
                     c=df['votes'], cmap='YlOrRd', alpha=0.5, s=30)
plt.colorbar(scatter, ax=ax, label='Votes')
z = np.polyfit(df['avg_cost_for_two'], df['aggregate_rating'], 1)
p = np.poly1d(z)
x_line = np.linspace(df['avg_cost_for_two'].min(), df['avg_cost_for_two'].max(), 100)
ax.plot(x_line, p(x_line), ZOMATO_RED, linewidth=2, label='Trend')
ax.set_title('Cost vs Rating (colored by votes)')
ax.set_xlabel('Avg Cost for Two (₹)')
ax.set_ylabel('Aggregate Rating')
ax.legend()

plt.tight_layout(rect=[0,0,1,0.96])
plt.savefig('zomato_city_dashboard.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Saved: zomato_city_dashboard.png")

# ============================================================
# FIGURE 2: CUISINE ANALYSIS
# ============================================================
fig2, axes2 = plt.subplots(1, 2, figsize=(16, 6))
fig2.suptitle('Zomato — Cuisine Analysis', fontsize=16, fontweight='bold',
               color=ZOMATO_RED)

cuisine_stats = df.groupby('cuisines').agg(
    count=('cuisines','count'),
    avg_rating=('aggregate_rating','mean'),
    avg_cost=('avg_cost_for_two','mean')
).sort_values('count', ascending=False).reset_index()

# 2a. Restaurant count by cuisine
ax = axes2[0]
sns.barplot(data=cuisine_stats, y='cuisines', x='count', ax=ax, palette='YlOrRd_r')
ax.set_title('Restaurants per Cuisine')
ax.set_xlabel('Count')
ax.set_ylabel('')

# 2b. Bubble chart: Cuisines by cost, rating, popularity
ax = axes2[1]
sc = ax.scatter(cuisine_stats['avg_cost'], cuisine_stats['avg_rating'],
                s=cuisine_stats['count']*20, c=range(len(cuisine_stats)),
                cmap='tab10', alpha=0.8, edgecolors='white', linewidth=1.5)
for _, row in cuisine_stats.iterrows():
    ax.annotate(row['cuisines'],
                (row['avg_cost'], row['avg_rating']),
                textcoords='offset points', xytext=(5,3), fontsize=8)
ax.set_title('Cuisine: Cost vs Rating (bubble = count)')
ax.set_xlabel('Avg Cost for Two (₹)')
ax.set_ylabel('Avg Rating')
ax.axhline(df['aggregate_rating'].mean(), color='gray', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('zomato_cuisine_analysis.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Saved: zomato_cuisine_analysis.png")

# ============================================================
# FIGURE 3: HEATMAP — City vs Cuisine
# ============================================================
fig3, ax3 = plt.subplots(figsize=(14, 7))
pivot = df.pivot_table(values='aggregate_rating', index='city',
                        columns='cuisines', aggfunc='mean').round(2)
sns.heatmap(pivot, annot=True, fmt='.2f', cmap='RdYlGn',
            linewidths=0.5, ax=ax3, vmin=2.5, vmax=5.0,
            cbar_kws={'label':'Avg Rating'})
ax3.set_title('Average Rating Heatmap: City × Cuisine',
               fontsize=14, fontweight='bold', color=ZOMATO_RED)
ax3.set_xlabel('Cuisine')
ax3.set_ylabel('City')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('zomato_heatmap.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Saved: zomato_heatmap.png")

# ============================================================
# FIGURE 4: CORRELATION MATRIX
# ============================================================
fig4, ax4 = plt.subplots(figsize=(8, 6))
num_df = df[['aggregate_rating','avg_cost_for_two','votes',
             'has_online_delivery','has_table_booking','price_range']]
corr_matrix = num_df.corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f',
            cmap='coolwarm', center=0, ax=ax4,
            linewidths=0.5, square=True,
            cbar_kws={'shrink':0.8})
ax4.set_title('Feature Correlation Matrix', fontsize=14,
               fontweight='bold', color=ZOMATO_RED)
plt.tight_layout()
plt.savefig('zomato_correlation.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Saved: zomato_correlation.png")
print("\n✅ All visualizations generated!")