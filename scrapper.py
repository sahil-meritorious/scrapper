import csv
import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def scrape_urls_with_cookies(
    urls,
    cookies,
    xpaths,
    output_csv="output.csv",
    headless=False,
    timeout=20,
):

    options = webdriver.ChromeOptions()

    if headless:
        options.add_argument("--headless=new")

    options.add_argument("--incognito")

    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    results = []

    try:
        driver.get(urls[0])

        time.sleep(random.uniform(2, 5))
        for cookie in cookies:
            cookie = cookie.copy()
            for key in (
                "sameSite",
                "hostOnly",
                "storeId",
                "session",
                "id",
            ):
                cookie.pop(key, None)

            try:
                driver.add_cookie(cookie)
            except Exception as e:
                print(f"Cookie skipped ({cookie.get('name')}): {e}")

        driver.refresh()

        time.sleep(random.uniform(2, 5))

        for url in urls:

            print(f"\nProcessing {url}")

            driver.get(url)

            # Random delay (1–10 sec)
            time.sleep(random.uniform(1, 10))

            row = {"URL": url}

            for column_name, xpath in xpaths.items():

                # Random delay before each lookup
                time.sleep(random.uniform(1, 10))

                try:
                    element = WebDriverWait(driver, timeout).until(
                        EC.presence_of_element_located((By.XPATH, xpath))
                    )

                    row[column_name] = element.text.strip()

                except TimeoutException:
                    row[column_name] = "NOT FOUND"

                except Exception as e:
                    row[column_name] = f"ERROR: {e}"

            results.append(row)

        # Save CSV
        fieldnames = ["URL"] + list(xpaths.keys())

        with open(output_csv, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        print(f"\nSaved {len(results)} rows to {output_csv}")

        return results

    finally:
        driver.quit()

urls = ["https://www.linkedin.com/in/sahilsoni2272/", "https://www.linkedin.com/in/dr-dur-muhammad-pathan-b84455ab/"]
xpaths = {
    "Name": "//*[@id='com.linkedin.sdui.profile.card.refACoAABdhnVQBRPAaANtzwZkxtjszspC5rwxaKvATopcard']/div/section/div/div/div[2]/div[1]/div[1]/div/div[1]/div/div/h2",
    "Headline": "/html/body/div[1]/div[2]/div[2]/div[2]/div/main/div/div/section/div/div/div[1]/div/section/div/div/div[2]/div[1]/div[1]/div/p[1]"
}

cookies = [
    {
        "name": "li_at",
        "value": "AQEDAUt9sfMDGkeSAAABn4h8MaMAAAGfrIi1o1YASeTAY4obXzLu38WaoaHMpcuPikBbe_93fgotyvZCJNPULtdya7MXwlaYO5b2oXJvRKM1gzWeUmsweIZ0FZfrwLrDpEMOCofkhzTFGmOUaTQOY924",
        "domain": "www.linkedin.com",
        "path": "/"
    }
]

results = scrape_urls_with_cookies(
    urls=urls,
    cookies=cookies,
    xpaths=xpaths,
    output_csv="/home/ss/Downloads/products.csv",
)