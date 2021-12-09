import csv
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from selenium.webdriver.common.keys import Keys
import locale


class Table:
    """
    Класс таблицы с методом сохранения данных в файл csv
    """
    def __init__(self, head, rows):
        self.head = head
        self.rows = rows

    def save_table(self):
        """
        Сохраняет страницу в файл csv
        """
        locale.setlocale(locale.LC_ALL, '')
        delimiter = ';' if locale.localeconv()['decimal_point'] == ',' else ','
        with open("table.csv", "w", encoding="utf-8", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.head, dialect='excel', delimiter=delimiter)
            writer.writeheader()
            for row in self.rows:
                dict_ = {self.head[i]: row[i] for i in range(11)}
                writer.writerow(dict_)


def start(url):
    """
    Основная функция, производятся все действия в браузере
    :param url: ссылка на страницу
    """
    _service = Service(r'chromedriver.exe')
    _options = webdriver.ChromeOptions()

    _options.add_experimental_option("excludeSwitches", ["enable-automation"])
    _options.add_experimental_option('useAutomationExtension', False)

    browser = webdriver.Chrome(service=_service, options=_options)
    browser.maximize_window()

    stealth(browser,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    action = ActionChains(browser)

    try:
        # Открываем сайт в браузере
        browser.get(url)
        sleep(3)

        # Находим кнопку MARKET DATA и наводимся на нее
        elements = browser.find_elements(By.XPATH, "//li[@class='nav-item dropdown  ']")
        action.move_to_element_with_offset(elements[1], 10, 10).perform()
        sleep(1)

        # Находим кнопку Pre Market и кликаем на нее
        elements = browser.find_element(By.XPATH, "//li[@class='nav-item']")
        action.move_to_element_with_offset(elements, 25, 25).click().perform()
        sleep(2)

        # Немного прокручиваем страницу вниз и сохраняем таблицу
        html = browser.find_element("tag name", 'html')
        for _ in range(12):
            html.send_keys(Keys.DOWN)
            sleep(0.2)
        my_table = parser(BeautifulSoup(browser.page_source, "html.parser"))
        my_table.save_table()
        sleep(2)

        # Имитируем пользовательские действия
        human_imitation(browser)

    except Exception as ex:
        print(ex)

    finally:
        browser.close()
        browser.quit()


def parser(page):
    """
    Функция разбивает таблицу поэлементно и сохраняет текст каждой ячейки
    :param page: страница с таблицей
    :return: Возвращает отформатированную таблицу
    """
    text_rows = []
    text_head = []
    table = page.find("table", {"id": "livePreTable"})
    rows = table.find_all("tr")

    # Достаем шапку таблицы
    head = rows[0].find_all("th")
    head.pop(0)
    head.pop()
    for head_element in head:
        text_head.append(head_element.text)

    # Достаем строки
    rows.pop(0)
    for row in rows:
        text_row = []
        elements = row.find_all("td")
        elements.pop(0)
        elements.pop()
        for element in elements:
            text_row.append(element.text)
        text_rows.append(text_row)

    return Table(text_head, text_rows)


def human_imitation(browser):
    """
    Имитирует пользовательские действия
    :param browser: наш браузер
    :return:
    """
    # Возвращаемся на главную страницу
    browser.execute_script("window.history.go(-1)")
    sleep(2)

    # Прокручиваем страницу вниз до графика
    html = browser.find_element("tag name", 'html')
    for _ in range(16):
        html.send_keys(Keys.DOWN)
        sleep(0.2)
    sleep(2)

    # Кликаем на кнопку Stock Watch
    element = browser.find_element(By.XPATH, "//a[@href='/market-data/live-equity-market?symbol=NIFTY 50']")
    element.click()
    sleep(2)

    # Прокручиваем таблицу вниз до таблицы
    html = browser.find_element("tag name", 'html')
    for _ in range(9):
        html.send_keys(Keys.DOWN)
        sleep(0.2)
    sleep(1)

    # Прокручиваем таблицу до конца
    for y in range(525):
        browser.execute_script(f"document.getElementById('equityStockTable').style.top='{str(-y*2)}px';")
    sleep(2)


if __name__ == '__main__':
    start("https://www.nseindia.com/")
