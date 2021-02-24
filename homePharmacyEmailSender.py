import homePharmacyEmailSenderService as service
import medicineWebSearch as webSearch
import schedule
import time

schedule.every().hour.do(webSearch.fill_drug_description())
schedule.every().hour.do(webSearch.alternatives_search())
schedule.every().hour.do(service.create_reminder_mail())
schedule.every().monday.do(service.create_out_of_date_mail())
schedule.every().day.at("10:00").do(service.create_vitamins_mail())
schedule.every().day.at("10:00").do(service.create_near_expiry_date_mail())


if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
