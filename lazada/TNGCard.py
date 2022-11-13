from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # => 引入Chrome的配置
from selenium.webdriver.common.by import By

# 配置文件
from configparser import ConfigParser
configur = ConfigParser()
configur.read('d://python_conf.txt')

pushbulletkey = configur.get('pushbullet','key')
print(pushbulletkey)

# 配置
ch_options = Options()
# ch_options.add_argument("--headless")  # => 为Chrome配置无头模式
ch_options.add_experimental_option('excludeSwitches', ['enable-automation'])
ch_options.add_experimental_option('useAutomationExtension', False)

# 加速加载
# 不加载图片 start
prefs = {
    'profile.default_content_setting_values': {
        'images': 2,
    }
}
ch_options.add_experimental_option('prefs', prefs)
# 不加载图片end
ch_options.page_load_strategy = 'eager'
# eager：等待整个dom树加载完成，即DOMContentLoaded这个事件完成，也就是只要 HTML 完全加载和解析完毕就开始执行操作。放弃等待图片、样式、子帧的加载。

# 在启动浏览器时加入配置
driver = webdriver.Chrome(options=ch_options)  # => 注意这里的参数

url = "https://www.lazada.com.my/products/pre-order-delivery-in-14-days-enhanced-touch-n-go-card-to-be-released-by" \
      "-batches-i3175099305-s16072707014.html "

if __name__ == '__main__':
    driver.get(url)
    do = True
    times = 0
    while do:
        sleep(1)
        title = driver.find_element(By.XPATH, '//*[@id="module_product_title_1"]/div/div/h1').text
        Quantity = driver.find_element(By.XPATH, '//*[@id="module_quantity-input"]/div/div/span').text
        # new selenium don't support find_element_by_xpath  need use new By.XPATH
        # ref:https://stackoverflow.com/questions/66735222/attributeerror-webdriver-object-has-no-attribute-findelement
        print(times, " :  ", title, Quantity)
        if Quantity == "Out of stock":
            print("no")
            sleep(2)
            times = times + 1
            driver.refresh()
        else:
            import requests
            # https://docs.pushbullet.com/#create-push
            headers = {
                "Access-Token": pushbulletkey,
                "Content-Type": "application/json"
            }
            base = 'https://api.pushbullet.com'
            end_point_note = '/v2/pushes'
            url2 = f'{base}{end_point_note}'
            data = {
                "type": "note",
                "title": "TNG",
                "body": "有库存了"
            }
            resp = requests.post(url2, headers=headers, json=data)
            print(resp.text)
            print("yes")
            do = False
