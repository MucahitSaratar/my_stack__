#!/usr/bin/python3
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

html = """
<html>
   <body>
      <form action = "http://192.168.1.106:8000/uploader" method = "POST" 
         enctype = "multipart/form-data">
         <input type = "file" name = "file" />
         <input type = "submit"/>
      </form>
   </body>
</html>"""


@app.route('/')
def upload_file():
   return html


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file_my_function0x01():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully<br /><a href="http://192.168.1.106:8000/">Tekrar yukle</a>'

if __name__ == '__main__':
   app.run(host="0.0.0.0",port=8000)
