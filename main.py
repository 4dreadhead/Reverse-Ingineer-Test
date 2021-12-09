from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys


class Post:
    """
    Класс для удобства вывода поста в строковый формат
    """
    def __init__(self, text, commentators):
        self.text = text
        self.commentators = commentators

    def __str__(self):
        return f"\n-= Post =-\n{self.text}\n" \
               f"-= ==== =-\n-= Comments =-:\n" + "\n".join(str(item) for item in self.commentators) + \
               "\n-= ==== =-\n"


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


def get_data(url):
    """
    Основной блок управления браузером
    :param url: ссылка на страницу
    """
    _service = Service(r'chromedriver.exe')
    _options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(service=_service, options=_options)
    posts = []
    pages = []
    y_old = 500

    try:
        browser.get(url=url)
        sleep(2.5)
        html = browser.find_element("tag name", 'html')

        # Цикл for i in range(10) и дальнейшее использование i в качестве индекса объекта списка постов
        # - костыль для упрощения кода, правильнее перебирать все прогруженные страницы с самого начала,
        # чтобы не допустить пропуска постов, поскольку если твит ушел далеко вверх по ленте,
        # при обновлении страницы он не подгружается

        # На момент написания такой метод работал для 10 постов без пропусков, были пропуски, начиная с 12
        # При необходимости написания программы для большего числа постов, этот метод использовать нельзя,
        # и пришлось бы перебирать все прогруженные посты полностью

        for i in range(10):
            posts = browser.find_elements("xpath", "//div[@class='css-1dbjc4n r-k4xj1c r-18u37iz r-1wtj0ep']")
            print(posts)

            y = posts[i].location.get('y')

            # Эмпирическим путем определил, что одно нажатие клавиши вниз пролистывает страницу вниз
            # Примерно на 37 пикселей
            for _ in range((y - y_old) // 37):
                html.send_keys(Keys.DOWN)
                sleep(0.2)
            print(f"Пост {i}, {y}, {y_old}")
            y_old = y

            sleep(1)

            posts[i].click()

            sleep(2.5)

            pages.append(save_data(browser))
            browser.execute_script("window.history.go(-1)")

            sleep(0.5)

            html = browser.find_element("tag name", 'html')

            sleep(0.5)

    except Exception as ex:
        print(ex)
        print("Произошла ошибка: пост находится за пределами экрана/миссклик по посту")

    finally:
        for item in pages:
            posts.append(parser(item))
        with open("output.txt", "w") as file:
            for post in posts:
                file.write(str(post))

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
    get_data("https://twitter.com/elonmusk")
