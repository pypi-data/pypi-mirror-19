--------------------
--------------------

# Install the package

you can install the package locally in the current folder by using the following command:

#from test PIP repo
pip install -t ./ -i https://testpypi.python.org/pypi VoiceInsights

#from main public PIP repo
pip install -t ./ VoiceInsights

--------------------
--------------------

## SDK usage:


from voicelabs import  VoiceInsights

appToken = '<YOUR APP TOKEN>'   
vi = VoiceInsights()

def on_session_started(session_started_request, session):
    # Called when the session starts """   
    vi.initialize(appToken, session)

def on_intent(intent_request, session):
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    response = None
    #Logic to populate response goes here

    #invoke SDK track method like follows
    vi.track(intent_name, intent_request, response)

    return response


--------------------
--------------------


