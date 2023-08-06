from skitai.saddle import Saddle
import skitai

app = Saddle (__name__)

app.debug = True
app.use_reloader = True
app.jinja_overlay ()

@app.route ("/echo")
def echo (was, message = ""):
	if "websocket_init" in was.env:
		was.env ["websocket_init"] = (skitai.WEBSOCKET_REQDATA, 60, "message")
		return ""
	return "ECHO:" + message

@app.route ("/talk")
def talk (was, name = "Hans Roh"):
	if "websocket_init" in was.env:
		was.env ["websocket_init"] = (skitai.WEBSOCKET_DEDICATE, 60, None)
		return ""
	
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
def chat (was, roomid):
	if "websocket_init" in was.env:
		was.env ["websocket_init"] = (skitai.WEBSOCKET_MULTICAST, 60, "roomid")
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
		mode += "?roomid=1"
	return was.render ("websocket.html", path = mode)
	
if __name__ == "__main__":
	import skitai
	skitai.run (
		address = "0.0.0.0",
		port = 5000,
		mount = ("/websocket", app)
	)
	