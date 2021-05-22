import smtplib
import imghdr
from email.message import EmailMessage
import pandas as pd
from datetime import datetime

def mail(to,attachment,date,time):
    df=pd.read_csv('Student List.csv')
    student_name=list(df.loc[df['SRN'] == to].Name)
    EMAIL_ADDRESS=''
    EMAIL_PASSWORD=''
    msg = EmailMessage()
    msg['Subject'] = 'Mask Cop Alert!!!'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to.lower()+'@cit.reva.edu.in'

    msg.set_content(f'Dear {student_name[0]},\nAs you know, the country is currently taking measures to respond to COVID-19.\nThe Organization is also considering methods to protect our members following guidance from the governmental authorities. In line with those safety measures, we are providing this service regarding the use of face coverings to prevent the spread of COVID-19.\nIt has come to our notice that you have been found violating the Covid Protocols on {date} at {time} inside the premises of the Organization. So you have been imposed with a fine of Rs. 250/- for the violation. If the violation is repeated severe action will be taken.\nPlease find the attachment for the proclamation made, if there are any discrepancies contact our Team.\nYours truly,\nTeam MaskCop')

    with open(str(attachment),'rb') as f:
        file_data=f.read()
        file_type=imghdr.what(f.name)
        file_name=f.name

    msg.add_attachment(file_data,maintype='image',subtype=file_type,filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

def sendmail():
    df=pd.read_csv('Email.csv')
    df=df.drop_duplicates(subset=['Unnamed: 0'])
    SRN=list(df['Unnamed: 0'])
    filename=list(df['0'])

    for i in range(0,len(SRN)):
        timestamp=filename[i]
        dt= timestamp[:-4]
        date=datetime.strptime(dt,'%d_%m_%Y_%H_%M_%S').strftime("%d-%m-%Y")
        time=datetime.strptime(dt,'%d_%m_%Y_%H_%M_%S').strftime("%H:%M:%S")
        mail(SRN[i],filename[i],date,time)
