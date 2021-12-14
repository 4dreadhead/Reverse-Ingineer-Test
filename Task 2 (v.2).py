import requests
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
            dict__[f"Commentator {i+1}"] = "https://twitter.com/" + self.commentators[i]
        dict_['Commentators'] = dict__

        return dict_


def variables_for_url(param, post):
    """
    Возвращает словарь, который содержит параметры url для запросов
    :param param: 'TweetDetail' или 'UserTweets', в зависимости от параметра возвращает нужный словарь
    :param post: пост, либо None
    :return: возвращает нужный словарь
    """
    if param == 'TweetDetail':
        # Для TweetDetail
        variables = {
            "focalTweetId": f"{post.url}",
            "referrer": "profile",
            "with_rux_injections": False,
            "includePromotedContent": True,
            "withCommunity": True,
            "withQuickPromoteEligibilityTweetFields": True,
            "withTweetQuoteCount": True,
            "withBirdwatchNotes": False,
            "withSuperFollowsUserFields": True,
            "withBirdwatchPivots": False,
            "withDownvotePerspective": False,
            "withReactionsMetadata": False,
            "withReactionsPerspective": False,
            "withSuperFollowsTweetFields": True,
            "withVoice": True,
            "withV2Timeline": False
        }
    else:
        # Для UserTweets
        variables = {
            "userId": "44196397",
            "count": 20,
            "withTweetQuoteCount": True,
            "includePromotedContent": True,
            "withQuickPromoteEligibilityTweetFields": True,
            "withSuperFollowsUserFields": True,
            "withBirdwatchPivots": False,
            "withDownvotePerspective": False,
            "withReactionsMetadata": False,
            "withReactionsPerspective": False,
            "withSuperFollowsTweetFields": True,
            "withVoice": True,
            "withV2Timeline": False
        }
    return variables


def get_headers_and_session_cookies():
    """
    Делаем запрос на твиттер для установления куков, сохраняем значение для идентификации 'x-guest-token'
    :return: Возвращает необходимые для идентификации сессии заголовки
    """
    # Делаем запрос, куки автоматически записываются в response.cookies
    link = 'https://twitter.com/elonmusk'
    response = SESSION.get(link)
    print(f"status: {response}, request: get({link})")

    headers = {
        # Заголовок для авторизации, одинаковый для всех сеансов, поэтому оставил его как константу
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I'
                         '8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    }

    # Делаем запрос для получения токена 'x-guest-token'
    link = 'https://api.twitter.com/1.1/guest/activate.json'
    response = SESSION.post(link, headers=headers)
    print(f"status: {response}, request: post({link})")

    # Добавляем в заголовки необходимый токен
    dict_ = json.loads(response.content)
    headers['x-guest-token'] = dict_['guest_token']

    return headers


def get_response(param, post=None):
    """
    Выполняет get запрос, возвращает ответ
    :param param: параметр имеет 1 из 2 значений: 'UserTweets' или 'TweetDetail', чтобы выполнить необходимый запрос
    :param post: если param имеет значение 'TweetDetail', передается твит
    :return: возвращает ответ в json формате
    """
    # Получаем значения параметров url для запросов
    variables = variables_for_url(param, post)
    variables_encoded = json.dumps(variables)

    # По значению param и variables_encoded генерируем url
    if param == 'UserTweets':
        link = 'https://twitter.com/i/api/graphql/mTSXUZHwc3vjzSE94Xsttg/UserTweets?variables=' + variables_encoded
    else:
        link = 'https://twitter.com/i/api/graphql/MwoNOssr8CR7CxUWbBQO9w/TweetDetail?variables=' + variables_encoded

    # Делаем запрос, выводим в терминал статус
    json_ = SESSION.get(link, headers=HEADERS)
    print(f"status: {json_}, request: get({link})")
    return json_


def main_page_parser():
    """
    Основная функция, выполняется парсинг главной страницы и каждого из постов
    """
    # Преобразуем данные json в объект Python "dict"
    json_ = get_response('UserTweets')
    parsed_string = json.loads(json_.content)
    post_list = parsed_string['data']['user']['result']['timeline']['timeline']['instructions'][0]['entries']

    posts = []

    # По заданным ключам добираемся до номера поста, и заодно забираем текст поста
    max_posts = 10
    for index in range(max_posts):
        link = str(post_list[index]['sortIndex'])
        if 'itemContent' in post_list[index]['content']:
            if 'full_text' in post_list[index]['content']['itemContent']['tweet_results']['result']['legacy']:
                text = post_list[index]['content']['itemContent']['tweet_results']['result']['legacy']['full_text']
                text = " ".join(x for x in text.split() if not x.startswith("https://t.co"))
            else:
                text = ''
            posts.append(Post(link, text, ['', '', '']))
        else:
            max_posts += 1

    # Запускаем парсер для получения ссылок на комментаторов
    tweet_parser(posts)


def tweet_parser(posts):
    """
    Парсит каждый твит и сохраняет ссылки на комментаторов
    :param posts: Список твитов
    """
    # Начинаем перебор постов
    for post in posts:
        commentators = []
        index = 0
        index_ = 0

        # Делаем запрос, получаем ответ
        json_ = get_response('TweetDetail', post)

        # Переводим в dict
        parsed_string = json.loads(json_.text)
        post_list = parsed_string["data"]["threaded_conversation_with_injections"]["instructions"][0]["entries"]

        # Забираем первые 3 ссылки на комментаторов, ищем их по ключам
        while len(commentators) < 3:
            commentator_link = 'elonmusk'
            if 'items' in post_list[index]["content"]:
                if 'tweet_results' not in post_list[index]["content"]["items"][index_]['item']["itemContent"]:
                    index_ += 1
                    if index_ == len(post_list[index]["content"]["items"]):
                        index += 1
                        index_ = 0
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
            count += 1
            dict_[f"Post {count}"] = post.save_to_dict()
            dict_[f"Post {count}"]["Link"] = "https://twitter.com/elonmusk/status/" + post.url
        file.write(json.dumps(dict_, indent=4))


if __name__ == '__main__':
    # Создаем экземпляр класса Session, который при выполнении запросов сохраняет cookie
    SESSION = requests.Session()
    # Определяем заголовки и сохраняем cookie
    HEADERS = get_headers_and_session_cookies()
    # Запускаем процесс
    try:
        main_page_parser()
    except Exception as ex:
        print(ex)
