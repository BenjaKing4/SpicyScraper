import requests
from bs4 import BeautifulSoup
import re

# Function to clean and format text
def clean_text(text):
    # Remove any trailing characters like 'k'
    cleaned_text = re.sub(r'[^\w\s]', '', text).strip()  # Remove punctuation
    return cleaned_text.capitalize()

# Function to extract and format text for tags, artists, etc.
def extract_info(section_id, key, is_page=False):
    section = soup.find('section', id=section_id)
    containers = section.find_all('div', class_='tag-container')
    result = []
    for container in containers:
        if key in container.get_text():
            if is_page:
                # Special case for pages
                result = [clean_text(container.find('span', class_='name').get_text(strip=True))]
            else:
                result = [clean_text(tag.find('span', class_='name').get_text(strip=True))
                          for tag in container.find_all('a', class_='tag')]
            break
    return result

# Function to extract pages number
def extract_pages():
    section = soup.find('section', id='tags')
    if section:
        # Find the div containing 'Pages:' text by searching the text content
        pages_div = None
        for div in section.find_all('div', class_='tag-container'):
            if 'Pages:' in div.get_text():
                pages_div = div
                break
        if pages_div:
            # Find the span with the page number
            pages_span = pages_div.find('span', class_='name')
            if pages_span:
                return pages_span.get_text(strip=True)
    return 'Unknown'

# Function to extract data from a given nhentai page
def scrape_nhentai_info(url):
    response = requests.get(url)

    # Check if the page was successfully fetched
    if response.status_code != 200:
        print("Failed to retrieve the page")
        return None

    global soup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract relevant info from the page
    title = soup.find('h1', class_='title').get_text(strip=True)
    japanese_title = soup.find('h2', class_='title').get_text(strip=True)

    # Extract the tags section
    tags = extract_info('tags', 'Tags:')
    characters = extract_info('tags', 'Characters:')
    artist = extract_info('tags', 'Artists:')
    group = extract_info('tags', 'Groups:')
    languages = extract_info('tags', 'Languages:')
    categories = extract_info('tags', 'Categories:')

    # Extract the number of pages
    pages = extract_pages()

    # Format the result as requested
    formatted_info = f"""
[{title}]
[{japanese_title}]

Tags: [{', '.join(tags)}]

Characters: [{', '.join(characters)}]

Artist: [{', '.join(artist)}]

Group: [{', '.join(group)}]

Language: [{', '.join(languages)}]

Categories: [{', '.join(categories)}]

Pages: [{pages}]
    """
    return formatted_info

# Function to save the formatted info into a .txt file
def save_to_file(formatted_info, filename='nhentai_info.txt'):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(formatted_info)

# Example usage
url = 'https://nhentai.net/g/486029/'  # Replace this with the actual URL of the doujin
formatted_info = scrape_nhentai_info(url)

# If data was successfully retrieved, save it to a file
if formatted_info:
    save_to_file(formatted_info, 'doujin_info.txt')
    print("Data saved to doujin_info.txt")
