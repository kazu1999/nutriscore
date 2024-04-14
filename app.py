from flask import Flask, render_template, request, url_for, redirect
import os
import google.generativeai as genai
import PIL.Image
import re

from sql import handler

app = Flask(__name__, static_folder='./static/')

'''
@app.route('/', methods=['GET', 'POST'])
def upload():
    # URLでhttp://127.0.0.1:5000/uploadを指定したときはGETリクエストとなるのでこっち
    if request.method == 'GET':
        return render_template('upload.html')
    # formでsubmitボタンが押されるとPOSTリクエストとなるのでこっち
    elif request.method == 'POST':
        file = request.files['example']
        file.save(os.path.join('./static/image', file.filename))
        path = os.path.join('./static/image', file.filename)
        ret, nutri_dict = cal_nutri_score(path)
        db = handler.db()
        db.connect()
        db.insertRecord(nutri_dict['calories'],nutri_dict['fat'],nutri_dict['protein'],nutri_dict['carbohydrates'],'1')
        db.close()

        return render_template('uploaded_file.html', text = ret,path = path)
'''

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        print(request.form)
        email_address = request.form['email_address']
        password = request.form['password']
        print(email_address)
        print(password)
        db = handler.db()
        db.connect()
        db.insertId(email_address, password)
        db.close()
        return render_template('registered.html')
        

@app.route('/login', methods=['GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        email_address = request.form['email_address']
        password = request.form['password']
        print(email_address)
        print(password)
        # TODO emailとpasswordの確認
        db = handler.db()
        db.connect()
        selected = db.selectId(email_address)
        db.close()
        db_password = selected[2]
        indivi_id = selected[0]
        if password!=db_password:
            return render_template('login_fail.html')
        next_url_upload='/result/'+str(indivi_id)
        next_url_view='/view/'+str(indivi_id)
        return render_template('upload.html',next_url_upload=next_url_upload, next_url_view=next_url_view)

@app.route('/result/<int:indivi_id>', methods=['POST'])
def result(indivi_id):
    if request.method == 'POST':
        print('a')
        file = request.files['example']
        file.save(os.path.join('./static/image', file.filename))
        path = os.path.join('./static/image', file.filename)
        print(path)
        ret, nutri_dict,isSucceeded = cal_nutri_score(path)
        if isSucceeded==False:
            return render_template('nofood.html', text = ret,path = path)
        db = handler.db()
        db.connect()
        db.insertRecord(nutri_dict['calories'],nutri_dict['fat'],nutri_dict['protein'],nutri_dict['carbohydrates'],indivi_id)
        db.close()
        path = os.path.join('/image', file.filename)
        return render_template('uploaded_file.html', text = ret,path = path)

@app.route('/view/<int:indivi_id>',methods=['GET'])
def view(indivi_id):
    if request.method == 'GET':
        db = handler.db()
        db.connect()
        nutri_score = db.selectRecord(indivi_id)
        db.close()
        print(nutri_score)
        return render_template('cambas.html',nutri_score=nutri_score)

@app.route('/cambas', methods=['GET'])
def cambas():
    if request.method == 'GET':
        return render_template('cambas.html')
        

        

def cal_nutri_score(path):
    isSucceeded=True
    genai.configure(api_key="AIzaSyD9YFFyOY-jbEJ5PfqC5ufTvXfr0QRtBAE")
    model = genai.GenerativeModel('gemini-pro-vision')
    img = PIL.Image.open(path)
    response = model.generate_content([
    "Please calculate the nutrition score. Please answer this format 'calories : {calories}, fat : {fat}, protein : {protein}, carbohydrates : {carbohydrates}'. If there is no foods, please say 'NoFood'. ", 
    img
    ], stream=True)
    response.resolve()
    print(response.text)
    if response.text=='NoFood' or response.text==' NoFood':
        isSucceeded=False
        return response.text, '', isSucceeded
    response_spl = response.text.split(',')
    print(response_spl)
    nutri_dict={}
    nutri_key = ['calories','fat','protein','carbohydrates']
    for i in range(len(response_spl)):
        nutri_dict[nutri_key[i]] = re.sub(r"\D", "",response_spl[i].split(':')[1])
    print(nutri_dict) 
    return response.text, nutri_dict, isSucceeded

if __name__ == '__main__':
    app.run(debug=True)