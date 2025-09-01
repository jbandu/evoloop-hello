import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    driver = webdriver.Chrome()
    driver.get("https://jbandu.github.io/evoloop-hello/")

    wait = WebDriverWait(driver, 10)

    # Counter appears
    wait.until(EC.presence_of_element_located((By.ID, "counter")))
    assert int(driver.find_element(By.ID, "counter").text) == 0, "Counter should start at 0"

    # Increment
    driver.find_element(By.XPATH, "//button[contains(., 'Increment')]").click()
    wait.until(lambda d: int(d.find_element(By.ID, "counter").text) == 1)
    assert int(driver.find_element(By.ID, "counter").text) == 1, "Counter should increment"

    # Decrement
    driver.find_element(By.XPATH, "//button[contains(., 'Decrement')]").click()
    wait.until(lambda d: int(d.find_element(By.ID, "counter").text) == 0)
    assert int(driver.find_element(By.ID, "counter").text) == 0, "Counter should go back to 0 after decrement"

    # Dark mode toggle
    driver.find_element(By.XPATH, "//button[contains(., 'Toggle')]").click()
    wait.until(lambda d: "dark-mode" in d.find_element(By.TAG_NAME, "body").get_attribute("class"))
    driver.refresh()
    wait.until(lambda d: "dark-mode" in d.find_element(By.TAG_NAME, "body").get_attribute("class"))

    print("Tests passed!")
finally:
    driver.quit()
