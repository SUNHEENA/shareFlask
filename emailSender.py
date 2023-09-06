
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email.utils import formatdate

def mainEmail(toAdd : str):
    style = """ .t2{font-size:10pt; font-family:"맑은 고딕"}
                                .t3{font-size:11pt; font-family:"맑은 고딕"}
                                .dataframe  {font-size: 11pt; font-family: Arial; border: 1px solid; border-color:black; border-collapse: collapse;text-align:center;}
                                .dataframe th {padding: 5px; background-color:rgb(204,217,255); border-color:black; border-collapse: collapse;}
                                .dataframe  td {padding: 5px; border-color:black; border-collapse: collapse;}"""
    html = """<html>
                                <head><style> {0} </style></head>
                                <body>
                                    <div class="t2"> 
                                    ▣ 안녕하세요 ㅎㅎ 저는 web 입니다.<br><br> 
                                  </div>""".format(style)
    msg = MIMEMultipart()
    msgAlternative = MIMEMultipart('alternative')
    msg['From'] = 'SystemAdmin'
    msg['To'] =toAdd
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = Header(s='flask web에서 버튼을 눌러서 간 메일 입니다.', charset='utf-8')
    msgText = MIMEText(html, 'html')
    msgAlternative.attach(msgText)
    msg.attach(msgAlternative)
    smtp_server = "k1mh02.amkor.co.kr"
    port = 25
    s = smtplib.SMTP(smtp_server, port)
    s.send_message(msg)
    s.quit()
    return 'sucess'