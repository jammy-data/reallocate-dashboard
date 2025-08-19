import pandas as pd
import json

# Load Excel
excel_path = './pilot_static_data.xlsx'
df = pd.read_excel(excel_path, engine='openpyxl')

# Clean column names
df.columns = df.columns.str.strip()

# Convert lat/lon from comma to dot and cast to float
if 'lat' in df.columns:
    df['lat'] = pd.to_numeric(df['lat'].astype(str).str.replace(',', '.', regex=False), errors='coerce')

if 'lon' in df.columns:
    df['lon'] = pd.to_numeric(df['lon'].astype(str).str.replace(',', '.', regex=False), errors='coerce')

# Convert all datetime columns to string format
for col in df.select_dtypes(include=['datetime64[ns]', 'datetime64']).columns:
    df[col] = df[col].dt.strftime('%d/%m/%Y')

# Just in case any column is still a Timestamp object (e.g., mixed types), convert everything to string-safe
df = df.applymap(lambda x: x.strftime('%d/%m/%Y') if isinstance(x, pd.Timestamp) else x)

# Convert to list of dicts
records = df.to_dict(orient='records')


# Save to JSON file
output_path = './pilot_static_data.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(records, f, ensure_ascii=False, indent=2)

print(f"✅ JSON file created with all columns at: {output_path}")
