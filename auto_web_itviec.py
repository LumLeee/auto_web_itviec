import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import schedule
import time

def crawl_data(username, password):
    driver = uc.Chrome()# Khởi tạo trình điều khiển trình duyệt Chrome

    driver.get("https://itviec.com/")# Truy cập vào https://itviec.com/

    time.sleep(3)

    #Click link sign in
    xpath_signin='/html/body/header/div[1]/nav/div/div[2]/ul[2]/li[2]/a'
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_signin))).click()

    #Nhập email
    xpath_email='//*[@id="user_email"]'
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_email))).send_keys(username)

    #Nhập mật khẩu
    xpath_password='//*[@id="user_password"]'
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_password))).send_keys(password)

    #Click vào nút sign in with email
    xpath_login='/html/body/main/div/div[1]/div/div/div/div[2]/form/div[3]/div/button'
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_login))).click()

    #Click vào danh mục chọn thành phố
    xpath_city='//*[@id="dropdown"]'
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_city))).click()

    #Chọn dòng Da Nang
    xpath_da_nang='/html/body/main/div/div[2]/div/div/div[1]/form/div[1]/div[1]/div[2]/div[2]/label[4]'
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_da_nang))).click()

    #Click vào nút tìm
    xpath_search='/html/body/main/div/div[2]/div/div/div[1]/form/div[1]/div[2]/div[2]/button'
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_search))).click()

    time.sleep(3) #Chờ web tải

    links=[] #Danh sách để lưu link bài viết từ trang

    #Duyệt qua các trang và lấy link bài viết
    while True:

        urls = driver.find_elements(By.CSS_SELECTOR, "h3.imt-3.text-break")
        link = [url.get_attribute("data-url") for url in urls] #Lấy link bài viết từ thuộc tính data-url
        links.extend(link) #Thêm danh sách link trang hiện tại vào danh sách links đã tạo ở trên
        
        try:
            xpath_next='/html/body/main/div[1]/div[2]/div[2]/div[3]/div/div[6]/nav/div[4]/a'
            element_next = driver.find_element(By.XPATH, xpath_next)
            driver.execute_script("arguments[0].scrollIntoView();", element_next) # Cuộn tới nút nút sang trang kế tiếp
            time.sleep(5)
            element_next.click() #Click nút sang trang kế tiếp
            time.sleep(3)
        except:
            break #Nếu không còn trang tiếp theo, thoát vòng lặp

    data=[] #Danh sách lưu dữ liệu bài viết

    #Truy cập từng link bài viết và lấy dữ liệu chi tiết
    for index, link in enumerate(links[:3]):
        driver.get(link) #Truy cập vào từng bài viết
        time.sleep(3)

        #Lấy tiêu đề công việc
        xpath_tittle="/html/body/main/div[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[1]/h1"
        title = driver.find_element(By.XPATH, xpath_tittle).text

        #Lấy mô tả chi tiết
        xpath_description="/html/body/main/div[1]/div[1]/div[4]/div[1]/div[1]/section"
        description = driver.find_element(By.XPATH, xpath_description).text.strip()

        #Lấy tên công ty
        xpath_company="/html/body/main/div[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]"
        company = driver.find_element(By.XPATH, xpath_company).text
        
        #Lấy tiền lương
        xpath_salary="/html/body/main/div[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[1]/div[2]/div/span"
        salary = driver.find_element(By.XPATH, xpath_salary).text

        #Lấy địa chỉ
        xpath_address="/html/body/main/div[1]/div[1]/div[4]/div[1]/div[1]/div[2]/div/div/div[1]/span"
        address = driver.find_element(By.XPATH, xpath_address).text

        #Gộp dữ liệu thành 1 hàng
        tmp=[title, description, company, salary, address]

        #Thêm vào danh sách dữ liệu
        data.append(tmp)

    #Xuất dữ liệu ra file Excel
    df = pd.DataFrame(data, columns=["Tiêu đề", "Mô tả", "Công ty", "Lương", "Địa chỉ"])
    df.to_excel(r"D:\Desktop\itviec.xlsx", index=False)

#Nhập tên đăng nhập và mật khẩu
username=""
password=""

# Lên lịch lấy thông tin việc làm vào lúc 6h sáng hằng ngày
schedule.every().day.at("06:00").do(lambda:crawl_data(username=username,password=password))
print("Lấy thông tin việc làm mỗi ngày vào 06:00")

while True:
    schedule.run_pending()
    time.sleep(1)