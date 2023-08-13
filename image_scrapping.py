import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
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
num_of_images_to_save = 20

# 페이지 좌측에 "일본술" 카테고리 클릭
iframe = driver.find_element(By.XPATH, '//*[@id="leftcolumn"]/iframe')
wait = WebDriverWait(driver, 20)
print('홈페이지에서 iframe 가져오기 성공')
driver.switch_to.frame(iframe)
print('iframe으로 driver switching 성공')
category = driver.find_element(By.PARTIAL_LINK_TEXT, '일본술')
category.click()
wait = WebDriverWait(driver, 10)
print('일본술 페이지로 이동 성공')

# # 추후 드라이버 옵션 설정용. 현재는 작업을 위해 창 띄움.
# options = webdriver.ChromeOptions()
# options.add_argument("--headless") 
# driver = webdriver.Chrome(options=options)


# 페이지별로 상품 20개씩 있음. -> 사진 / 상품명 스크래핑
# for 20 상품 - click해서 상세 페이지 - click해서 확대 후 이미지 저장 - back(20 상품 페이지로 이동)
# 위 loop 끝내면 - 다음페이지 이동 - 끝날 때까지(or num_of_images_to_save 지정)
# 현재 version에서는 num_of_images_to_save 지정해서 진행 

# category == 일본술 페이지
image_total_number = 0
image_index = 0
image_url_list = []
while image_total_number < num_of_images_to_save:
    images = driver.find_elements(By.CLASS_NAME, 'picture')
    if image_total_number >= len(images):
        break
    
    image = images[image_total_number]
    time.sleep(2)
    image.click()  # 상세정보 페이지로 이동
    print('상세정보 페이지 이동 성공')

    try:
        driver.find_element(By.CLASS_NAME, 'picture').click()  # 상세정보에서 이미지 클릭
        print('상세정보 이미지 클릭 성공')
        wait = WebDriverWait(driver, 20)  # wait time은 하면서 조정 필요.
        image_to_download = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="facebox"]/div/div/div/img')))
        print('다운받을 이미지 element로 가져오기 성공')

        # 확대 이미지 URL 얻기
        image_url = image_to_download.get_attribute("src")
        image_url_list.append(image_url)
        print("Image URL 가져오기 성공")
        print("Image URL:", image_url)

        driver.back()
        print('일본술 페이지로 뒤로가기 성공')
        image_total_number += 1
        print(f'현재 image 개수: {image_total_number}')

    except TimeoutException:
        print("TimeOut.")
    
    # Increase the image_total_number after each iteration
    # Go back to the list of images
   
print(image_url_list)
print(len(image_url_list))
time.sleep(2)
driver.quit()
            
                   
        # image_to_download = driver.find_element(By.TAG_NAME, 'img')  # 실제로 다운받을 element
        # image_url = image_to_download.get_attribute('src') # 다운받을 url 따오기
        # image_filename =  os.path.join(image_download_path, f'test_{image_total_number+1:04d}.jpg') # filename 지정
        # response = requests.get(image_url)
        # with open(image_filename, 'wb') as f:
        #     f.write(response.content)
        # image_total_number += 1
        # driver.back()
        
   