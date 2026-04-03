# Usage Examples

This guide shows how to work with the Hardware Friction Scorecard Dataset.

---

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Verify CSV is up-to-date
python parse_scored_architectures.py
```

---

## Basic Queries

### Load and Explore

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('scored_architectures.csv')

print(f"Total architectures: {len(df)}")
print(f"Sections: {df['Section'].nunique()}")
print(f"Era coverage: {df['Era'].unique()}")
```

### Filter by Friction Zone

```python
# Production-ready (Green) architectures
green = df[df['Zone'] == '🟢 Green']
print(f"Green zone: {len(green)} architectures")
print(green[['Architecture', 'Year', 'H', 'E']].to_string())

# Research-only (Red) architectures
red = df[df['Zone'] == '🔴 Red']
print(f"\\nRed zone: {len(red)} architectures")
print(red[['Architecture', 'Year', 'Notes']].to_string())
```

### Filter by Hardware Score

```python
# High-hardware-friendliness (H >= 5)
hardware_friendly = df[df['H'] >= 5]
print(f"Hardware-friendly (H≥5): {len(hardware_friendly)}")

# Show distribution
print(df.groupby('H')['Architecture'].count())
```

---

## Analysis Examples

### 1. Hardware vs Ecosystem Friction

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Create scatter plot
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='H', y='E', hue='Zone', 
                style='Era', s=100, alpha=0.7)
plt.xlabel('Hardware Score (H)', fontsize=12)
plt.ylabel('Ecosystem Score (E)', fontsize=12)
plt.title('Hardware Friction Scorecard: H vs E', fontsize=14)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('h_vs_e_scatter.png', dpi=300)
plt.show()
```

### 2. Zone Distribution by Era

```python
# Zone distribution over time
zone_by_era = df.groupby(['Era', 'Zone']).size().unstack(fill_value=0)
zone_by_era.plot(kind='bar', stacked=True, figsize=(10, 6), 
                 color=['#2ecc71', '#f39c12', '#e67e22', '#e74c3c'])
plt.xlabel('Era', fontsize=12)
plt.ylabel('Number of Architectures', fontsize=12)
plt.title('Zone Distribution by Era', fontsize=14)
plt.legend(title='Zone')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('zone_by_era.png', dpi=300)
plt.show()
```

### 3. Average Hardware Score by Era

```python
# Hardware friendliness trend
era_h_mean = df.groupby('Era')['H'].mean()
print("Average H-score by era:")
print(era_h_mean)

# Plot trend
era_h_mean.plot(kind='bar', figsize=(8, 5), color='steelblue')
plt.xlabel('Era', fontsize=12)
plt.ylabel('Average H Score', fontsize=12)
plt.title('Hardware Friendliness Trend Over Time', fontsize=14)
plt.ylim(0, 6)
plt.axhline(y=5, color='red', linestyle='--', alpha=0.5, label='Production threshold')
plt.legend()
plt.tight_layout()
plt.savefig('h_score_trend.png', dpi=300)
plt.show()
```

### 4. Architecture Family Comparison

```python
# Extract families from Architecture column
def get_family(arch):
    if 'Transformer' in arch or 'BERT' in arch or 'GPT' in arch or 'T5' in arch:
        return 'Transformer'
    elif 'MoE' in arch or 'Mixtral' in arch or 'DeepSeek' in arch:
        return 'MoE'
    elif 'Mamba' in arch or 'S4' in arch or 'SSM' in arch:
        return 'SSM'
    elif 'LSTM' in arch or 'GRU' in arch or 'RNN' in arch:
        return 'RNN'
    elif 'ViT' in arch or 'DiT' in arch or 'UNet' in arch:
        return 'Vision'
    else:
        return 'Other'

df['Family'] = df['Architecture'].apply(get_family)

# Compare average scores
family_scores = df.groupby('Family')[['GA', 'MAL', 'PAR', 'STI', 'IM', 'H', 'E']].mean()
print(family_scores.round(2))

# Heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(family_scores[['GA', 'MAL', 'PAR', 'STI', 'IM']], 
            annot=True, cmap='YlOrRd', vmin=0, vmax=2)
plt.title('Average Gate Scores by Architecture Family', fontsize=14)
plt.tight_layout()
plt.savefig('family_heatmap.png', dpi=300)
plt.show()
```

---

## Advanced Queries

### Transformers vs SSMs

```python
# Compare Transformer variants with SSMs
transformers = df[df['Architecture'].str.contains('Transformer|BERT|GPT|T5', case=False, na=False)]
ssms = df[df['Architecture'].str.contains('Mamba|SSM|S4', case=False, na=False)]

print(f"Transformers: H={transformers['H'].mean():.2f}, E={transformers['E'].mean():.2f}")
print(f"SSMs: H={ssms['H'].mean():.2f}, E={ssms['E'].mean():.2f}")
```

### Find "Ghost Winners" (High H, Low Adoption)

```python
# Architectures with H≥5 but not Green zone (potential ecosystem failures)
ghost_winners = df[(df['H'] >= 5) & (df['Zone'] != '🟢 Green')]
print("High hardware score but not production-ready:")
print(ghost_winners[['Architecture', 'Year', 'H', 'E', 'Zone', 'Notes']].to_string())
```

### Multimodal Convergence

```python
# Section 5: Multimodal architectures
multimodal = df[df['Section'].str.contains('5.', na=False)]
print(f"Multimodal architectures: {len(multimodal)}")
print(f"Average H-score: {multimodal['H'].mean():.2f}")
print(f"Green zone: {len(multimodal[multimodal['Zone'] == '🟢 Green'])}/{len(multimodal)}")
```

---

## Export Filtered Data

```python
# Export production-ready architectures only
green_df = df[df['Zone'] == '🟢 Green']
green_df.to_csv('production_ready_architectures.csv', index=False)
print(f"Exported {len(green_df)} production-ready architectures")

# Export by era
for era in df['Era'].unique():
    era_df = df[df['Era'] == era]
    filename = f"architectures_{era.replace('–', '_').replace('+', 'plus')}.csv"
    era_df.to_csv(filename, index=False)
    print(f"Exported {len(era_df)} architectures from {era}")
```

---

## Predictive Modeling

See `experiments/predict_zones.py` for full decision tree / logistic regression examples.

Quick preview:

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# Prepare features
X = df[['GA', 'MAL', 'PAR', 'STI', 'IM']].fillna(0)
y = df['Zone'].map({'🟢 Green': 3, '🟡 Yellow': 2, '🟠 Orange': 1, '🔴 Red': 0})

# Train simple tree
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
tree = DecisionTreeClassifier(max_depth=3, random_state=42)
tree.fit(X_train, y_train)

print(f"Accuracy: {tree.score(X_test, y_test):.2f}")
```

---

## Questions?

- Check the [main README](README.md) for methodology
- Read the essays in `essays/` for context
- Open an issue on GitHub for dataset questions
