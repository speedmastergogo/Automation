"""
Selenium script: Find duplicate titles while scrolling down (using DOWN arrow key)
and take a screenshot the first time each duplicate title is found — including its
position on the page (index + first-seen position).

FIXES IN THIS VERSION
----------------------
1. POSITION TRACKING: each title's first-seen index (its order of appearance on the
   page) and vertical pixel position are recorded. When a duplicate shows up, the
   report tells you both where it was first seen and where the repeat is.
2. NO DUPLICATE SCREENSHOTS: a title is only ever screenshotted ONCE, the first time
   it's detected as a duplicate, even if it stays on screen across several scrolls.
3. KEEPS SCROLLING PROPERLY: instead of stopping just because no *new duplicate* was
   found in a pass (which stopped the script almost immediately), it now tracks the
   page's scrollHeight. It keeps scrolling as long as new titles are appearing OR the
   page is still growing (lazy-loaded content), and only stops once both plateau.
4. Sends several DOWN key presses per cycle (one press only scrolls ~1 line, which is
   too slow to reach lazy-loaded content in reasonable time).

CUSTOMIZE BEFORE RUNNING
-------------------------
- URL
- Xpath (the XPath that matches each "title" element on the page)
"""

import os
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


# ----------------------------- CONFIG ----------------------------- #
URL = "https://www.ubuy.co.in/search/?q=shoes"
Xpath = "//h2[contains(@class, 'product-title m-0 mt-2')]"
SCREENSHOT_DIR = "screenshots"
REPORT_FILE = "duplicate_titles_report.txt"
MAX_SCROLLS = 500                 # hard safety cap
NO_NEW_CONTENT_LIMIT = 8          # stop only after this many cycles with NO new titles AND NO page growth
KEY_PRESSES_PER_CYCLE = 15        # how many DOWN presses per cycle (1 press ~= 1 line)
SCROLL_PAUSE = 1.0                # seconds to wait after each batch of key presses
HEADLESS = False
# --------------------------------------------------------------------- #


def make_driver():
    options = Options()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=options)
    return driver


def safe_filename(text: str, maxlen: int = 60) -> str:
    keep = "".join(c if c.isalnum() or c in (" ", "-", "_") else "_" for c in text)
    return keep.strip().replace(" ", "_")[:maxlen]


def get_current_titles_with_position(driver):
    """
    Return list of (title_text, index_on_page, y_pixel_position) for every
    title element currently in the DOM, in document order.
    """
    results = []
    try:
        elements = driver.find_elements(By.XPATH, Xpath)
        for idx, el in enumerate(elements):
            try:
                text = el.text.strip()
                if not text:
                    continue
                y_pos = el.location.get("y", -1)
                results.append((text, idx, y_pos))
            except StaleElementReferenceException:
                continue
    except NoSuchElementException:
        pass
    return results


def get_scroll_height(driver):
    try:
        return driver.execute_script("return document.body.scrollHeight;")
    except Exception:
        return -1


def main():
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    driver = make_driver()
    driver.get(URL)
    time.sleep(2)

    # title -> (first_index, first_y_position)   -- where we FIRST saw this title
    seen_titles = {}
    # titles we've already screenshotted as duplicates, so we never do it twice
    screenshotted_titles = set()

    no_new_content_count = 0
    last_scroll_height = get_scroll_height(driver)

    body = driver.find_element(By.TAG_NAME, "body")
    body.click()

    with open(REPORT_FILE, "w", encoding="utf-8") as report:
        report.write(f"Duplicate Title Report - {datetime.now()}\n")
        report.write(f"URL: {URL}\n{'-' * 60}\n")

        for cycle in range(1, MAX_SCROLLS + 1):
            current_titles = get_current_titles_with_position(driver)
            found_new_title_this_cycle = False

            for title, idx, y_pos in current_titles:
                if title in seen_titles:
                    # It's a duplicate. Only screenshot / log it once.
                    if title not in screenshotted_titles:
                        screenshotted_titles.add(title)
                        first_idx, first_y = seen_titles[title]

                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"{safe_filename(title)}_{timestamp}.png"
                        filepath = os.path.join(SCREENSHOT_DIR, filename)
                        driver.save_screenshot(filepath)

                        line = (
                            f"[DUPLICATE] '{title}'\n"
                            f"    First seen  -> position #{first_idx} on page, y={first_y}px\n"
                            f"    Duplicate at-> position #{idx} on page, y={y_pos}px\n"
                            f"    Screenshot  -> {filepath}\n"
                        )
                        print(line)
                        report.write(line)
                        report.flush()
                else:
                    seen_titles[title] = (idx, y_pos)
                    found_new_title_this_cycle = True

            current_scroll_height = get_scroll_height(driver)
            page_grew = current_scroll_height > last_scroll_height
            last_scroll_height = current_scroll_height

            if not found_new_title_this_cycle and not page_grew:
                no_new_content_count += 1
            else:
                no_new_content_count = 0

            if no_new_content_count >= NO_NEW_CONTENT_LIMIT:
                print("No new titles and page stopped growing — reached the bottom. Stopping.")
                break

            # Scroll down with several DOWN key presses so we actually move enough
            # to reach lazy-loaded content within a reasonable time.
            for _ in range(KEY_PRESSES_PER_CYCLE):
                body.send_keys(Keys.DOWN)
            time.sleep(SCROLL_PAUSE)

        report.write(f"\nTotal unique titles seen: {len(seen_titles)}\n")
        report.write(f"Total duplicate titles found: {len(screenshotted_titles)}\n")

    print(f"\nDone. {len(screenshotted_titles)} duplicate title(s) found.")
    print(f"Report saved to: {REPORT_FILE}")
    print(f"Screenshots saved to: {SCREENSHOT_DIR}/")

    driver.quit()


if __name__ == "__main__":
    main()