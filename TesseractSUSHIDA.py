import time
import locale
locale.setlocale(locale.LC_ALL,"C")
import tesserocr
import cv2
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import os


START_BUTTON = (250,250)
SUSHIDA_URL = "http://typingx0.net/sushida/play.html"
WINDOW_SIZE = (990,1080)


def cv2pil(image):
    ''' OpenCV型 -> PIL型 '''
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image


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
time.sleep(2)

#入力開始
start_time = time.time()
while time.time() - start_time < TIME_LIMIT:
    driver.save_screenshot("frame.png")
    frame = cv2.imread("frame.png")
    sentence_area = frame[360:390,325:635]
    sentence_area = cv2pil(sentence_area)
    sentence = tesserocr.image_to_text(sentence_area,lang="eng")
    element.send_keys(sentence)
    print(sentence)

#終わり
input("エンターキーを押すと終了するよ")
driver.close()
driver.quit()
os.remove("frame.png")
