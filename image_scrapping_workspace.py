import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os

# Chrome driver version 103.0.5060.134
# Chrome browser version 103.0.5060.53
url = "http://sake09.com/shop/"
driver = webdriver.Chrome()
driver.get(url)
image_download_path = 'C:\\Users\\qhshd\\sake_project\\dataset\\sake\\images'
num_of_images_to_save = 20
desired_num_of_pages = 3  # Set the desired number of pages to scrape

# 페이지 좌측에 "일본술" 카테고리 클릭
iframe = driver.find_element(By.XPATH, '//*[@id="leftcolumn"]/iframe')
driver.switch_to.frame(iframe)
category = driver.find_element(By.PARTIAL_LINK_TEXT, '일본술')
category.click()
print('일본술 페이지로 이동 성공')

# Initialize variables
image_total_number = 0
current_page = 1
image_url_list = []

while current_page <= desired_num_of_pages:
    images = driver.find_elements(By.CLASS_NAME, 'picture')
    if image_total_number >= len(images):
        # Click the "次へ>>" link to go to the next page
        next_page_link = driver.find_element(By.XPATH, '//a[contains(text(), "次へ>>")]')
        next_page_link.click()

        # Update the current page number and reset the image_total_number
        current_page += 1
        image_total_number = 0
        continue
    
    image = images[image_total_number]
    time.sleep(2)
    image.click()  # 상세정보 페이지로 이동
    print('상세정보 페이지 이동 성공')

    try:
        driver.find_element(By.CLASS_NAME, 'picture').click()  # 상세정보에서 이미지 클릭
        print('상세정보 이미지 클릭 성공')
        wait = WebDriverWait(driver, 10)  # wait time은 하면서 조정 필요.
        image_to_download = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="facebox"]/div/div/div/img')))
        print('다운받을 이미지 element로 가져오기 성공')

        # 확대 이미지 URL 얻기
        image_url = image_to_download.get_attribute("src")
        image_url_list.append(image_url)
        print("Image URL:", image_url)

        driver.back()
        print('일본술 페이지로 뒤로가기 성공')
        image_total_number += 1
        print(f'현재 image 개수: {image_total_number}')

    except TimeoutException:
        print("TimeOut.")

    # Go back to the list of images
    driver.back()
    print('상품 목록 페이지로 뒤로가기 성공')

print(image_url_list)
print(len(image_url_list))
time.sleep(2)
driver.quit()
