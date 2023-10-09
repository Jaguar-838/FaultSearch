import requests

_token='6019932064:AAEeXWnahlFx959i_j_t7MR5w9O_n3JVC-E'
_chat_id='-1001927552347' #Группа "репорты для ремонта"
#https://api.telegram.org/bot6019932064:AAEeXWnahlFx959i_j_t7MR5w9O_n3JVC-E/getUpdates
#Так можно узнать chat_id
def send_document(token=_token, chat_id=_chat_id, document_path=''):
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    with open(document_path, 'rb') as document_file:
        files = {'document': document_file}
        data = {'chat_id': chat_id}
        response = requests.post(url, files=files, data=data)
    return response.json()

def send_mess(token=_token, chat_id=_chat_id, text='0'):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.post(url, data=data)
    return response.json()