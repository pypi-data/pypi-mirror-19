from skitai.saddle import Saddle

app = Saddle (__name__)
app.debug = True
app.use_reloader = True

Tokens = {
	"12345678-1234-123456": ("hansroh", ["user", "admin"], 0)
}

@app.startup
def startup (wasc):
	wasc.handler.set_token_storage (Tokens)
	
@app.route ("/")
def index (was):
	return "<h1>API Gateway</h1>"
