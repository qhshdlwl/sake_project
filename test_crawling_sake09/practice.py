import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

url = "http://sake09.com/shop/"
driver = webdriver.Chrome()
driver.get(url)
picture_download_path = 'C:\\Users\\qhshd\\sake_project\\test_crawling_sake09\\test_image'


# 페이지 좌측에 "일본술" 카테고리 클릭
iframe = driver.find_element(By.XPATH, '//*[@id="leftcolumn"]/iframe')
driver.switch_to.frame(iframe)
element = driver.find_element(By.PARTIAL_LINK_TEXT, '일본술')
element.click()

# 페이지별로 상품 20개씩 있음. -> 사진 / 상품명 스크래핑
# 사진 클릭 후 원본 이미지 가져와야함. 

pictures = driver.find_elements(By.CLASS_NAME, 'picture')
print(f'"일본술" 페이지에 있는 picture class의 개수 : {len(pictures)}') # 사진 20개 따오는지 확인

# 상품 페이지에 class가 picture인 element 1개 확인, 1개 다운로드 작업
pictures[0].click()

# 상세 페이지
driver.find_element(By.CLASS_NAME, 'picture').click()


picture_to_download = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div')

image_filename =  os.path.join(picture_download_path, 'test_download.jpg')
image_url = picture_to_download.get_attribute('src')
response = requests.get(image_url)
with open(image_filename, 'wb') as f:
    f.write(response.content)

driver.back()
# 상품 20개 나와있는 페이지에서의 image source = 상품 클릭 후 image source인지 확인 필요함. 
# 같을 경우 : 20개짜리 페이지에서 스크래핑 가능.
# 다를 경우 : 클릭해서 들어가서 스크래핑 후에 다시 back 해서 작업 진행..



# pictures[0].click()
# org_picture = driver.find_elements(By.CLASS_NAME, 'picture')
# print(f'상품 페이지에 있는 picture class의 개수 : {len(org_picture)}')




# for pic in pictures:
#     pic.click() # 상품페이지로 이동

time.sleep(0.5)
driver.quit()


##### 목표: 첫 페이지 20개 스크래핑 --> iteration으로 200개 try #####







# iframes = driver.find_elements(By.TAG_NAME, 'iframe')

# for i in iframes:
#     print(i)



