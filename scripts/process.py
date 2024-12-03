import os
import datetime
import requests 
import pandas as pd

url = 'http://www.ici.org/info/flows_data_2015.xls'
archive = 'archive/'

pd.options.mode.chained_assignment = None

def download_historical_data():
    for date in range(2011,2021):
        if date == 2016 or date == 2017:
            continue
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

def extract():
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
    list_of_files = os.listdir(archive)
    monthly = pd.DataFrame(columns=fields)
    weekly = pd.DataFrame(columns=fields)
    # Process files between 2016 and 2020
    for file in list_of_files:
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

        # Concatenate data
        monthly = pd.concat([monthly, monthly_data], ignore_index=True)
        weekly = pd.concat([weekly, weekly_data], ignore_index=True)

    # Save to CSV
    monthly.to_csv('monthly.csv', index=False)
    weekly.to_csv('weekly.csv', index=False)



def process():
    download_historical_data()
    download_present_data()
    extract()

if __name__ == '__main__':
    process()

