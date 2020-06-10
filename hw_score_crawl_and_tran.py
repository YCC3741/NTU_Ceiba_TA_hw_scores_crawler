from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import random
from time import sleep
import sys
import getpass

import os
from pathlib import Path
import pandas as pd
from tqdm import tqdm

def crawler():
    # for fake usre agent generating
    user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36']
    user_agent = random.choice(user_agent_list)
    
    # set up chrome options
    chrome_options = Options() 
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()  
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("user-agent={}".format(user_agent))

    # use driver 
    driver_path = input("Type in your driver path (or directly drag the driver to terminal):")
    driver_path = driver_path if (driver_path[-1] != " ") else driver_path[:-1] ## prevent end with space, while using dragging way
    browser = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)

    # get website
    browser.get("https://ceiba.ntu.edu.tw/index.php")
    browser.find_element_by_xpath('//input[@value="1"]').click()

    # account and passward
    name = browser.find_element_by_name("loginid")
    pw = browser.find_element_by_name("password")

    user_name = input("Type in username:")
    password = getpass.getpass("Type in passward:")

    name.send_keys(user_name)
    pw.send_keys(password)

    # get into homework part of ceiba
    browser.find_element_by_xpath("//input[@class='btn'][@type='submit'][@value='登入']").submit()
    browser.find_element_by_name("b1").click()
    browser.find_element_by_xpath("//input[@onclick=\"singleadm('hw')\"]").click()
    browser.find_element_by_link_text("批改作業").click()

    # get information in homework table
    trows = browser.find_elements_by_xpath('//*[@id="sect_cont"]/table/tbody//tr')

    print("\nStart crawling scores...")
    # get the column lable of student IDs and column lables of names of homework 
    hw_id = []
    hw_name = []
    for i, row in enumerate(tqdm(trows)):
        if i>0:
            hw_id.append(str(row.find_element_by_xpath(".//td[1]").text))
            hw_name.append(str(row.find_element_by_xpath(".//td[2]").text))

    all_score = pd.DataFrame()
    
    for i, id_no in enumerate(tqdm(hw_id)):
        one_hw_score = []
        browser.find_element_by_xpath("//input[@onclick=\"singlehw('%s')\"]" %id_no).click()
        browser.find_element_by_link_text("此作業所有列表").click()

        # get students IDs and homework names
        if (i<1):
            student_ids = []
            students = browser.find_elements_by_name("student[]")
            for student in students:
                student_ids.append(student.get_attribute("value"))

            student_names = [browser.find_element_by_xpath(
                                            '//*[@id="hw_corr_list"]/table/tbody/tr[{}]/td[4]/span'.format(x)).text
                                            for x in range(2, len(students)+2)]

            all_score["id"] = student_ids
            all_score["name"] = student_names

        # get scores for each of homework
        # if score is ordinal
        if(len(browser.find_elements_by_name("old_rank_choice[]")) == len(all_score)):
            scores = browser.find_elements_by_name("old_rank_choice[]")
        # if score is continuous
        else:
            scores = browser.find_elements_by_name("old_score[]")

        for score in scores:
            one_hw_score.append(score.get_attribute("value"))
        all_score["{}".format(hw_name[i])] = one_hw_score 
        
        sleep(0.2)

        # go back two previous pages
        browser.execute_script("window.history.go(-2)")

    print("End crawling scores\n")
    
    # close browser
    browser.quit()
    return all_score


def transform(score_to_transform):
    return score_to_transform.replace({"A+":95, "A":87, "A-":82,
                                       "B+":78, "B":75, "B-":70,
                                       "C+":68, "C":65, "C-":60,
                                       "F":50, "X":0})

def output(output_file):

    output_path = str(os.path.join(Path.home(), "Downloads"))
    if not os.path.exists(output_path):
        output_path = ("Default Output path not exist, please type your own path:")
        if not os.path.exists(output_path):
            os.makedirs(output_path)

    output_file.to_csv("{}/students_scores.csv".format(output_path), encoding="utf_8_sig", index=False)


def main():
    all_score = crawler()
    final_score = transform(all_score)
    output(final_score)

    print("<=== Program Done ===>")

if __name__ == "__main__":
    main()