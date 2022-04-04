
import requests as req


class Data:
    
    def __init__(self, reason) -> None:
        self.reason = reason


def send_mail(data):
    
    body = data["email-body"]
    receivers = data["email-receiver"]
    subject  = data["email-subject"]
    
    
    payload = {
        "subject":subject,
        "body": body,
        "recipients":receivers,
        "template_type":"follow_up",
        "email_name":"udicti",
        "email_key":"ohhbcgI2H8gI"
        }
    
    print(payload)
    
    res = req.post("http://auth.janjas.ml/api/email/send_email/", data=payload)
    

    
    
    ret = Data(reason="")
    
    
    if res.status_code == 200:
        ret.reason = "OK"
    else:
        ret.reason = "FAILED"
        
    print(ret.reason)
        
    return ret

