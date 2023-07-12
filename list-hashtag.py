from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from time import sleep, strftime
from random import randint
import itertools
import pandas as pd
import PySimpleGUI as sg
import os
import logging
import requests
import json
import sys
from uuid import getnode as get_mac
import hashlib
import datetime
import re
sg.theme('light grey1')
ROOT_PATH = './'
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
def find_regex_1(k, s):
    reg = f'{k}\s*=\s*(\S+)'
    return re.search(reg, s).group(1)


def read_configs(config_file):
    with open(config_file, "r") as f:
        content = f.read()
        license_code = find_regex_1('LICENSE CODE', content)
        activation_code = find_regex_1('ACTIVATION CODE ', content)
    return license_code, activation_code


if __name__ == '__main__':
    license_code, activation_code = read_configs('license.txt')
def custom_meter_example():
    layout = [[sg.Text('در حال ارتباط با سرور جهت اعتبارسنجی لایسنس', justification='right', font=("iranyekan"))],
              [sg.ProgressBar(1, orientation='h', size=(35, 20), key='progress')],
              [sg.Cancel('لغو')]]
    now = datetime.datetime.now()
    future = now + datetime.timedelta(seconds=5)
    window = sg.Window('اعتبارسنجی لایسنس', layout ,font=("iranyekan"), icon="logo.ico", element_justification='r')
    progress_bar = window['progress']
    while True:
        delta = future - datetime.datetime.now()
        sec_left = delta.seconds
        event, values = window.read(timeout=100)
        progress_bar.update_bar(5-sec_left, 5)
        if event in (None, 'لغو') or sec_left <= 0:
            break
    window.close()

custom_meter_example()

def activate_license(license_key):
  machine_fingerprint = hashlib.sha256(str(get_mac()).encode('utf-8')).hexdigest()
  validation = requests.post(
    "https://api.keygen.sh/v1/accounts/d1f000c1-8f6a-4b57-ad04-f630d15740f3/licenses/actions/validate-key",
    headers={
      "Content-Type": "application/vnd.api+json",
      "Accept": "application/vnd.api+json"
    },
    data=json.dumps({
      "meta": {
        "key": license_code,
        "scope": {
            "fingerprint": machine_fingerprint
        }

      }
    })
  ).json()
  if validation["meta"]["valid"]:
      layout = [[sg.Text('به ربات یاس گرام خوش آمدید', justification='center', font='iranyekan 18')],
                [sg.Text('لطفا قبل از استفاده از ربات موارد زیر را در نظر داشته باشید', justification="center",
                         font="iranyekan 14")],
                [sg.Text('اکانت حداقل ۱۴ روز از ساخت آن گذشته و به فیسبوک متصل باشد', text_color='#922B21',
                         font="iranyekan 11")],
                [sg.Text('تایید دو مرحله ای فعال نباشد', text_color='#922B21', font="iranyekan 11")],
                [sg.Text('حداقل ۱۰۰ نفر را فالو داشته باشید تا استوری برای نمابش کم نیاید', text_color='#922B21',
                         font="iranyekan 11")],
                [sg.Text("chromedriver.exe = فایل درایور گوگل کروم در پوشه ربات موجود باشد", font="iranyekan 11",
                         text_color='#922B21')],
                [sg.Text("ربات برای بلاک نشدن شما به صورت تصادفی در مراحل کار خود مکث خواهد کرد", font="iranyekan 11",
                         text_color='#922B21')],
                [sg.Text("و پس از هر ۱۰۰ لایک به مدت ۵ دقیقه به چک کردن استوری می پردازد", font="iranyekan 11",
                         text_color='#922B21')],
                [sg.Text('لطفا در روند کار ربات در گوگل کروم تداخل ایجاد نکنید', font="iranyekan 11",
                         text_color='red')],
                [sg.Submit('شروع', font="iranyekan"), sg.Cancel('لغو', font="iranyekan")]]
      window = sg.Window('یاس گرام', layout, font="iranyekan", icon="logo.ico", element_justification='c')
      window.read()
      window.close()
      layout = [[sg.Text('لطفا اطلاعات زیر را با دقت وارد کنید', justification=("right"), font=("iranyekan"))],
                [sg.InputText(key='-INPUT-', size=(40, 1)),sg.Text('نام کاربری اینستاگرام', size=(15, 1))],
                [sg.InputText(key='-INPUT2-', size=(40, 1)),sg.Text('پسورد اینستاگرام', size=(15, 1))],
                [sg.InputText(key='-INPUT3-', size=(40, 1)),sg.Text('هشتگ', size=(15, 1))],
                [sg.Text('نام کاربری خود و هشتگ بدون @ یا # وارد شود')],
                [sg.Submit('تایید', font=("iranyekan")), sg.Cancel('لغو', font=("iranyekan"))]]
      window = sg.Window('اطلاعات ورود', layout, font=("iranyekan"), icon="logo.ico", element_justification='r')
      while True:
          event, values = window.read()
          if event == 'لغو' or event == sg.WIN_CLOSED:
              sys.exit()  # exit button clicked
          usr = window['-INPUT-'].get().strip()
          if usr == '':
              sg.popup(f"نام کاربری وارد نشده است")
          psw = window['-INPUT2-'].get().strip()
          if  psw == '':
              sg.popup(f"پسورد وارد نشده است")
          utag = window['-INPUT3-'].get().strip()
          if utag == '':
              sg.popup(f"هشتگ وارد نشده است")
          else:
               username_input = values['-INPUT-']
               password_input = values['-INPUT2-']
               hashtag_input = values['-INPUT3-']
               break
      window.close()

      chromedriver_path = './chromedriver'
      options = webdriver.ChromeOptions()
      options.add_argument("--disable-blink-features")
      options.add_experimental_option("excludeSwitches", ["enable-automation"])
      options.add_experimental_option('useAutomationExtension', False)
      driver = webdriver.Chrome(options=options, executable_path=chromedriver_path)
      driver.maximize_window()
      driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

      sleep(randint(2, 3))
      driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
      sleep(randint(2, 3))
      try:
          sleep(randint(2, 3))
          accept = driver.find_element_by_xpath("//button[text()='Accept All']")
          accept.click()
      except NoSuchElementException:
          pass

      username = driver.find_element_by_name('username')
      username.send_keys(username_input)
      password = driver.find_element_by_name('password')
      password.send_keys(password_input)
      sleep(randint(4, 5))
      button_login = driver.find_element_by_css_selector('form div:nth-of-type(3)')
      button_login.click()
      sleep(randint(3, 4))
      try:
          loginfail = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div[1]/div/form/div[2]/p")
          sg.Print('نام کاربری یا پسورد اشتباه است', text_color='red', font='iranyekan')
      except:
          sg.Print('ورود به اکانت موفقیت آمیز بود', text_color='green', font='iranyekan')
          sleep(randint(4, 5))
          sg.Print('طی کردن مراحل اولیه', font='iranyekan')
          sleep(randint(2, 3))
          notnow = driver.find_element_by_xpath("//button[text()='Not Now']")
          notnow.click()
      sleep(randint(10, 15))

      notnow2 = driver.find_element_by_xpath("//button[text()='Not Now']")
      notnow2.click()
      sleep(randint(4, 5))

      user_list = pd.read_csv('list_tagged.csv')
      user_list = list(user_list['0'])

      hashtags_list = [hashtag_input]

      user_list = []
      tag = -1
      sg.Print('رفتن به صفحه هشتگ', font='iranyekan')
      sleep(randint(2, 3))
      for hashtags in hashtags_list:
          tag += 1
          try:
              driver.get('https://www.instagram.com/explore/tags/'+ hashtags_list[tag] + '/')
              sg.Print('رفتن به صفحه هشتگ موفقیت آمیز بود', text_color='green', font='iranyekan')
              sleep(randint(2, 3))
          except:
              sg.Print('اشکال در رفتن به صفحه هشتگ', text_color='red', font='iranyekan')
          sleep(randint(15, 20))
          sg.Print('آماده سازی پنجره برای چک کردن استوری', font='iranyekan')
          sleep(randint(2, 3))
          driver.execute_script("window.open('');")
          driver.switch_to.window(driver.window_handles[1])
          driver.get('https://www.instagram.com/')
          sleep(randint(15, 20))
          sg.Print('بازگشت به صفحه هشتگ', font='iranyekan')
          sleep(randint(2, 3))
          driver.switch_to.window(driver.window_handles[0])
          sg.Print('تشخیص اولین پست', font='iranyekan')
          sleep(randint(2, 3))
          try:
              first_thumbnail = driver.find_element_by_xpath(
                  '/html/body/div[1]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div/div[2]')
              first_thumbnail.click()
          except NoSuchElementException:
              first_thumbnail = driver.find_element_by_xpath(
                  '//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div/div[2]')
              first_thumbnail.click()
          except:
              sg.Print('هیچ پستی در هشتگ موجود نیست', text_color='red', font='iranyekan')
          sg.Print('تشخیص اولین پست موفق بود', text_color='green', font='iranyekan')
          sleep(randint(15, 20))
          sg.Print('اقدام به شناسایی کاربر', font='iranyekan')
          sleep(randint(2, 3))
          try:
              user = webdriver.find_element_by_xpath(
                  '/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div/span/a').text
              sleep(randint(2, 3))
              sg.Print(user + ' از این هشتگ استفاده کرده است ')
              user_list.append(user)
          except NoSuchElementException:
              user = webdriver.find_element_css_selector(
                  'body > div._2dDPU.CkGkG > div.zZYga > div > article > div.eo2As > div.EtaWk > ul > div > li > div > div > div.C4VMK > h2 > div > span > a').text
              sleep(randint(2, 3))
              sg.Print(user + ' از این هشتگ استفاده کرده است ')
              user_list.append(user)
          sleep(randint(15, 20))
          for x in itertools.count(start=1):
              for v in range(1, 100):
                  driver.find_element_by_link_text('Next').click()
                  sleep(randint(5, 7))
                  try:
                      user = driver.find_element_by_xpath(
                          '/html/body/div[5]/div[2]/div/article/div[3]/div[1]/ul/div/li/div/div/div[2]/h2/div/span/a').text
                      sleep(randint(2, 3))
                      sg.Print(user)
                      user_list.append(user)
                      user_df = pd.DataFrame(set(user_list))
                      user_df.to_csv('list.csv')
                  except NoSuchElementException:
                      user = driver.find_element_css_selector(
                          'body > div._2dDPU.CkGkG > div.zZYga > div > article > div.eo2As > div.EtaWk > ul > div > li > div > div > div.C4VMK > h2 > div > span > a').text
                      sleep(randint(2, 3))
                      sg.Print(user)
                      user_list.append(user)
                      user_df = pd.DataFrame(set(user_list))
                      user_df.to_csv('list-hashtag.csv')
              sg.Print('سوئيچ به پنجره استوري', font='iranyekan')
              driver.switch_to.window(driver.window_handles[1])
              sleep(randint(7, 10))
              driver.get('https://www.instagram.com')
              sleep(randint(7, 10))
              refresh_logo = driver.find_element_by_xpath(
                  '/html/body/div[1]/section/nav/div[2]/div/div/div[1]/a/div/div')
              refresh_logo.click()
              sleep(randint(5, 7))
              sg.Print('چک کردن استوری به مدت ۵ دقیقه', font='iranyekan')
              try:
                  check_story = driver.find_element_by_xpath(
                      '/html/body/div[1]/section/main/section/div[1]/div[1]/div/div/div/div/ul/li[3]/div/button')
                  check_story.click()
                  sleep(randint(300, 360))
              except NoSuchElementException:
                  check_story = driver.find_element_by_xpath(
                      '//*[@id="react-root"]/section/main/section/div[1]/div[1]/div/div/div/div/ul/li[3]/div/button')
                  check_story.click()
                  sleep(randint(300, 360))
              else:
                  pass
              sleep(randint(2, 3))
              driver.get('https://www.instagram.com')
              sleep(randint(2, 3))
              sg.Print('سوئيچ به پنجره شناسایی', font='iranyekan')
              sleep(randint(2, 3))
              driver.switch_to.window(driver.window_handles[0])
              sleep(randint(5, 10))
      return True,

  if validation["meta"]["constant"] != "NOT_FOUND" or "PRODUCT_SCOPE_MISMATCH" or "FINGERPRINT_SCOPE_MISMATCH" or "MACHINE_SCOPE_MISMATCH":
    layout = [[sg.Text('لطفا لایسنس و کد فعالسازی خود را وارد کنید', justification=("right"), font='iranyekan')],
              [sg.InputText(key='-INPUT-',size=(40, 1)),sg.Text('کد لایسنس :',size=(10, 1), justification=("right"), font='iranyekan')],
              [sg.InputText(key='-INPUT2-',size=(40, 1)),sg.Text('کد فعالسازی:',size=(10, 1), justification=("right"), font='iranyekan')],
              [sg.Submit('تایید', font='iranyekan'), sg.Cancel('لغو', font='iranyekan')]]
    window = sg.Window('لایسنس معتبر نیست', layout, font='iranyekan', element_justification='r')

    while True:
        event, values = window.read()
        if event == 'لغو' or event == sg.WIN_CLOSED:
            break  # exit button clicked
        inp = window['-INPUT-'].get().strip()
        if event == 'تایید' and inp == '':
            sg.popup(f"اراعه کد لایسنس الزامی است")
        inp2 = window['-INPUT2-'].get().strip()
        if event == 'تایید' and inp2 == '':
            sg.popup(f"اراعه کد فعالسازی الزامی است")
        else:
            license_input = values['-INPUT-']
            read_configs('license.txt')
            lic = "license.txt"
            with open(lic, 'r+') as f:
                text = f.read()
                text = re.sub(license_code, license_input, text)
                f.seek(0)
                f.write(text)
                f.truncate()
            activation_input = values['-INPUT2-']
            read_configs('license.txt')
            lic = "license.txt"
            with open(lic, 'r+') as f:
                text = f.read()
                text = re.sub(activation_code, activation_input, text)
                f.seek(0)
                f.write(text)
                f.truncate()
            sg.popup(f"برنامه را دوباره اجرا کنید")
            sleep(3)
            break
    window.close()
    return False,


  if validation["meta"]["constant"] != "EXPIRED":
      layout = [[sg.Text('لطفا لایسنس و کد فعالسازی خود را وارد کنید', justification=("right"), font='iranyekan')],
                [sg.InputText(key='-INPUT-', size=(40, 1)),
                 sg.Text('کد لایسنس :', size=(10, 1), justification=("right"), font='iranyekan')],
                [sg.InputText(key='-INPUT2-', size=(40, 1)),
                 sg.Text('کد فعالسازی:', size=(10, 1), justification=("right"), font='iranyekan')],
                [sg.Submit('تایید', font='iranyekan'), sg.Cancel('لغو', font='iranyekan')]]
      window = sg.Window('لایسنس معتبر نیست', layout, font='iranyekan', element_justification='r')

      while True:
          event, values = window.read()
          if event == 'لغو' or event == sg.WIN_CLOSED:
              sys.exit()  # exit button clicked
          inp = window['-INPUT-'].get().strip()
          if event == 'تایید' and inp == '':
              sg.popup(f"اراعه کد لایسنس الزامی است")
          inp2 = window['-INPUT2-'].get().strip()
          if event == 'تایید' and inp2 == '':
              sg.popup(f"اراعه کد فعالسازی الزامی است")
          else:
              license_input = values['-INPUT-']
              read_configs('license.txt')
              lic = "license.txt"
              with open(lic, 'r+') as f:
                  text = f.read()
                  text = re.sub(license_code, license_input, text)
                  f.seek(0)
                  f.write(text)
                  f.truncate()
              activation_input = values['-INPUT2-']
              read_configs('license.txt')
              lic = "license.txt"
              with open(lic, 'r+') as f:
                  text = f.read()
                  text = re.sub(activation_code, activation_input, text)
                  f.seek(0)
                  f.write(text)
                  f.truncate()
              sg.popup(f"برنامه را دوباره اجرا کنید")
              sleep(3)
              break
      window.close()
      return False, "license {}".format(validation["meta"]["detail"])

  if validation["meta"]["constant"] != "SUSPENDED":
      layout = [[sg.Text('لطفا لایسنس و کد فعالسازی خود را وارد کنید', justification=("right"), font='iranyekan')],
                [sg.InputText(key='-INPUT-', size=(40, 1)),
                 sg.Text('کد لایسنس :', size=(10, 1), justification=("right"), font='iranyekan')],
                [sg.InputText(key='-INPUT2-', size=(40, 1)),
                 sg.Text('کد فعالسازی:', size=(10, 1), justification=("right"), font='iranyekan')],
                [sg.Submit('تایید', font='iranyekan'), sg.Cancel('لغو', font='iranyekan')]]
      window = sg.Window('لایسنس معتبر نیست', layout, font='iranyekan', element_justification='r')

      while True:
          event, values = window.read()
          if event == 'لغو' or event == sg.WIN_CLOSED:
              break  # exit button clicked
          inp = window['-INPUT-'].get().strip()
          if event == 'تایید' and inp == '':
              sg.popup(f"اراعه کد لایسنس الزامی است")
          inp2 = window['-INPUT2-'].get().strip()
          if event == 'تایید' and inp2 == '':
              sg.popup(f"اراعه کد فعالسازی الزامی است")
          else:
              license_input = values['-INPUT-']
              read_configs('license.txt')
              lic = "license.txt"
              with open(lic, 'r+') as f:
                  text = f.read()
                  text = re.sub(license_code, license_input, text)
                  f.seek(0)
                  f.write(text)
                  f.truncate()
              activation_input = values['-INPUT2-']
              read_configs('license.txt')
              lic = "license.txt"
              with open(lic, 'r+') as f:
                  text = f.read()
                  text = re.sub(activation_code, activation_input, text)
                  f.seek(0)
                  f.write(text)
                  f.truncate()
              sg.popup(f"برنامه را دوباره اجرا کنید")
              sleep(3)
              break
      window.close()
      return False, "license {}".format(validation["meta"]["detail"])

  if validation["meta"]["constant"] != "NO_MACHINE":
    return False, "license {}".format(validation["meta"]["detail"])

  activation = requests.post(
    "https://api.keygen.sh/v1/accounts/d1f000c1-8f6a-4b57-ad04-f630d15740f3/machines",
    headers={
      "Authorization": "Bearer "+ activation_code,
      "Content-Type": "application/vnd.api+json",
      "Accept": "application/vnd.api+json"
    },
    data=json.dumps({
      "data": {
        "type": "machines",
        "attributes": {
          "fingerprint": machine_fingerprint
        },
        "relationships": {
          "license": {
            "data": {"type": "licenses", "id": validation["data"]["id"]}
          }
        }
      }
    })
  ).json()
  if activation["meta"]["constant"] != "PRODUCT_SCOPE_MISMATCH" or "NOT_FOUND" or "MACHINE_SCOPE_MISMATCH" or "FINGERPRINT_SCOPE_MISMATCH":
     layout = [[sg.Text('لطفا لایسنس و کد فعالسازی خود را وارد کنید', justification=("right"), font='iranyekan')],
                [sg.InputText(key='-INPUT-', size=(40, 1)),
                 sg.Text('کد لایسنس :', size=(10, 1), justification=("right"), font='iranyekan')],
                [sg.InputText(key='-INPUT2-', size=(40, 1)),
                 sg.Text('کد فعالسازی:', size=(10, 1), justification=("right"), font='iranyekan')],
                [sg.Submit('تایید', font='iranyekan'), sg.Cancel('لغو', font='iranyekan')]]
     window = sg.Window('لایسنس معتبر نیست', layout, font='iranyekan', element_justification='r')

     while True:
          event, values = window.read()
          if event == 'لغو' or event == sg.WIN_CLOSED:
              break  # exit button clicked
          inp = window['-INPUT-'].get().strip()
          if event == 'تایید' and inp == '':
              sg.popup(f"اراعه کد لایسنس الزامی است")
          inp2 = window['-INPUT2-'].get().strip()
          if event == 'تایید' and inp2 == '':
              sg.popup(f"اراعه کد فعالسازی الزامی است")
          else:
              license_input = values['-INPUT-']
              read_configs('license.txt')
              lic = "license.txt"
              with open(lic, 'r+') as f:
                  text = f.read()
                  text = re.sub(license_code, license_input, text)
                  f.seek(0)
                  f.write(text)
                  f.truncate()
              activation_input = values['-INPUT2-']
              read_configs('license.txt')
              lic = "license.txt"
              with open(lic, 'r+') as f:
                  text = f.read()
                  text = re.sub(activation_code, activation_input, text)
                  f.seek(0)
                  f.write(text)
                  f.truncate()
              sg.popup(f"برنامه را دوباره اجرا کنید")
              sleep(3)
              break
     window.close()
     return False, "license {}".format(activation["meta"]["detail"])

     if "errors" in activation:
      errs = activation["errors"]

      return False, "license activation failed: {}".format(
        map(lambda e: "{} - {}".format(e["title"], e["detail"]).lower(), errs)
       )

  return True, "license activated"


status, msg = activate_license(sys.argv[0])

print(status, msg)
