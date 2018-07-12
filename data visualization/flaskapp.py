from flask import Flask,render_template,request
import csv,base64,time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import pymysql
from collections import OrderedDict

db=pymysql.connect(host="localhost",user="root",passwd="",db="test",local_infile=True)
app=Flask(__name__)

def readbytesfile(file_name):
	data=open(file_name,'rb').read()
	return data
def k_mean_distance(data, cx, cy, i_centroid, cluster_labels):
        distances = [np.sqrt((x-cx)**2+(y-cy)**2) for (x, y) in data[cluster_labels == i_centroid]]
        return np.mean(distances)

@app.route("/")
def main():
	return render_template("main_page.html")

@app.route("/upload",methods=['POST'])
def upload():
	list=[]
	file_name="minnow.csv"
	cluster=int(request.form['cluster'])
	attribute1=request.form['attribute1']
	attribute2=request.form['attribute2']
	val1=[]
	val2=[]
	if(attribute1=="CabinNum"):
		a=0
	if(attribute1=="Fname"):
		a=1
	if(attribute1=="Lname"):
		a=2
	if(attribute1=="Age"):
		a=3
	if(attribute1=="Survived"):
		a=4
	if(attribute1=="Lat"):
		a=5
	if(attribute1=="Long"):
		a=6
	if(attribute1=="PictureCap"):
		a=7
	if(attribute1=="PicturePas"):
		a=8
	if(attribute1=="Fare"):
		a=9
	if(attribute2=="CabinNum"):
		b=0
	if(attribute2=="Fname"):
		b=1
	if(attribute2=="Lname"):
		b=2
	if(attribute2=="Age"):
		b=3
	if(attribute2=="Survived"):
		b=4
	if(attribute2=="Lat"):
		b=5
	if(attribute2=="Long"):
		b=6
	if(attribute2=="PictureCap"):
		b=7
	if(attribute2=="PicturePas"):
		b=8
	if(attribute2=="Fare"):
		b=9
	start=time.time()
	f=open(file_name)
	for row in csv.reader(f):
		try:
			valx=float(row[a])
			if a==0:
				valx=int(valx/100)
			valy=row[b]
			if valy not in list :
				list.append(valy)
			lindex=list.index(valy)
			val1.append(valx)
			val2.append(lindex)
		except ValueError:
			continue
	dl=[]
	udl=[]
	for i in range(0,len(val1)-1):
		dl.append(val1[i])
		dl.append(val2[i])
		udl.append(dl)
		dl=[]
	final=np.array(udl)
	km=KMeans(n_clusters=cluster).fit(final)
	labels=km.labels_
	centroids=km.cluster_centers_
	#https://stackoverflow.com/questions/40828929/sklearn-mean-distance-from-centroid-of-each-cluster
	c_mean_distances = []
	for i, (cx, cy) in enumerate(centroids):
		mean_distance = k_mean_distance(final, cx, cy, i, labels)
		c_mean_distances.append(mean_distance)
	len_centroid=len(centroids)
	length={len(final[np.where(labels == i)]) for i in range(km.n_clusters)}
	points={i: final[np.where(labels == i)] for i in range(km.n_clusters)}
	plt.scatter(final[:,0],final[:,1], c=[plt.cm.nipy_spectral(float(i)/10) for i in labels])
	plt.scatter(centroids[:,0],centroids[:,1],marker='x')
	plt.savefig("visualization.png")
	plt.clf()
	fileinfo=base64.b64encode(readbytesfile("visualization.png")).decode()
	end=time.time()
	elapsed=end-start
	distance=[] 
	fields=zip(c_mean_distances,length,centroids)
	return render_template("main_page.html",fileinfo="data:image/jpg;base64,"+fileinfo,timeelapsed=str(elapsed),length=length,points=str(points),distance=c_mean_distances,fields=fields,centroids=centroids)
	#return '''<html><body><img src="data:image/jpg;base64,'''+fileinfo+'''" style="width:500px;height:500px;"/><br>Time Elapsed:'''+str(elapsed)+'''<br>'''+str(length)+'''<br>'''+str(points)+'''<br>'''+str(c_mean_distances)+'''</body></html>'''
	#return '''<html><head><style>td {border: solid 2px black;}</style></head><body><img src="data:image/jpg;base64,'''+fileinfo+'''" style="width:500px;height:500px;"/><br>Time Elapsed:'''+str(elapsed)+'''<br>'''+str(length)+'''<br>'''+str(points)+'''<br>'''+str(c_mean_distances)+'''

	
@app.route("/nupload",methods=['POST'])
def nupload():
	list=[]
	file_name="minnow.csv"
	cluster=int(request.form['cluster'])
	attribute1=request.form['attribute1']
	attribute2=request.form['attribute2']
	val1=[]
	val2=[]
	sql="select sum(case when latitude=2 and longitude=152 then 1 end) as first from minnow";
	cursor=db.cursor();
	cursor.execute(sql);
	result=cursor.fetchall()
	for vals in result[0]:
		val1.append(float(vals))
			
	sql="select sum(case when latitude=43 and longitude=26 then 1 end) as first from minnow";
	cursor=db.cursor();
	cursor.execute(sql);
	result=cursor.fetchall()
	for vals in result[0]:
		val2.append(float(vals))
	dl=[]
	udl=[]
	for i in range(0,len(val1)-1):
		dl.append(val1[i])
		dl.append(val2[i])
		udl.append(dl)
		dl=[]
	final=np.array(udl)
	km=KMeans(n_clusters=cluster).fit(final)
	labels=km.labels_
	centroids=km.cluster_centers_
	c_mean_distances = []
	for i, (cx, cy) in enumerate(centroids):
		mean_distance = k_mean_distance(final, cx, cy, i, labels)
		c_mean_distances.append(mean_distance)
	len_centroid=len(centroids)
	length={len(final[np.where(labels == i)]) for i in range(km.n_clusters)}
	points={i: final[np.where(labels == i)] for i in range(km.n_clusters)}
	plt.scatter(final[:,0],final[:,1], c=[plt.cm.nipy_spectral(float(i)/10) for i in labels])
	plt.scatter(centroids[:,0],centroids[:,1],marker='x')
	plt.savefig("visualization.png")
	plt.clf()
	fileinfo=base64.b64encode(readbytesfile("visualization.png")).decode()
	end=time.time()
	elapsed=end-start
	distance=[] 
	fields=zip(c_mean_distances,length,centroids)
	return render_template("main_page.html",fileinfo="data:image/jpg;base64,"+fileinfo,timeelapsed=str(elapsed),length=length,points=str(points),distance=c_mean_distances,fields=fields)
	
	#return '''<html><body><img src="data:image/jpg;base64,'''+fileinfo+'''" style="width:500px;height:500px;"/><br>Time Elapsed:'''+str(elapsed)+'''<br>'''+str(length)+'''<br>'''+str(points)+'''</body></html>'''
@app.route("/supload",methods=['POST'])
def supload():
	list=[]
	slist=[]
	file_name="minnow.csv"
	cluster=int(request.form['cluster'])
	attribute1=request.form['attribute1']
	attribute2=request.form['attribute2']
	val1=[]
	val2=[]
	if(attribute1=="CabinNum"):
		a=0
	if(attribute1=="Fname"):
		a=1
	if(attribute1=="Lname"):
		a=2
	if(attribute1=="Age"):
		a=3
	if(attribute1=="Survived"):
		a=4
	if(attribute1=="Lat"):
		a=5
	if(attribute1=="Long"):
		a=6
	if(attribute1=="PictureCap"):
		a=7
	if(attribute1=="PicturePas"):
		a=8
	if(attribute1=="Fare"):
		a=9
	if(attribute2=="CabinNum"):
		b=0
	if(attribute2=="Fname"):
		b=1
	if(attribute2=="Lname"):
		b=2
	if(attribute2=="Age"):
		b=3
	if(attribute2=="Survived"):
		b=4
	if(attribute2=="Lat"):
		b=5
	if(attribute2=="Long"):
		b=6
	if(attribute2=="PictureCap"):
		b=7
	if(attribute2=="PicturePas"):
		b=8
	if(attribute2=="Fare"):
		b=9
	start=time.time()
	f=open(file_name)
	for row in csv.reader(f):
		try:
			valx=row[a]
			if valx not in slist :
				slist.append(valx)
			sindex=slist.index(valx)
			valy=row[b]
			if valy not in list :
				list.append(valy)
			lindex=list.index(valy)
			val1.append(sindex)
			val2.append(lindex)
		except ValueError:
			continue
	dl=[]
	udl=[]
	for i in range(0,len(val1)-1):
		dl.append(val1[i])
		dl.append(val2[i])
		udl.append(dl)
		dl=[]
	final=np.array(udl)
	km=KMeans(n_clusters=cluster).fit(final)
	labels=km.labels_
	centroids=km.cluster_centers_
	c_mean_distances = []
	for i, (cx, cy) in enumerate(centroids):
		mean_distance = k_mean_distance(final, cx, cy, i, labels)
		c_mean_distances.append(mean_distance)
	len_centroid=len(centroids)
	length={len(final[np.where(labels == i)]) for i in range(km.n_clusters)}
	points={i: final[np.where(labels == i)] for i in range(km.n_clusters)}
	plt.scatter(final[:,0],final[:,1], c=[plt.cm.nipy_spectral(float(i)/10) for i in labels])
	plt.scatter(centroids[:,0],centroids[:,1],marker='x')
	plt.savefig("visualization.png")
	plt.clf()
	fileinfo=base64.b64encode(readbytesfile("visualization.png")).decode()
	end=time.time()
	elapsed=end-start
	distance=[] 
	fields=zip(c_mean_distances,length,centroids)
	return render_template("main_page.html",fileinfo="data:image/jpg;base64,"+fileinfo,timeelapsed=str(elapsed),length=length,points=str(points),distance=c_mean_distances,fields=fields)
	
	#return '''<html><body><img src="data:image/jpg;base64,'''+fileinfo+'''" style="width:500px;height:500px;"/><br>Time Elapsed:'''+str(elapsed)+'''<br>'''+str(length)+'''<br>'''+str(points)+'''</body></html>'''

#PIE CHART TO SHOW PERCENTAGE OF FEMALE SURVIVORS	
@app.route("/piechartforfemalesurvivors",methods=['POST'])
def piechartforfemalesurvivors():
	start=time.time()
	sql="select sum(case when survived=1 and sex='female'  then 1 end) as first,sum(case when survived=0 and sex='female'  then 1 end) as second from titanic";
	cursor=db.cursor();
	cursor.execute(sql);
	result=cursor.fetchall()
	val=[]
	for vals in result[0]:
		val.append(float(vals))
	labels=["survived","not survived"]
	total=0
	for vals in val:
		total=total+vals
	legendtab=[]
	for i in range(len(labels)):
		legendtab.append(labels[i]+" - "+str(round(val[i]/total*100,2))+"%")
	index=np.arange(len(labels))
	patch=plt.pie(val,shadow=False,startangle=140,pctdistance=0.9, radius=2)
	plt.legend(patch[0],legendtab,bbox_to_anchor=(0.5,0.5),bbox_transform=plt.gcf().transFigure,loc="best")
	plt.axis("equal")
	plt.title("Female Survivors of titanic")
	plt.tight_layout()
	plt.show()
	plt.savefig("visualization.png")
	plt.clf()
	fileinfo=base64.b64encode(readbytesfile("visualization.png")).decode()
	end=time.time()
	elapsed=end-start
	elapsed="%.3f" % elapsed
	return render_template("main_page.html",piefileinfo="data:image/jpg;base64,"+fileinfo,pietime=str(elapsed)+"s")
	
#BAR GRAPH TO SHOW PERCENTAGE OF MALE SURVIVORS	
@app.route("/barchartformalesurvivors",methods=['POST'])
def barchartformalesurvivors():
	start=time.time()
	#sql="select sum(case when survived=1 and sex='male'  then 1 end) as first,sum(case when survived=0 and sex='male'  then 1 end) as second from titanic";
	sql="select sum(case when fare=100 then 1 end) as first,\
	sum(case when fare=200 then 1 end) as second,\
	sum(case when fare=500 then 1 end) as third,\
	sum(case when fare=800 then 1 end) as fourth,\
	sum(case when fare=2500 then 1 end) as fifth from minnow";
	cursor=db.cursor();
	cursor.execute(sql);
	result=cursor.fetchall()
	val=[]
	for vals in result[0]:
		val.append(float(vals))
	labels=["100","200","500","800","2500"]
	total=0
	for vals in val:
		total=total+vals
	legendtab=[]
	for i in range(len(labels)):
		legendtab.append(labels[i]+" - "+str(round(val[i]/total*100,2))+"%")
	index=np.arange(len(labels))
	#for bar graph
	colors=["darkgreen","crimson","red","green","blue"]
	plt.barh(index,val,color=colors)
	plt.yticks(index,labels,fontsize=8,rotation=0)
	plt.xlabel("Percentage of Passengers")
	plt.ylabel("Fare")
	plt.title("Fare")
	plt.savefig("visualization.png",bbox_inches="tight")
	plt.clf()
	fileinfo=base64.b64encode(readbytesfile("visualization.png")).decode()
	end=time.time()
	elapsed=end-start
	elapsed="%.3f" % elapsed
	return render_template("main_page.html",barfileinfo="data:image/jpg;base64,"+fileinfo,bartime=str(elapsed)+"s")
	
@app.route("/earthquakepie",methods=['POST'])
def earthquakepie():
	start=time.time()
	sql="select sum(case when age between 10 and 19 then 1 end) as first,\
	sum(case when age between 20 and 29 then 1 end) as second,\
	sum(case when age between 30 and 39 then 1 end) as third,\
	sum(case when age between 40 and 49 then 1 end) as fourth,\
	sum(case when age between 70 and 79 then 1 end) as fifth,\
	sum(case when age between 140 and 149 then 1 end) as sixth from minnow";
	cursor=db.cursor();
	cursor.execute(sql);
	result=cursor.fetchall()
	cursor.close()
	val=[]
	for vals in result[0]:
		val.append(float(vals))
	labels=["10 to 19","20 to 29","30 to 39","40 to 49","70 to 79","140 to 149"]
	total=0

	for vals in val:
		total+=vals
	legendtab=[]
	for i in range(len(labels)):
		legendtab.append(labels[i]+" - "+str(round(val[i]/total*100,2))+"%")
	index=np.arange(len(labels))
	#for bar graph
	# plt.barh(index,val)
	# plt.yticks(index,labels,fontsize=8,rotation=30)
	# plt.xlabel("Magnitude Count")
	# plt.ylabel("Magnitude")
	# plt.title("Earthquakes")
	# plt.savefig("visualization.png",bbox_inches="tight")
	#plt.clf()
	# for pie chart graph
	patch=plt.pie(val,shadow=False,startangle=140,pctdistance=0.9, radius=2)
	plt.legend(patch[0],legendtab,bbox_to_anchor=(0.5,0.5),bbox_transform=plt.gcf().transFigure,loc="best")
	plt.axis("equal")
	plt.title("Earthquakes")
	plt.tight_layout()
	plt.show()
	plt.savefig("visualization.png")
	plt.clf()
	fileinfo=base64.b64encode(readbytesfile("visualization.png")).decode()
	end=time.time()
	elapsed=end-start
	#distance=[] 
	#fields=zip(c_mean_distances,length,centroids)
	return render_template("main_page.html",fileinfo="data:image/jpg;base64,"+fileinfo)
	

if __name__=="__main__":
	app.run(debug=True)