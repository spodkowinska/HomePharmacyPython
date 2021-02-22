import homePharmacyEmailSenderService as service


if __name__ == '__main__':
    service.create_out_of_date_mail()
    service.create_near_expiry_date_mail()
    service.create_vitamins_mail()
