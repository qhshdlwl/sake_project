import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os



url = "http://sake09.com/shop/"
driver = webdriver.Chrome()
driver.get(url)
image_download_path = 'C:\\Users\\qhshd\\sake_project\\dataset\\sake\\images'
num_of_images_to_save = 5

# 페이지 좌측에 "일본술" 카테고리 클릭
iframe = driver.find_element(By.XPATH, '//*[@id="leftcolumn"]/iframe')
driver.switch_to.frame(iframe)
category = driver.find_element(By.PARTIAL_LINK_TEXT, '일본술')
category.click()


# 현재 페이지 : 상품 20개 출력되는 페이지
images = driver.find_elements(By.CLASS_NAME, 'picture') # 20개의 element 리스트로 저장
print(f'"일본술" 페이지에 있는 picture class의 개수 : {len(images)}') # 사진 20개 따오는지 확인
images[0].click()


# 상세 페이지
driver.find_element(By.CLASS_NAME, 'picture').click()

# Wait for the modal content to be visible
try:
    wait = WebDriverWait(driver, 20)  # Increased wait time
    image_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="facebox"]/div/div/div/img')))
    
    # Get the image source URL
    image_url = image_element.get_attribute("src")
    print("Image URL:", image_url)

    driver.back()
    driver.quit()

except TimeoutException:
    print("Modal content did not become visible within the specified timeout.")
    driver.back()
    driver.quit()