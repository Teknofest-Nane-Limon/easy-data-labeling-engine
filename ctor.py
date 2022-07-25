import csv
import pandas as pd
from sqlalchemy import create_engine
import os

basedir = os.path.abspath(os.path.dirname(__file__))
# Create engine to connect with DB
try:
    engine = create_engine('sqlite:///' + os.path.join(basedir, 'database.db'), echo=True)
    print('Engine created!')
except:
    print("Can't create 'engine")
else:
    # Get data from CSV file to DataFrame(Pandas)
    with open('static/datas/data.csv', newline='\n') as csvfile:
        reader = csv.DictReader(csvfile)
        columns = [
            'id',
            'text',
            'label',
            'tagging_status'
        ]
        df = pd.DataFrame(data=reader, columns=columns)
        # Dataframe editing.
        df['id'] = df['id'].astype(int)
        df['label'] = df['label'].astype(bool)
        df['tagging_status'] = df['tagging_status'].astype(bool)
        df['tagging_status'] = df['tagging_status'].ffill()
        print(df.head(15))
    # Standart method of Pandas to deliver data from DataFrame to Database table.
    try:
        # load the data into a Pandas DataFrame
        with engine.begin() as connection:
            df.to_sql('scraped', con=connection, if_exists='append')
            print('Done, ok!')
    except:
        print('Something went wrong!')