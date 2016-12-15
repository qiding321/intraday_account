# -*- coding: utf-8 -*-
"""
Created on 2016/12/14 9:12

@version: python3.5
@author: qiding
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header

def email():
    server="smtp.exmail.qq.com"
    sender = 'guangy@mingshiim.com'
    print "type in psw: "
    psw=raw_input()

    ############### info 1 ################
    receiver_main='account@mingshiim.com'
    receiver_cc1='dqi@mingshiim.com'
    receiver_cc2='Stephan.zhou@mingshiim.com'
    receivers = [receiver_main, receiver_cc1, receiver_cc2, sender]

    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver_main
    subject = 'T0 accounts ' + today.strftime("%Y-%m-%d") + ' auto_sent_by_Python'
    message['Subject'] = Header(subject, 'utf-8')

    message.attach(MIMEText('Dear all,\n\nPlease see the attached T0 trading reports for Account 1, 2, 4, 5, 7, 8, 16, 19, 101, 102.\n\nCheers,\nGuang', 'plain', 'utf-8'))

    os.system('e:')
    os.system('cd ' + exe_path)
    att1 = MIMEApplication(open('t0_Print.xlsx', 'rb').read())
    att1.add_header('Content-Disposition', 'attachment', filename="t0_Print.xlsx")
    message.attach(att1)

    ############### info 2 ################
    receiver_sp1 = 'lixd@tailaifund.com'
    receiver_sp2 = 'yilj@tailaifund.com'
    receiver_sp3 = 'product@tailaifund.com'
    receivers_sp = [receiver_sp1,  receiver_sp2, receiver_sp3, sender]
    message_sp = MIMEMultipart()
    message_sp['From'] = sender
    message_sp['To'] = sender
    subject_sp = 'Summary of Account 7 on ' + today.strftime("%Y-%m-%d") + ' auto_sent_by_Mingshi'
    message_sp['Subject'] = Header(subject_sp, 'utf-8')
    message_sp.attach(MIMEText('Dear all,\n\nPlease see the attached reports for Account 7.\n\nCheers,\nGuang@Mingshi', 'plain', 'utf-8'))

    att1_sp = MIMEText(open('E:\\Development\\Intraday\\NO7\\7t0report.csv', 'rb').read())
    att1_sp.add_header('Content-Disposition', 'attachment', filename="7t0_report.csv")
    message_sp.attach(att1_sp)

    att1p_sp = MIMEText(open('E:\\Development\\Intraday\\NO7\\' + today.strftime("%Y-%m-%d") + '\\event_tl.csv', 'rb').read())
    att1p_sp.add_header('Content-Disposition', 'attachment', filename="7t0_event_tl.csv")
    message_sp.attach(att1p_sp)

    path_att2, file_name_att2, valuation_date= find_attach2()
    att2_sp = MIMEApplication(open(path_att2, 'rb').read())
    print "Please check the file name for Account 7: " + file_name_att2
    raw_input("Press any key after you check the file name.")
    table_name = "MSLH07_VALUATION_"+valuation_date+".xls"
    att2_sp.add_header('Content-Disposition', 'attachment', filename=table_name)
    message_sp.attach(att2_sp)

    try:
        smtpObj = smtplib.SMTP(server)
        smtpObj.login(sender, psw)
        ############### info 1 ################
        smtpObj.sendmail(sender, receivers, message.as_string())

        ############### info 2 ################
        smtpObj.sendmail(sender, receivers_sp, message_sp.as_string())

        print "emails sent!"
        smtpObj.close()
    except smtplib.SMTPException:
        print "Error: cannot send emails"

