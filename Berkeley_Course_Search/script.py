from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

def extract_courses(driver):
    # Extract all course numbers in "HISTORY 104" format
    page_source = driver.page_source
    matches = re.findall(r'alt="([A-Z]+ \d+[A-Z]?)', page_source)
    return set(matches)

def navigate_pages(driver):
    courses = set()
    while True:
        time.sleep(1)
        courses |= extract_courses(driver)
        try:
            next_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.next a'))
            )
            if 'disabled' in next_button.get_attribute("class"):
                break
            next_button.click()
        except:
            break
    return courses

def apply_filter(driver, section_label, filter_name):
    filter_section = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//div[@filter-name='{section_label}']"))
    )
    button = filter_section.find_element(By.XPATH, f".//span[contains(text(), '{filter_name}')]")
    button.click()
    time.sleep(2)

def main():
    options = Options()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)

    driver.get("https://classes.berkeley.edu/search/class?search=")
    wait = WebDriverWait(driver, 10)

    # Select Term: Fall 2025
    term_section = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@filter-name='term']")))
    fall_button = term_section.find_element(By.XPATH, ".//span[contains(text(), 'Fall 2025')]")
    fall_button.click()
    time.sleep(2)

    # Define all breadth and UC (general) requirement filters to test
    breadths = [
        "Arts & Literature", "Biological Science", "Historical Studies", "International Studies",
        "Philosophy & Values", "Physical Science", "Social & Behavioral Sciences"
    ]
    general_uc = ["American Cultures", "American History", "American Institutions"]

    results = {}

    for breadth in breadths:
        driver.get("https://classes.berkeley.edu/search/class?search=")
        time.sleep(2)
        fall_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Fall 2025')]")
        fall_button.click()
        time.sleep(2)
        apply_filter(driver, "breadthRequirements", breadth)
        breadth_courses = navigate_pages(driver)

        for uc_req in general_uc:
            driver.get("https://classes.berkeley.edu/search/class?search=")
            time.sleep(2)
            fall_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Fall 2025')]")
            fall_button.click()
            time.sleep(2)
            apply_filter(driver, "breadthRequirements", breadth)
            apply_filter(driver, "generalRequirements", uc_req)
            common_courses = navigate_pages(driver) & breadth_courses
            key = f"{breadth} & {uc_req}"
            results[key] = sorted(common_courses)

    driver.quit()

    # Print results
    for k, v in results.items():
        print(f"\n{k}:\n{'-' * len(k)}")
        for course in v:
            print(course)

if __name__ == "__main__":
    main()
