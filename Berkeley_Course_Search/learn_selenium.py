'''# Launch browser and open Google
drv = webdriver.Chrome()
drv.get("https://www.google.com")
# Search "GeeksforGeeks"
box = drv.find_element(By.NAME, "q")
box.send_keys("GeeksforGeeks", Keys.RETURN)
# Wait and close browser
time.sleep(20)
drv.quit()'''

'''driver.get("https://www.geeksforgeeks.org/")
element = driver.find_element(By.LINK_TEXT, "Courses")
action = ActionChains(driver)
action.click(on_element=element)
action.perform()
time.sleep(10)
driver.quit()'''

'''driver.get("https://classes.berkeley.edu/")
element = driver.find_element(By.CLASS_NAME, "facet-item__value")
action = ActionChains(driver)
action.click(on_element=element)
action.perform()
time.sleep(10)
driver.quit()'''

'''fall_2025_btn = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.XPATH, "//span[@class='facet-item__value' and text()='Fall 2025']"))
)
WebDriverWait(driver, 15).until(
    EC.invisibility_of_element_located((By.CLASS_NAME, "loading-popup"))
)
fall_2025_btn.click()
time.sleep(10)'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import NoSuchElementException, TimeoutException

breadth_requirements = ["Arts & Literature", "Biological Science", "Historical Studies", "International Studies", "Philosophy & Values", "Physical Science", "Reading and Composition B", "Social & Behavioral Sciences"]
general_requirements = ["2nd Half of Reading & Composition", "American Cultures", "American History", "American Institutions"]
#changed & to &amp; because that is what it looks like in html code -- change back to & if code doesn't work due to this

driver = webdriver.Chrome()
#action = ActionChains(driver)
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
    for section in sections:
        try:
            all_courses[section].append(breadth)
        except:
            all_courses[section] = [breadth]
    #for title, section in zip(titles, sections):
        #print(f"{title.text} | {section.text}")
    #time.sleep(5)

def paginate(driver, wait):
    active_li = driver.find_element(By.XPATH,
                                    "//li[contains(@class, 'pager__item') and contains(@class, 'is-active')]")

    # Try to find the next sibling li (next page)
    next_li = active_li.find_element(By.XPATH, "following-sibling::li[1]")

    # Inside that li, get the <a> tag and click
    next_link = next_li.find_element(By.TAG_NAME, "a")

    # Scroll and click
    driver.execute_script("arguments[0].scrollIntoView();", next_link)
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "loading-popup")))
    next_link.click()

    # Wait for the new page to load
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "loading-popup")))
    time.sleep(1)

all_courses = {}

driver.get("https://classes.berkeley.edu")
click_filter(driver, wait, "Fall 2025")
for breadth in breadth_requirements:
    count = 0
    print (breadth)
    #wait.until(EC.presence_of_element_located((By.CLASS_NAME, "filters-panel")))
    click_filter(driver, wait, breadth)
    while True:
        try:
            extract_courses(driver, breadth)
            paginate(driver, wait)
            count += 1
            print (count)
        #except (NoSuchElementException, TimeoutException):
        except:
            break
    click_filter(driver, wait, breadth)
    #print (breadth)
for gen in general_requirements:
    count = 0
    print (gen)
    #wait.until(EC.presence_of_element_located((By.CLASS_NAME, "filters-panel")))
    click_filter(driver, wait, gen)
    while True:
        try:
            extract_courses(driver, gen)
            paginate(driver, wait)
            count += 1
            print(count)
        except (NoSuchElementException, TimeoutException):
            break
    click_filter(driver, wait, gen)
    #print (gen)
#print ([i, all_courses[i]] for i in all_courses.keys() if len(all_courses[i]) > 1)
print ("\n"*3)
for i in list([*all_courses]):
    if len(all_courses[i]) > 1:
        print (i, "|", all_courses[i])

#class="facet-item__value" NO
#class = "st--title" --> for all the actual course names on the page
#class="st--section-name" --> for all the actual course numbers on the page