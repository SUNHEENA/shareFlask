import pandas as pd
from flask import Flask, render_template
import pandas
import pymysql
import dbHandling
from flask import Flask, request
from flask.json import jsonify
from flask.templating import render_template
from flask import Flask, redirect, url_for
import logging
import MyEnDecryption
app = Flask(__name__, template_folder='static/FrontEnd')
accountUser = MyEnDecryption.decrypt_account('mysqlUser','userAcount')
def loopDataWithGoogleChart(inputList : dict):
    ##디폴트값 세트
    resultData = [['Task', 'Page Count']]
    for keyList in inputList:
        tmpList=list()
        tmpList.append(keyList)
        tmpList.append(inputList[keyList])
        resultData.append(tmpList)
    return resultData

@app.route('/')
def home():
    db = dbHandling.DB()
    countList = db.mainLogin()
    db.insertSiteCount("MAIN",str(countList['MAIN']+1))
    del db
    data = loopDataWithGoogleChart(countList)
    # data = [['Task', 'Hours per Day'],['Main', countList['MAIN']],
    #         ['index2', countList['idx2']],['DataFrame', countList['dff']],['MySQL', countList['mysql']],['Chart', countList['cht']]]
    return render_template('index.html', charData=data)

@app.route('/index2')
def home2():
    db = dbHandling.DB()
    r = db.getData("idx2")
    db.insertSiteCount("idx2", str(r + 1))
    return render_template('index2.html')

@app.route('/pandas')
def home3():
    db = dbHandling.DB()
    r = db.getData("dff")
    db.insertSiteCount("dff", str(r + 1))
    df = pd.read_excel('C:/판다스실습/명단파일.xls')
    df_html = df.to_html()
    return df_html

@app.route('/df_site')
def pandasLink():
    db = dbHandling.DB()
    r = db.getData("dff")
    db.insertSiteCount("dff", str(r + 1))
    del db
    df = pd.read_excel(r'C:/Users\suhna/jupyter_notebook_Source/python_intermediate/im_test_문서/IM_TEST_DF1.xlsx')
    return render_template('df_site.html',  tables=[df.to_html(classes='data', header="true", index=False)])

@app.route('/mysql_test')
def sqllink():
    db = dbHandling.DB()
    r = db.getData("mysql")
    db.insertSiteCount("mysql", str(r + 1))
    juso_db = pymysql.connect(
     user=accountUser[0], #아이디
     passwd=accountUser[1], #패스워드
     host='KRK4OFLTP00765', #cmd 에서 hostname 넣으시거나 localhost, ipv4 주소 
     db='flask_db', #스키마 이름
     charset='utf8'
    )
    cursor = juso_db.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM usertable as a left join userinfo_sec as b on a.badge=b.badge "
    cursor.execute(sql)
    result = cursor.fetchall()
    df = pd.DataFrame(result)
    juso_db.close()
    cursor.close()
    return render_template('mysql_test.html',  tables=[df.to_html(classes='data', header="true", index=False)])

@app.route('/chart')
def chartLink():
    db = dbHandling.DB()
    r = db.getData("cht")
    db.insertSiteCount("cht", str(r + 1))
    candleData = [
        ['Mon', 20, 28, 38, 45],
        ['Tue', 31, 38, 55, 66],
        ['Wed', 50, 55, 77, 80],
        ['Thu', 77, 77, 66, 50],
        ['Fri', 68, 66, 22, 15]]
    return render_template("chart_sample.html", chartData=candleData)


@app.route('/pyscript')
def pyScriptSample():
    return render_template('pyscript.html',)

##TABLE 실습예제
@app.route('/tableUpdate')
def emp():
    db = dbHandling.DB()
    cntList = db.getSample("")
    return render_template("tableTest.html", cntList=cntList)

#insert ajax 통신을 위한 구문
@app.route('/ins.ajax', methods=['POST'])
def ins_ajax():
    data = request.get_json()
    type = data['type']
    count = data['cnt']
    db = dbHandling.DB()
    cnt = db.insertSite(type,count)
    result = "success" if cnt==1 else "fail"
    return jsonify({'msg': result})



#delete를 위한 구문
@app.route('/del.ajax', methods=['POST'])
def del_ajax():
    data = request.get_json()
    type = data['type']
    db = dbHandling.DB()
    cnt = db.deleteType(type)
    result = "success" if cnt==1 else "fail"
    return jsonify({'msg': result})

##get 하는 주소 GET이 기본 셋팅임.
@app.route('/getTest', methods=['GET'])
def getterSetter():
    parameter_dict = request.args.to_dict()
    if len(parameter_dict) == 0:
        return 'No parameter'

    parameters = ''
    for key in parameter_dict.keys():
        parameters += 'key: {}, value: {}\n'.format(key, request.args[key])
    db = dbHandling.DB()
    cntList = db.getSample(parameter_dict['name'])
    return jsonify(cntList)

##나는 가져오는 부분
@app.route('/getallData', methods=['GET'])
def read_data():
    return jsonify({'msgReturn': '요고 들어온 겁니다.'})

@app.route('/onlySTRING', methods=['GET'])
def onlyStringReturn():
    return '아주 심플하죠\n이런것도 먹습니다'
    
## GET API SAMPLE##
@app.route('/silsoupSample')
def read_data_userInfo():
    parameter_dict = request.args.to_dict()
    if len(parameter_dict) == 0:
        return 'No parameter'

    parameters = ''
    for key in parameter_dict.keys():
        parameters += 'key: {}, value: {}\n'.format(key, request.args[key])
    db = dbHandling.DB()
    cntList = db.getSampleUserInfo(parameter_dict['name'])
    return jsonify(cntList)
## POST API SAMPLE##
@app.route('/deleteData', methods=['POST'])
def deleteWithWeb():
    result = ''
    parameter_dict = request.args.to_dict()
    if len(parameter_dict) == 0:
        return 'No parameter'
    parameters = ''
    for key in parameter_dict.keys():
        parameters += 'key: {}, value: {}\n'.format(key, request.args[key])
    result = parameter_dict['para']
    return result
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

if __name__ == '__main__':
    app.run(host='KRK4OFLTP00765', port=9874,debug=True) # debug = True는 해당 파일의 코드를 수정할 때마다 Flask가 변경된 것을 인식하고 다시 시작한다.