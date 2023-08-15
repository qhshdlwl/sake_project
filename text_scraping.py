from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

def extract_values_from_content(content):
    # Split the content by <br> to get a list of strings
    lines = content.split('<br>')
    
    # Remove any whitespace from each line
    values = [line.strip().lstrip('■').strip() for line in lines]
    
    # Extract relevant data for lines with colons
    for i, line in enumerate(values):
        if ':' in line:
            # Split by colon and take the right part, then strip whitespace
            values[i] = line.split(':', 1)[1].strip()
    
    return values

# Assuming that Chrome and ChromeDriver are set up
driver = webdriver.Chrome()
driver.get('https://sake09.com/shop/products/detail.php?product_id=9968')  # Visit the provided URL

# Get the element based on the provided XPath
element = driver.find_element(By.XPATH, '//*[@id="detailrightbloc"]/div[2]')

# Extract the div content
main_comment_content = element.get_attribute('innerHTML')

# Extract values from the content
extracted_values = extract_values_from_content(main_comment_content)

# Print the extracted values
print(extracted_values)
print(type(extracted_values))
print(len(extracted_values))

# Close the browser
driver.close()