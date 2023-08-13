# import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
import time


# import os

#### Chrome driver version 114.0.5735.90 ####
#### Chrome browser version 115.0.5790.171 ####

### 홈페이지 -> 일본술 카테고리 이동이 계속 오류나서 url 수정.
url = 'http://sake09.com/shop/products/list.php?category_id=15'


# url = 'http://sake09.com/shop/'
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox') 
# chrome_options.add_argument('--disable-dev-shm-usage') 
driver = webdriver.Chrome()
driver.get(url)

image_download_path = 'C:\\Users\\qhshd\\sake_project\\dataset\\sake\\images'
images_per_page = 20
desired_num_of_pages = 3 # 스크래핑할 페이지 조절

# # 페이지 좌측에 "일본술" 카테고리 클릭
# iframe = driver.find_element(By.XPATH, '//*[@id="leftcolumn"]/iframe')
# wait = WebDriverWait(driver, 20)
# print('홈페이지에서 iframe 가져오기 성공')
# driver.switch_to.frame(iframe)
# print('iframe으로 driver switching 성공')
# category = driver.find_element(By.PARTIAL_LINK_TEXT, '일본술')
# category.click()
# wait = WebDriverWait(driver, 10)
# print('일본술 페이지로 이동 성공')


### 페이지별로 상품 20개씩 있음. -> 사진 / 상품명 스크래핑
### for 20 상품 - click해서 상세 페이지 - click해서 확대 후 이미지 저장 - back(20 상품 페이지로 이동)

### category == 일본술 페이지 ###
image_index = 0
current_page = 1
image_url_list = []

while current_page <= desired_num_of_pages:
    images = driver.find_elements(By.CLASS_NAME, 'picture')
    if image_index >= len(images):
        ### 다음페이지로 이동(Update the current page number and reset the image_index)
        next_page_link = driver.find_element(By.XPATH, '//a[contains(text(), "次へ>>")]')
        next_page_link.click()
        current_page += 1
        image_index = 0
        continue
        
    image = images[image_index]
    # time.sleep(2)
    
    ### 상세정보 페이지로 들어가기 ###
    ### 상품이 품절일 시 가운데 클릭이 안돼서 예외처리 필요 ###
    try:
        driver.execute_script("arguments[0].scrollIntoView();", image) # 스크롤 해서 클릭
        # element_height = image.size['height']
        # print(element_height)
        offset = 30  
        
        # offset만큼 이동해서 클릭하는 actionchains 객체 생성
        actions = ActionChains(driver)
        actions.move_to_element_with_offset(image, 0, offset)
        actions.click()
        actions.perform()
        print('상세정보 페이지 이동 및 클릭 성공')
        
    except TimeoutException:
        print('TimeoutException 발생')
        break
        
    ### 상세정보 페이지에서 이미지 클릭 -> 확대 후 저장 ###
    try:
        img = driver.find_element(By.CLASS_NAME, 'picture')
        actions = ActionChains(driver)
        offset = 30
        actions.move_to_element_with_offset(img, 0, offset)
        actions.click()
        actions.perform()
        print('확대 이미지 클릭 성공')
        
        wait = WebDriverWait(driver, 20)  # wait time은 하면서 조정 필요.
        image_to_download = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="facebox"]/div/div/div/img')))
        print('다운받을 이미지 element로 가져오기 성공')

        ### 확대 이미지 URL 얻기
        image_url = image_to_download.get_attribute("src")
        image_url_list.append(image_url)
        print("Image URL 가져오기 성공")
        print("Image URL:", image_url)

        driver.back()
        print('일본술 페이지로 뒤로가기 성공')
        image_index += 1
        print(f'현재 image 개수: {image_index + (current_page-1)*images_per_page}')

    except TimeoutException:
        print("TimeoutException 발생")
        break
    
print(f'저장된 URL의 개수 : {len(image_url_list)}')    
         
# image_to_download = driver.find_element(By.TAG_NAME, 'img')  # 실제로 다운받을 element
# image_url = image_to_download.get_attribute('src') # 다운받을 url 따오기
# image_filename =  os.path.join(image_download_path, f'test_{image_index+1:04d}.jpg') # filename 지정
# response = requests.get(image_url)
# with open(image_filename, 'wb') as f:
#     f.write(response.content)
# image_index += 1
# driver.back()
    
   