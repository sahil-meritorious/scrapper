from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
)
import csv
import time


PROFILE_XPATH = "//a[contains(@href,'/in/')]"

def get_profile_url(driver, element, timeout=20):
    """
    Click a profile, capture its URL, then return to the search page.
    """

    search_url = driver.current_url
    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        element
    )

    driver.execute_script("arguments[0].click();", element)

    WebDriverWait(driver, timeout).until(
        lambda d: d.current_url != search_url
    )

    profile_url = driver.current_url

    driver.back()

    WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.XPATH, PROFILE_XPATH))
    )

    return profile_url


def scrape_profile_urls(driver):
    """
    Extract profile URLs directly from the search results.
    No clicking or navigation required.
    """

    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, PROFILE_XPATH))
    )

    results = driver.find_elements(By.XPATH, PROFILE_XPATH)

    print(f"Found {len(results)} profiles")

    profile_urls = []

    for result in results:
        href = result.get_attribute("href")
        if href and href not in profile_urls:
            print(href)
            profile_urls.append(href)

    return profile_urls


def login_with_cookie(driver, url, cookie_name, cookie_value):
    """
    Login using a single session cookie.

    Parameters
    ----------
    driver : webdriver.Chrome
    url : str
        Base URL of the website.
    cookie_name : str
        Name of the session cookie.
    cookie_value : str
        Value of the session cookie.
    """

    driver.get(url)

    cookie = {
        "name": cookie_name,
        "value": cookie_value,
        "path": "/",
    }

    driver.add_cookie(cookie)

    driver.refresh()

driver = webdriver.Chrome()

login_with_cookie(
    driver,
    url="https://www.linkedin.com/search/results/people/?keywords=RAG&origin=SWITCH_SEARCH_VERTICAL",
    cookie_name="li_at",
    cookie_value="AQEDAUt9sfMDGkeSAAABn4h8MaMAAAGfrIi1o1YASeTAY4obXzLu38WaoaHMpcuPikBbe_93fgotyvZCJNPULtdya7MXwlaYO5b2oXJvRKM1gzWeUmsweIZ0FZfrwLrDpEMOCofkhzTFGmOUaTQOY924",
)
# ---------------------------------
# Assumes 'driver' is already logged in
# and currently on the LinkedIn search page.
# ---------------------------------
print(driver.current_url)
print(driver.title)
profile_urls = scrape_profile_urls(driver)

with open("linkedin_profiles.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["Profile URL"])

    for url in profile_urls:
        writer.writerow([url])

print(f"Saved {len(profile_urls)} profile URLs.")
