from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys

def writeToFile(filename, text):
    with open(filename, 'w') as f:
        f.write(text)
    return


def loginToHR(driver):
    username_value="manasmishra1996@gmail.com"
    password_value=""

    driver.get('https://www.hackerrank.com/auth/login')

    #this waits for the event to happen or 10 secs
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "input-1"))
    )

    #this finds element by id namedi nput-1
    username = driver.find_element_by_id("input-1")
    username.clear()
    username.send_keys(username_value)

    password = driver.find_element_by_id("input-2")
    password.clear()
    password.send_keys(password_value)

    login=driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div[2]/div/div/div[2]/div/div/div[2]/div[1]/form/div[4]/button/div/span')
    print(login)
    login.click()
    print("login done")
    time.sleep(4)




def navigateToSubmissionPage(driver, url):
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
    driver.get(url)
    print("navigated to submissions page")
    time.sleep(2)


def printLines(my_code, lineAlreadyPrinted, finalStringList):
    count=0
    for line in my_code:
        linePrinted=lineAlreadyPrinted
        flag=False
        for each in line.text.splitlines():
  
            if each.isdigit():
                if int(each) == linePrinted+1:
                    linePrinted=linePrinted+1
                    flag=True
                    #print("line printed : {}".format(linePrinted))
                    continue
                if int(each) >= lineAlreadyPrinted+1:
                    flag=False
                    break
                else:
                    flag=False
                    #print("in error line {}".format(each))
            if flag:
                finalStringList.append(each)
                flag=False
            #print("end of line")
        count = count + 1
    return linePrinted


def getSubmittedCode(driver):
    verticaScrollbar = driver.find_element_by_class_name("CodeMirror-vscrollbar")

    prevCount=0
    counts=0
    finalStringList=[]
    for attempts in range(0, 10):
        my_code = driver.find_elements_by_class_name("CodeMirror-lines")
        #print("attemps number {}".format(attempts))
        prevCount=counts
        counts = printLines(my_code, prevCount, finalStringList)
        if prevCount == counts:
            break
        #print("prevCount : {}\ncounts : {}".format(prevCount, counts))
        for count in range(0, 10):
            verticaScrollbar.send_keys(Keys.ARROW_DOWN)
            time.sleep(1)
    finalString = ("\n").join(finalStringList)
    return finalString


def getSubmissionForUrl(driver, url):
    navigateToSubmissionPage(driver, url)
    fs=getSubmittedCode(driver)
    print("\n\n\n\nFinal string is \n{}".format(fs))


PATH = "C:\\Users\\manasm\\Downloads\\chromedriver_win32\\chromedriver.exe"
driver = webdriver.Chrome(PATH)
loginToHR(driver)
getSubmissionForUrl(driver, 'https://www.hackerrank.com/challenges/coin-change/submissions/code/182034719')
getSubmissionForUrl(driver, 'https://www.hackerrank.com/challenges/stockmax/submissions/code/183693884')
#navigateToSubmissionPage(driver, 'https://www.hackerrank.com/challenges/coin-change/submissions/code/182034719')
#navigateToSubmissionPage(driver, 'https://www.hackerrank.com/challenges/stockmax/submissions/code/183693884')

text=driver.page_source
writeToFile('tannu.txt', text.encode('utf-8').decode('ascii', 'ignore'))

#fs=getSubmittedCode(driver)
#print("\n\n\n\nFinal string is \n{}".format(fs))

sys.exi(0)