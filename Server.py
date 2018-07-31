from flask import Flask, redirect
from Classes.DB import *

app = Flask(__name__)
redirectURL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" #change this as needed

@app.route("/<string:key>")
def getPayload(key):
	#fetch the payload from the db
	payload = Get_Payload(key)
	if payload is None:
		return redirect(redirectURL, code=302)
	#check the number of times the payload has been fetched does not exceed the number allowed
	if payload['access_count'] < payload['allowed_access_count']:
		#return the payload
		with open(payload['file_path']) as f:
			payload_string = f.read()
		#increment the number of reads before returning the file
		Increment_Access_count(key)
		return payload_string
	else:
		return redirect(redirectURL, code=302)


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80)
