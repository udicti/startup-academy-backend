
import requests as req

API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluQGV4YW1wbGUuY29tIiwiaWF0IjoxNjM5MzAyNzk5LCJleHAiOjE2NDE5MzA3OTksImp0aSI6ImZlNjllNTAyLWU2MGQtNDY3Mi1hNjkyLTk3YTg0ODE4ZDA4NSIsInVzZXJfaWQiOjEsIm9yaWdfaWF0IjoxNjM5MzAyNzk5fQ.JPVsFaOz7XjumqyTdWqDqUciSdJQzRH8LEX5swtPkwRMAxwXdI5SbKGWV1bDPVxJ7B6D3teW5rfk71lu0N8FutqCGicXnwreCQLNqLIyJgpkjxEm3KoZx2beFj1x5cvsDdZJnK8hWv4pBuiMvjmmqkDDaOpXLvZPHTIKslKU2S7_kGB96v63hRJppztnwsBLBYXifiwSL-PMZ6qJ5IORo81U_EiVRBmmMNDgftaRN5riWSYiEqmpYbmENq5t23EKEG-PA-HnhDaro2U5y96DMJy_TkjwgOHwn1dAGiBASoh3PHqEFVN9DLvIhW43YtIKnGDCt7vOYeVU143_JiKAbQ"

def send_mail(data):
    
    data["email-body"]
    data["email-body"]
    data["email-body"]
    data = req.post("https://udictimailer.herokuapp.com/send/", data=data)
    # print(data.text)
    return data