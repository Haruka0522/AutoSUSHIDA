import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

#コース選択(UI)
print("コースを選択してね")
flag = True
while flag:
    diff = input("3000円なら１,5000円なら２,10000円なら３　")
    if diff == "1":
        MODE_BUTTON = (250,180)
        TIME_LIMIT = 60
        flag = False
    elif diff == "2":
        MODE_BUTTON = (250,275)
        TIME_LIMIT = 90
        flag = False
    elif diff == "3":
        MODE_BUTTON = (250,300)
        TIME_LIMIT = 120
        flag = False
    else:
        print("[ERROR] mode select again")

START_BUTTON = (250,250)
SUSHIDA_URL = "http://typingx0.net/sushida/play.html"
WINDOW_SIZE = (990,1080)

#Chromeウェブドライバーの作成
driver = webdriver.Chrome()

#ウィンドウを開く
driver.set_window_size(*WINDOW_SIZE)
driver.get(SUSHIDA_URL)
webgl_element = driver.find_element_by_xpath('//*[@id="game"]/div')
actions = ActionChains(driver)
actions.move_to_element(webgl_element).perform()

#ロードの待機
time.sleep(10)

#スタートボタンのクリック
actions = ActionChains(driver)
actions.move_to_element_with_offset(webgl_element,START_BUTTON[0],START_BUTTON[1]).click().perform()
print("スタートボタンをクリックしたよ")
time.sleep(1)

#難易度選択ボタンのクリック
actions = ActionChains(driver)
actions.move_to_element_with_offset(webgl_element,MODE_BUTTON[0],MODE_BUTTON[1]).click().perform()
print("難易度を選択したよ")
time.sleep(1)

#スペースキーでスタート
element = driver.find_element_by_xpath("/html/body")
element.send_keys(" ")
print("開始！！")

#総当り入力開始
start_time = time.time()
while time.time() - start_time < TIME_LIMIT:
    element.send_keys("abcdefghijklmnopqrstuvwxyz-!?,.")

#終わり
input("エンターキーを押すと終了するよ")
driver.close()
driver.quit()
