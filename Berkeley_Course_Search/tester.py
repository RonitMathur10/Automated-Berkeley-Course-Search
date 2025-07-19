from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import NoSuchElementException, TimeoutException
import pickle

'''
breadth_requirements = ["Arts & Literature", "Biological Science", "Historical Studies", "International Studies", "Philosophy & Values", "Physical Science", "Reading and Composition B", "Social & Behavioral Sciences"]
general_requirements = ["2nd Half of Reading & Composition", "American Cultures", "American History", "American Institutions"]
#changed & to &amp; because that is what it looks like in html code -- change back to & if code doesn't work due to this

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)

def click_filter(driver, wait, label_text): # can use this for fall 2025 AND breadth and gen requirements??
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
    time.sleep(1)

def show_all_filters(driver, wait, section_label):
    section_label = section_label.replace(" ", "").lower()
    legend = driver.find_element(By.ID, f"block-{section_label}")
    driver.execute_script("arguments[0].scrollIntoView();", legend)
    show_more = legend.find_elements(By.XPATH, ".//*[contains(text(), 'Show more')]")
    driver.execute_script("arguments[0].scrollIntoView();", show_more[0])
    show_more[0].click()
    time.sleep(0.1)

all_courses = {}
driver.get("https://classes.berkeley.edu")

click_filter(driver, wait, "Fall 2025")

breadth = "Biological Science"
count = 0
extract_courses(driver, breadth)
count += 1
print (count)
print (all_courses)

for breadth in breadth_requirements:
    count = 0
    print (breadth)
    show_all_filters(driver, wait, "Breadth Requirements")
    click_filter(driver, wait, breadth)
    while True:
        try:
            extract_courses(driver, breadth)
            paginate(driver, wait)
            count += 1
            print (count)
        except:
            print (all_courses)
            break
    show_all_filters(driver, wait, "Breadth Requirements")
    click_filter(driver, wait, breadth)

for gen in general_requirements:
    count = 0
    print (gen)
    show_all_filters(driver, wait, "General Requirements")
    click_filter(driver, wait, gen)
    while True:
        try:
            extract_courses(driver, gen)
            paginate(driver, wait)
            count += 1
            print(count)
        except:
            break
    show_all_filters(driver, wait, "General Requirements")
    click_filter(driver, wait, gen)

#print ([i, all_courses[i]] for i in all_courses.keys() if len(all_courses[i]) > 1)
print ("\n"*3)
for i in list([*all_courses]):
    if len(all_courses[i]) > 1:
        print (i, "|", all_courses[i])
'''

'''
test_list = {'AFRICAM 5A': ['Arts & Literature'], 'AGRS 10A': ['Arts & Literature'], 'AGRS 17A': ['Arts & Literature'], 'AGRS R44': ['Arts & Literature'], 'AGRS 130M': ['Arts & Literature'], 'AMERSTD 10': ['Arts & Literature'], 'AMERSTD 102': ['Arts & Literature'], 'AMERSTD C152': ['Arts & Literature'], 'ARCH 170A': ['Arts & Literature'], 'ART 8': ['Arts & Literature'], 'ART 12': ['Arts & Literature'], 'ART 13': ['Arts & Literature'], 'ART 14': ['Arts & Literature'], 'ART 15': ['Arts & Literature'], 'ART 21': ['Arts & Literature'], 'ART 26': ['Arts & Literature'], 'ART 102': ['Arts & Literature']}
file_path = '/Users/ronitmathur/Desktop/Ronit/Coding/Berkeley_Course_Search/test_list'
with open(file_path, 'wb') as file:
    pickle.dump(test_list, file)

with open(file_path, 'rb') as file:
    test_list_read = pickle.load(file)
print (test_list_read)
'''
with open('/Users/ronitmathur/Desktop/Ronit/Coding/Berkeley_Course_Search/All_Courses', 'rb') as file:
    all_courses = pickle.load(file)
#print (all_courses)

breadth_requirements = ["Arts & Literature", "Biological Science", "Historical Studies", "International Studies", "Philosophy & Values", "Physical Science", "Reading and Composition B", "Social & Behavioral Sciences"]
general_requirements = ["2nd Half of Reading & Composition", "American Cultures", "American History", "American Institutions"]

#first_filter_courses = {i: all_courses[i] for i in all_courses if len(all_courses[i]) > 1}
#first_filter_courses = "/Users/ronitmathur/Desktop/Ronit/Coding/Berkeley_Course_Search/first_filter_courses"
#with open(first_filter_courses, 'wb') as file:
    #pickle.dump(first_filter_courses, file)
with open("/first_filter_courses", 'rb') as file:
    first_filter_courses = pickle.load(file)
#print (first_filter_courses)

#second_filter_courses = [course for course in first_filter_courses if any(req in breadth_requirements for _, req in course[1]) and any(req in general_requirements for _, req in course[1])]
second_filter_courses = {course: req_list for course, req_list in first_filter_courses.items() if any(req in breadth_requirements for req in req_list) and any(req in general_requirements for req in req_list)}
print (second_filter_courses)
second_filter_courses_file_path = "/second_filter_courses"
with open(second_filter_courses_file_path, 'wb') as file:
    pickle.dump(second_filter_courses, file)