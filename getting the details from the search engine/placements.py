import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time

# Read the Excel file
df = pd.read_excel("C:\\Users\\pavan\\OneDrive\\Desktop\\ython\\FTP database, Colleges and Final selects.xlsx",sheet_name='Sheet6')
print(df.columns)

# Function to extract placement details
def get_placement_details(university_name):
    search_url = f"https://www.google.com/search?q={university_name}+placement+cell+contact+details"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    response = requests.get(search_url, headers=headers)
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
        
        # Extract email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        if email_match:
            email = email_match.group()
        
        # Extract coordinator name
        if 'mr' in text.lower() or 'dr' in text.lower():
            coordinator_name = text

    return mobile, email, coordinator_name

# Iterate through each university and fill the details
for index, row in df.iterrows():
    university_name = row['Name of the University']
    print(f"Fetching details for: {university_name}")
    mobile, email, coordinator_name = get_placement_details(university_name)
    df.at[index, 'Mobile Number'] = mobile
    df.at[index, 'Email Address'] = email
    df.at[index, 'TPO/Coordinator'] = coordinator_name
    time.sleep(2)  # Adding delay to avoid getting blocked

# Save the updated Excel file
df.to_excel('C:\\Users\\pavan\\OneDrive\\Desktop\\ython\\FTP database, Colleges and Final selects final.xlsx', index=False)
print(df)