from selenium import webdriver

driver = webdriver.Firefox()
driver.get('https://www.cdv.com')
driver.close()