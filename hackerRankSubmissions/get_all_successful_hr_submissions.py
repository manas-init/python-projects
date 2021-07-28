import os
import sys
import json
import time
import errno
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains



# Python program\to print
# colored text and background
class colors:
    #to make ansci colour coding work even in windows
    from platform import system
    if "win" in system().lower(): #works for Win7, 8, 10 ...
        from ctypes import windll
        k=windll.kernel32
        k.SetConsoleMode(k.GetStdHandle(-11),7)
    black='\033[30m'
    red='\033[31m'
    green='\033[32m'
    orange='\033[33m'
    blue='\033[34m'
    purple='\033[35m'
    cyan='\033[36m'
    lightgrey='\033[37m'
    darkgrey='\033[90m'
    lightred='\033[91m'
    lightgreen='\033[92m'
    yellow='\033[93m'
    lightblue='\033[94m'
    pink='\033[95m'
    lightcyan='\033[96m'

def writeToFile(filename, text):
    with open(filename, 'w') as f:
        f.write(text)
    return


##This part deals with getting all the required metadata about successful submissions to hacker rank
def getAllSubmissions(request_session, request_header):
    all_submissions = None
    offset = 0
    limit = 200
    return_value = 1
    count = 1
    while return_value != 0:
        url='https://www.hackerrank.com/rest/contests/master/submissions/?offset={}&limit={}&_=1602098151802'.format(offset, limit)
        response = request_session.get(url, headers=request_header)
        soup = BeautifulSoup(response.text, 'html.parser')
        temp_dict = response.json()
        if all_submissions == None:
            all_submissions = temp_dict
        else:
            all_submissions["models"].extend(temp_dict["models"])
            all_submissions["total"] += temp_dict["total"]
        offset += limit
        count = count+1
        return_value = len(temp_dict["models"])
    #if len(all_submissions["models"]) != all_submissions["total"]:
    #    print("something wrong in getAllSubmissions function: len(models) != total")
    #    print(len(all_submissions["models"]))
    #    print(all_submissions["total"])
    return all_submissions


def getAcceptedSumissionDict(all_submissions):
    ac_submissions = {}
    for submission in all_submissions["models"]:
        challenge_id = submission["challenge_id"]
        if submission["status"] == "Accepted":
            temp_dict = {}
            temp_dict["challenge_id"] = challenge_id
            temp_dict["id"] = submission["id"]
            temp_dict["language"] = submission["language"]
            temp_dict["inserttime"] = submission["inserttime"]
            temp_dict["kind"] = submission["kind"]
            temp_dict["challenge_name"] = submission["challenge"]["name"]
            temp_dict["challenge_slug"] = submission["challenge"]["slug"]
            if ac_submissions.get("challenge_id") is None:
                ac_submissions[challenge_id] = temp_dict
            elif ac_submissions["challenge_id"]["inserttime"] <  submission["challenge_id"]["inserttime"]:
                submissions[challenge_id] = temp_dict
    return ac_submissions


def readJson(filename):
    try:
        with open(filename) as param_file:
            paramsMap = json.loads(param_file.read())
        return paramsMap
    except:
        print("error in readJson function\n{} :{} : {}".format(sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2]))
        print("filename : {}".format(filename))
        exit(1)


def readFile(filename):
    file1 = open(filename, "r")
    content = file1.read()
    file1.close()
    return content


def loginRequests(request_session, username, password):
    #header string picked from chrome
    header_string='''
    {
    "accept": "text/html,application/xhtml+xml,application/xml;q':0.9,image/avif,image/webp,image/apng,*/*;q':0.8,application/signed-exchange;v':b3;q':0.9',text/html,application/xhtml+xml,application/xml;q':0.9,image/avif,image/webp,image/apng,*/*;q':0.8,application/signed-exchange;v':b3;q':0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q':0.9",
    "cache-control": "max-age=0",
    "cookie": "hackerrank_mixpanel_token':7283187c-1f24-4134-a377-af6c994db2a0; hrc_l_i':F; _hrank_session':653fb605c88c81624c6d8f577c9094e4f8657136ca3487f07a3068c25080706db7178cc4deda978006ce9d0937c138b52271e3cd199fda638e8a0b8650e24bb7; _ga':GA1.2.397113208.1599678708; _gid':GA1.2.933726361.1599678708; user_type':hacker; session_id':h3xb3ljp-1599678763378; __utma':74197771.397113208.1599678708.1599678764.1599678764.1; __utmc':74197771; __utmz':74197771.1599678764.1.1.utmcsr':(direct)|utmccn':(direct)|utmcmd':(none); __utmt':1; __utmb':74197771.3.10.1599678764; _biz_uid':5969ac22487d4b0ff8d000621de4a30c; _biz_sid:79bd07; _biz_nA':1; _biz_pendingA':%5B%5D; _biz_flagsA':%7B%22Version%22%3A1%2C%22ViewThrough%22%3A%221%22%2C%22XDomain%22%3A%221%22%7D; _gat_UA-45092266-28':1; _gat_UA-45092266-26':1; session_referrer':https%3A%2F%2Fwww.google.com%2F; session_referring_domain':www.google.com; session_landing_url':https%3A%2F%2Fwww.hackerrank.com%2Fprefetch_data%3Fcontest_slug%3Dmaster%26get_feature_feedback_list%3Dtrue",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    }
    '''
    header_dict = json.loads(header_string)

    #creating session
    url = 'https://www.hackerrank.com/auth/login'
    response = request_session.get(url, headers=header_dict)

    #getting the csrf_token
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('meta', id='csrf-token')['content']

    #using it in login post call
    request_header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
    "x-csrf-token": csrf_token
    }
    payload = {"login":username, "password":password,"remember_me":False,"fallback":True}
    response = request_session.post(url, headers=request_header, data=payload)
    return request_header


def getSubmissionsMetadata(username, password):
    request_session = requests.Session()
    login_response_header = loginRequests(request_session, username, password)
    all_submissions = getAllSubmissions(request_session, login_response_header)
    accepted_submissions_dict = getAcceptedSumissionDict(all_submissions)
    return accepted_submissions_dict



##This part deals with getting the code of a particular submission
def loginSelenium(driver, username, password):
    driver.get('https://www.hackerrank.com/auth/login')

    #this waits for the event to happen or 10 secs
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "input-1"))
    )

    #this finds element by id namedi nput-1
    username_feild = driver.find_element_by_id("input-1")
    username_feild.clear()
    username_feild.send_keys(username)

    password_feild = driver.find_element_by_id("input-2")
    password_feild.clear()
    password_feild.send_keys(password)

    #login = driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div[2]/div/div/div[2]/div/div/div[2]/div[1]/form/div[4]/button/div/span')
    login = driver.find_element_by_xpath('//button[normalize-space()="Log In"]')
    #print(login)
    login.click()
    print("{}login successful{}".format(colors.lightcyan, colors.lightgrey))
    time.sleep(4)


def navigateToSubmissionPage(driver, url):
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
    driver.get(url)
    print("{}navigated to submissions page{}".format(colors.pink, colors.lightgrey))
    time.sleep(2)


def printLines(my_code, lines_already_printed, final_string_list):
    count=0
    for line in my_code:
        line_printed = lines_already_printed
        flag = False
        for each in line.text.splitlines():
            if each.isdigit():
                if int(each) == line_printed+1:
                    line_printed = line_printed+1
                    flag = True
                    #print("line printed : {}".format(line_printed))
                    continue
                if int(each) >= lines_already_printed+1:
                    flag = False
                    break
                else:
                    flag = False
                    #print("in error line {}".format(each))
            if flag:
                final_string_list.append(each)
                flag = False
            #print("end of line")
        count = count + 1
    return line_printed


def getSubmittedCode(driver, file_name, challange_class):
    final_string = ""
    prev_count = 0
    counts = 0
    final_string_list = []
    try:
        vertical_scrollbar = driver.find_element_by_class_name("CodeMirror-vscrollbar")
        breadcrumb_items = driver.find_elements_by_class_name("breadcrumb-item-text")
        challange_class.clear()
        for i in breadcrumb_items:
            challange_class.append(i.text)
        if checkCodeAlreadyPresent(challange_class[:-1], file_name) == True:
            return None
        if vertical_scrollbar.is_displayed() == False:
            raise NoSuchElementException
        for attempts in range(0, 10):
            my_code = driver.find_elements_by_class_name("CodeMirror-lines")
            #print("attemps number {}".format(attempts))
            prev_count = counts
            counts = printLines(my_code, prev_count, final_string_list)
            if prev_count == counts:
                break
            #print("prev_count : {}\ncounts : {}".format(prev_count, counts))
            for count in range(0, 10):
                vertical_scrollbar.send_keys(Keys.ARROW_DOWN)
                time.sleep(0.1)
        final_string = ("\n").join(final_string_list)
    except NoSuchElementException:
        my_code = driver.find_elements_by_class_name("CodeMirror-lines")
        counts = printLines(my_code, 0, final_string_list)
        final_string = ("\n").join(final_string_list)
    except:
        print("Error in function getSubmittedCode\n{} : {} : {}".format(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))
    return final_string


def getSubmissionForUrl(driver, file_name, url):
    navigateToSubmissionPage(driver, url)
    challange_class = []
    code_string = getSubmittedCode(driver, file_name, challange_class)
    #print("\n\n\n\nFinal string is \n{}".format(code_string))
    if code_string == None:
        return ()
    return challange_class[:-1], code_string


def createSubmissionUrl(challange_name, challange_id):
    return "https://www.hackerrank.com/challenges/{}/submissions/code/{}".format(challange_name, challange_id)


def removeInvalidCharacters(unfiltered_string):
    invalid_chars = ["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]
    for char in unfiltered_string:
        if char in invalid_chars:
            unfiltered_string = unfiltered_string.replace(char, "")
    return unfiltered_string


def checkCodeAlreadyPresent(submission_class, file_name):
    submission_class = ("/").join(submission_class)
    file_path = "submissions/{}/{}".format(submission_class, file_name)
    if os.path.isfile(file_path):
        print("{}File present{} : {}".format(colors.orange, colors.lightgrey, file_path))
        return True
    return False


def printSummary(total, new_subs, failed, failure_string):
    success_count = total-failed
    print("\n\n{0}{1}{2}Summary of execution{2}{1}{3}".format(colors.yellow, "=" * 40, " " * 10, colors.lightgrey))
    print("{}Total Submissions Found{} : {}".format(colors.lightblue, colors.lightgrey, total))
    print("{}Successfully traversed{} : {}".format(colors.lightgreen, colors.lightgrey, success_count))
    print("\t{0}new submissions{1} : {2}\n\t{0}old submissions{1} : {3}".format(colors.green, colors.lightgrey, new_subs, success_count - new_subs))
    print("{}Falied count{} : {}".format(colors.lightred, colors.lightgrey, failed))
    if failed != 0:
        print(failure_string)
    return

if __name__ == "__main__":
    config = readJson("config.json")
    username = config["username"]
    password = config["password"]
    accepted_submissions_dict = getSubmissionsMetadata(username, password)
    #print(json.dumps(accepted_submissions_dict, indent=4))
    submission_metadata_file = "my_subs_metadata.json"
    writeToFile(submission_metadata_file, json.dumps(accepted_submissions_dict, indent=4))
    readJson(submission_metadata_file)
    

    accepted_submissions_dict = readJson("my_subs_metadata.json")
    file_format_dict = readJson("lang_extension.json")
    PATH = config["path_to_chromedriver"]
    driver = webdriver.Chrome(executable_path=PATH)
    loginSelenium(driver, username, password)
    if not os.path.exists("submissions"):
        os.makedirs("submissions")
    failed_count = 0
    new_submission_count = 0
    failure_string = ""
    for submission in accepted_submissions_dict:
        file_name = accepted_submissions_dict[submission]["challenge_name"]
        file_name = removeInvalidCharacters(file_name)
        try:
            sub_url = createSubmissionUrl(accepted_submissions_dict[submission]["challenge_slug"], accepted_submissions_dict[submission]["id"])
            print("\n{}Starting{} : {}".format(colors.cyan, colors.lightgrey, sub_url))
            file_format = file_format_dict.get(accepted_submissions_dict[submission]["language"])
            submission_tuple = getSubmissionForUrl(driver, file_name+"."+file_format, sub_url)
            if len(submission_tuple) != 2:
                print("{}Ended{} : {}".format(colors.cyan, colors.lightgrey, sub_url))
                continue
            submission_class, submitted_string = submission_tuple
            submission_class = ("/").join(submission_class)
            file_path = "submissions/{}/{}.cpp".format(submission_class, file_name)
            if not os.path.exists(os.path.dirname(file_path)):
                try:
                    os.makedirs(os.path.dirname(file_path))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            writeToFile(file_path, submitted_string)
            print("{}File created{} : {}".format(colors.purple, colors.lightgrey, file_path))
            new_submission_count += 1
            print("{}Ended{} : {}".format(colors.cyan, colors.lightgrey, sub_url))
            #break
        except:
            failed_count += 1
            failed_string = "{}Failure{} when trying for \"{}\"".format(colors.red, colors.lightgrey, accepted_submissions_dict[submission]["challenge_name"])
            failure_string += ("\n" + failed_string)
            print(failed_string)
            print("{} : {} : {}".format(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))
        #x = input("Press Enter to continue")
    driver.quit()
    printSummary(len(accepted_submissions_dict), new_submission_count, failed_count, failure_string)    
    #text = driver.page_source
    #writeToFile('page_code_text.txt', text.encode('utf-8').decode('ascii', 'ignore'))
