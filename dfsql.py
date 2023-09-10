import pandas as pd
from sqlalchemy import create_engine

# Reading the CSV into a DataFrame
df = pd.read_csv('books_data.csv')

# Database connection parameters
db_username = 'root'
db_password = ''
db_name = 'books'
db_host = 'localhost'  # Usually 'localhost' if the database is on the same machine
table_name = 'books_data'

import urllib.parse

# URL encode the password to handle special characters
encoded_password = urllib.parse.quote_plus(db_password)
engine = create_engine(f"mysql+pymysql://{db_username}:{encoded_password}@{db_host}/{db_name}")


# Create a connection to the MySQL database
# engine=create_engine(f'mysql+mysqlconnector://{os.getenv("user")}:{os.getenv("password")}@{os.getenv("host")}/bookdata')
# engine = create_engine(f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}")
import pandas as pd

# Create a sample DataFrame
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40],
    'City': ['New York', 'San Francisco', 'Los Angeles', 'Chicago']
}

df = pd.DataFrame(data)


# Save the DataFrame to the MySQL table
df.to_sql(table_name, engine, if_exists='replace', index=False)

print(f"Data saved to table {table_name} in database {db_name}")
