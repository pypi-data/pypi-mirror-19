import json
from voicelabs_assistant import VoiceInsights

token = '97455a0a-a920-3d1b-abcb-36dba02c5141'

intentName = "TEST_INTENT"
agentTTS = "wasssaaaup!"
request = '{"user":{"user_id":"r6CbYTY+8MrzSgEWAi5yWtBGe0xU7Pn5KKEnlLK3YVo="},"conversation":{"conversation_id":"1484179642211","type":1},"inputs":[{"intent":"assistant.intent.action.MAIN","raw_inputs":[{"input_type":2,"query":"talk to silly name maker"}],"arguments":[]}]}'


vi = VoiceInsights(token)
x = vi.track(intentName, json.loads(request), agentTTS)
if x.json()['msg'] == 'success':
  print 'test case#1 passed'
else:
  print 'test case#1 failed'

x = vi.track(None, None, None)
if x is None:
  print 'test case#2 passed'
else:
  print 'test case#2 failed'

x = vi.track(None, json.loads(request), agentTTS)
if x is None:
  print 'test case#3 passed'
else:
  print 'test case#3 failed'

x = vi.track(intentName, json.loads(request), None)
if x.json()['msg'] == 'success':
  print 'test case#4 passed'
else:
  print 'test case#4 failed'

x = vi.track(None, json.loads(request), None)
if x is None:
  print 'test case#5 passed'
else:
  print 'test case#5 failed'

#wihtout session_id
request = '{"user":{"user_id":"r6CbYTY+8MrzSgEWAi5yWtBGe0xU7Pn5KKEnlLK3YVo="},"conversation":{"type":1},"inputs":[{"intent":"assistant.intent.action.MAIN","raw_inputs":[{"input_type":2,"query":"talk to silly name maker"}],"arguments":[]}]}'
x = vi.track(intentName, json.loads(request), agentTTS)
if x is None:
  print 'test case#6 passed'
else:
  print 'test case#6 failed'

