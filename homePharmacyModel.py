import smtplib, ssl


messageExpiryDate = """\
Subject: Some drugs are going to expire soon
Dear {user_name},
Your drug {name} in amount of {amount} is going to expire in {days} days.

Remember not to throw the package 
and rest of drug in to the bin but take it 
to the closest pharmacy's special containers.

Take care of your health and your planet.
Your HomePharmacy Team"""


messageVitamins = """\
Subject: Your vitamins are still in time 
Dear {user_name},
Your vitamins: {name} in amount of {amount} 
are going to expire in less than 30 days.

Maybe that's the best time to think about some additional supplementation?

Stay healthy and full of energy!
Your HomePharmacy Team"""


messageOutOfDate = """\
Subject: Expired drugs in your medicine cabinet 
Dear {user_name},
Your drug {name} in amount {amount} is expired. 

Out of date drugs are not properly tested and 
their effect on people is difficult to predict. 
Do not risk your health by using them.

Remember not to throw the package 
and rest of drug in to the bin but take it 
to the closest pharmacy's special containers.

Take care of your health and your planet.
Your HomePharmacy Team"""

port = 465
password = "homepharmacy123$"
context = ssl.create_default_context()
sender_email = "home.pharmacy.application@gmail.com"

