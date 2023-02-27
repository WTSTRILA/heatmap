from selenium import webdriver

def parser():
    driver = webdriver.Chrome()
    driver.get("https://www.mydevice.io/")
    monitor_width = driver.execute_script("return screen.width;")
    monitor_height = driver.execute_script("return screen.height;")
    driver.quit()
    return monitor_width, monitor_height