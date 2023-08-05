# analytics-python-sdk
Voice insights analytics sdk for Python for Alexa skill platform

## instructions to build and distribute

### setup: create a file called .pypirc in your user home folder (~). Put the following contents in it:
```
[distutils]
index-servers =
  pypi
  pypitest

[pypi]
repository=https://pypi.python.org/pypi
username=voicelabs

[pypitest]
repository=https://testpypi.python.org/pypi
username=voicelabs
```

### cleanup the build artifacts (optional). Cleanup not needed if it wasnt done before on the machine.
```
rm -r dist/*

rm -r build/*

rm -r VoiceInsights.egg-info/*
```

### build 
```
python setup.py sdist

python setup.py bdist_wheel
```
### distribute

```
#for publishing to sandbox PIP repo
twine register dist/VoiceInsights-0.0.1-py2.py3-none-any.whl -r pypitest
twine upload dist/* -r pypitest

#for publishing to sandbox PIP repo
twine register dist/VoiceInsights-0.0.1-py2.py3-none-any.whl -r pypi
twine upload dist/* -r pypi
```

when prompted for a password use: V0icelab5

Login to the urls provided above in .pypirc file to check the package has been correctly exported. 

--------------------

## To test the uploaded package

you can install the package locally in the current folder by using the following command:
```
#from test PIP repo
pip install -t ./ -i https://testpypi.python.org/pypi VoiceInsights

#from main public PIP repo
pip install -t ./ -i https://pypi.python.org/pypi VoiceInsights
```

--------------------

## SDK usage:

```python
from VoiceInsights import VoiceInsights

appToken = '450f1ca5-da5b-3877-b6ad-389ba3f49f5d'   
vi = VoiceInsights()

def on_session_started(session_started_request, session):
    """ Called when the session starts """   
    vi.initialize(appToken, session)

def on_intent(intent_request, session):
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    response = None
    #Logic to populate response goes here

    #invoke SDK track method like follows
    vi.track(intent_name, intent_request, response)

    return response

```



