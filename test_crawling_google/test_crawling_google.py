import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from PIL import Image
import io

# Specify the search query and the number of images to download
search_query = "sake"
num_images_to_download = 50

# Specify the path where you want to save the downloaded images
download_path = "C:\\Users\qhshd\\sake_project\\test_crawling_google\\test_images"

# Specify the path to your ChromeDriver executable
chromedriver_path = r"C:\\Users\\qhshd\\Downloads\\chromedriver_win32\\chromedriver.exe"

# Set up the Selenium driver
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Run Chrome without headless mode
options.binary_location = chromedriver_path  # Set the binary location

# Initialize the WebDriver
driver = webdriver.Chrome(options=options)

# Open Google Images
driver.get("https://www.google.com/imghp")

# Locate the search box and input the search query
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys(search_query)
search_box.send_keys(Keys.RETURN)

# Scroll and collect images
scroll_pause_time = 3
last_height = driver.execute_script("return document.body.scrollHeight")

while len(driver.find_elements(By.CSS_SELECTOR, "img.rg_i")) < num_images_to_download:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)
    
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Get image elements
images = driver.find_elements(By.CSS_SELECTOR, "img.rg_i")

# Extract image URLs
image_urls = [img.get_attribute("src") for img in images if img.get_attribute("src")]

# Create the download folder if it doesn't exist
if not os.path.exists(download_path):
    os.makedirs(download_path)

# Download and save the images
for idx, image_url in enumerate(image_urls):
    print(f"Image URL: {image_url}")  # Print the image URL for debugging
    try:
        response = requests.get(image_url)
        image_extension = "jpg"  # Default to jpg extension if not determined
        
        if "content-type" in response.headers:
            content_type = response.headers["content-type"]
            if "image/jpeg" in content_type:
                image_extension = "jpg"
            elif "image/png" in content_type:
                image_extension = "png"
            elif "image/gif" in content_type:
                image_extension = "gif"
        
        image_filename = os.path.join(download_path, f"sake_{idx+1:04d}.{image_extension}")
        
        with open(image_filename, "wb") as img_file:
            img_file.write(response.content)
        print(f"Downloaded image {idx+1}/{min(num_images_to_download, len(image_urls))}: {image_filename}")

    except Exception as e:
        print(f"Error downloading image {idx+1}: {e}")



# Close the browser window
driver.quit()

print("Image downloading complete.")
