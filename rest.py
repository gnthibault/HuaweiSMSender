import flask
import requests
import xml.etree.ElementTree as ET
import time


app = flask.Flask(__name__)
ip = "192.168.8.1" #Dongle ip

@app.route('/', methods=['GET'])
def home():
	return ''

# A route to return all of the available entries in our catalog.
@app.route('/api/v1/sendsms', methods=['GET'])
def api_all():
	number  = flask.request.args.get('number', None)
	content  = flask.request.args.get('content', None)
	app.logger.info(f"Number was {number} and content was {content}")

	#Get token
	r = requests.get(f"http://{ip}/api/webserver/token")
	root = ET.fromstring(r.content)
	token = root[0].text

	#Send sms
	now_date = time.strftime("%Y-%m-%d %H:%M:%S")
	headers = { "__RequestVerificationToken": token, "Content-Type": "text/xml" }
	data = f"<request><Index>-1</Index><Phones><Phone>{number}</Phone></Phones><Sca/><Content>{content}</Content><Length>{float(len(content))}</Length><Reserved>1</Reserved><Date>{now_date}</Date></request>"
	app.logger.info(f"data is {data}")
	r = requests.post(f"http://{ip}/api/sms/send-sms", data=data, headers=headers)

	resp = flask.jsonify(success=True)
	return resp

app.run(debug=True,
	host='0.0.0.0')
