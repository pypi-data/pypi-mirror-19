from skitai.saddle import Saddle
import time

app = Saddle (__name__)
app.debug = True
app.use_reloader = True

class Tokens:
	def __init__ (self):
		self.tokens = {
			"12345678-1234-123456": ("hansroh", ["user", "admin"], 0)
		}
		
	def get (self, request, callback):
		username, roles, expires = self.tokens.get (request.token)
		if expires and expires < time.time ():
			self.tokens.popitem (request.token)
			callback (request)
		callback (request, username, roles)

	
@app.startup
def startup (wasc):
	wasc.handler.set_token_storage (Tokens ())
	
@app.route ("/")
def index (was):
	return "<h1>Skitai App Engine: API Gateway</h1>"
