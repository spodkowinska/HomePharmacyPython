import smtplib, ssl

port = 465
password = input("Type your password and press enter: ")
context = ssl.create_default_context()

sender_email = "home.pharmacy.application@gmail.com"
receiver_email = "spodkowinska@gmail.com"
messageExpiryDate = """\
Subject: Some drugs are going to expire soon
Your drug {name} is going to expire in {days} days.
Remember not to throw the package and rest of drug in to the bin 
but take it to the closest pharmacy's special containers.
Take care of your health and your planet."""
messageVitamins = """\
Subject: Your vitamins are still in time 
Your {name} is going to expire in less than 30 days.
Maybe that's the best time to think about some suplementation?
Stay healthy and full of energy!"""
messageOutOfDate = """\
Subject: Expired drugs in your medicine cabinet 
Your drug {name} is expired. Out of date drugs are not tested 
and their effect on people is difficult to predict. 
Do not risk your health by using them.
Remember not to throw the package and rest of drug in to the bin 
but take it to the closest pharmacy's special containers.
Take care of your health and your planet."""
if __name__ == '__main__':
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)