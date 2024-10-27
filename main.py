import requests
import json
import pandas as pd
from datetime import datetime


# download data
url = "https://gpp.ppda.go.ug/adminapi/public/api/tender/notices"
request = requests.get(url)
content = request.json()
print(content.keys())

#  length of data list
print(f"Number of items in data: {len(content['data'])}")

# latest tender ( orlargest ID value) 
max_id_item = max(content['data'], key=lambda x: x['id'])
print("\nItem with largest ID:")
print(json.dumps(max_id_item, indent=2))

# dataframe
df = pd.DataFrame(content['data'])

# convert to datetime, invalid dates will become NaT 
df['deadline_dt'] = pd.to_datetime(df['deadline'], errors='coerce')

# deadline field analysis
today = datetime.now()
total = len(df)
valid_dates = df['deadline_dt'].notna().sum()
future_dates = len(df[df['deadline_dt'] > today])
invalid_dates = df['deadline_dt'].isna().sum()

print(f"\nDeadline field summary:")
print(f"Total tenders: {total}")
print(f"Valid dates: {valid_dates}")
print(f"Future deadlines: {future_dates}")
print(f"Invalid/empty dates: {invalid_dates}")