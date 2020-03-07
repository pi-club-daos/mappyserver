import os
import json
import folium
from app import app, db
from flask import jsonify, request, flash, redirect, send_file
from models import ReadingFile, AlchemyEncoder

# base router
@app.route('/')
@app.route('/index')
def index():
	return "Hello, World!"

# get all the data in the db
@app.route('/alldata', methods=['GET'])
def get_alldata():
	# read the data from the db
	datafiles = ReadingFile.query.all()
	# print out in jsonify form
	print (json.dumps(datafiles, cls=AlchemyEncoder)    )
	# return as json to web caller
	return json.dumps(datafiles, cls=AlchemyEncoder)

# get a avgeraged set of reading for a data/hour in form of yyyy-mm-dd-hh
@app.route('/readings/<string:datehour>', methods=['GET'])
def get_reading(datehour):
	# the following gets the data grouped and avaraged
	datafiles = db.session.query( ReadingFile.date,ReadingFile.hour, ReadingFile.district, db.func.avg(ReadingFile.reading).label('avgread') ).filter_by(date=datehour[:10],hour=datehour[-2:]).group_by(ReadingFile.date,ReadingFile.hour,ReadingFile.district).all()
	res = ''
	# loop round the results and form return string
	for r in datafiles:
		print(r)
		print(type(r))
		res += str(r)
	print(res)
	return res


# get a tst state map
@app.route('/tstmap', methods=['GET'])
def get_tstmap():
	import pandas as pd
	url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
	state_geo = f'{url}/us-states.json'
	state_unemployment = './testdata/tstmapdata.csv'
	state_data = pd.read_csv(state_unemployment)
	m = folium.Map(location=[48, -102], zoom_start=3)
	folium.Choropleth(
		geo_data=state_geo,
		name='choropleth',
		data=state_data,
		columns=['State', 'Unemployment'],
		key_on='feature.id',
		fill_color='YlGn',
		fill_opacity=0.7,
		line_opacity=0.2,
		legend_name='Unemployment Rate (%)'
	).add_to(m)
	return m._repr_html_()

# get a map version of the  data
@app.route('/map/<string:datehour>', methods=['GET'])
def get_map(datehour):
	import pandas as pd
	ldn_geo = './testdata/londongeo.json'
	datafiles = db.session.query( ReadingFile.district, db.func.avg(ReadingFile.reading).label('reading') ).filter_by(date=datehour[:10],hour=datehour[-2:]).group_by(ReadingFile.date,ReadingFile.hour,ReadingFile.district).statement
	readins_data = pd.read_sql(datafiles,db.session.bind)
	m = folium.Map(location=[51.5972, -0.1098], zoom_start=10)
	folium.Choropleth(
		geo_data=ldn_geo,
		name='choropleth',
		data=readins_data,
		columns=['district', 'reading'],
		key_on='feature.properties.NAME',
		fill_color='YlOrRd',
		threshold_scale=[0, .1, .2, .3, .4, .5, .6, .7,1],
		fill_opacity=0.4,
		line_opacity=1,
		legend_name='Unemployment Rate (%)'
	).add_to(m)
	return m._repr_html_()

# upload a readings file
@app.route('/readings', methods=['POST','PUT'])
def upload_readings():
	print(request.files)
	for k in request.files:
			print(k)
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		print(file)
		print(file.filename)
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file:
			filename = file.filename
			print(file.read())
			# make sure we are at the start of the file
			file.seek(0)
			# process file data into the db
			processData(file.read().decode("utf-8"))
			# go back to root
			return redirect('/')

# process the datafile
def processData(datarecvd):
	data = []
	# strip any newlines etc
	datarecvd.replace("\r","")
	datarecvd.replace("\n","")
	# split using ; into an array
	dataformatted = datarecvd.split(";")
	# now put into as array of arrays
	for i in dataformatted:
		data.append((i).split(","))
	print(data)
	for i in data:
		print(i)
		# get the data and time parts out of the string
		date = i[0][:10]
		time = i[0][-8:]
		print('date %s time %s' % (date,time))
		# form a single data row
		datafile = ReadingFile( date = date, hour = time[:2] , minutes=time[3:5], seconds=time[-2:],district = i[1] , reading = float(i[4]))
		print(datafile)
		# merge into the db, note exitsing line will be overwritten
		db.session.merge(datafile)
	# and commit it all, if large files, might need to move commit into loop
	db.session.commit()			
