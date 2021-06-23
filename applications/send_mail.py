
import requests as req

def send_mail(data):
    headers={"Authorization":"Token "+ "5511bb046ac1cefb1129a17498d8c5c0786474d7"}
    data = req.post("https://udictimailer.herokuapp.com/send/", data=data, headers=headers)
    # print(data.text)
    return data