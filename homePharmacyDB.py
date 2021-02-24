import mysql.connector
from datetime import date

connection = mysql.connector.connect(host='localhost', port='3306', user='root', password='root', database='home_pharmacy')

def find_name_and_email(user_id):
    query = ("SELECT name, email FROM users WHERE id = %s")
    cursor = connection.cursor()
    cursor.execute(query, (user_id,))
    email_and_name = cursor.fetchone()
    return email_and_name


def are_drugs_expired(date):
    query = ("SELECT m.user_id, m.name, SUM(mi.quantity_left) FROM medicines as m LEFT JOIN medicine_instances as mi "
             "ON m.id = mi.medicine_id WHERE mi.expiry_date = %s GROUP BY m.id")
    cursor = connection.cursor()
    cursor.execute(query, (date,))
    medicine_with_quantity = cursor.fetchall()
    return medicine_with_quantity


def vitamins_to_expire(date):
    query = ("SELECT m.user_id, m.name, SUM(mi.quantity_left) FROM medicines as m LEFT JOIN medicine_instances as mi "
             "ON m.id = mi.medicine_id WHERE mi.expiry_date = %s and m.is_vitamin = true GROUP BY m.id")
    cursor = connection.cursor()
    cursor.execute(query, (date,))
    vitamins = cursor.fetchall()
    return vitamins


def find_drug_to_search_alternative():
    query = ("SELECT m.id, m.name FROM medicines as m WHERE m.alternative_searched is NULL")
    cursor = connection.cursor()
    cursor.execute(query)
    drugs_to_search = cursor.fetchall()
    query = ("UPDATE medicines SET alternative_searched = %s WHERE id = %s")
    today = date.today().strftime("%Y-%m-%d")
    cursor = connection.cursor()
    for drug in drugs_to_search:
        cursor.execute(query, (today, drug[0],))
    return drugs_to_search


def save_alternative(alternative):
    query = ("SELECT name, medicine_id FROM medicine_alternatives")
    cursor = connection.cursor()
    cursor.execute(query)
    drugs_to_search = cursor.fetchall()
    name_to_search = (alternative["name"],alternative["medicine_id"],)
    print(name_to_search)
    if name_to_search not in drugs_to_search:
        query = ("INSERT INTO medicine_alternatives VALUES (null, %s, %s, %s, %s, %s, %s, %s)")
        cursor = connection.cursor()
        cursor.execute(query, (alternative["description"], alternative["is_antibiotic"], alternative["is_prescription_needed"],
                           alternative["is_steroid"], alternative["name"], alternative["url_link"], alternative["medicine_id"],))
        connection.commit()

def save_description(drug_id, description):
    query = ("UPDATE medicines SET description = %s WHERE id = %s")
    cursor = connection.cursor()
    cursor.execute(query, (description, drug_id,))
    connection.commit()

def find_empty_descriptions():
    query = ("SELECT name, id FROM medicines WHERE (medicines.description is NULL or medicines.description = '')")
    cursor = connection.cursor()
    cursor.execute(query)
    drugs_to_search = cursor.fetchall()
    return drugs_to_search

def save_additional_info(json):
        query = ("UPDATE medicines SET is_prescription_needed = %s, is_steroid= %s, is_antibiotic= %s WHERE id = %s")
        cursor = connection.cursor()
        cursor.execute(query, (json["is_prescription_needed"], json["is_steroid"], json["is_antibiotic"], json["id"],))
        connection.commit()
