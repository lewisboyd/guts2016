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

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == "HowAreYouIntent":
        session_attributes = {}
        return build_response(session_attributes, build_speechlet_response(
        "HowAreYouCard", "I am a robot", "", False))

    if intent_name == "NewsIntent":
        return handle_news_intent(session)

    if intent_name == "TellMeMoreIntent":
        return handle_tell_me_more_intent(session)

    if intent_name == "AnoArtSiteIntent":
        return handle_another_article_site_intent(session)

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

def handle_news_intent(session):
    return True

def handle_tell_me_more_intent(session):
    return True

def handle_another_article_site_intent(session):
    return True


# This handles when the program in the wrong for the given intent
def handle_incorrect_state(session):
    return True