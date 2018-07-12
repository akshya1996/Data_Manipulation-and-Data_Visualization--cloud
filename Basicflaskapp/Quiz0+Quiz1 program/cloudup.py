from flask import Flask,render_template,request,url_for
import os,base64
import os, sys
from ibm_botocore.client import Config
import ibm_boto3
import boto3
from botocore.client import Config

from flask_db2 import DB2
app1=Flask(__name__)

	
port=int(os.getenv("VCAP_APP_PORT"))

app1.config['DB2_DATABASE'] = 'BLUDB'
app1.config['DB2_HOSTNAME'] = ''
app1.config['DB2_PORT'] = 50000
app1.config['DB2_PROTOCOL'] = 'TCPIP'
app1.config['DB2_USER'] = ''
app1.config['DB2_PASSWORD'] = ''

db=DB2(app1)

def readbytesfile(file_name):
	data=open(file_name,'rb').read()
	return data

@app1.route("/")
def main():
	sql="select name from people"
	cursor=db.connection.cursor()
	cursor.execute(sql)
	data=cursor.fetchall()
	return render_template('main.html',data=data)


# @app1.route("/upload", methods=['POST'])
# def upload():
	# file_name=request.form['file']
	
	# #sql="""LOAD DATA LOCAL INFILE %s INTO TABLE people FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES"""
	# cursor=db.connection.cursor()
	# #cursor.execute(sql,(file_name,))
	# cursor.execute(sql)
	# return render_template("main_page.html",message1="File Uploaded")
@app1.route("/upload",methods=['POST'])
def upload():
	#s3 = ibm_boto3.resource('s3','e6d202d5a64a4857bd306cdd352760fb','d6cc895110d6f9e42447973226248b89a9d23426281129d6')
	cos = ibm_boto3.client('s3',ibm_api_key_id="_y2USdPQ3SkQLxMIZUtTXH0LJ6fXkVxOs2uvMAbrG0np",ibm_service_instance_id="crn:v1:bluemix:public:cloud-object-storage:global:a/54f64b1bbc6e4f44af926be29ed43851:8dcf1b66-d262-497c-acb3-b4e2c76304e7::",ibm_auth_endpoint="	http://iam.bluemix.net/oidc/token",config=Config(signature_version='oauth'),endpoint_url="https://s3.us-south.objectstorage.softlayer.net")
	fname=str(request.form['title'])
	fbody=request.files['myfile']
	#cos.upload_file(fname,'cloud3-storage',fbody)
	# Call COS to list current objects
	response = cos.list_objects(Bucket='cloud3-storage')
	# Get a list of all object names from the response
	objects = [object['Key'] for object in response['Contents']]
	# Print out the object list
	print("Objects in %s:" % 'cloud3-storage')
	print(json.dumps(objects, indent=2))
	return  render_template('main.html')
	


@app1.route("/showpictureforname", methods=['POST'])
def showpictureforname():
	# file_name=request.form['personname']
	# sql="select picture from people where name= ?"
	# cursor=db.connection.cursor()
	# cursor.execute(sql,(file_name,))
	# #cursor.execute(sql)
	# name=cursor.fetchall()
	# name1=name.split('.')
	# name1=name1[0]
	# filekey=bucket.new_key(name1)
	# filekey1=bucket.new_key(name)
	# fileinfo=filekey.get_contents_as_string().decode()
	# fileinfo1=base64.b64encode(filekey1.get_contents_as_string()).decode()
	# if fileinfo not in file_dict:
		# file_dict[fileinfo]=fileinfo1
	# #return render_template("main.html",file_dict=file_dict)

	# return render_template("main.html",file_dict=file_dict)
	personname=request.form['personname']
	sql="select picture from people where name=?"
	cursor=db.connection.cursor()
	cursor.execute(sql,(personname,))
	data=cursor.fetchall()
	return render_template("main.html",data2=data)
	
	
@app1.route("/getnamesforgrade", methods=['POST'])
def getnamesforgrade():
	fromgrade=request.form['fromgrade']
	tograde=request.form['tograde']
	sql="select name from people1 where grade between ? and ?"
	#sql="""LOAD DATA LOCAL INFILE %s INTO TABLE people FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES"""
	cursor=db.connection.cursor()
	cursor.execute(sql,(fromgrade,tograde,))
	#cursor.execute(sql)
	data=cursor.fetchall()
	#return render_template("main.html",count=count)
	return render_template("main.html",data2=data)

	#return render_template("main.html",message1="File Uploaded")
	
@app1.route("/changekeywords", methods=['POST'])
def changekeywords():
	name=request.form['name']
	modkey=request.form['modkey']
	sql="UPDATE people SET keywords=? WHERE name=?"

	
	cursor=db.connection.cursor()
	cursor.execute(sql,(modkey,name,))
	#cursor.execute(sql)
	
	#return render_template("main.html",count=count)
	return render_template("main.html",message1="Modified")

	#return render_template("main.html",message1="File Uploaded")	
@app1.route("/getkeywords", methods=['POST'])
def getkeywords():
	name=request.form['name']
	sql="select keywords from people where name=?"
	cursor=db.connection.cursor()
	cursor.execute(sql,(name,))
	#cursor.execute(sql)
	data=cursor.fetchall()
	#return render_template("main.html",count=count)
	return render_template("main.html",keywords=data)

	#return render_template("main.html",message1="File Uploaded")	


if __name__=="__main__":
	#app1.run(debug=True)
	app1.run(host='0.0.0.0',port=port,debug=True)