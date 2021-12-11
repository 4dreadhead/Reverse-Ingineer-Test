
Оба задания реализованы на языке Python 3.9, виртуальное окружение для проекта прилагается. Для работы необходим браузер Chrome.

Для запуска запустить в виртуальном окружении соответствующие файлы:

Первое тестовое задание - Task 1.py (Результат в table.csv)

Второе тестовое задание - Task 2.py (Результат в output.txt)

***** АКТИВАЦИЯ И ЗАПУСК В КОНСОЛИ(Для WINDOWS) *****

1) cd "Полный путь до папки с проектом"
2)venv\scripts\activate.bat
3)venv\scripts\python.exe "Task 1.py"
4)venv\scripts\python.exe "Task 2.py"

-------------------------------------------

# nseindia

-------------------------------------------

Задание: 1. Парсер данных через селениум на сайте https://www.nseindia.com/

Алгоритм:

1. Зайти на https://www.nseindia.com

2. Навестись (hover) на MARKET DATA

3. Кликнуть на Pre-Open Market

4. Спарсить данные Final Price по всем позициям на странице и вывести их в csv файл. Имя; цена

После этого сымитировать небольшой пользовательский сценарий использования сайта. Здесь по своему желанию, но как пример:

1. Зайти на главную страницу

2. Пролистать вниз до графика

3. Выбрать график "NIFTY BANK"

4. Нажать “View all” под "TOP 5 STOCKS - NIFTY BANK"

5. Выбрать в селекторе “NIFTY ALPHA 50”

6. Пролистать таблицу до конца

-------------------------------------------

Реализация: 

Используется selenium, bs4, браузер Chrome

Полученный результат в файле table.csv

-------------------------------------------

-------------------------------------------

# twitter

-------------------------------------------

Задание: Парсинг последних твитов Elon Musk.
Используя HTTP-запрос получить список последних 10 твитов Илона Маска .
Вывести в лог только текст (если есть) последних твитов и для каждого поста вывести ссылки на аккаунты авторов 3х последних комментариев.Действия должны повторять пользовательский путь, официальное API Twitter в задаче не должно быть использовано.

-------------------------------------------

Реализация:

Используется selenium, bs4, браузер Chrome

Полученный результат в файле output.txt

-------------------------------------------

Что делает скрипт:

   С помощью selenium открывает браузер Chrome, скроллит посты, кликая по каждому из них, сохраняет оттуда нужную информацию. Скрипт достаточно схож с сеансом обычного пользователя.
   
-------------------------------------------

Почему не get запросы?

   При реализации проекта через html запросы возникла проблема, в ответе на get запрос получал лишь обрывок кода страницы, в которой не было необходимой информации.
Думаю, это связано с тем, что на сайте присустствуют скрипты, которые динамически подгружают страницу по мере необходимости.
Так же, при прослушивании сети в браузере, я пытался найти, какие дополнительные запросы отправляются с сайта, чтобы вписать их в скрипт, но найти мне их не удалось.
Поэтому я реализовал парсер не через html запрос, а через selenium.webdriwer, имитируя работу с сайтом через браузер.
Алгоритм прокручивает страницу и улавливает посты как объекты, за тем переходит по ним, откуда берется необходимая информация.

--------------------------------------------

!!! Возможны пропуски (комментарии из main.py):

        # Цикл for i in range(10) и дальнейшее использование i в качестве индекса объекта списка постов
        # - костыль для упрощения кода, правильнее перебирать все прогруженные страницы с самого начала,
        # чтобы не допустить пропуска постов, поскольку если твит ушел далеко вверх по ленте,
        # при обновлении страницы он не подгружается

        # На момент написания такой метод работал для 10 постов без пропусков, были пропуски, начиная с 12
        # При необходимости написания программы для большего числа постов, этот метод использовать нельзя,
        # и пришлось бы перебирать все прогруженные посты полностью
