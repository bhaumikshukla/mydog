# mydog
A python dog to watch your Ubuntu laptop/machine access.
It watches auth.log file in Ubuntu Machine and let you know who interacted with your machine/laptop by taking picture from cam and send it over email.

### Following sequence of steps it performs:
* Watches /var/log/auth.log
* If any events related to authentication occurs (like Unlocked machine, authentication failure, wrong password input, etc), it will consider this as event
* If event, then it take a picture from the laptop camera / machine's webcam, prepares an email, attach image and send it to configured email address immidiately.

## Requirement
- Python2.7 & Python-pip
- cv2 package is required (not available in Pypi)
```
sudo apt-get update (if required)
sudo apt-get install python-opencv
```
### Install dependencies
```
pip install -r requirements.txt
```

## SMTP Configuration for email
Please provide your email ID and passwords in config.cfg file before running.
```
[config]
YOUR_EMAIL_ID=example@email.com
YOUR_EMAIL_PASSWORD=PASSWORD
EMAIL_TO=example@email.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```


## RUN
You can simply run as python application.
```
python dog.py
```
or you can configure as system job using *systemd*

### create system service file
```
vim /etc/systemd/system/mydog.service
```
mydog.service
```
[Service]
Type=simple
User=YOUR_SYSTEM_USER
WorkingDirectory=/PATH/TO/mydog
ExecStart=/usr/bin/python /PATH/TO/dog.py --option=123
Restart=on-abort
```

### Start/Stop service
```
sudo systemctl start mydog
```

ENJOY.  You will get Email with Picture of a person attached who accessed your laptop/machine 


