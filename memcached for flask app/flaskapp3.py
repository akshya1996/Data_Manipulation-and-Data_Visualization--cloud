from flask import Flask,render_template,request
import csv,pymysql,memcache,time,random,hashlib

app=Flask(__name__)
db=pymysql.connect(host="",user="",passwd="",db="",local_infile=True)
memc=memcache.Client([''],debug=1)

@app.route("/")
def main():
	# conn=db.connect()
	# cursor=conn.cursor()
	cursor=db.cursor()
	query="select * from earthquake"
	cursor.execute(query)
	data=cursor.fetchall()
	return render_template("main_page.html",data=data)

@app.route("/upload",methods=['POST'])
def upload():
	file_name="/home/akshya/flaskapp/"+request.form['uploadfile']
	sql="""LOAD DATA LOCAL INFILE %s INTO TABLE earthquake FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES"""
	cursor=db.cursor()
	cursor.execute(sql,(file_name,))
	db.commit()
	return render_template("main_page.html",message1="File Uploaded")

@app.route("/uploadnewtable",methods=['POST'])
def uploadnewtable():
	file_name="/home/akshya/flaskapp/"+request.form['uploadnewfile']
	sql="""LOAD DATA LOCAL INFILE %s INTO TABLE titanic FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES"""
	cursor=db.cursor()
	cursor.execute(sql,(file_name,))
	db.commit()
	return render_template("main_page.html",message2="New File Uploaded")


@app.route("/memcache_page",methods=['POST'])
def memcache_page():

	fromlat=int(request.form['latitude'])
	fromlon=int(request.form['longitude'])
	ranger=int(request.form['range'])
	ranger=ranger*2
	lrange=ranger
	srange=ranger
	tolat=fromlat+lrange
	tolon=fromlon+srange
	fromlat=str(fromlat)
	tolat=str(tolat)
	fromlon=str(fromlon)
	tolon=str(tolon)

	query="select id from earthquake"
	cursor=db.cursor()
	result=cursor.execute(query)
	count=result
	before=time.time()
	for i in range(1,30):
		number=random.randrange(0,5)
		#query="select nst from earthquake limit {}".format(number)
		query="select * from earthquake where (latitude between %s and %s) and (longitude between %s and %s)".format(number)
		enctext=hashlib.md5(query.encode())
		enctext=enctext.hexdigest()
		value=memc.get(enctext)
		if not value:
			print(enctext)
			cursor=db.cursor()
			#result1=cursor.execute(query)
			result1=cursor.execute(query,(fromlat,tolat,fromlon,tolon,))
			memc.set(enctext,result1)
			print(memc.get(enctext))
	after=time.time()
	dif=after-before
	print(dif)
	cursor.close()
	return render_template("memcache_page.html",before=before,after=after,dif=dif)
@app.route("/latlon",methods=['POST'])
def latlon():
	fromlat=int(request.form['latitude'])
	fromlon=int(request.form['longitude'])
	range=int(request.form['range'])
	range=range*2
	lrange=range
	srange=range
	tolat=fromlat+lrange
	tolon=fromlon+srange
	fromlat=str(fromlat)
	tolat=str(tolat)
	fromlon=str(fromlon)
	tolon=str(tolon)
	sql="select * from earthquake where (latitude between %s and %s) and (longitude between %s and %s)"
	cursor=db.cursor()
	cursor.execute(sql,(fromlat,tolat,fromlon,tolon))
	data20=cursor.fetchall()
	cursor.close()
	return render_template("main_page.html",data20=data20)
@app.route("/magrange",methods=['POST'])
def magrange():
	fmag=int(request.form['fmag'])
	tmag=int(request.form['tmag'])
	flag=0
        before1=[]
	after1=[]
	diff1=[]
	bef=time.time()

	while fmag<=tmag:
	
		fmagnitude=str(fmag)
		before=time.time()
		query1="select count(*) from earthquake where mag =%s" 
		sql="select place from earthquake where mag =%s limit 1 "
		cursor=db.cursor()
		cursor.execute(sql,(fmagnitude,))
		data10=cursor.fetchall()
		cursor.execute(query1,(fmagnitude,))
		data11=cursor.fetchall()
		after=time.time()
		dif=after-before
		fmag=fmag+0.1
		if flag==0:
			data108=data10
			data109=data11
			before1.append(before)
			after1.append(after)
			diff1.append(dif)
		if flag!=0:
			data108=data108+data10
			data109=data109+data11
			before1.append(before)
			after1.append(after)
			diff1.append(dif)
		flag=1
	aft=time.time()
	d=aft-bef
		
		
	cursor.close()
	return render_template("main_page.html",data108=data108,before1=before1,after1=after1,diff1=diff1,bef=bef,aft=aft,d=d,data109=data109)
	
	
@app.route("/latrange",methods=['POST'])	
def latrange():
	fromlat=request.form['fromlat']
	tolat=request.form['tolat']
	sql="select * from earthquake where latitude between %s and %s order by mag desc limit 5"
	cursor=db.cursor()
	cursor.execute(sql,(fromlat,tolat,))
	data200=cursor.fetchall()
	
	cursor.close()
	return render_template("main_page.html",data200=data200)

@app.route("/memcache_latrange",methods=['POST'])
def memcache_latrange():

	fromlat=int(request.form['fromlat'])
	tolat=int(request.form['tolat'])
	
	query="select * from earthquake where latitude"
	cursor=db.cursor()
	result=cursor.execute(query)
	count=result
	before=time.time()
	for i in range(1,30):
		number=random.randrange(0,5)
		#query="select nst from earthquake limit {}".format(number)
		query="select * from earthquake where latitude between %s and %s order by mag desc limit 5".format(number)
		enctext=hashlib.md5(query.encode())
		enctext=enctext.hexdigest()
		value=memc.get(enctext)
		if not value:
			print(enctext)
			cursor=db.cursor()
			#result1=cursor.execute(query)
			result1=cursor.execute(query,(fromlat,tolat,))
			memc.set(enctext,result1)
			print(memc.get(enctext))
	after=time.time()
	dif=after-before
	print(dif)
	cursor.close()
	return render_template("memcache_page.html",before=before,after=after,dif=dif)
	
@app.route("/placepattern",methods=['POST'])	
def placepattern():
	location=request.form['place']
	sql="select * from earthquake where place like '%"+location+"%'"
	cursor=db.cursor()
	cursor.execute(sql)
	data201=cursor.fetchall()
	
	cursor.close()
	return render_template("main_page.html",data201=data201)

@app.route("/memcache_findplace",methods=['POST'])
def memcache_findplace():

	location=request.form['place']
	query="select * from earthquake"
	cursor=db.cursor()
	result=cursor.execute(query)
	count=result
	before=time.time()
	for i in range(1,30):
		number=random.randrange(0,5)
		#query="select nst from earthquake limit {}".format(number)
		query="select * from earthquake where place like '%"+location+"%'".format(number)
		enctext=hashlib.md5(query.encode())
		enctext=enctext.hexdigest()
		value=memc.get(enctext)
		if not value:
			print(enctext)
			cursor=db.cursor()
			#result1=cursor.execute(query)
			result1=cursor.execute(query)
			memc.set(enctext,result1)
			print(memc.get(enctext))
	after=time.time()
	dif=after-before
	print(dif)
	cursor.close()
	return render_template("memcache_page.html",before=before,after=after,dif=dif)
	
#this is for 30 days database	
@app.route("/locsource",methods=['POST'])	
def locsource():
	location=request.form['place']
	sql="select * from earthquake where locsource like '%"+location+"%'"
	cursor=db.cursor()
	cursor.execute(sql)
	locsourcedata=cursor.fetchall()
	cursor.close()
	return render_template("main_page.html",locsourcedata=locsourcedata)

@app.route("/memcache_locsource",methods=['POST'])
def memcache_locsource():
	location=request.form['place']
	query="select * from earthquake"
	cursor=db.cursor()
	result=cursor.execute(query)
	count=result
	before=time.time()
	for i in range(1,30):
		number=random.randrange(0,5)
		query="select * from earthquake where locsource like '%"+location+"%'".format(number)
		enctext=hashlib.md5(query.encode())
		enctext=enctext.hexdigest()
		value=memc.get(enctext)
		if not value:
			print(enctext)
			cursor=db.cursor()
			result1=cursor.execute(query)
			memc.set(enctext,result1)
			print(memc.get(enctext))
	after=time.time()
	dif=after-before
	print(dif)
	cursor.close()
	return render_template("memcache_page.html",before=before,after=after,dif=dif)
	
	
#executing 1000 queries	
@app.route("/memcache_thousand",methods=['POST'])
def memcache_thousand():
	count=0
	query="select * from earthquake"
	cursor=db.cursor()
	result=cursor.execute(query)
	count=result
	before=time.time()
	mag = -500;
	while count<1000:
		count = count+1
		smag=str(mag)
		for i in range(1,30):
			number=random.randrange(0,5)
			query="select * from earthquake where mag = %s".format(number)
			enctext=hashlib.md5(query.encode())
			enctext=enctext.hexdigest()
			value=memc.get(enctext)
			if not value:
				print(enctext)
				cursor=db.cursor()
				result1=cursor.execute(query,(smag,))
				memc.set(enctext,result1)
				print(memc.get(enctext))
		mag=mag+1
	after=time.time()
	dif=after-before
	cursor.close()
	return render_template("memcache_page.html",before=before,after=after,dif=dif)

@app.route("/nearlocation",methods=['POST'])	
def nearlocation():
	location=request.form['location']
	distance=request.form['distance']
	distance=distance+"km"
	cursor=db.cursor()
	sql="select * from earthquake where place like '%"+location+"%' and place like '"+distance+"%'"
	cursor.execute(sql)
	data=cursor.fetchall()
	count=0
	for row in data:
		count+=1
	cursor.close()
	return render_template("main_page.html",sourcedata=data)	



	
#to find if there are more quakes at night
@app.route("/morequakes",methods=['POST'])	
def morequakes():
	mag=request.form['mag']
	cursor=db.cursor()
	sql="select * from earthquake where (etime like '%%T20%%' or etime like '%%T21%%' or etime like '%%T22%%' or etime like '%%T23%%' or etime like '%%T24%%' or etime like '%%T01%%' or etime like '%%T02%%' or etime like '%%T03%%' or etime like '%%T04%%' or etime like '%%T05%%') and (mag > %s)"
	cursor.execute(sql,(mag,))
	data=cursor.fetchall()
	count4=0
	for row in data:
		count4+=1
	query1="select * from earthquake where mag>%s"
	cursor.execute(query1,(mag))
	data=cursor.fetchall()
	count5=0
	for row in data:
		count5+=1
	count5=count5-count4
	queryres="Earthquakes occur more often at daytime"	
	if count4>count5:
	    queryres="Earthquakes occur more often at night"
	return render_template("main_page.html",count4=count4,count5=count5,queryres=queryres,data10=data)	


if __name__=="__main__":
	app.run(debug=True)