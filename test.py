import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    # Configure Chrome to download to the current directory
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "download.default_directory": os.getcwd(),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })
    driver = webdriver.Chrome(options=options)
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

    # Save counter test
    wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Save Counter')]")))
    driver.find_element(By.XPATH, "//button[contains(., 'Save Counter')]").click()
    # Wait for download with a custom timeout loop
    wait.until(lambda d: any("counter_value.txt" in f for f in os.listdir()), message="Download did not complete")
    expected_value = int(driver.find_element(By.ID, "counter").text)
    with open("counter_value.txt", "r") as f:
        actual_value = f.read().strip()
        assert actual_value == f"Counter Value: {expected_value}", "Save should export correct counter value"
    os.remove("counter_value.txt")  # Clean up

    # Suggest route test
    wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Suggest Route')]")))
    driver.find_element(By.XPATH, "//button[contains(., 'Suggest Route')]").click()
    alert = wait.until(EC.alert_is_present())
    assert "SFO -> LAX" in alert.text, "Suggest Route should show SFO -> LAX"
    alert.accept()

    print("Tests passed!")
finally:
    driver.quit()
