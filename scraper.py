from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pickle
import time

# Setup and Configuration
BASE_URL = 'http://sake09.com/shop/'  # Update to your main page URL
# DRIVER_PATH = '/path_to_driver/driver.exe'
driver = webdriver.Chrome()


def navigate_to_category_page(category_index):
    """
        category_index (int): 0 navigates to 일본술\t1 navigates to 일본소주\t2 navigates to 와인\t3 navigates to 리큐어\
            \t4 navigates to 술잔/술병 등\t5 navigates to 식자재\t6 navigates to 일본인기 직구상품
        returns: None
    """
    try:
        iframe = driver.find_element(By.XPATH, '//*[@id="leftcolumn"]/iframe')
        driver.switch_to.frame(iframe)
        categories = driver.find_elements(By.ID, 'mainbtn2') 
        categories[category_index].click()
    except Exception as e:
        print(f"Error navigating to category page: {e}")

def change_disp_number(disp_number_index):
    """
        disp_number_index (0,1,2): respectively 20 / 40/ 60 items
        returns: None
    """
    try:
        select = Select(driver.find_element(By.XPATH, '//*[@id="page_navi_top"]/div/div[1]/select'))
        select.select_by_index(disp_number_index)  # item 표시 20건 / 40건 / 60건
    except Exception as e:
        print(f"Error changing the number of item display: {e}")

def get_items_list():
    """getting the list of item elements
       returns WebElements
    """
    try:
        items = driver.find_elements(By.CLASS_NAME, 'picture')
        return items
    except NoSuchElementException as e:
        print(f"Error getting the list of item elements: {e}")
    
def navigate_to_item_page(item):
    """
        Navigating to the item page
    Args:
        item (WebElements): image element to click
    """
    try:
        # Clicking the image
        actions = ActionChains(driver)
        offset = 30
        actions.move_to_element_with_offset(item, 0, offset)
        actions.click()
        actions.perform()
    except Exception as e:
        print(f"Error navigating to item page: {e}")

# Returning raw text data
def extract_text_data():
    """Extracting raw text data of item from the page.
    Returns:
        _type_: str
    """
    try:
        element = driver.find_element(By.XPATH, '//*[@id="detailrightbloc"]/div[2]')
        text_data = element.get_attribute('innerHTML')
        return text_data
    except NoSuchElementException:
        print("Text data not found.")

def get_zoomed_image_url():
    """Getting URL of zoomed image
    Returns:
        _type_: str
    """
    try:
        # Clicking the image
        img = driver.find_element(By.CLASS_NAME, 'picture')
        actions = ActionChains(driver)
        offset = 30
        actions.move_to_element_with_offset(img, 0, offset)
        actions.click()
        actions.perform()
        
        # Get URL        
        wait = WebDriverWait(driver, 20) 
        zoomed_image = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="facebox"]/div/div/div/img')))
        zoomed_image_url = zoomed_image.get_attribute("src")
       
        return zoomed_image_url

    except Exception as e:
        print(f"Error getting image URL: {e}")

def move_to_next_page():
    try:
        wait = WebDriverWait(driver, 10) 
        next_page_link = wait.until(EC.visibility_of_element_located((By.XPATH, '//a[contains(text(), "次へ>>")]')))
        next_page_link.click()        
    except Exception as e:
        print(f"Error moving to the next page: {e}")
       

# Main Logic
driver.get(BASE_URL)
all_extracted_data = [] # uploaded at the end of each page
current_page = 1
number_of_data_saved = 0

# scraping the items in 일본술 category / diplay 60 items per page
navigate_to_category_page(0)
change_disp_number(2)

while current_page < 3:
    extracted_data = [] # for data from one page(~60 items)  
    # This is the loop for each category page and its items
    
    items = get_items_list()
    for item in items:
        navigate_to_item_page(item) # into item info page
        
        # text_data = extract_text_data()
        # image_url = get_zoomed_image_url()
        # extracted_data.append((text_data, image_url))

        driver.back()   # out of item info page -> into category page
    
    # all_extracted_data += extracted_data
    # with open('Raw_dataset.p', 'wb') as f:
    #         pickle.dump(all_extracted_data, f)
    #         number_of_data_saved = len(f)
    # print(f'Extracted_data saved as pickle ~ page {current_page}')

    try:
        next_page_button = driver.find_element(By.XPATH, '//a[contains(text(), "次へ>>")]')
        if next_page_button:
            current_page += 1
            next_page_button.click()
        else:
            break
    except NoSuchElementException:
        break

print('Scraping complete:')
print(f'Total page: {current_page}')
print(f'# of dataset: {number_of_data_saved}')
driver.quit()