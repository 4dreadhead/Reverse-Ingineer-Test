import requests
from bs4 import BeautifulSoup
import json


class Post:
    """
    Класс поста для удобства
    """
    def __init__(self, url, text, commentators):
        self.url = url
        self.text = text
        self.commentators = commentators

    def __str__(self):
        return f"\n-= Post =-\n{self.text}\n" \
               f"-= ==== =-\n-= Commentators =-:\n" + "\n".join(str(item) for item in self.commentators) + \
               f"\n-= ==== =-\n Link: {self.url}\n"

    def save_to_dict(self):
        """
        Преобразует данные в формат словаря
        :return: словарь
        """
        dict__ = {}
        dict_ = {'Text': self.text}

        for i in range(len(self.commentators)):
            dict__[f"Commentator {i}"] = "https://twitter.com/" + self.commentators[i]
        dict_['Commentators'] = dict__

        return dict_


def get_one_post(post, headers):
    """
    Выполняет get запрос на твиттер по номеру поста'
    При успешном запросе в консоли будет выведет response 200
    :param post: Пост
    :param headers: Заголовки запроса
    :return: возвращает ответ в json формате
    """
    json_ = requests.get(f"https://twitter.com/i/api/graphql/WCPfjCbV22zfq-_pPrAGeQ/TweetDetail?variables=%7B%22"
                         f"focalTweetId%22%3A%22{str(post.url)}%22%2C%22referrer%22%3A%22profile%22%2C%22with_"
                         f"rux_injections%22%3Afalse%2C%22includePromotedContent%22%3Atrue%2C%22withCommunity%"
                         f"22%3Atrue%2C%22withQuickPromoteEligibilityTweetFields%22%3Atrue%2C%22withTweetQuote"
                         f"Count%22%3Atrue%2C%22withBirdwatchNotes%22%3Afalse%2C%22withSuperFollowsUserFields%"
                         f"22%3Atrue%2C%22withUserResults%22%3Atrue%2C%22withBirdwatchPivots%22%3Afalse%2C%22w"
                         f"ithDownvotePerspective%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22with"
                         f"ReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Atrue%2C%22with"
                         f"Voice%22%3Atrue%2C%22withV2Timeline%22%3Afalse%7D", headers=headers)
    print(json_)
    return json_


def get_all_posts(headers):
    """
    Выполняет get запрос для получения списка постов
    :param headers: Заголовки запроса
    :return: возвращает ответ в json формате
    """
    jsn_ = requests.get("https://twitter.com/i/api/graphql/mTSXUZHwc3vjzSE94Xsttg/UserTweets?variables=%7B%22"
                        "userId%22%3A%2244196397%22%2C%22count%22%3A20%2C%22withTweetQuoteCount%22%3Atrue%2C%22"
                        "includePromotedContent%22%3Atrue%2C%22withQuickPromoteEligibilityTweetFields%22%3Atrue%2C%22wi"
                        "thSuperFollowsUserFields%22%3Atrue%2C%22withUserResults%22%3Atrue%2C%22withBirdwatchPivots%22%"
                        "3Afalse%2C%22withDownvotePerspective%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22"
                        "withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Atrue%2C%22withVoice%"
                        "22%3Atrue%2C%22withV2Timeline%22%3Afalse%7D", headers=headers)
    print(jsn_)
    return jsn_


def main_page_parser(headers):
    """
    Основная функция, выполняется парсинг главной страницы и каждого из постов
    :param headers: Заголовки запроса
    """
    # Преобразуем данные json в объект Python "dict"
    json_ = get_all_posts(headers)
    parsed_string = json.loads(json_.content)
    post_list = parsed_string['data']['user']['result']['timeline']['timeline']['instructions'][0]['entries']

    posts = []

    # По заданным ключам добираемся до номера поста, и заодно забираем текст поста (Ключи подбирал в файле page.html)
    # page.html - сохраненный ответ в json формате get запроса на сервер
    for index in range(10):
        link = str(post_list[index]['sortIndex'])
        if 'full_text' in post_list[index]['content']['itemContent']['tweet_results']['result']['legacy']:
            text = post_list[index]['content']['itemContent']['tweet_results']['result']['legacy']['full_text']
            text = " ".join(x for x in text.split() if not x.startswith("https://t.co"))
        else:
            text = ''
        posts.append(Post(link, text, ['', '', '']))

    # Запускаем парсер для получения ссылок на комментаторов
    tweet_parser(posts, headers)


def tweet_parser(posts, headers):
    """
    Парсит каждый твит и сохраняет ссылки на комментаторов
    :param posts: Список твитов
    :param headers: Заголовки запроса
    """
    # Начинаем перебор постов
    for post in posts:
        commentators = []
        index = 0
        index_ = 0

        # Делаем запрос, получаем ответ
        json_ = get_one_post(post, headers)

        # Переводим в dict
        parsed_string = json.loads(json_.text)
        post_list = parsed_string["data"]["threaded_conversation_with_injections"]["instructions"][0]["entries"]

        # Забираем первые 3 ссылки на комментаторов, ищем их по ключам (Ключи брал из tweet.html)
        while len(commentators) < 3:
            commentator_link = 'elonmusk'
            if 'items' in post_list[index]["content"]:
                if 'tweet_results' not in post_list[index]["content"]["items"][index_]['item']["itemContent"]:
                    index_ += 1
                    continue
                commentator_link = \
                post_list[index]["content"]["items"][index_]['item']["itemContent"]["tweet_results"]["result"]["core"][
                    'user_results']['result']['legacy']['screen_name']
                index_ = 0
            if commentator_link != 'elonmusk':
                commentators.append(commentator_link)
            index += 1
        post.commentators = commentators

    # Осталось сохранить все в файл
    save_data_in_file(posts)


def save_data_in_file(posts):
    """
    Сохраняет посты в json формате в файл output_v2.txt
    :param posts: Посты
    """
    dict_ = {}
    count = 0
    with open("output_v2.txt", "w") as file:
        for post in posts:
            print(post)
            count += 1
            dict_[f"Post {count}"] = post.save_to_dict()
            dict_[f"Post {count}"]["Link"] = "https://twitter.com/status/" + post.url
        file.write(json.dumps(dict_, indent=4))


if __name__ == '__main__':
    # Заголовки
    #
    # Для того, чтобы не вылетала ошибка 403, в браузере взял заголовки сессии
    # - cookie
    # - x-csrf-token
    # - x-guest-token
    # - authorization
    #
    # Без них ответа не дождаться, если переставали работать эти куки и токены, я чистил кукри браузера и вводил сюда
    # новые значения заголовков, как бы имитируя свою новую сессию с браузера
    HEADERS = {
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'x-csrf-token': '65bda309a86b7c2ba599add2b884eecb',
        'x-guest-token': '1470341330631073794',
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
        'cookie': 'guest_id_marketing=v1%3A163879710358226793; guest_id_ads=v1%3A163879710358226793; personalization_id="v1_ScVokRvGE0+FFJ41DSInmA=="; guest_id=v1%3A163879710358226793; external_referer=padhuUp37zjgzgv1mFWxJ12Ozwit7owX|0|ziZgIoZIK4nlMKUVLq9KcnBFms0d9TqBqrE%2FyjvSFlFJR45yIlYF%2Bw%3D%3D; _ga=GA1.2.2039911237.1638797106; ct0=65bda309a86b7c2ba599add2b884eecb; gt=1470341330631073794; _gid=GA1.2.554430793.1639391668; _gat=1'
    }

    # Запускаем процесс
    try:
        main_page_parser(HEADERS)
    except Exception as ex:
        print(ex)
