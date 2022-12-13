from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from random import randint
from jdatetime import datetime
from colorama import Fore
import requests


class InstaBot:
    UserName = ""
    Password = ""
    timeSleep = 4
    story_link = []

    def __init__(self, username, password):
        self.UserName = username
        self.Password = password

    def login(self, driver):  # login in instagram
        driver.get('https://www.instagram.com/accounts/login/')
        try:
            try:
                allow_cookies = driver.find_element(
                    By.XPATH,
                    '/html/body/div[4]/div/div/button[2]'
                    )
                allow_cookies.click()
                time.sleep(self.timeSleep)
            except Exception as e:
                allow_cookies = driver.find_element(
                    By.XPATH,
                    '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]'
                )
                allow_cookies.click()
                time.sleep(self.timeSleep)
            try:
                enter_username = driver.find_element(
                    By.XPATH,
                    '/html/body/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[1]/div/label/input'
                    )
            except Exception as e:
                enter_username = driver.find_element(
                    By.XPATH,
                    '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[1]/div/label/input'
                )
            enter_username.send_keys(self.UserName)
            try:
                enter_password = driver.find_element(
                    By.XPATH,
                    '/html/body/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[2]/div/label/input'
                )
            except Exception as e:
                enter_password = driver.find_element(
                    By.XPATH,
                    '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[2]/div/label/input'
                )
            enter_password.send_keys(self.Password)

            try:
                click_login = driver.find_element(
                    By.XPATH,
                    '/html/body/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[3]/button'
                    )
            except Exception as e:
                try:
                    click_login = driver.find_element(
                        By.XPATH,
                        '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[3]/button'
                    )
                except Exception as e:
                    click_login = driver.find_element(
                        By.XPATH,
                        '/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button'
                    )

            click_login.click()

            time.sleep(self.timeSleep*2)
        except Exception as e:
            enter_username = driver.find_element(
                By.XPATH,
                '/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input'
                )
            enter_username.send_keys(self.UserName)

            enter_password = driver.find_element(
                By.XPATH,
                '/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input'
                )
            enter_password.send_keys(self.Password)
            try:
                click_login = driver.find_element(
                    By.XPATH,
                    '/html/body/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[3]/button'
                    )
            except Exception as e:
                click_login = driver.find_element(
                    By.XPATH,
                    '/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button'
                    )
            click_login.click()

            time.sleep(self.timeSleep*2)  # 5
        get_url = driver.current_url
        if get_url == 'https://www.instagram.com/accounts/login/':
            print(Fore.RED + '================================')
            print(Fore.RED + 'login faild! -> check internet connection & username password.')
            print(Fore.RED + '================================' + Fore.WHITE)
            return False
        else:
            return True

    def find_user(self, driver, user_name):
        driver.get('https://www.instagram.com/{}/'.format(user_name))
        time.sleep(15)

    def open_story(self, driver):
        try:
            story_img = driver.find_element(
                By.XPATH,
                '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/div/div/span/img'
            )
        except Exception as e:
            return False

        story_img.click()
        time.sleep(self.timeSleep)
        return True

    def get_story_content(self, driver, need_pause=False):
        # ? check story play or pause mode
        if need_pause:
            story = driver.find_element(
                By.XPATH,
                '/html/body'
            )
            story.send_keys(Keys.SPACE)
        time.sleep(3)
        try:
            story_content = driver.find_element(
                By.XPATH,
                '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/div[1]/div/div/video/source'
            )
        except Exception as e:
            story_content = driver.find_element(
                By.XPATH,
                '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/div[1]/div/div/img'
            )
        self.story_link.append(story_content.get_attribute("src"))
        try:
            if need_pause:
                click_next = driver.find_element(
                    By.XPATH,
                    '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/button'
                )
            else:
                click_next = driver.find_element(
                    By.XPATH,
                    '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/button[2]'
                )
            driver.execute_script("arguments[0].click();", click_next)
            self.get_story_content(driver)
        except Exception as e:
            return False

    def download_video_series(self):
        video_links = self.story_link
        for link in video_links:

            # split link for find file name
            file_name = link.split('/')[-1]
            file_name = file_name.split('?')[0]

            print("Downloading file:%s"%file_name)

            # create response object
            r = requests.get(link, stream=True)

            # download started
            with open(file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)

            print("%s downloaded!\n"%file_name)

        print("All videos downloaded! ")
        return

print(Fore.GREEN + '\n================================')
print(Fore.GREEN + '==== Instagram DATA Crawler ====')
print(Fore.GREEN + '================================\n')

print(Fore.BLUE + 'First enter your input list then select option\n')
print(Fore.RED + '↪ ' + Fore.YELLOW + 'input list pattern ' + Fore.RED + '-> ' + Fore.YELLOW + 'username password page')
print(Fore.RED + '↪ ' + Fore.BLUE + 'input list EX ' + Fore.RED + '-> ' + Fore.BLUE + 'pytest62 !@981234 fars_news\n')
while True:
    all_input = list(map(str, input(Fore.GREEN + "Enter your input list: " + Fore.WHITE).split()))
    if len(all_input) == 3:
        username = all_input[0]
        password = all_input[1]
        targetUser = all_input[2]
        break
    else:
        print(Fore.RED + 'your input list is not valid try again please!')
        continue

driver = webdriver.Chrome()
FirstObject = InstaBot(username, password)  # make object of Instabot class
canLogin = FirstObject.login(driver)  # !call login method(function)
if canLogin:
    FirstObject.find_user(driver, targetUser)
    print("open Story")
    FirstObject.open_story(driver)
    FirstObject.get_story_content(driver, True)
    FirstObject.download_video_series()
a = input()
