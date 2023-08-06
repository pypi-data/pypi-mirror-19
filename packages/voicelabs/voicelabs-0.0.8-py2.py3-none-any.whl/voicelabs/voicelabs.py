'''
Created on Sep 18, 2016

@author: sridharn
'''
import json
import requests
import hashlib
import logging

class VoiceInsights:
    
    appToken = ''
    session = None

        
    def sendVLEvent(self, payload):
        url = "https://api.voicelabs.co/events"
        params = { "auth_token" : payload['app_token']}
        data_json = json.dumps(payload)
        headers = {'Content-type': 'application/json'}
        response = requests.post(url, params=params, data=data_json, headers=headers, timeout=1)
        return response


    def md5(self, input_string):
        return hashlib.md5(input_string).hexdigest()
        
            
    def __init__(self):
        pass
        
    def initialize(self, appToken, session):
        
        if session is None or appToken is None or len(appToken.strip()) == 0:
            logging.error("ERROR: cannot initialize VoiceInsights SDK. either session or appToken are 'None'")
            return
        
        if session.get('user',{}).has_key('userId') is False:
            logging.error("ERROR: cannot initialize VoiceInsights SDK. User Id is not found in session")
            
        if session.has_key('sessionId') is False:
            logging.error("ERROR: cannot initialize VoiceInsights SDK. User Id is not found in session")
            
        
        if self.session is not None and self.session['sessionId'] == session['sessionId']:
            logging.error("ERROR: Redundant Initialization. A session has already been started with sessionId: %s", session['sessionId'])
            return

        self.appToken = appToken
        self.session = session
        p =  {}
        p['app_token'] = self.appToken
        p['user_hashed_id'] = self.md5(self.session['user']['userId'])
        p['session_id'] = self.session['sessionId'];
        p['event_type'] = 'INITIALIZE'
        p['data'] = None
        resp = self.sendVLEvent(p)
        return resp

    def track(self, intent_name, intent_request, response):
        
        if self.session is None:
            logging.error("ERROR: Voice Insights has not been initialized. Initalize() method need to have been invoked before tracking")
            return
              
        p =  {}
        p['app_token'] = self.appToken
        p['user_hashed_id'] = self.md5(self.session['user']['userId'])
        p['session_id'] = self.session['sessionId'];
        p['event_type'] = 'SPEECH'
        p['intent'] = intent_name
        p['data'] = {}
        
        if intent_request is not None and intent_request.get('intent',{}).has_key('slots'):
            p['data']['metadata'] = intent_request['intent']['slots']
        else:
            p['data']['metadata'] = None
        
        if isinstance(response, basestring):
            p['data']['speech'] = response

        elif response is not None and response.has_key('response') and response.get('response', {}).has_key('outputSpeech') is True:

            speechObj = response['response']['outputSpeech']

            if speechObj.has_key('type'):
                
                if speechObj['type'] == 'SSML':
                    p['data']['speech'] = response['response']['outputSpeech']['ssml']

                elif speechObj['type'] == 'PlainText':
                    p['data']['speech'] = response['response']['outputSpeech']['text']

                else:
                    logging.error("ERROR: passed a response object with an unknown Type") 

            else:
                logging.error("ERROR: passed a response object thats not an Alexa response") 

        else:
            p['data']['speech'] = None

        resp = self.sendVLEvent(p)             
        return resp
    