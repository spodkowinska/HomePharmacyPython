import homePharmacyDB as db
import homePharmacyModel as model
import smtplib
from datetime import datetime, timedelta


def create_message_expiry_date(user_name, name, amount, days):
        message = model.messageExpiryDate.format(user_name = user_name, name = name, amount = amount, days = days)
        return message


def create_message_out_of_date(user_name, name, amount):
    message = model.messageOutOfDate.format(user_name=user_name, name=name, amount=amount)
    return message

def create_message_vitamins(user_name, name, amount):
    message = model.messageVitamins.format(user_name=user_name, name=name, amount=amount)
    return message


def find_name_and_email(user_id):
        return db.find_name_and_email(user_id)

def are_drugs_expired(date):
        return db.are_drugs_expired(date)

# add link with possibility to remove out of date instance

def create_out_of_date_mail():
    today = datetime.today()
    drugs_expired = are_drugs_expired(today.strftime('%Y-%m-%d'))
    if drugs_expired is not None:
        for drugs_expired_row in drugs_expired:
            with smtplib.SMTP_SSL("smtp.gmail.com", model.port, context=model.context) as server:
                server.login(model.sender_email, model.password)
                name_and_email = find_name_and_email(int(drugs_expired_row[0]))
                server.sendmail(model.sender_email, name_and_email[1], create_message_out_of_date(name_and_email[0]
                            ,drugs_expired_row[1], drugs_expired_row[2]))


def create_near_expiry_date_mail():
    today = datetime.today()
    days = 14
    expiry_date = today + timedelta(days=days)
    drugs_expired = are_drugs_expired(expiry_date.strftime('%Y-%m-%d'))
    if drugs_expired is not None:
        for drugs_expired_row in drugs_expired:
            with smtplib.SMTP_SSL("smtp.gmail.com", model.port, context=model.context) as server:
                server.login(model.sender_email, model.password)
                name_and_email = find_name_and_email(int(drugs_expired_row[0]))
                server.sendmail(model.sender_email, name_and_email[1], create_message_expiry_date(name_and_email[0]
                            ,drugs_expired_row[1], drugs_expired_row[2], days))


def create_vitamins_mail():
    today = datetime.today()
    days = 30
    expiry_date = today + timedelta(days=days)
    vitamins = db.vitamins_to_expire(expiry_date.strftime('%Y-%m-%d'))
    if vitamins is not None:
        for vitamins_row in vitamins:
            with smtplib.SMTP_SSL("smtp.gmail.com", model.port, context=model.context) as server:
                server.login(model.sender_email, model.password)
                name_and_email = find_name_and_email(int(vitamins_row[0]))
                server.sendmail(model.sender_email, name_and_email[1], create_message_vitamins(name_and_email[0]
                            ,vitamins_row[1], vitamins_row[2]))

def create_reminder_mail():
    today = datetime.today()
