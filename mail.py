# libraries to be imported
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import ConfigParser

#reading config
configParser = ConfigParser.RawConfigParser()   
configFilePath = r'config.cfg'
configParser.read(configFilePath)

'''
Gmail ID and password
'''
MY_GMAIL_ID = configParser.get('config','YOUR_EMAIL_ID')
MY_GMAIL_PASSWORD = configParser.get('config','YOUR_EMAIL_PASSWORD')
SMTP_HOST = configParser.get('config','SMTP_HOST')
SMTP_PORT = configParser.get('config','SMTP_PORT')

def sendmail(fromaddr=MY_GMAIL_ID,toaddr="", body="Laptop unlocked or accessed", subject = "Laptop unlocked or accessed at ",file = None):
	  
	# instance of MIMEMultipart
	msg = MIMEMultipart()
	 
	# storing the senders email address  
	msg['From'] = fromaddr
	 
	# storing the receivers email address 
	msg['To'] = toaddr
	 
	# storing the subject 
	msg['Subject'] = subject
	 
	# string to store the body of the mail
	body = body
	 
	# attach the body with the msg instance
	msg.attach(MIMEText(body, 'plain'))
	 
	
	if file is not None: 
		# open the file to be sent 
		filename = "image.png"
		attachment = open(file, "rb")
		# instance of MIMEBase and named as p
		p = MIMEBase('application', 'octet-stream')
		 
		# To change the payload into encoded form
		p.set_payload((attachment).read())
		 
		# encode into base64
		encoders.encode_base64(p)
		  
		p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
		 
		# attach the instance 'p' to instance 'msg'
		msg.attach(p)
	
	try:	 
		# creates SMTP session
		s = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
		 
		# start TLS for security
		s.starttls()
		
		# Authentication, put your gmail PASSWORD
		s.login(fromaddr, MY_GMAIL_PASSWORD)
		 
		# Converts the Multipart msg into a string
		text = msg.as_string()
		 
		# sending the mail
		s.sendmail(fromaddr, toaddr, text)
		 
		# terminating the session
		s.quit()
		print "Email sent to: %s" % toaddr
		return True
	except Exception as e:
		print "Something went wrong while sending email", e
		return False
