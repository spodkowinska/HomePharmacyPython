import mysql.connector

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


def save_alternative(alternative):
    query = ("INSERT INTO medicine_alternatives VALUES (null, %s, %s, %s, %s, %s, %s, %s)")
    cursor = connection.cursor()
    cursor.execute(query, (alternative["description"], alternative["is_antibiotic"], alternative["is_prescription_needed"],
                           alternative["is_steroid"], alternative["name"], alternative["url_link"], alternative["medicine_id"],))
    connection.commit()