
import requests as req

API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluQGV4YW1wbGUuY29tIiwiaWF0IjoxNjM5MzAyNzk5LCJleHAiOjE2NDE5MzA3OTksImp0aSI6ImZlNjllNTAyLWU2MGQtNDY3Mi1hNjkyLTk3YTg0ODE4ZDA4NSIsInVzZXJfaWQiOjEsIm9yaWdfaWF0IjoxNjM5MzAyNzk5fQ.JPVsFaOz7XjumqyTdWqDqUciSdJQzRH8LEX5swtPkwRMAxwXdI5SbKGWV1bDPVxJ7B6D3teW5rfk71lu0N8FutqCGicXnwreCQLNqLIyJgpkjxEm3KoZx2beFj1x5cvsDdZJnK8hWv4pBuiMvjmmqkDDaOpXLvZPHTIKslKU2S7_kGB96v63hRJppztnwsBLBYXifiwSL-PMZ6qJ5IORo81U_EiVRBmmMNDgftaRN5riWSYiEqmpYbmENq5t23EKEG-PA-HnhDaro2U5y96DMJy_TkjwgOHwn1dAGiBASoh3PHqEFVN9DLvIhW43YtIKnGDCt7vOYeVU143_JiKAbQ"

def send_mail(data):
    
    body = data["email-body"]
    recivers = data["email-receivers"]
    receivers  = data["email-receivers"]
    
    
    payload = {
            "subject":"Testing",
            "body": [
            "p> Hello",
            "p> You are receing this email as a test. Using a simple syntax, links and buttons cab be encorporated in emails via the janjas api.",
            "b> This is a link button to janjas.tk href> https://janjas.tk",
            "p> Below is a link",
            "a> This is a link to janjas.tk href> https://janjas.tk"
            ],
            "recipient_list":["jackkweyunga@gmail.com"],
            "emailer_name":"admin",
            "template_type":"follow_up",
            "api_key":"eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluQGV4YW1wbGUuY29tIiwiaWF0IjoxNjM4ODY0ODkzLCJleHAiOjE2NDE0OTI4OTMsImp0aSI6IjVlMzFjODlkLTQxMTYtNDRmYy05MjQwLWMwMDczNzI3MjZlOCIsInVzZXJfaWQiOjEsIm9yaWdfaWF0IjoxNjM4ODY0ODkzfQ.olJW2Obr6dtNNHyI703P7_0l0hAyWAcE2hRjz_ROL4AmEUmcgljZ0WQOH_dx4uBGslfEkiHuAkvsddGWTljzECe0ZPKvas8PFJKR18ebjYuKnPo_vi0Nc0DcSdLw88uPu85P7NeXz_l3KM4pwmu1TTiq6dHfjmuwIQaao6zvqS4LbNfxl17006TrpDpR9gBP1NZe_XSmUfmw1BwkDAV0V8CywTZTQPWYofPysBN9ISCnyO4C0DZj_hieS3nyRnL-jVmgnIF4OdawDSeXF8wJZzG7Di3SowVQvXmyYXOt1f_SZtt6J_ltGGfTK_A7lki4A6ESNnr8k1dglYCF6lJrsA"
            }
    
    data = req.post("https://udictimailer.herokuapp.com/send/", data=data)
    # print(data.text)
    return data