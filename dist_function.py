from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from multiprocessing import Process, Queue


def get_dist(Q_out, Q_in):
    options = Options()
    options.headless = True

    driver = webdriver.Chrome(options=options, executable_path=r'D:\resume projects\genetic algorithm\chromedriver.exe')
    driver.delete_all_cookies()
    print("driver is setup")

    driver.get("https://www.google.de/maps/dir/" + "Bann" + "/" + "Landstuhl" + "/")
    python_button = WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, '//*[@id=\"yDmH0d\"]/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div[1]/div/button/span')))
    python_button.click()

    print("driver pressed 'accept' button")

    counter = 0

    while True:
        counter += 1
        if counter % 10 == 0:
            driver.delete_all_cookies()
            driver.get("https://www.google.de/maps/dir/" + "Bann" + "/" + "Landstuhl" + "/")
            python_button = WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id=\"yDmH0d\"]/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div[1]/div/button/span')))
            python_button.click()
        q_item = Q_in.get()
        print(q_item)
        if q_item == "done":
            break
        loc1, loc2 = q_item[0], q_item[1]

        if loc1 == loc2:
            Q_out.put([loc1 + "-" + loc2 + ":" + "0 min"])
        else:
            try:
                driver.get("https://www.google.de/maps/dir/" + loc1 + "/" + loc2 + "/")

                python_button = WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, '//*[@id=\"omnibox-directions\"]/div/div[2]/div/div/div[1]/div[2]/button/img')))
                python_button.click()

                knob_element = WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, '/html/body/jsl/div[3]/div[10]/div[8]/div/div[1]/div/div/div[5]/div/div/div[1]/div[1]/div[1]/span[1]')))
                res = knob_element.text

                Q_out.put([loc1 + "-" + loc2 + ":" + res])

            except:
                print("didn't work")
                Q_in.put(q_item)

    print("done")

    driver.quit()


def get_multiple_distances_parallel(locations, cores=4, verbose=True):
    to_check = []

    for loc1 in locations:
        for loc2 in locations:
            to_check.append([loc1, loc2])

    to_check_size = len(to_check)

    Q_out = Queue()
    Q_in = Queue()

    processes = [Process(target=get_dist, args=(Q_out, Q_in,)) for i in range(cores)]
    for p in processes:
        p.start()

    if verbose:
        print("processes started")

    for item in to_check:
        Q_in.put(item)

    if verbose:
        print("q_in created")

    shared_queue_list = []
    for i in range(to_check_size):
        if i % 10 == 0 and verbose:
            print(i / to_check_size)

        queue_item = Q_out.get()
        shared_queue_list.append(queue_item)

    for _ in range(cores):
        Q_in.put("done")

    if verbose:
        print("processes done")

    for p in processes:
        p.join()

    if verbose:
        print("processes joined")

    ret = {}
    for loc in locations:
        ret[loc + "-" + loc] = 0

    for item in shared_queue_list:
        ret[item[0][:item[0].find(":")]] = item[0][item[0].find(":") + 1:]

    if verbose:
        print("string times to int times (in minutes)")

    for key in ret:
        if ret[key] == "unclear":
            ret[key] = 999_999_999
        else:
            ret[key] = convert_time(ret[key])

    return ret


def convert_time(time):
    if 'h' not in time:
        return int(time[:-4])
    else:
        hours = time[:time.find('h')]
        minutes = time[time.find('h') + 2:-4]
        if minutes != '':
            return int(hours) * 60 + int(minutes)
        else:
            return int(hours) * 60