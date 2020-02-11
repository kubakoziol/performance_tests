from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from influxdb import InfluxDBClient
import json
import datetime


class ManualTesting():

    def live_testing_ios(self):
        baseUrl = "https://cloud.bitbar.com/"
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(baseUrl)
        driver.implicitly_wait(60)

        # Provide Login
        time.sleep(5)
        driver.execute_script("window.scrollBy(0, 1000);")
        element = driver.find_element(By.XPATH, "//input[@id='login-email']")
        element.send_keys("live.test.performance+ios@gmail.com")

        # Provide Password
        element = driver.find_element(By.XPATH, "//input[@id='login-password']")
        element.send_keys("testdroid2011")
        time.sleep(1)

        # Push Submit
        element = driver.find_element(By.XPATH, "//button[@id='login-submit']")
        element.click()
        time.sleep(1)

        # User logged in to Live Testing
        driver.find_element(By.XPATH, "//div[@class='widget-title'][contains(text(), 'Choose device to start')]")
        print("User logged in successfuly. Live Testing page opened.")
        time.sleep(1)

        # Choose device
        driver.find_element(By.ID, 'device-3529').click()
        start_time = time.time()
        print("User have chosen device for Live Testing.")

        # Wait until element appear
        wait = WebDriverWait(driver, 90, poll_frequency=1)
        wait.until(EC.text_to_be_present_in_element((By.XPATH, "//div[@class='session-status']//div[2]"), "Connected"))
        elapsed_time_ios = time.time() - start_time

        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        print("Live session started in: " + str(elapsed_time_ios) + " seconds.")

        client = InfluxDBClient("10.10.65.141", "8086", "admin", "admin", "qastats")
        o = [{
            "measurement": "selenium_data",
            "tags": {
                "ostype": "ios"
            },
            # "time": current_time,
            "fields": {
                "ios_time_production": elapsed_time_ios
            }
        }]

        print(json.dumps(o))
        client.write_points(o)


perf = ManualTesting()
perf.live_testing_ios()
