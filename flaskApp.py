from flask import Flask # flask를 import 한다.
app = Flask(__name__,template_folder='static/FrontEnd') # 항상 기본적으로 선언되는 app 변수

@app.route('/') # route 안에는 실제 이동하고자 하는 url를 입력한다.
def home():
    return 'Hello, World!' # url를 방문했을 때 display할 내용을 return 시켜주자.

if __name__ == '__main__':
    app.run(debug=True) 