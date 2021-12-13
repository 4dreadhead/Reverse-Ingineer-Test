from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json


class Post:
    """
    Класс поста для удобства
    """
    def __init__(self, text, commentators):
        self.text = text
        self.commentators = commentators

    def __str__(self):
        return f"\n-= Post =-\n{self.text}\n" \
               f"-= ==== =-\n-= Commentators =-:\n" + "\n".join(str(item) for item in self.commentators) + \
               "\n-= ==== =-\n"

    def save_to_dict(self):
        dict__ = {}
        dict_ = {'Text': self.text}

        for i in range(len(self.commentators)):
            dict__[f"Commentator {i}"] = self.commentators[i]
        dict_['Commentators'] = dict__

        return dict_


class Page:
    """
    Класс для хранения сохраненной страницы поста
    """
    def __init__(self, code):
        self.code = code


def save_data(browser):
    """
    Сохраняет html-код поста
    :param browser: наш браузер
    :return: возвращает сохраненную страницу
    """
    page = Page(BeautifulSoup(browser.page_source, "html.parser"))
    return page


def get_data(url, pages_count):
    """
    Основной блок управления браузером
    :param url: ссылка на страницу
    """
    _service = Service(r'chromedriver.exe')
    _options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(service=_service, options=_options)
    browser.maximize_window()
    posts_rendered = []
    pages = []
    post_urls = []
    y_old = 500

    try:
        browser.get(url=url)
        sleep(2.5)
        html = browser.find_element("tag name", 'html')

        # Основной цикл
        for i in range(pages_count):
            posts = browser.find_elements("xpath", "//div[@class='css-1dbjc4n r-k4xj1c r-18u37iz r-1wtj0ep']")

            # Перебор всех прогруженных постов для проверки, были ли они уже обработаны
            soup = BeautifulSoup(browser.page_source, "html.parser")
            posts_soup = soup.find_all("article", {"data-testid": "tweet"})
            counter = 0
            for post in posts_soup:
                post_href = post.find("a", {"class": "css-4rbku5 css-18t94o4 css-901oao r-9ilb82 r-1loqt21 r-1q142lx "
                                                     "r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0"},
                                      href=True)
                if post_href['href'] not in post_urls:
                    post_urls.append(post_href['href'])
                    break
                else:
                    counter += 1

            # Улавливаем координаты следующего для обработки поста
            y = posts[counter].location.get('y')

            # Пролистываем страницу вниз с помощью клавиши
            # Эмпирическим путем определил, что одно нажатие клавиши вниз пролистывает страницу вниз
            # Примерно на 37 пикселей
            for _ in range((y - y_old) // 37):
                html.send_keys(Keys.DOWN)
                sleep(0.15)
            y_old = y
            sleep(0.25)

            # Переходим к посту
            posts[counter].click()
            sleep(2)

            # Сохраняем пост и выходим обратно в ленту
            pages.append(save_data(browser))
            browser.execute_script("window.history.go(-1)")
            sleep(0.25)

            html = browser.find_element("tag name", 'html')
            sleep(0.25)

    except Exception as ex:
        print(ex)

    finally:
        # Все успешно сохраненные посты выводятся в файл output.txt
        dict_ = {}
        count = 0
        for item in pages:
            posts_rendered.append(parser(item))
        with open("output.txt", "w") as file:
            for post in posts_rendered:
                count += 1
                dict_[f"Post {count}"] = post.save_to_dict()
                dict_[f"Post {count}"]["Link"] = "https://twitter.com" + post_urls[count-1]

            file.write(json.dumps(dict_, indent=4))

        browser.close()
        browser.quit()


def parser(page):
    """
    Ищет необходимые данные на странице
    :param page: сохранненная страница
    :return: Возвращает текст поста и ссылки на первых трех комментаторов
    """
    text = ""

    user_profiles = []
    right_text = ""
    soup = page.code.find_all("article", {"data-testid": "tweet"})

    # Сохраняем ссылки комментаторов и текст поста
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


if __name__ == '__main__':
    PAGES_COUNT = 20
    get_data("https://twitter.com/elonmusk", PAGES_COUNT)
