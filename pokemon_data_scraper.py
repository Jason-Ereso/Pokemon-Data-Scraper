import requests
import pandas as pd
from bs4 import BeautifulSoup
import sqlite3

# URL of the webpage to scrape
url = 'https://pokemondb.net/pokedex/all'

# Send a GET request to the webpage
response = requests.get(url)

# Parse the content of the webpage
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing the Pokemon data
table = soup.find('table', {'id': 'pokedex'})

# Extract the table headers
headers = [header.text for header in table.find_all('th')]

# Extract the table rows
rows = table.find_all('tr')[1:]  # Skip the header row

# Extract the data from each row
data = []
for row in rows:
    cells = row.find_all('td')
    cells_text = [cell.text.strip() for cell in cells]
    data.append(cells_text)

# Create a DataFrame from the extracted data
df = pd.DataFrame(data, columns=headers)

# Save the DataFrame to a CSV file
csv_file_path = 'pokemon_data.csv'
df.to_csv(csv_file_path, index=False)

# Save the DataFrame to a database file (SQLite)
# SQLite database file path
db_file_path = 'pokemon_data.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_file_path)

# Save the DataFrame to a SQLite table
df.to_sql('pokemon', conn, if_exists='replace', index=False)

# Close the database connection
conn.close()

print(f"Data saved to CSV file: {csv_file_path}")
print(f"Data saved to SQLite database file: {db_file_path}")
