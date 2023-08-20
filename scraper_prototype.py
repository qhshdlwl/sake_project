import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
import time
import os
import pickle


start = time.time()
#### Chrome driver version 114.0.5735.90 ####
#### Chrome browser version 115.0.5790.171 ####

# 상품 상세정보 불러오기 위한 함수
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

### 홈페이지 -> 일본술 카테고리 이동이 계속 오류나서 url 수정.
url = 'https://sake09.com/shop/products/list.php?transactionid=ef176dd02116b9e66226a51e33cd4e7a171cddd0&mode=&category_id=15&maker_id=0&name=&orderby=&disp_number=20&pageno=206&rnd=phi'


# url = 'http://sake09.com/shop/'
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox') 
# chrome_options.add_argument('--disable-dev-shm-usage') 
driver = webdriver.Chrome()
driver.get(url)

image_download_path = 'C:\\Users\\qhshd\\sake_project\\raw_sample_dataset\\sake\\images'
images_per_page = 20
desired_num_of_pages = 20 # 스크래핑할 페이지 조절

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
all_extracted_values = []

while current_page <= desired_num_of_pages:
    print(f'페이지 {current_page} - {image_index+1}번째 이미지 진행중')
    images = driver.find_elements(By.CLASS_NAME, 'picture')
    if image_index >= len(images):
        ### 다음페이지로 이동(Update the current page number and reset the image_index)
        try:
            wait = WebDriverWait(driver, 10) 
            next_page_link = wait.until(EC.visibility_of_element_located((By.XPATH, '//a[contains(text(), "次へ>>")]')))
            next_page_link.click()
            current_page += 1
            image_index = 0
            print(f'페이지{current_page}로 이동')
            mid = time.time()
            print(f'실행 시간 : {round(mid-start)//3600} hrs {(round(mid-start)%3600)//60} min {(round(mid-start)%3600)%60} sec')
            continue
        except TimeoutException:
            print('TimeoutException 발생 - 다음 페이지 이동 실패')
            break
            
            
        
    image = images[image_index]
    # time.sleep(2)
    
    ### 상세정보 페이지로 들어가기 ###
    ### 상품이 품절일 시 가운데 클릭이 안돼서 예외처리 필요 ###
    try:
        actions = ActionChains(driver)
        actions.move_to_element_with_offset(image, 0, 30)
        actions.click()
        actions.perform()
        print('상세정보 페이지 이동 및 클릭 성공')
        
    except TimeoutException:
        print('TimeoutException 발생 - 상세페이지 클릭 실패')
        continue
        
    ### 상세정보 페이지 : 텍스트 추출 + 이미지 URL 추출 ###
    element = driver.find_element(By.XPATH, '//*[@id="detailrightbloc"]/div[2]')
    main_comment_content = element.get_attribute('innerHTML')
    extracted_values = extract_values_from_content(main_comment_content)
    all_extracted_values.append(extracted_values)
    print('상세정보 추출 성공')
    
    try:
        img = driver.find_element(By.CLASS_NAME, 'picture')
        actions = ActionChains(driver)
        offset = 30
        actions.move_to_element_with_offset(img, 0, offset)
        actions.click()
        actions.perform()
        print('확대 이미지 클릭 성공')
        
        wait = WebDriverWait(driver, 10) 
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
        print(f'현재 URL 개수: {image_index + (current_page-1)*images_per_page}\n')

    except TimeoutException:
        print("TimeoutException 발생- 이미지 확대 실패")
        image_to_download = driver.find_element(By.CLASS_NAME, 'picture')
        image_url = image_to_download.get_attribute("src")
        image_url_list.append(image_url)
        print("Image URL 가져오기 성공")
        print("Image URL:", image_url)
        driver.back()
        print('일본술 페이지로 뒤로가기 성공')
        image_index += 1
        print(f'현재 URL 개수: {image_index + (current_page-1)*images_per_page}\n')
        continue
    finally:
        # 20개마다 url 리스트 + extracted_values pickle로 저장
        if len(image_url_list) % 1 == 0:
            with open('image_url_list5.p', 'wb') as f:
                pickle.dump(image_url_list, f)
                print(f'피클 업데이트 완료 - len(image_url_list) = {len(image_url_list)}')
            with open('extracted_values5.p', 'wb') as f:
                pickle.dump(all_extracted_values, f)
                print(f'Extracted values pickle update complete - len(all_extracted_values) = {len(all_extracted_values)}')        
        else:
            pass
        
print(f'저장된 URL의 개수 : {len(image_url_list)}')
print(f'저장된 URL의 개수(중복제외) : {len(set(image_url_list))}')

# URL을 통한 이미지 저장
# 중복된 URL에 대해서도 이미지를 저장하는게 좋아보임(추후에 사케 이름과 index matching을 위해)
# for index, image_url in enumerate(image_url_list, start=1):
#     image_filename = os.path.join(image_download_path, f'raw_sake_{(index+2740):04d}.jpg')
#     response = requests.get(image_url)
#     with open(image_filename, 'wb') as f:
#         f.write(response.content)
        
# print('이미지 다운로드 완료')
# print(f'저장된 이미지 개수 : {len(os.listdir(image_download_path))}')

# end = time.time()
# print(f'총 실행 시간 : {round(end-start)//3600} hrs {(round(end-start)%3600)//60} min {(round(end-start)%3600)%60} sec')