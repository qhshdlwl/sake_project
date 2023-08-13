import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Specify the search query and the number of images to download
search_query = "sake"
num_images_to_download = 50

# Define the directory for downloading images
base_download_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_images")
download_path = os.path.join(base_download_path, "sake")

# Ensure the directory structure exists
os.makedirs(download_path, exist_ok=True)

# Specify the path to your ChromeDriver executable
chromedriver_path = r"C:\\Users\\qhshd\\Downloads\\chromedriver_win32\\chromedriver.exe"

# Set up the Selenium driver
options = webdriver.ChromeOptions()
options.binary_location = chromedriver_path
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)

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
    print(f"Image URL: {image_url}")
    try:
        if image_url.startswith('http'):
            # Extract the image extension from the URL
            image_extension = image_url.split(".")[-1].split("?")[0]
            if len(image_extension) > 4:
                image_extension = "jpg"  # Fallback to 'jpg' extension if extension is invalid

            # Generate a unique filename for each image
            image_filename = os.path.join(download_path, f"sake_{idx+1:04d}.{image_extension}")


            # Download the image using requests and save it
            response = requests.get(image_url, stream=True)
            with open(image_filename, "wb") as img_file:
                for chunk in response.iter_content(chunk_size=8192):
                    img_file.write(chunk)

            print(f"Downloaded image {idx+1}/{min(num_images_to_download, len(image_urls))}: {image_filename}")
        else:
            print(f"Skipping image {idx+1}/{min(num_images_to_download, len(image_urls))}: Invalid URL")

    except Exception as e:
        print(f"Error downloading image {idx+1}: {e}")

# Close the browser window
driver.quit()

print("Image downloading complete.")
