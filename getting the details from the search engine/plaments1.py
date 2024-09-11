
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
from requests.exceptions import ConnectionError

# Read the Excel file
df = pd.read_excel("C:\\Users\\pavan\\OneDrive\\Desktop\\priyanka\\btech1.xlsx")
print(df.columns)

# Function to extract placement details
def get_placement_details(university_name, address):
    query = f"{university_name} {address} placement cell contact details"
    search_url = f"https://www.google.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    retries = 3
    for _ in range(retries):
        try:
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses
            soup = BeautifulSoup(response.text, 'html.parser')

            # Initialize default values
            mobile = "Not Found"
            email = "Not Found"
            coordinator_name = "Not Found"

            # Example parsing logic - this may need adjustment based on actual page structure
            contact_info = soup.find_all('div', class_='BNeawe')
            for info in contact_info:
                text = info.get_text()

                # Extract phone number (digits only)
                phone_match = re.search(r'\b\d{10,}\b', text)
                if phone_match:
                    mobile = phone_match.group()

                # Extract placement email
                email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
                if email_match:
                    email = email_match.group()

                # Extract coordinator name with specific titles and full name
                name_match = re.search(r'\b(Mr\.|Dr\.|Prof\.|Mrs\.|Miss)\s[A-Za-z]+\s[A-Za-z]+\b', text, re.IGNORECASE)
                if name_match:
                    coordinator_name = name_match.group()

            return mobile, email, coordinator_name
        
        except ConnectionError:
            print(f"Connection failed for {university_name}. Retrying...")
            time.sleep(5)  # Exponential backoff can be implemented here
    
    return "Not Found", "Not Found", "Not Found"

count = 0
# Iterate through each university and fill the details
for index, row in df.iterrows():
    count += 1
    university_name = row['Name of the University']
    address = row['Address']
    print(f"Fetching details for({count}): {university_name}, {address}")
    mobile, email, coordinator_name = get_placement_details(university_name, address)
    df.at[index, 'Mobile Number'] = mobile
    df.at[index, 'Email Address'] = email
    df.at[index, 'TPO/Coordinator'] = coordinator_name
    time.sleep(2)  # Increase delay to avoid getting blocked

# Save the updated Excel file
df.to_excel("C:\\Users\\pavan\\OneDrive\\Desktop\\priyanka\\btech12.xlsx", index=False)
print(df)