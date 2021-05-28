import requests
import json
from operator import itemgetter
from datetime import date
from flask import Flask, jsonify, request

today = date.today()
app=Flask(__name__)

def listOut():

	header= {
		"Accept": "application/json, text/plain, */*",
		"Accept-Encoding": "gzip, deflate, br",
		"Accept-Language": "en-GB",
		"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJlNjI0OGI1YS1mMDI5LTQ2OWEtOTI2OC1kMDA4NzU3YzQyYTkiLCJ1c2VyX2lkIjoiZTYyNDhiNWEtZjAyOS00NjlhLTkyNjgtZDAwODc1N2M0MmE5IiwidXNlcl90eXBlIjoiQkVORUZJQ0lBUlkiLCJtb2JpbGVfbnVtYmVyIjo5ODA5ODY0Mjc1LCJiZW5lZmljaWFyeV9yZWZlcmVuY2VfaWQiOjc1OTExNDUzNTA1MDMwLCJzZWNyZXRfa2V5IjoiYjVjYWIxNjctNzk3Ny00ZGYxLTgwMjctYTYzYWExNDRmMDRlIiwic291cmNlIjoiY293aW4iLCJ1YSI6Ik1vemlsbGEvNS4wIChYMTE7IExpbnV4IHg4Nl82NDsgcnY6ODguMCkgR2Vja28vMjAxMDAxMDEgRmlyZWZveC84OC4wIiwiZGF0ZV9tb2RpZmllZCI6IjIwMjEtMDUtMjhUMTE6Mzc6MTEuOTk2WiIsImlhdCI6MTYyMjIwMTgzMSwiZXhwIjoxNjIyMjAyNzMxfQ.JJ_TMYQ95taOFbJ3lRN3RPe_sTXqiNBUzIgoxyAJbOU",
		"Connection": "keep-alive",
		"Host": "cdn-api.co-vin.in",
		"Origin": "https://selfregistration.cowin.gov.in",
		"Referer": "https://selfregistration.cowin.gov.in/",
		"TE": "Trailers",
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"
	}
	s =requests.session()
	output=s.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=307&date="+today.strftime("%d-%m-%Y"),headers=header).text
	output=json.loads(output)
	centers=output["centers"]

	mainList=[]
	for i in centers:
		tempList=[i["center_id"],i["name"],i["pincode"],i["fee_type"]]
		# print(len(i["sessions"]))
		aviDoses=0
		for b in i["sessions"]:
			aviDoses=aviDoses+b["available_capacity"]
			tempList.append([b["date"],b["available_capacity"],b["min_age_limit"],b["vaccine"],b["available_capacity_dose1"],b["available_capacity_dose2"]])
		tempList.append(aviDoses)
		mainList.append(tempList)
	# print(mainList)
	# sorted_list = sorted(mainList, key=itemgetter(1))
	# print(sorted_list)
	def myFunc(e):
		return e[-1]
	mainList.sort(key=myFunc,reverse=True)
	# print(mainList)
	return mainList

@app.route('/', methods = ['GET', 'POST'])
def home():
	if(request.method == 'GET'):
		data = listOut()
		return (jsonify({'data': data}))


if __name__ == "__main__":#check wether the ___name__ == __main__ conforming only devoloper can debug the code... if this command is not here anyone can access and debug the code..
    app.run()