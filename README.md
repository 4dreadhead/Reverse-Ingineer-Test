# twitter

-------------------------------------------

Задание: Парсинг последних твитов Elon Musk.
Используя HTTP-запрос получить список последних 10 твитов Илона Маска .
Вывести в лог только текст (если есть) последних твитов и для каждого поста вывести ссылки на аккаунты авторов 3х последних комментариев.Действия должны повторять пользовательский путь, официальное API Twitter в задаче не должно быть использовано.

-------------------------------------------

Реализация:

Для запуска скрипта активировать виртуальное окружение и запустить файл main.py

Используется selenium, браузер Chrome

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
