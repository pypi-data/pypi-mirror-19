
if __name__ == "__main__":
	import skitai
	import os
	
	skitai.run (
		mount = [
			("/", os.path.join (os.getcwd (), os.path.join (os.path.split (__file__)[0], "app.py"))),
			("/", 'static')
		],
		certfile = r"C:\skitaid\etc\certifications\example.pem",
		keyfile = r"C:\skitaid\etc\certifications\example.key",
		passphrase = "fatalbug"
	)
