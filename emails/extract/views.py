from signal import raise_signal
from django.shortcuts import render
from django.http import HttpResponse
import imaplib
import email
# models
from extract.models import EmailData
from django.conf import settings
import os
import magic
  


# Create your views here.

def extract_email(request):

    imap_url = 'imap.gmail.com'
    my_mail = imaplib.IMAP4_SSL(imap_url)
    my_mail.login('awsjithu5@gmail.com','**********************')
    my_mail.select('Inbox')

    key = 'FROM'
    value = 'jithinbuasc@gmail.com'
    # below code is ued to filter the mail based on the 
    # the parameters
    k = key,value
    type_,data = my_mail.search(None,*k)
    # type which defining the type of the response ok or not
    mail_id_list = data[0].split()
    msgs = []
    for num in mail_id_list:
        _type,data= my_mail.fetch(num,'(RFC822)')
        # RFC822 IS an internet message access protocol
        msgs.append(data)
    # print(msgs)
    # msg contains a list of list , it contains the tuple inside of the list [[()]]

    for msg in msgs:
        for response_data in msg:
            if type(response_data) is tuple:
                '''the above line we can write like if isinstance(response_data,tuple):'''
                # my_message that contains two parts , header and payload
                # my_msg is an object that contains header ang payload
                # payload that contains the body of the mail means content
                my_msg = email.message_from_bytes(response_data[1])
                from_ = my_msg['from']
                emails = from_.split('<')
                from_email = emails[1].replace('>','')
                # print(from_email)
                subject = my_msg['subject']
                email_data =  EmailData(_from=from_email,subject=subject)
                # print(f'from {from_}')
                # print(f'subject: {subject}')
                #_____________________________________________________________________________
                # here we are printing the body part note that this body part from the payload
                for part in my_msg.walk():
                    # print(part.get_content_type())
                    # below code is the output for the # print(part.get_content_type())
                    # multipart/alternative
                    # text/plain
                    # text/html
                    if part.get_content_type()== 'text/plain':
                        body = part.get_payload()
                    # for file handling
                    file_name = part.get_filename()
                    if file_name:
                        print(file_name)
                        filePath = os.path.join(settings.BASE_DIR, 'files', file_name)
                        print(filePath)
                        # os.path.isfile() method in Python is used to check whether the specified path is an existing regular file or not
                        if not os.path.isfile(filePath) :
                            fp = open(filePath, 'wb')
                            # wb method writinge file
                            # if the file is not exist it will create the file
                            fp.write(part.get_payload(decode=True))
                            fp.close()
                            
                        
                if EmailData.objects.filter(_from=from_email,subject=subject,body=body).exists():
                    pass
                else:
                    email_data.body = body
                    email_data.save()
                

    return HttpResponse('hai')