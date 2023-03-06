from prefect import flow, task

from iconic.service.customer_payment import CustomerPaymentService
from iconic.service.email import EmailService


@task
def query():
    result_1 = customer_payment_service.get_total_credit_card_revenue()
    result_2 = customer_payment_service.\
        get_percentage_of_customer_purchased_female_items_via_credit_cards()
    result_3 = customer_payment_service.get_average_revenue_for_customer_on_platform()
    result_4 = customer_payment_service.get_list_of_customers_for_men_luxury_brand_campaign()
    return result_1, result_2, result_3, result_4


@task
def send_email(result_1, result_2, result_3, result_4):
    message_input = {
        'cc_revenue': result_1,
        'cc_female_item_revenue': result_2,
        'avg_each_platform_revenue': result_3,
        'customer_campaign_list': result_4,
    }
    email_service.send_daily_report_email(message_input, receiver_email='danhvo.uit@gmail.com')


@flow(log_prints=True)
def report():
    result_1, result_2, result_3, result_4 = query()
    send_email(result_1, result_2, result_3, result_4)


if __name__ == '__main__':
    email_service = EmailService()
    customer_payment_service = CustomerPaymentService()
    report()
