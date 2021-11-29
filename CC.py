from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
from PIL import Image
import base64
import json
import requests
from configparser import ConfigParser


chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver = webdriver.Chrome()
conf = ConfigParser()
conf.read("init.conf", encoding="utf8")
# client = pymongo.MongoClient('localhost',27017)
# mis = client['mis']
# schedule = mis['schedule']

wait = WebDriverWait(driver, 10)
url = 'https://mis.bjtu.edu.cn/home/'
URL = 'http://jwc.bjtu.edu.cn'


type = conf.getint("token", "type")  # 1为本方案课程 2为其他方案课程
type2 = conf.getint("token", "type2")  # 1为搜索 0为不搜索
user_id_str = conf.get("token", "user_id_str")  # 学号
password_str = conf.get("token", "password_str")  # 密码
xpath_str = conf.get("token", "xpath_str")
delta = conf.getfloat("token", "delta")
course_number = conf.get("token", "course_number")
# course_number = 'A101020B'


def search():
    try:
        # 进入mis
        driver.get('https://mis.bjtu.edu.cn/home/')
        time.sleep(delta)
        name = driver.find_element_by_xpath('//*[@id="id_loginname"]')
        password = driver.find_element_by_xpath('//*[@id="id_password"]')
        submit = driver.find_element_by_xpath(
            '//*[@id="login"]/dl/dd[2]/div/div[3]/button')
        name.send_keys(user_id_str)
        password.send_keys(password_str)
        submit.click()
        # 进入教务系统
        time.sleep(delta)
        driver.get('https://mis.bjtu.edu.cn/module/module/10')
        time.sleep(delta)
        step1 = driver.find_element_by_xpath(
            '/html/body/div[2]/div[1]/div/div[1]/ul/li[4]/a')
        step1.click()
        step2 = driver.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div/div[1]/div[1]/div[1]/div/ul/li[2]/ul/li[1]/a'
        )
        step2.click()
        time.sleep(delta)
        # 上面的是通用步骤 到达“网上选课”一栏
        if type == 1:
            # 本方案
            this_program()
        elif type == 2:
            # 其他方案
            other_program()
        XuanKe(type)

    except:
        # 进入教务系统
        time.sleep(delta)
        driver.get('https://mis.bjtu.edu.cn/module/module/10')
        time.sleep(delta)
        step1 = driver.find_element_by_xpath(
            '/html/body/div[2]/div[1]/div/div[1]/ul/li[4]/a')
        step1.click()
        step2 = driver.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div/div[1]/div[1]/div[1]/div/ul/li[2]/ul/li[1]/a'
        )
        step2.click()
        time.sleep(delta)
        # 上面的是通用步骤 到达“网上选课”一栏
        if type == 1:
            # 本方案
            this_program()
        elif type == 2:
            # 其他方案
            other_program()
        XuanKe(type)


def alert(type):
    driver.switch_to.default_content()

    driver.find_element_by_xpath(
        '/html/body/div[4]/div/div/div[3]/button[1]').click()
    if type == 1:
        # 本方案
        driver.switch_to.frame(
            driver.find_element_by_xpath(
                '/html/body/div[2]/div[2]/div/div[2]/div[5]/div[1]/iframe'))
    else:
        # 其他方案
        driver.switch_to.frame(
            driver.find_element_by_xpath(
                '/html/body/div[2]/div[2]/div/div[2]/div[5]/div[2]/iframe'))


def duoXuan(i):
    if i == 1:
        driver.find_element_by_xpath(
            '//*[@id="container"]/table/tbody/tr[3]/td[1]/input').click()
        alert(type)
    if i == 2:
        driver.find_element_by_xpath(
            '//*[@id="container"]/table/tbody/tr[4]/td[1]/input').click()
    elif i == 3:
        driver.find_element_by_xpath(
            '//*[@id="container"]/table/tbody/tr[5]/td[1]/input').click()
    elif i == 4:
        driver.find_element_by_xpath(
            '//*[@id="container"]/table/tbody/tr[6]/td[1]/input').click()
    elif i == 5:
        driver.find_element_by_xpath(
            '//*[@id="container"]/table/tbody/tr[2]/td[1]/input').click()
    elif i == 6:
        driver.find_element_by_xpath(
            '//*[@id="container"]/table/tbody/tr[7]/td[1]/input').click()
    elif i == 7:
        driver.find_element_by_xpath(
            '//*[@id="container"]/table/tbody/tr[8]/td[1]/input').click()
    else:
        driver.find_element_by_xpath(
            '//*[@id="current"]/table/tbody/tr[9]/td[1]/label').click()
    return True


def XuanKe(type):
    tag = 1
    i = 1
    count = 1
    while tag:
        try:
            driver.find_element_by_xpath(
                '//*[@id="container"]/table/tbody/tr[2]/td[1]/input').click()
            alert(type)
            # duoXuan(i)
            tag = 0
        except Exception as e:
            count = count + 1
            if count == 600:
                main()
            print(count)
            time.sleep(delta)

            if type2 == 1:
                driver.find_element_by_xpath('/html/body/form/button').click()
            else:
                driver.refresh()
                if type == 1:
                    # 本方案
                    driver.switch_to.frame(
                        driver.find_element_by_xpath(
                            '/html/body/div[2]/div[2]/div/div[2]/div[5]/div[1]/iframe'
                        ))
                else:
                    # 其他方案
                    driver.switch_to.frame(
                        driver.find_element_by_xpath(
                            '/html/body/div[2]/div[2]/div/div[2]/div[5]/div[2]/iframe'
                        ))
    time.sleep(delta)
    flag = False
    try_cnt = 1
    '''
    while not flag:
        try:
            flag = duoXuan(i)
        except Exception as e:
            print(i)
            print(e)
            if i == 3:
                i = 0
            i += 1
            driver.refresh()
            try_cnt += 1
            time.sleep(delta)
            '''
    # 弹窗提交按钮

    # //*[@id="container"]/table/tbody/tr[4]/td[9]/div[1]
    driver.find_element_by_xpath('//*[@id="select-submit-btn"]').click()
    time.sleep(delta)


def other_program():
    step3 = driver.find_element_by_xpath(
        '/html/body/div[2]/div[2]/div/div[2]/div[4]/label[2]')
    step3.click()
    driver.switch_to.frame(
        driver.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div/div[2]/div[5]/div[2]/iframe'))

    if type2 == 1:
        course = driver.find_element_by_xpath(
            '/html/body/form/input[1]').send_keys(course_number)
        submit_course = driver.find_element_by_xpath('/html/body/form/button')
        try:
            course.send_keys(course_number)
        except Exception as e:
            submit_course.click()
        # //*[@id="thepage"]//*[@id="page_go"]
        time.sleep(2)
        submit_page = driver.find_element_by_xpath('//*[@id="page_go"]')
        submit_page.click()


def this_program():
    driver.switch_to.frame(
        driver.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div/div[2]/div[5]/div[1]/iframe'))
    if type2 == 1:
        course = driver.find_element_by_xpath(
            '/html/body/form/input[1]').send_keys(course_number)
        submit_course = driver.find_element_by_xpath('/html/body/form/button')
        try:
            course.send_keys(course_number)
        except Exception as e:
            submit_course.click()
        # //*[@id="thepage"]//*[@id="page_go"]
        time.sleep(2)
        submit_page = driver.find_element_by_xpath('//*[@id="page_go"]')
        submit_page.click()
    # driver.find_element_by_xpath('//*[@id="container"]/table/tbody/tr[2]/td[1]/input').click()


def base64_api(uname, pwd, img, typeid):
    with open(img, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        b64 = base64_data.decode()
    data = {"username": uname, "password": pwd, "typeid": typeid, "image": b64}
    result = json.loads(
        requests.post("http://api.ttshitu.com/predict", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]
    return ""


def screenshot():
    driver.save_screenshot('full_baidu.png')
    left = 500
    top = 145
    right = left + 214
    bottom = top + 62
    photo = Image.open('full_baidu.png')
    photo = photo.crop((left, top, right, bottom))
    photo.save('full_baidu.png')


def verification_code_submit(result):
    driver.switch_to.default_content()
    verification_code = driver.find_element_by_xpath(
        '/html/body/div[4]/div/div/div[2]/div/div/input[2]')
    verification_code.send_keys(result)
    submit = driver.find_element_by_xpath(
        '/html/body/div[4]/div/div/div[3]/button[1]')
    submit.click()
    if type2 == 1:
        driver.find_element_by_xpath('/html/body/form/button')
    else:
        if type == 1:
            # 本方案
            driver.switch_to.frame(
                driver.find_element_by_xpath(
                    '/html/body/div[2]/div[2]/div/div[2]/div[5]/div[1]/iframe')
            )
        else:
            # 其他方案
            driver.switch_to.frame(
                driver.find_element_by_xpath(
                    '/html/body/div[2]/div[2]/div/div[2]/div[5]/div[2]/iframe')
            )


def main():

    search()
    # get_img()

    screenshot()

    img_path = "full_baidu.png"
    # 用的是图鉴的api去解验证码
    result = base64_api(uname=conf.get("ttpicture", "uname"), pwd=conf.get("ttpicture", "pwd"),
                        img=img_path, typeid=16)
    verification_code_submit(result)

    # print(result)

    XuanKe(type)


if __name__ == '__main__':
    main()
