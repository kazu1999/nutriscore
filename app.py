from flask import Flask, render_template, request, url_for, redirect
import os
import google.generativeai as genai
import PIL.Image
import re
import pandas as pd
import datetime
from sql import handler

app = Flask(__name__, static_folder='./static/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        email_address = request.form['email_address']
        password = request.form['password']
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
        db = handler.db()
        db.connect()
        selected = db.selectId(email_address)
        db.close()
        db_password = selected[2]
        indivi_id = selected[0]
        if password!=db_password:
            return render_template('login_fail.html')
        next_url_upload='/result/'+str(indivi_id)
        next_url_view_today = '/view/today/'+str(indivi_id)
        next_url_view_calories = '/view/calories/'+str(indivi_id)
        next_url_view_fat = '/view/fat/'+str(indivi_id)
        next_url_view_protein = '/view/protein/'+str(indivi_id)
        next_url_view_carbohydrates = '/view/carbohydrates/'+str(indivi_id)
        return render_template('upload.html',next_url_upload=next_url_upload,\
        next_url_view_today=next_url_view_today, next_url_view_calories=next_url_view_calories, next_url_view_fat=next_url_view_fat,\
        next_url_view_protein=next_url_view_protein, next_url_view_carbohydrates=next_url_view_carbohydrates)


@app.route('/upload/<int:indivi_id>', methods=['GET'])
def upload_back(indivi_id):
    if request.method == 'GET':
        next_url_upload='/upload/'+str(indivi_id)
        next_url_view_today = '/view/today/'+str(indivi_id)
        next_url_view_calories = '/view/calories/'+str(indivi_id)
        next_url_view_fat = '/view/fat/'+str(indivi_id)
        next_url_view_protein = '/view/protein/'+str(indivi_id)
        next_url_view_carbohydrates = '/view/carbohydrates/'+str(indivi_id)
        return render_template('upload.html',next_url_upload=next_url_upload, \
        next_url_view_today=next_url_view_today, next_url_view_calories=next_url_view_calories, next_url_view_fat=next_url_view_fat,\
        next_url_view_protein=next_url_view_protein, next_url_view_carbohydrates=next_url_view_carbohydrates)



@app.route('/result/<int:indivi_id>', methods=['POST'])
def result(indivi_id):
    if request.method == 'POST':
        file = request.files['example']
        file.save(os.path.join('./static/image', file.filename))
        path = os.path.join('./static/image', file.filename)
        ret, nutri_dict,isSucceeded = cal_nutri_score(path)
        if isSucceeded==False:
            return render_template('nofood.html', text = ret,path = path)
        db = handler.db()
        db.connect()
        db.insertRecord(nutri_dict['calories'],nutri_dict['fat'],nutri_dict['protein'],nutri_dict['carbohydrates'],indivi_id)
        db.close()
        path = os.path.join('/image', file.filename)
        next_url_upload='/upload/'+str(indivi_id)
        next_url_view_today = '/view/today/'+str(indivi_id)
        next_url_view_calories = '/view/calories/'+str(indivi_id)
        next_url_view_fat = '/view/fat/'+str(indivi_id)
        next_url_view_protein = '/view/protein/'+str(indivi_id)
        next_url_view_carbohydrates = '/view/carbohydrates/'+str(indivi_id)
        return render_template('uploaded_file.html', text = ret,path = path, next_url_upload=next_url_upload, \
        next_url_view_today=next_url_view_today, next_url_view_calories=next_url_view_calories, next_url_view_fat=next_url_view_fat,\
        next_url_view_protein=next_url_view_protein, next_url_view_carbohydrates=next_url_view_carbohydrates)


@app.route('/view/today/<int:indivi_id>',methods=['GET'])
def view_today(indivi_id):
    if request.method == 'GET':
        db = handler.db()
        db.connect()
        record = db.selectRecord(indivi_id)
        db.close()
        df = pd.DataFrame(record)
        df['dt_time'] = pd.to_datetime(df['time'])
        today = datetime.datetime.now() 
        df = df[df['dt_time']>datetime.datetime(today.year,today.month,today.day)]
        df['date'] = df['dt_time'].dt.strftime('%Y-%m-%d')
        df_nutri = df[['calories','fat','protein','carbohydrates','date']]
        df_agg = df_nutri.groupby('date').sum()
        calories = df_agg['calories'].to_list()
        fat = df_agg['fat'].to_list()
        protein = df_agg['protein'].to_list()
        carbohydrates = df_agg['carbohydrates'].to_list()

        if len(df_agg)==0:
            calories.append(0)
            fat.append(0)
            protein.append(0)
            carbohydrates.append(0)

        labels = ['calories','fat','protein','carohydrates']
        data = [calories[0],fat[0],protein[0],carbohydrates[0]]

        return render_template('today_result.html',labels=labels, data=data)



@app.route('/view/<category>/<int:indivi_id>',methods=['GET'])
def view_week(indivi_id, category):
    print(category)
    if request.method == 'GET':
        db = handler.db()
        db.connect()
        record = db.selectRecord(indivi_id)
        db.close()

        df = pd.DataFrame(record)
        df['dt_time'] = pd.to_datetime(df['time'])

        one_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        df = df[df['dt_time']>datetime.datetime(one_week_ago.year,one_week_ago.month,one_week_ago.day)]
        df['date'] = df['dt_time'].dt.strftime('%Y-%m-%d')
        df_nutri = df[['calories','fat','protein','carbohydrates','date']]
        df_agg = df_nutri.groupby('date').sum()
        date = df_agg.index.to_list()
        data = df_agg[category].to_list()

        if len(df_agg)==0:
            date.append(0)
            data.append(0)
        
        return render_template('chartjs-example.html',labels=date, data=data,category=category)


def cal_nutri_score(path):
    isSucceeded=True
    genai.configure(api_key="AIzaSyD9YFFyOY-jbEJ5PfqC5ufTvXfr0QRtBAE")
    model = genai.GenerativeModel('gemini-pro-vision')
    img = PIL.Image.open(path)
    response = model.generate_content([
    "Please calculate the nutrition score of the food in this picture. Please answer this format 'calories : {calories}, fat : {fat}, protein : {protein}, carbohydrates : {carbohydrates}'. And don't write anything other than this format ", 
    img
    ], stream=True)
    response.resolve()
    response_spl = response.text.split(',')
    #これのlenでfood non food振り分け
    nutri_dict={}
    nutri_key = ['calories','fat','protein','carbohydrates']
    for i in range(len(response_spl)):
        nutri_dict[nutri_key[i]] = re.sub(r"\D", "",response_spl[i].split(':')[1])
    print(nutri_dict) 
    return response.text, nutri_dict, isSucceeded


if __name__ == '__main__':
    app.run(debug=True)