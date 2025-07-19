from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import NoSuchElementException, TimeoutException
import pickle

breadth_requirements = ["Arts & Literature", "Biological Science", "Historical Studies", "International Studies", "Philosophy & Values", "Physical Science", "Reading and Composition B", "Social & Behavioral Sciences"]
general_requirements = ["2nd Half of Reading & Composition", "American Cultures", "American History", "American Institutions"]
#changed & to &amp; because that is what it looks like in html code -- change back to & if code doesn't work due to this

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)

def click_filter(label_text): # can use this for fall 2025 AND breadth and gen requirements??
    xpath = f"//span[@class='facet-item__value' and text()='{label_text}']"
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    driver.execute_script("arguments[0].scrollIntoView();", btn)
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "loading-popup")))
    btn.click()
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "loading-popup")))
    time.sleep(0.75)  # Let content refresh

def extract_courses(breadth):
    #titles = driver.find_elements(By.CLASS_NAME, "st--title")  ---  NOT NEEDED FOR RN AT LEAST
    sections = driver.find_elements(By.CLASS_NAME, "st--section-name")
    section_text = [s.text.strip() for s in sections]
    for section in section_text:
        try:
            if breadth not in all_courses[section]:
                all_courses[section].append(breadth)
        except:
            all_courses[section] = [breadth]

def paginate():
    active_li = driver.find_element(By.XPATH,
                                    "//li[contains(@class, 'pager__item') and contains(@class, 'is-active')]")
    next_li = active_li.find_element(By.XPATH, "following-sibling::li[1]")
    next_link = next_li.find_element(By.TAG_NAME, "a")
    driver.execute_script("arguments[0].scrollIntoView();", next_link)
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "loading-popup")))
    next_link.click()
    # Wait for the new page to load
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "loading-popup")))
    time.sleep(1)

def show_all_filters(section_label):
    section_label = section_label.replace(" ", "").lower()
    legend = driver.find_element(By.ID, f"block-{section_label}")
    driver.execute_script("arguments[0].scrollIntoView();", legend)
    show_more = legend.find_elements(By.XPATH, ".//*[contains(text(), 'Show more')]")
    driver.execute_script("arguments[0].scrollIntoView();", show_more[0])
    show_more[0].click()
    time.sleep(0.1)

def run(requirements):
    requirements_list_name = requirements.lower.replace(" ", "_")
    requirements_list = globals()[requirements_list_name]

    for req in requirements_list:
        count = 0
        print (req)
        show_all_filters(requirements)
        click_filter(req)
        while True:
            try:
                extract_courses(req)
                paginate()
                count += 1
                print (count)
            except:
                #print (all_courses)
                break
        show_all_filters(requirements)
        click_filter(req)


all_courses = {}

def main():
    driver.get("https://classes.berkeley.edu")
    click_filter("Fall 2025")

    #'''
    for breadth in breadth_requirements:
        count = 0
        print (breadth)
        show_all_filters("Breadth Requirements")
        click_filter(breadth)
        while True:
            try:
                extract_courses(breadth)
                paginate()
                count += 1
                print (count)
            except:
                print (all_courses)
                break
        show_all_filters("Breadth Requirements")
        click_filter(breadth)
    #'''

    for gen in general_requirements:
        count = 0
        print (gen)
        show_all_filters("General Requirements")
        click_filter(gen)
        while True:
            try:
                extract_courses(gen)
                paginate()
                count += 1
                print(count)
            except:
                break
        show_all_filters("General Requirements")
        click_filter(gen)

    print ("Course Search Complete")

    all_courses_file_path = "/Users/ronitmathur/Desktop/Ronit/Coding/Berkeley_Course_Search/All_Courses"
    with open(all_courses_file_path, 'wb') as file:
        pickle.dump(all_courses, file)

    #print ([i, all_courses[i]] for i in all_courses.keys() if len(all_courses[i]) > 1)
    #print ("\n"*3)
    first_filter_courses = {i: all_courses[i] for i in all_courses if len(all_courses[i]) > 1}
    '''for i in list([*all_courses]):
        if len(all_courses[i]) > 1:
            first_filter_courses.append(all_courses[i])
            #print (i, "|", all_courses[i])'''
    first_filter_courses_file_path = "/first_filter_courses"
    with open(first_filter_courses_file_path, 'wb') as file:
        pickle.dump(first_filter_courses, file)

    second_filter_courses = [course for course in first_filter_courses if any(req in breadth_requirements for _, req in course) and any(req in general_requirements for _, req in course)]
    '''for i in range(len(first_filter_courses)):
        for _, j in first_filter_courses[i]:
            breadth_check = False
            gen_check = False
            if not breadth_check and j in breadth_requirements:
                breadth_check = True
            elif not gen_check and j in general_requirements:
                gen_check = True
        if not (breadth_check and gen_check):
            first_filter_courses.remove(first_filter_courses[i])
        else:
            i += 1'''
    second_filter_courses_file_path = "/second_filter_courses"
    with open(second_filter_courses_file_path, 'wb') as file:
        pickle.dump(first_filter_courses, file)

if __name__ == "__main__":
    main()