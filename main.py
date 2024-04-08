import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from config import URL, userName, password
from selenium import webdriver
from data import courseInfos

global courseInfos

def start():
    driver=webdriver.Chrome()

    driver.get(URL) 
    driver.maximize_window()

    loginBtn = driver.find_element(by=By.CSS_SELECTOR, value='button.btn.btn-primary.fw-bold')

    time.sleep(1)

    loginBtn.click()



    while True:
        try:
            captchaEle = driver.find_element(by=By.ID, value="captchaBlock")
            break
        except:
            driver.refresh()





    driver.find_element(by=By.ID,value="username").send_keys(userName)
    driver.find_element(by=By.ID,value="password").send_keys(password)

    time.sleep(8) #TODO: CLICK WITHIN 10s


    signInBtn = driver.find_element(by=By.ID,value='submitBtn')

    signInBtn.click()

    driver.implicitly_wait(3)

    

    # # NOW SIGNED-IN;

    expandBtn = driver.find_element(by=By.CSS_SELECTOR, value='button.btn.btn-sm.bg-transparent.d-none.d-sm-block.ms-0')
    expandBtn.click()


    openExmBtn = driver.find_element(by=By.ID, value='acMenuItemHDG0070')
    openExmBtn.click()


    exmBtns = driver.find_elements(by=By.CSS_SELECTOR, value="a.dropdown-item.menuFontStyle.textColor2.systemMainMenu")
    # print(exmBtns)

    driver.implicitly_wait(3)

    for btn in exmBtns:
        if btn.get_attribute("data-url") == "examinations/examGradeView/StudentGradeHistory":
            btn.click()
            break
    

    time.sleep(2)

    collapseBtn = driver.find_element(by=By.CSS_SELECTOR, value='button[data-bs-dismiss="offcanvas"]')
    collapseBtn.click()

    time.sleep(3)

    rows = driver.find_elements(by=By.CSS_SELECTOR, value='tr.tableContent')

    
    weighted_score = 0
    total_credits = 0
        

    for row in rows:
        course_name = row.find_element(by=By.CSS_SELECTOR, value='td:nth-of-type(3)').text
        course_credits = row.find_element(by=By.CSS_SELECTOR, value='td:nth-of-type(5)').text
        course_grade = row.find_element(by=By.CSS_SELECTOR, value='td:nth-of-type(6)').text
        # course_credits = int(course_credits)
        if(course_grade == 'S' or course_grade == 'A' or course_grade == 'B'):
            course_credits = float(course_credits)
            if course_credits == 1:
                #STS
                course_credits = 3.0

            total_credits = total_credits + course_credits
            # CHANGE YOUR COURSE GRADE HERE!
            if course_name == "Introduction to Nanotechnology":
                weighted_score = weighted_score + (course_credits*9)
                continue
            if course_name == "Basic Spanish":
                weighted_score = weighted_score + (course_credits*9)
                continue
            if(course_grade == 'S'):
                weighted_score = weighted_score + (course_credits*10)
            if(course_grade == 'A'):
                weighted_score = weighted_score + (course_credits*9)
            if(course_grade == 'B'):
                weighted_score = weighted_score + (course_credits*8)
                
        courseInfos.append({"name": course_name, "credits": course_credits, "grade": course_grade})
        print(course_name + " " + str(course_credits) + "\t" + course_grade)

    print("New Grade: ", (weighted_score/total_credits))

    print(courseInfos)