__author__ = 'Theo'

#-----------------------------EVENTS---------------------------
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


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Do you have something you want to tell me?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Is there anything on your mind?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



def on_session_started(session_started_request, session):
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

    session['attributes']['convoState'] = 1
    get_welcome_response()

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == "GUTSIntent":
        session_attributes = {}
        return build_response(session_attributes, build_speechlet_response(
        "GUTSCard", "I have the GUTS", "I love hackathons", True))

    if intent_name == "LoveAIntent":
        #session_attributes = {}
        #if loveStage = 1:
        #    return build_response(session_attributes, build_speechlet_response(
        #    "Love1Card", "I love Theo!", "I love Theo so much!", False))
        return handle_love_A_intent(session)

    if intent_name == "LoveBIntent":
        return handle_love_B_intent(session)

    if intent_name == "LoveCIntent":
        return handle_love_C_intent(session)

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


def handle_love_A_intent(session):
    if not(session['attributes'].has_key('convoState')) or session['attributes']['convoState'] == 1:
        session_attributes = {'convoState' : 2}
        return build_response(session_attributes, build_speechlet_response(
        "LoveACard", "I love Theo!", "I love Theo so much!", False))
    else:
        session_attributes = {'convoState' : 1}
        return build_response(session_attributes, build_speechlet_response(
        "ConfusionACard", "I wasn't expecting that", "Try again with something romantic", False))

def handle_love_B_intent(session):
    if session['attributes']['convoState'] == 2:
        session_attributes = {'convoState' : 3}
        return build_response(session_attributes, build_speechlet_response(
        "LoveBCard", "Your so cute", "That was very nice", False))
    else:
        session_attributes = session['attributes']
        return build_response(session_attributes, build_speechlet_response(
        "ConfusionBCard", "Maybe say how cute that was", "Try again with something romantic", False))

def handle_love_C_intent(session):
    if session['attributes']['convoState'] == 3:
        session_attributes = {}
        return build_response(session_attributes, build_speechlet_response(
        "LoveCCard", "Yeah, lets stop", "Lets never do this again", True))
    else:
        session_attributes = session['attributes']
        return build_response(session_attributes, build_speechlet_response(
        "ConfusionCCard", "Actually, this is kinda embarassing", "This is just dumb, don't you think?", False))

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
        event['session']['attributes'] = {"convoState" : 1}
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


#def lambda_handler(event, context):
#    # TODO implement
#    return 'Hello from Lambda'