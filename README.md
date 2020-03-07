# mappyserver
rasp pi air sensor

examples of curl to upload files
for a file in c:\temp\atstdatafile.txt
locally
     curl -X POST -F file=@c:/temp/atstdatafile.txt  http://localhost:5000/files
remote
    curl -X POST -F file=@c:/temp/atstdatafile.txt  https://smello-vision.herokuapp.com/files

in browser 
    http://127.0.0.1:5000/files/atstdatafile.txt
or
    https://smello-vision.herokuapp.com/files/atstdatafile.txt

useful stuff to do with heroku

#this will show the remote heroku runtime log, so you can watch the web server
heroku logs --tail
#push git code to heroku, which will build and deploy
git push heroku master
#push code to github, you'll need to do this as git on heroku has no gui
git push origin master
#git stuff
if using git on command line
#add all changed files
git commit add .
#commit the added changes
git commit -m "a comment here"
#then u can do the pushedhttp://127.0.0.1:5000/readings/2020-03-05-20

#to run webserver locally in root of directory
flask run
#turn on debug stuff for web server, will see crash stack on web page
set FLASK_DEBUG=1

================================
readings
==================================
 curl -X POST -F file=@c:/temp/hello.txt http://127.0.0.1:5000/readings
 http://127.0.0.1:5000/readings/2020-03-05-20
 or
 https://smello-vision.herokuapp.com/readings/2020-03-05-20


