import os
import shutil
import requests 
import pandas as pd

archive = 'archive/'

pd.options.mode.chained_assignment = None

fields = [ 
        'Date',
        'Total Equity',
        'Domestic Equity',
        'World Equity',
        'Hybrid',
        'Total Bond',
        'Taxable Bond',
        'Municipal Bond',
        'Total'
    ]

def download_historical_data():
    for date in range(2011,2021):
        source = 'http://www.ici.org/info/flows_data_%s.xls' % date
        path = 'archive/flows_data_%s.xls' % date
        response = requests.get(source)
        with open(path, 'wb') as f:
            f.write(response.content)

def download_present_data():
    base_url = "https://www.ici.org/system/files/{year}-{month:02d}/etf_flows_data_{year}.xls"

    years = range(2021, 2025)  
    months = range(1, 13)

    # Check each URL
    for year in years:
        for month in months:
            url = base_url.format(year=year, month=month)
            try:
                response = requests.head(url)
                if response.status_code == 200:
                    print(f"Downloading {url}")
                    response = requests.get(url)
                    with open(f"archive/flows_data_{year}-{month:02d}.xls", "wb") as f:
                        f.write(response.content)
                else:
                    print(f"No data found for {year}-{month:02d}")
            except requests.RequestException as e:
                print(f"Error checking {year}-{month:02d}: {e}")

def standardize_date(date):
    return pd.to_datetime(date).strftime('%Y-%m-%d')

def extract_2016_2020(file):
    print(f"Processing {archive + file}")
    df = pd.read_excel(archive + file)
    df = df.dropna(how='all').reset_index(drop=True)
    df.rename(columns={
        'Investment Company Institute': 'Date',
        'Unnamed: 3': 'Total Equity',
        'Unnamed: 5': 'Domestic Equity',
        'Unnamed: 17': 'World Equity',
        'Unnamed: 23': 'Hybrid',
        'Unnamed: 25': 'Total Bond',
        'Unnamed: 27': 'Taxable Bond',
        'Unnamed: 39': 'Municipal Bond',
        'Unnamed: 1': 'Total'
    }, inplace=True)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    # Find the split points
    monthly_start = df[df.iloc[:, 0].str.lower().str.contains("monthly", na=False)].index[0]
    weekly_start = df[df.iloc[:, 0].str.lower().str.contains("weekly", na=False)].index[0]

    # Extract Monthly and Weekly DataFrames
    monthly_data = df.iloc[monthly_start+1:weekly_start].dropna(axis=1, how='all')
    weekly_data = df.iloc[weekly_start+1:].dropna(how='all')

    monthly_data.iloc[:, 0] = pd.to_datetime(monthly_data.iloc[:, 0], errors='coerce').dt.strftime('%Y-%m-%d')
    monthly_data.dropna(subset=[monthly_data.columns[0]], inplace=True, how='all')
    weekly_data.iloc[:, 0] = pd.to_datetime(weekly_data.iloc[:, 0], errors='coerce').dt.strftime('%Y-%m-%d')
    weekly_data.dropna(subset=[weekly_data.columns[0]], inplace=True, how='all')

    # Reset index for clarity
    monthly_data.reset_index(drop=True, inplace=True)
    weekly_data.reset_index(drop=True, inplace=True)

    return monthly_data, weekly_data

def extract_all(file):
    print(f"Processing {archive + file}")
    df = pd.read_excel(archive + file)
    df = df.dropna(how='all').reset_index(drop=True)

    # Find the split points
    monthly_start = df[df.iloc[:, 0].str.lower().str.contains("monthly", na=False)].index[0]
    weekly_start = df[df.iloc[:, 0].str.lower().str.contains("weekly", na=False)].index[0]

    # Extract Monthly and Weekly DataFrames
    monthly_data = df.iloc[monthly_start+1:weekly_start]
    weekly_data = df.iloc[weekly_start+1:].dropna(how='all')

    # Clean column names for both DataFrames
    monthly_data.columns = df.iloc[monthly_start - 1]
    weekly_data.columns = df.iloc[weekly_start - 1]

    # Handle cases where data has 18 columns
    if len(monthly_data.columns) == 18:
        monthly_data = monthly_data.iloc[:, :len(fields)]  # Take the first 9 columns
    if len(weekly_data.columns) == 18:
        weekly_data = weekly_data.iloc[:, :len(fields)]  # Take the first 9 columns

    # Assign correct column names
    monthly_data.columns = fields
    weekly_data.columns = fields

    # Convert the first column to datetime
    monthly_data.iloc[:, 0] = pd.to_datetime(monthly_data.iloc[:, 0], errors='coerce').dt.strftime('%Y-%m-%d')
    monthly_data.dropna(subset=[monthly_data.columns[0]], inplace=True, how='all')
    weekly_data.iloc[:, 0] = pd.to_datetime(weekly_data.iloc[:, 0], errors='coerce').dt.strftime('%Y-%m-%d')
    weekly_data.dropna(subset=[weekly_data.columns[0]], inplace=True, how='all')

    # Reset index for clarity
    monthly_data.reset_index(drop=True, inplace=True)
    weekly_data.reset_index(drop=True, inplace=True)

    return monthly_data, weekly_data
    

def process():
    if not os.path.exists(archive):
        os.makedirs(archive)
    download_historical_data()
    download_present_data()
    list_of_files = os.listdir(archive)
    merged_monthly = pd.DataFrame(columns=fields)
    merged_weekly = pd.DataFrame(columns=fields)
    for file in list_of_files:
        if '2016' in file or '2017' in file or '2018' in file or '2019' in file or '2020' in file:
            monthly1, weekly1 = extract_2016_2020(file)
            merged_monthly = pd.concat([merged_monthly, monthly1], ignore_index=True)
            merged_weekly = pd.concat([merged_weekly, weekly1], ignore_index=True)
        else:
            monthly2, weekly2 = extract_all(file)
            merged_monthly = pd.concat([merged_monthly, monthly2], ignore_index=True)
            merged_weekly = pd.concat([merged_weekly, weekly2], ignore_index=True)

    # Sort by Date
    merged_monthly.sort_values(by='Date', inplace=True)
    merged_weekly.sort_values(by='Date', inplace=True)

    # Drop Duplicates
    merged_monthly.drop_duplicates(inplace=True)
    merged_weekly.drop_duplicates(inplace=True)

    # Save to CSV
    merged_monthly.to_csv('data/monthly.csv', index=False)
    merged_weekly.to_csv('data/weekly.csv', index=False)

    # Remove the downloaded files after processing
    shutil.rmtree(archive)

if __name__ == '__main__':
    process()

