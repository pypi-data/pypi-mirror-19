from skitai.saddle import Saddle
import skitai

app = Saddle (__name__)

app.debug = True
app.use_reloader = True
app.jinja_overlay ()

@app.route ("/echo")
def echo (was, message):
	if "websocket_init" in was.env:
		#return was.wsconfig (skitai.WS_SIMPLE, 60, skitai.WS_MSG_JSON)			
		return was.wsconfig (skitai.WS_SIMPLE, 60)
	return message

@app.route ("/talk")
def talk (was, name = "Hans Roh"):
	if "websocket_init" in was.env:
		return was.wsconfig (skitai.WS_DEDICATE, 60)		
	
	ws = was.env ["websocket"]
	while 1:
		messages = ws.getswait (10)
		if messages is None:
			break	
		for m in messages:
			if m.lower () == "bye":
				ws.send ("Bye, have a nice day." + m)
				ws.close ()
				break
			elif m.lower () == "hello":
				ws.send ("Hello, " + name)				
			else:	
				ws.send ("You Said:" + m)

@app.route ("/chat")
def chat (was, message, client_id, room_id, event = None):
	if "websocket_init" in was.env:
		return was.wsconfig (skitai.WS_GROUPCHAT, 60)
	if event == skitai.WS_EVT_ENTER:
		return "Client %s has entered" % client_id
	if event == skitai.WS_EVT_EXIT:
		return "Client %s has leaved" % client_id
	return "Client %s Said: %s" % (client_id, message)

@app.route ("/multi")
def chat (was, room_id):
	if "websocket_init" in was.env:
		was.env ["websocket_init"] = (skitai.WS_MULTICAST, 60)
		return ""
	ws = was.env ["websocket"]	
	while 1:
		messages = ws.getswait (10)
		if messages is None:
			break	
		for client_id, m in messages:
			ws.sendall ("Client %d Said: %s" % (client_id, m))
			
@app.route ("/")
def websocket (was, mode = "echo"):
	if mode == "talk":
		mode += "?name=Hans"
	elif mode == "chat":	
		mode += "?room_id=1"
	elif mode == "multi":	
		mode += "?room_id=2"
	return was.render ("websocket.html", path = mode)
	
if __name__ == "__main__":
	import skitai
	skitai.run (
		address = "0.0.0.0",
		port = 5000,
		mount = ("/websocket", app)
	)
	