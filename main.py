from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys


class Post:
    def __init__(self, text, commentators):
        self.text = text
        self.commentators = commentators

    def __str__(self):
        return f"-= Пост =-\n{self.text}\n" \
               f"-= ==== =-\n-= Коментаторы =-:\n" + "\n".join(str(item) for item in self.commentators) + \
               "\n-= ==== =-\n"


class Page:
    def __init__(self, code):
        self.code = code


def save_data(browser):
    page = Page(BeautifulSoup(browser.page_source, "html.parser"))
    return page


def get_data(url):
    _service = Service(r'chromedriver.exe')
    _options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(service=_service, options=_options)
    posts = []
    pages = []
    action = webdriver.common.action_chains.ActionChains(browser)
    y_old = 500

    try:
        browser.get(url=url)
        sleep(2.5)
        html = browser.find_element("tag name", 'html')
        with open("selenium.html", "w", encoding="utf-8") as file:
            file.write(BeautifulSoup(browser.page_source, "lxml").prettify())

        for i in range(10):
            posts = browser.find_elements("xpath", "//div[@class='css-1dbjc4n r-1igl3o0 r-qklmqi r-1adg3ll r-1ny4l3l']")

            y = posts[i].location.get('y')

            for _ in range((y - y_old) // 36):
                html.send_keys(Keys.DOWN)
                sleep(0.2)

            y_old = y
            posts = browser.find_elements("xpath", "//div[@class='css-1dbjc4n r-1igl3o0 r-qklmqi r-1adg3ll r-1ny4l3l']")

            action.move_to_element_with_offset(posts[i], 1, 60)
            sleep(0.5)

            action.click()
            action.perform()

            sleep(2.5)

            pages.append(save_data(browser))
            browser.execute_script("window.history.go(-1)")

            sleep(0.5)

            html = browser.find_element("tag name", 'html')

            sleep(0.5)

        for item in pages:
            posts.append(parser(item))

        posts = posts[1:]
        for post in posts:
            print(str(post))

    except Exception as ex:
        print(ex)

    finally:
        browser.close()
        browser.quit()


def parser(page):
    text = ""

    user_profiles = []
    soup = page.code.find_all("article", {"data-testid": "tweet"})

    for item in soup:
        href = item.find("a", href=True)
        if str(href['href']) != '/elonmusk':
            user_profiles.append("https://twitter.com" + href['href'])
        else:
            text = item.find_all("span", {"class": "css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"})
            if len(text) >= 10:
                right_text = text

    post_text = right_text[-10].text
    user_profiles = user_profiles[:3]

    return Post(post_text, user_profiles)


get_data("https://twitter.com/elonmusk")


