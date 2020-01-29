from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import datetime

#アマゾンのwebサイトからレビューが高い順のプログラミング本のページに飛ぶ処理
driver = webdriver.Chrome(executable_path  = '/Users/maiko/Downloads/chromedriver')
driver.get('https://www.google.co.jp')
elem = driver.find_element_by_name('q')
driver.get('https://www.google.co.jp')
elem = driver.find_element_by_name('q')
elem.send_keys('アマゾン')
elem.send_keys(Keys.ENTER)
driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div/div/div/div[1]/a/h3').click()
elem2 = driver.find_element_by_id('twotabsearchtextbox')
elem2.send_keys('プログラミング本')
elem2.send_keys(Keys.ENTER)
driver.find_element_by_xpath('//*[@id="a-autoid-0-announce"]').click()
driver.find_element_by_xpath('//*[@id="s-result-sort-select_3"]').click()

#上位5位の本の名前、評価(5星中、星何個か？)
book_name = []
book_evaluation = []
book_comment = []
result = []

for i in range(1,6):
    address1 = '*[@id="search"]/div[1]/div[2]/div/span[4]/div[1]/div[' + str(i) +']/div/span/div/div/div[2]/h2/a/span'
    address2 = '*[@id="search"]/div[1]/div[2]/div/span[4]/div[1]/div[' + str(i) + ']/div/span/div/div/div[3]/div/span[1]'
    name = driver.find_element_by_xpath('//' + address1).text    
    evaluation = driver.find_element_by_xpath('//' + address2).get_attribute('aria-label')
    book_name.append(name)
    book_evaluation.append(evaluation)
    
#ブラウザを終了する
driver.quit()

#集めた情報を収納する
result = [book_name ,book_evaluation ]


#1日前スクレイピングした結果データをcsvから取ってくる
former_lines = [] 
with open("out.csv","r") as f:
    data = f.readlines()
    #同じランキングだったら、日付だけ表示されるようにする処理
    if  len(data[-1]) < 12:
        for i in range(-6,-1): 
            tmp2 = data[i]
            former_lines.append(tmp2)
    else:
        for i in range(-5,0):
            tmp2 = data[i]
            former_lines.append(tmp2)
former_lines2 = [i.rstrip('\n') for i in former_lines]

#csvファイルへの書き込み
result_lines = []
with open("out.csv", "a") as f:
    writer = csv.writer(f,lineterminator='\n') 
    dt_today = datetime.date.today()
    day = str(dt_today)
    f.write('\n')
    f.write(day)
    for i in range(0,5):
        part1_result = result[0][i]
        part2_result = result[1][i]
        recent_lines = [part1_result, part2_result ]
        a = ','.join(recent_lines)
        result_lines.append(a)
    if all([ former_lines2[i] == result_lines[i] for i in range(0,5)]) : 
        pass
    else:
        for i in range(0,5):
            writer.writerow(result_lines[i])
