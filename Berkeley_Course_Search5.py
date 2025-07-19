from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import pandas as pd

def click_filter(driver, wait, label_text):
    xpath = f"//span[@class='facet-item__value' and text()='{label_text}']"
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    driver.execute_script("arguments[0].scrollIntoView();", btn)
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "loading-popup")))
    btn.click()
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "loading-popup")))
    time.sleep(0.75)  # Let content refresh

def extract_courses(driver, breadth):
    #titles = driver.find_elements(By.CLASS_NAME, "st--title")  ---  NOT NEEDED FOR RN AT LEAST
    sections = driver.find_elements(By.CLASS_NAME, "st--section-name")
    section_text = [s.text.strip() for s in sections]
    for section in section_text:
        try:
            if breadth not in all_courses[section]:
                all_courses[section].append(breadth)
        except:
            all_courses[section] = [breadth]

def paginate(driver, wait):
    active_li = driver.find_element(By.XPATH,
                                    "//li[contains(@class, 'pager__item') and contains(@class, 'is-active')]")
    next_li = active_li.find_element(By.XPATH, "following-sibling::li[1]")
    next_link = next_li.find_element(By.TAG_NAME, "a")
    driver.execute_script("arguments[0].scrollIntoView();", next_link)
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "loading-popup")))
    next_link.click()
    # Wait for the new page to load
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "loading-popup")))
    time.sleep(0.7)

def show_all_filters(driver, section_label):
    section_label = section_label.replace(" ", "").lower()
    legend = driver.find_element(By.ID, f"block-{section_label}")
    driver.execute_script("arguments[0].scrollIntoView();", legend)
    show_more = legend.find_elements(By.XPATH, ".//*[contains(text(), 'Show more')]")
    driver.execute_script("arguments[0].scrollIntoView();", show_more[0])
    show_more[0].click()
    time.sleep(0.1)

def run(driver, wait, requirements):
    requirements_list_name = requirements.lower().replace(" ", "_")
    requirements_list = globals()[requirements_list_name]

    for req in requirements_list:
        count = 0
        print (req)
        show_all_filters(driver, requirements)
        click_filter(driver, wait, req)
        while True:
            try:
                extract_courses(driver, req)
                paginate(driver, wait)
                count += 1
                print (count)
            except:
                break
        show_all_filters(driver, requirements)
        click_filter(driver, wait, req)

all_courses = {}

def main():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 15)

    breadth_requirements = ["Arts & Literature", "Biological Science", "Historical Studies", "International Studies", "Philosophy & Values", "Physical Science", "Reading and Composition B", "Social & Behavioral Sciences"]
    general_requirements = ["2nd Half of Reading & Composition", "American Cultures", "American History", "American Institutions"]

    driver.get("https://classes.berkeley.edu")
    click_filter(driver, wait, "Fall 2025")
    run(driver, wait, "Breadth Requirements")
    run(driver, wait, "General Requirements")

    print ("Course Search Complete")

    all_courses_file_path = "/Users/ronitmathur/Desktop/Ronit/Coding/Berkeley_Course_Search/All_Courses"
    with open(all_courses_file_path, 'wb') as file:
        pickle.dump(all_courses, file)

    first_filter_courses = {i: all_courses[i] for i in all_courses if len(all_courses[i]) > 1}
    first_filter_courses_file_path = "/Users/ronitmathur/Desktop/Ronit/Coding/Berkeley_Course_Search/first_filter_courses"
    with open(first_filter_courses_file_path, 'wb') as file:
        pickle.dump(first_filter_courses, file)

    second_filter_courses = {course: req_list for course, req_list in first_filter_courses.items() if any(req in breadth_requirements for req in req_list) and any(req in general_requirements for req in req_list)}
    second_filter_courses_file_path = "/Users/ronitmathur/Desktop/Ronit/Coding/Berkeley_Course_Search/second_filter_courses"
    with open(second_filter_courses_file_path, 'wb') as file:
        pickle.dump(second_filter_courses, file)

    max_len = max(len(reqs) for reqs in second_filter_courses.values())
    # Pad lists with empty strings so all columns have the same length
    padded_dict = {
        course: reqs + [""] * (max_len - len(reqs))
        for course, reqs in second_filter_courses.items()
    }
    # Convert to DataFrame
    df = pd.DataFrame.from_dict(padded_dict, orient="columns")
    df.to_csv("/Users/ronitmathur/Desktop/Ronit/Coding/Berkeley_Course_Search/second_filter_courses_spreadsheet.csv",
              index=False)

if __name__ == "__main__":
    main()