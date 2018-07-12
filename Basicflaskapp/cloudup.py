from flask import Flask,render_template,request,url_for
import os,base64,csv
import os, sys
import csv,pymysql,time,hashlib,random,memcache
from flask_db2 import DB2



app1=Flask(__name__)
port=int(os.getenv("VCAP_APP_PORT"))



app1.config['DB2_DATABASE'] = 'BLUDB'
app1.config['DB2_HOSTNAME'] = ''
app1.config['DB2_PORT'] = 50000
app1.config['DB2_PROTOCOL'] = 'TCPIP'
app1.config['DB2_USER'] = 
app1.config['DB2_PASSWORD'] = 

db=DB2(app1)


@app1.route("/")
def main():
	return render_template('main.html')
	
@app1.route("/upload",methods=['POST'])
def upload():
	file_name=request.form['uploadfile']
	cursor=db.connection.cursor()
	file=open(file_name,'r')
	filecols=csv.reader(file)
	for row in filecols:
		sql="insert into test values(?,?)"
		cursor.execute(sql,(row[0],row[1]))
	return render_template("main.html",message1="Fileuploaded")
	
@app1.route("/greaterthanmag",methods=['POST'])
def greaterthanmag():
	magval=request.form['magval']
	cursor=db.connection.cursor()
	sql="select * from earthquake where mag>?"
	cursor.execute(sql,(magval,))
	data=cursor.fetchall()
	count=0
	for row in data:
		count+=1
	return render_template("main.html",count1=count,data7=data)
	
	
@app1.route("/nearlocation",methods=['POST'])
def nearlocation():
	location=request.form['location']
	distance=request.form['distance']
	distance=distance+"km"
	cursor=db.connection.cursor()
	sql="select * from earthquake where place like '%"+location+"%' and place like '"+distance+"%'"
	cursor.execute(sql,(location,distance,))
	data=cursor.fetchall()
	count=0
	for row in data:
		count+=1
	return render_template("main.html",count2=count,data8=data,distance=distance)
	
	
	
@app1.route("/withinrange",methods=['POST'])
def withinrange():
	range1=request.form['range1']
	range2=request.form['range2']
	cursor=db.connection.cursor()
	range1l=range1+1
	flag=0
	while rangel1<=range2:
		sql="select * from earthquake where mag between ? and ?"
		cursor.execute(sql,(range1,rangel1,))
		range1=rangel1+0.1
		rangel1=range1+1
		data=cursor.fetchall()
		if flag==0:
			data2=data
		if flag>0:
			data2=data2.append(data)
	count=0
	for row in data2:
		count+=1
	return render_template("main.html",count3=count,data9=data2)
	

	
@app1.route("/morequakes",methods=['POST'])
def morequakes():
	mag=request.form['mag']
	cursor=db.connection.cursor()
	sql="select * from earthquake where mag=? and (etime like '%T20%' or etime like '%T21%' or etime like '%T22%' or etime like '%T23%' or etime like '%T24%' or etime like '%T01%' or etime like '%T02%' or etime like '%T03%' or etime like '%T04%' or etime like '%T05%')"
	cursor.execute(sql,(mag,))
	data=cursor.fetchall()
	count4=0
	for row in data:
		count4+=1
	query1="select * from earthquake where mag>?"
	cursor.execute(query1,(mag,))
	data=cursor.fetchall()
	count5=0
	for row in data:
		count5+=1
	count5=count5-count4
	queryres="Earthquakes occur more often at daytime"	
	if count4>count5:
	    queryres="Earthquakes occur more often at night"
	return render_template("main.html",count4=count4,count5=count5,queryres=queryres,data10=data)
	
@app1.route("/latlon",methods=['POST'])
def latlon():
	fromlat=request.form['latitude']
	fromlon=request.form['longitude']
	range=request.form['range']
	range=range*2
	lrange=range
	srange=range
	fromlat=fromlat
	fromlon=fromlon
	if fromlat<0:
		lrange=-range
	tolat=fromlat+lrange
	if fromlon<0:
		srange=-range
	tolon=fromlon+srange
	cursor=db.connection.cursor()
	sql="select * from earthquake where latitude between ? and ? and (longitude between ? and ?) order by magnitude desc"
	cursor.execute(sql,(fromlat,tolat,fromlon,tolon,))
	data20=cursor.fetchall()
	return render_template("main.html",data20=data20)
	
	
	
	
@app1.route("/locmag",methods=['POST'])
def locmag():

	location=request.form['location']
	fmagnitude=request.form['fmagnitude']
	tmagnitude=request.form['tmagnitude']
	cursor=db.connection.cursor()
	sql="select etime,latitude,longitude,place from earthquake where place like '%"+location+"%' and (mag between ? and ?) "
	cursor.execute(sql,(fmagnitude,tmagnitude,))
	data=cursor.fetchall()
	count=0
	for row in data:
		count+=1
	return render_template("main.html",count100=count,data100=data)

@app1.route("/excelupload",methods=['POST'])
def excelupload():
	file_name=request.form['excelfile']
	cursor=db.connection.cursor()
	file=open(file_name,'r')
	filecols=csv.reader(file)
	counter=0
	for row in filecols:
		if counter!=0:
			sql="insert into earthquake values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
			cursor.execute(sql,(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15]))
		counter=counter+1
	sql="select * from earthquake"
	cursor.execute(sql)
	data=cursor.fetchall()
	count=0
	for row in data:
		count+=1
	
	return render_template("main.html",message2="Earthquake File uploaded",count=count)
	
	
	
@app1.route("/clustering",methods=['POST'])
def clustering():
	cluster=request.form['cluster']
	cursor=db.connection.cursor()
	sql="select * from earthquake where mag between 2 and 3"
	cursor.execute(sql)
	data11=cursor.fetchall()
	sql="select * from earthquake where mag between 3.1 and 4"
	cursor.execute(sql)
	data12=cursor.fetchall()
	sql="select * from earthquake where mag between 4.1 and 5"
	cursor.execute(sql)
	data13=cursor.fetchall()
	sql="select * from earthquake where mag between 5.1 and 6"
	cursor.execute(sql)
	data14=cursor.fetchall()
	return render_template("main.html",data11=data11,data12=data12,data13=data13,data14=data14)
	
@app1.route("/latclustering",methods=['POST'])
def latclustering():
	fromlat=request.form['latitude']
	range=request.form['range']
	tolat=int(fromlat)+int(range)
	cursor=db.connection.cursor()
	sql="select * from earthquake where latitude between ? and ?"
	cursor.execute(sql,(fromlat,tolat,))
	data20=cursor.fetchall()
	return render_template("main.html",data20=data20)
	
	
if __name__=="__main__":

	app1.run(host='0.0.0.0',port=port,debug=True)