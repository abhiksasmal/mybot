import requests
import json
from pdf2docx import Converter
token='5988714538:AAEfEtqb8RTwLXfUkGhV-yvA23hF64TSwU4'
url=f"https://api.telegram.org/bot{token}/"

def getupdate(stored_update):
    p={'offset':stored_update+1}
    resp=requests.get(f"{url}getUpdates",params=p)
    resp_dict=resp.json()
    with open ("update.json",'w') as file:
        json.dump(resp_dict,file, indent=3)
    larger_list=[]
    for update in resp_dict['result']:
        try:
            file_id = update['message']['document']['file_id']
            chat_id=update['message']['chat']['id']
            update_id=update['update_id']
            larger_list.append([file_id,chat_id,update_id])
        except:
            continue
    # print(larger_list)
    return larger_list


def get_file_path(file_id):
    file_id=file_id
    resp=requests.get(f"https://api.telegram.org/bot{token}/getFile?file_id={file_id}")
    resp_dict=resp.json()
    file_path=resp_dict['result']['file_path']
    return file_path

def download_file(file_path,chat_id):
    file_path=file_path
    chat_id=chat_id
    resp=requests.get(f"https://api.telegram.org/file/bot{token}/{file_path}").content
    with open(f"{chat_id}.pdf",'wb') as file:
        file.write(resp)

def convert_file(chat_id):
    pdf_file = f"{chat_id}.pdf"
    docx_file = f'{chat_id}.docx'
    cv = Converter(pdf_file)
    cv.convert(docx_file)      
    cv.close()


def sendfile(chat_id):
    chat_id=chat_id
    with open(f"{chat_id}.docx",'rb') as file:
    #     file_content=file
        file={'document': file}
        requests.post(f"{url}sendDocument?chat_id={chat_id}",files=file)
    print('inside_send')
# main

# with open("last_update.txt",'r') as file:

def main_function():
    with open("last_update.txt",'r') as file:
        stored_update=int(file.read())
    larger_list=getupdate(stored_update)
    if len(larger_list)>0:
            print(larger_list) 
    try:
        if larger_list[-1][-1]>stored_update:
            stored_update=larger_list[-1][-1]
        with open("last_update.txt",'w') as file:
            file.write(str(stored_update))
    except:
        pass

    for l in larger_list:
        file_id=l[0]
        chat_id=l[1]
        last_update_id=l[2]
        file_path=get_file_path(file_id)
        download_file(file_path,chat_id)
        convert_file(chat_id)
        sendfile(chat_id)
    #     print(file_id,chat_id,last_update_id,file_path)
    # with open("last_update.txt",'w') as file:
    #     file.write(str(last_update_id))

while True:
    try:
        main_function()
    except:
        continue