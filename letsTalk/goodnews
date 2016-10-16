def handle_good_news_intent(session):

    speech_output, session_attributes = get_rand_news()
    while article_sentimentality(session_attributes['title'],session_attributes['more'])!=u'pos':
        speech_output, session_attributes = get_rand_news()

    should_end_session = False
    card_title = "Good News"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def get_rand_news():
    card_title = "Rand News"

    json_obj = urllib2.urlopen('https://newsapi.org/v1/sources?sortBy=popular&apiKey=ef3e0724395d48ae8fef22341dc76428')
    data = json.load(json_obj)
    rand = random.randrange(0,len(data['sources']))
    source = data['sources'][rand]['name'].lower().replace(' ','-').replace('(','').replace(')','')
    print(source)
    json_obj = urllib2.urlopen("https://newsapi.org/v1/articles?source="+source+"&apiKey=ef3e0724395d48ae8fef22341dc76428")
    articles = json.load(json_obj)
    rand = random.randrange(0,len(articles['articles']))
    response = "Here is some good news :)"+ articles['articles'][rand]['title']
    session_attributes = {'title': articles['articles'][rand]['title'],
                            'more': articles['articles'][rand]['description']}
    return response, session_attributes