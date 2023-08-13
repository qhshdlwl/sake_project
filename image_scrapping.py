import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

#### Chrome driver version 103.0.5060.134 ####
#### Chrome browser version 103.0.5060.53 ####
#### https://chromedriver.storage.googleapis.com/index.html?path=103.0.5060.134/ (Chrome Driver) ####
#### https://www.slimjet.com/chrome/google-chrome-old-version.php (Chrome Browser) ####


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

# # 추후 드라이버 옵션 설정용. 현재는 작업을 위해 창 띄움.
# options = webdriver.ChromeOptions()
# options.add_argument("--headless") 
# driver = webdriver.Chrome(options=options)


# 페이지별로 상품 20개씩 있음. -> 사진 / 상품명 스크래핑
# for 20 상품 - click해서 상세 페이지 - click해서 확대 후 이미지 저장 - back(20 상품 페이지로 이동)
# 위 loop 끝내면 - 다음페이지 이동 - 끝날 때까지(or num_of_images_to_save 지정)
# 현재 version에서는 num_of_images_to_save 지정해서 진행 

# 현재 페이지 : 상품 20개 출력되는 페이지
image_number = 0
while True:
    images = driver.find_elements(By.CLASS_NAME, 'picture') # 20개의 element 리스트로 저장
    print(f'"일본술" 페이지에 있는 picture class의 개수 : {len(images)}') # 사진 20개 따오는지 확인
    
    for image in images:
        image.click() # 상세정보 페이지로 이동
        driver.find_element(By.CLASS_NAME, 'picture').click() # 상세정보에서 이미지 클릭
        image_to_download = driver.find_element(By.TAG_NAME, 'img')  # 실제로 다운받을 element
        image_url = image_to_download.get_attribute('src') # 다운받을 url 따오기
        image_filename =  os.path.join(image_download_path, f'test_{image_number+1:04d}.jpg') # filename 지정
        response = requests.get(image_url)
        with open(image_filename, 'wb') as f:
            f.write(response.content)
        image_number += 1
        driver.back()
        
    if image_number == num_of_images_to_save:
        break
    



time.sleep(2)
driver.quit()