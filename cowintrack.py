import requests
import json
from datetime import date
from flask import Flask, jsonify, request
import time
import csv
from fake_useragent import UserAgent

ua = UserAgent()

today = date.today()
app=Flask(__name__)

# class Config(object):
#     SCHEDULER_API_ENABLED = True

# app.config.from_object(Config())

# scheduler = APScheduler()
# # if you don't wanna use a config, you can set options here:
# # scheduler.api_enabled = True
# scheduler.init_app(app)
# scheduler.start()

districtDict={301:"Alappuzha",307:"Ernakulam",306:"Idukki",297:"Kannur",295:"Kasaragod",298:"Kollam",304:"Kottayam",305:"Kozhikode",302:"Malappuram",308:"Palakkad",300:"Pathanamthitta",296:"Thiruvananthapuram",303:"Thrissur",299:"Wayanad"}

districts = ""
districtCode=0
for hj in districtDict:
    districts=districts+ districtDict[hj] +" : "+ str(hj) +"\n"

stat=False
while not stat:
    districtCode=input(districts +"\n"+ "enter your destrict code and contrinue : ")
    if int(districtCode) in districtDict:
        stat=True
        print("\n \n \n Success goto the given link and check the status \n \n \n")
    else:
        print("\n \n Enter correct code TRY AGAIN \n \n ")


def listOut():
	header= {
		"Accept": "application/json, text/plain, */*",
		"Accept-Encoding": "gzip, deflate, br",
		"Accept-Language": "en-AU,en;q=0.9,en-IN;q=0.8",
		"Authorization": str((open("auth.txt","r")).read().strip()),
		"Connection": "keep-alive",
		"Host": "cdn-api.co-vin.in",
		"Origin": "https://selfregistration.cowin.gov.in",
		"Referer": "https://selfregistration.cowin.gov.in/",
		"TE": "Trailers",
		"User-Agent": str(ua.chrome),
	}
	# krlDst=[{"district_id": 301,"district_name": "Alappuzha"},{"district_id": 307,"district_name": "Ernakulam"},{"district_id": 306,"district_name": "Idukki"},{"district_id": 297,"district_name": "Kannur"},{"district_id": 295,"district_name": "Kasaragod"},{"district_id": 298,"district_name": "Kollam"},{"district_id": 304,"district_name": "Kottayam"},{"district_id": 305,"district_name": "Kozhikode"},{"district_id": 302,"district_name": "Malappuram"},{"district_id": 308,"district_name": "Palakkad"},{"district_id": 300,"district_name": "Pathanamthitta"},{"district_id": 296,"district_name": "Thiruvananthapuram"},{"district_id": 303,"district_name": "Thrissur"},{"district_id": 299,"district_name": "Wayanad"}]
	s =requests.session()
	mainList=[]
	# for d in krlDst:	
	output=s.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id="+str(districtCode)+"&date="+today.strftime("%d-%m-%Y"),headers=header).text
	#print(output)
	output=json.loads(output)
	centers=output["centers"]
	# print(centers)
	for i in centers:
		tempList=[i["center_id"],i["name"],i["pincode"],i["fee_type"],i["district_name"]]
		# print(len(i["sessions"]))
		dataCsv = csv.reader(open('center.csv', "r"), delimiter=",")
		fileStatus=True
		for cent in dataCsv:
			if str(i["center_id"]) in cent:
				fileStatus=False
		if fileStatus:
			file=open("center.txt","a+")
			file.write(str(i["center_id"])+","+i["name"]+","+i["address"]+","+i["state_name"]+","+i["district_name"]+","+i["block_name"]+","+str(i["pincode"])+","+str(i["lat"])+","+str(i["long"])+"\n")
			with open('center.csv', 'a', newline='') as file:
				writer = csv.writer(file)
				writer.writerow([str(i["center_id"]),i["name"],i["address"],i["state_name"],i["district_name"],i["block_name"],str(i["pincode"]),str(i["lat"]),str(i["long"])])				
		aviDoses=0
		aviDosesPople=0
		aviDosesEmp=0
		for b in i["sessions"]:
			aviDoses=aviDoses+b["available_capacity"]
			aviDosesPople=aviDosesPople+b["available_capacity_dose1"]
			aviDosesEmp=aviDosesEmp+b["available_capacity_dose2"]
			tempList.append([b["date"],b["available_capacity"],b["min_age_limit"],b["vaccine"],b["available_capacity_dose1"],b["available_capacity_dose2"]])
		tempList.append(aviDosesPople)
		tempList.append(aviDosesEmp)
		tempList.append(aviDoses)
		mainList.append(tempList)
		# time.sleep(1)
	def myFunc(e):
		return e[-1]
	mainList.sort(key=myFunc,reverse=True)
	finaList=[]
	for items in mainList:
		if items[-1]!=0:
			finaList.append(items)
	#print(finaList)
	return finaList


# @scheduler.task('interval', id='do_job_1', seconds=65, misfire_grace_time=5)
# def job1():
#     print ("updated")
#     listOut()

@app.route("/",methods=['POST','GET'])                #first line / represents the route dir 
def home():
	if(request.method == 'GET'):
		data = 0
		a=True
		while a:
			try:
				data=listOut()
				a=False
			except:
				a=True
				print("data fetching return an err")
		def myFunc(e):
			return e[-4]
		data.sort(key=myFunc)

		don="<html><head><meta http-equiv='refresh' content='5'></head><table><tr>"
		if len(data)>0:
			for i in data:
				don=don+"<td> District: <b>"+str(i[4])+"</b></td><td> Center name: <b>"+str(i[1])+"</b></td><td> pincode: <b>"+str(i[2])+"</b> </td><td> Free/Paid: <b>"+str(i[3])+"</b> </td><td> people portal: <b>"+str(i[-3])+"</b> </td><td> for employees portal : <b>"+str(i[-2])+"</b> </td><td> total : <b>"+str(i[-1])+"</b> </td> </tr>"
			return don+"</table></html>"
		else:
			return "<h1>nothing avilable</h1>"
	else:
		return("request correctly")

if __name__ == "__main__":#check wether the ___name__ == __main__ conforming only devoloper can debug the code... if this command is not here anyone can access and debug the code..
    app.run()




	# "content-type": "application/json",
	# 	"content-length": "141",
	# 	"dnt": "1",
	# 	"sec-ch-ua": "'Chromium';v='91', ' Not;A Brand';v='99'",
	# 	"sec-ch-ua-mobile": "?0",
	# 	"sec-fetch-dest": "empty",
	# 	"sec-fetch-mode": "cors",
	# 	"sec-fetch-site": "cross-site"
