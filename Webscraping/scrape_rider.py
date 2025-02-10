import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_rider_data(rider_name, year=2024):
    rider_slug = rider_name.lower().replace(" ", "-")
    url = f"https://www.procyclingstats.com/rider/{rider_slug}/{year}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    # Force the encoding to 'utf-8' to handle non-ASCII characters correctly
    response.encoding = 'utf-8'

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        rider_info_container = soup.find("div", class_="rdr-info-cont")
        
        if rider_info_container:
            details = {}

            # Extracting date of birth and age
            dob_section = rider_info_container.find(text="Date of birth:")
            if dob_section:
                dob_text = dob_section.find_next("b").parent.get_text(strip=True)
                dob_parts = dob_text.split('(')  # Split to check if age is present
                dob = dob_parts[0].strip()  # Always extract the date part
                age = dob_parts[1].split(')')[0] if len(dob_parts) > 1 else "N/A"  # Extract age if present
                details['dob'] = f"{dob} ({age})"
            else:
                details['dob'] = "N/A"

            # Extracting nationality
            nationality_element = rider_info_container.find("a", href=lambda href: href and "nation" in href)
            details['nationality'] = nationality_element.get_text(strip=True) if nationality_element else "N/A"


            # Extracting place of birth
            birth_place_element = rider_info_container.find("a", href=lambda href: href and "location" in href)
            details['place_of_birth'] = birth_place_element.get_text(strip=True) if birth_place_element else "N/A"

            # Extracting weight and height
            weight_text = rider_info_container.find(text="Weight:")
            details['weight'] = weight_text.next.strip() if weight_text else "N/A"

            height_text = rider_info_container.find(text="Height:")
            details['height'] = height_text.next.strip() if height_text else "N/A"

            # Extracting race statistics
            race_stats_container = soup.find("div", class_="rdrResultsSum")
            if race_stats_container:
                race_stats = race_stats_container.get_text(strip=True).split("|")
                details['km_ridden'] = race_stats[0].split("in")[0].strip() if len(race_stats) > 0 else "N/A"
                details['race_days'] = race_stats[0].split("in")[1].strip() if len(race_stats) > 0 else "N/A"
                details['uci_points'] = race_stats[1].split(":")[1].strip() if len(race_stats) > 1 else "N/A"
            else:
                details['km_ridden'], details['race_days'], details['uci_points'], details["place_of_birth"] = "N/A", "N/A", "N/A", "N/A"

            return details
    return None

# Input the rider's name and year
rider_name = input("Enter the rider's name: ")
year = input("Enter the year in question (e.g., 2024): ")

# Check if the input year is valid
try:
    year = int(year)
except ValueError:
    print("Invalid year input. Please enter a valid year.")
    exit()

# Fetch the rider data
rider_data = fetch_rider_data(rider_name, year)

print(rider_data)
