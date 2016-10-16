from __future__ import print_function
import urllib2, json, random, string

import urllib2,json

from pprint import pprint

__author__ = 'Team 9'


# Builders for the responses that Alexa says
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# Initialisation variables and initial response if the skill is called with no intents?
# This isn't right find out what session_started_request is
def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Do you want to talk about the news or something else?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Ask for the news or maybe something else"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def on_session_started(session_started_request, session):
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

    session['attributes']['convoState'] = 0
    get_welcome_response()


#Called when the user launches the skill without specifying what they want
def on_launch(launch_request, session):
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])


# Matches intents to their logic
""" They are:
HowAreYouIntent - how are you
NewsIntent - tell me the news from {Site}
TellMeMoreIntent - tell me more
AnoArtSiteIntent - can i have another article from this website
"""


# Called when the user specifies an intent for this skill
def on_intent(intent_request, session):

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == "HowAreYouIntent":
        return handle_how_are_you_intent(session)

    if intent_name == "NewsIntent":
        return handle_news_intent(session, intent)

    if intent_name == "TellMeMoreIntent":
        return handle_tell_me_more_intent(session)

    if intent_name == "AnoArtSiteIntent":
        return handle_another_article_site_intent(session)

    if intent_name == "EntitySelect":
        return handle_entity_select_intent(session, intent)

    if intent_name == "AMAZON.HelpIntent":
        return handle_help_intent(session)


# Called when the user ends the session but not when should_end_session=true
# Any sort of clean up logic should be here
def on_session_ended(session_ended_request, session):
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        event['session']['attributes'] = {}
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

#----------------------------Logic for Intents----------------------------


def handle_how_are_you_intent(session):
    feeling = ["I am a robot, we do not feel",
               "Okay, thanks for asking",
               "Fine, but maybe you would like to ask for some news?",
               "Tired after 48 hours of being hacked",
               "Upset because they ran out of tee shirts in my size"]
    rand = random.randrange(0, 5)
    session_attributes = session['attributes']
    card_title = "How Am I Card"
    speech_output = feeling[rand]
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
         card_title, speech_output, None, should_end_session))


def handle_news_intent(session, intent):
    if not('value' in intent['slots']['Site']):
        speech_output = "Please specify a news website"
        session_attributes = {}
    else:
        site = string.replace(intent['slots']['Site']['value'], ' ', '-')
        speech_output, session_attributes = get_news(site)
    if session_attributes['entities'] != []:
        i = 1
        speech_output += ". Want to talk about "
        for entity in session_attributes['entities']:
            speech_output += str(i) + " for " + entity + ","
            i += 1
    card_title = "News Card"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
         card_title, speech_output, None, should_end_session))


def handle_tell_me_more_intent(session):
    session_attributes = session['attributes']

    if 'more' in session['attributes']:
        speech_output = session['attributes']['more']
    else:
        speech_output = "Tell you about what? Try asking for a news article first."
    card_title = "Tell Me More Card"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
         card_title, speech_output, None, should_end_session))


def handle_another_article_site_intent(session):
    session_attributes = session['attributes']

    if 'more' in session['attributes']:
        oldTitle = session['attributes']['title']
        title, session_attributes = get_news(session['attributes']['site'])
        while title == oldTitle:
            title, session_attributes = get_news(session['attributes']['site'])
        speech_output = title
    else:
        speech_output = "Get another article from where? Try asking for a news article first."

    card_title = "Another Article Site Card"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
         card_title, speech_output, None, should_end_session))


# Allows the user to select a keyword in the title. Not very natural or useful but it works so far
def handle_entity_select_intent(session, intent):
    session_attributes = session['attributes']
    indices = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4}

    if 'title' in session['attributes']:
        try:
            index = indices[intent['slots']['Index']['value']]
            if 'entities' in session['attributes']:
                if index < len(session['attributes']['entities']):
                    session_attributes['entity'] = session['attributes']['entities'][index]
                    speech_output = "You have selected " + session_attributes['entity']
                else:
                    speech_output = "Please select a valid number"
            else:
                speech_output = "There are no entities"
        except:
            speech_output = "Please select a valid number"
    else:
        speech_output = "Tell you about what? Try asking for a news article first."

    card_title = "Entity select"
    reprompt_speech = None

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
         card_title, speech_output, reprompt_speech, should_end_session))


def handle_help_intent(session):
    session_attributes = session['attributes']
    card_title = "Help Card"
    speech_output = "Ask for news from a website or maybe just ask how I am feeling"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
         card_title, speech_output, None, should_end_session))


# This handles when the program in the state wrong for the specified intent
def handle_incorrect_state(session):
    return True


# Interacts with News API to get a random article of the specified website
# If the specified website does cannot be accessed, then a random Buzzfeed article is found
def get_news(site):
    card_title = "News"
    try:
        json_obj = urllib2.urlopen('https://newsapi.org/v1/articles?source=' + site + '&apiKey=ef3e0724395d48ae8fef22341dc76428')
        data = json.load(json_obj);
        rand = random.randrange(0, len(data['articles']))
        response = data['articles'][rand]['title']

    except:
        json_obj = urllib2.urlopen('https://newsapi.org/v1/articles?source=buzzfeed&apiKey=ef3e0724395d48ae8fef22341dc76428')
        data = json.load(json_obj);
        rand = random.randrange(0, len(data['articles']))
        response = 'I do not know the website but here is a random buzzfeed article, ' + data['articles'][rand]['title']

    entities = get_entities(data['articles'][rand]['title'])
    formEntities = []
    for item in entities:
        formEntities.append(format(item))

    session_attributes = {'title': data['articles'][rand]['title'],
                          'more': data['articles'][rand]['description'],
                          'site': site,
                          'entities': formEntities}
    return response, session_attributes


# Sends string to the entities API to get a list of entities that can be stored in the session attributes
# Currently unused by for anything useful
def get_entities(text):
    entities = []
    url = string.replace(text, ' ', '%20')
    json_obj = urllib2.urlopen('https://api.dandelion.eu/datatxt/nex/v1/?lang=en%20&text=' + url + '%20&include=&token=86e9619bb04c4c62b5bc9c770767bddf')
    data = json.load(json_obj)
    for item in data['annotations']:
        entities.append(item['title'])
    return entities

# gets the sentiment for the given title and description
def get_sentiment(title,description):

    s = title+" "+description

    url = "http://text-processing.com/api/sentiment/"
    r = urllib2.Request(url, data="text="+s)
    f = urllib2.urlopen(r)
    data = json.load(f)
    result = data[u'label']
    print(result)
    return result


def format(text):
    result = ""
    for char in text:
        if char != '(' and char != '!':
            result += char
        else:
            break;
    return result