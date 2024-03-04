from flask import Flask, render_template, request, url_for, redirect
import os
import google.generativeai as genai
import PIL.Image

app = Flask(__name__)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # URLでhttp://127.0.0.1:5000/uploadを指定したときはGETリクエストとなるのでこっち
    if request.method == 'GET':
        return render_template('upload.html')
    # formでsubmitボタンが押されるとPOSTリクエストとなるのでこっち
    elif request.method == 'POST':
        file = request.files['example']
        file.save(os.path.join('./static/image', file.filename))
        path = os.path.join('./static/image', file.filename)
        ret = cal_nutri_score(path)
        return render_template('uploaded_file.html', text = ret,path = path)


def cal_nutri_score(path):
    genai.configure(api_key="AIzaSyD9YFFyOY-jbEJ5PfqC5ufTvXfr0QRtBAE")
    model = genai.GenerativeModel('gemini-pro-vision')
    img = PIL.Image.open(path)
    response = model.generate_content([
    "Please calculate the nutrition score. Please answer this format 'calories : {calories}, fat : {fat}, protein : {protein}, carbohydrates : {carbohydrates}'", 
    img
    ], stream=True)
    response.resolve()
    return response.text

if __name__ == '__main__':
    app.run(debug=True)