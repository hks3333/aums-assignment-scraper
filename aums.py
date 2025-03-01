from playwright.sync_api import sync_playwright
import json
import os

USERNAME = ""
PASSWORD = ""
LOGIN_URL = "https://aumsam.amrita.edu/cas/login?service=https%3A%2F%2Faumsam.amrita.edu%2Faums%2FJsp%2FCore_Common%2Findex.jsp"

def login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=True to run in the background
        page = browser.new_page()

        page.goto(LOGIN_URL)

        page.fill("input#username", USERNAME) 
        page.fill("input#password", PASSWORD) 

        page.click("input[type='submit']") 

        page.wait_for_load_state("networkidle")

        print("Log in success")

        if not os.path.exists('links.json'):
            frame1 = page.frame_locator("#maincontentframe")
            frame2 = frame1.frame_locator("#Iframe1")
            frame3 = frame2.frame_locator("#sakaiframeId")

            links = frame3.locator("a.Mrphs-sitesNav__dropdown").all()
            flag = 0
            for link in links:
                link.click(force=True)
                page.wait_for_timeout(1000)
                if flag:
                    link.click(force=True)
                    page.wait_for_timeout(2500)
                flag = 1

            assignment_links = frame3.locator("a[title='Assignments']").all()
            href_list = [link.get_attribute("href") for link in assignment_links]
            
            print(href_list)

            with open('links.json', 'w') as f:
                json.dump(href_list, f)
        else:
            with open('links.json', 'r') as f:
                href_list = json.load(f)

        texts = []
        for href in href_list:
            page.goto(href)
            page.wait_for_load_state("domcontentloaded")
            try:
                page.wait_for_selector('a[name="asnActionLink"]', timeout=1000)
                assignments = page.locator('a[name="asnActionLink"]').all()
                for assignment in assignments:
                    texts.append(assignment.inner_text())
            except:
                continue 

        print(texts)


        page.pause()
        browser.close()

login()
