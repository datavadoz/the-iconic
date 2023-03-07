from iconic.model.customer_payment import CustomerPaymentModel
from iconic.service.base import BaseService


class CustomerPaymentService(BaseService):
    @staticmethod
    def get_customer_payment_schema():
        return CustomerPaymentModel.get_schema_dict()

    def upsert_df(self, df):
        self.db.upsert_df(df, CustomerPaymentModel)

    def get_total_credit_card_revenue(self):
        stmt = """
        SELECT ROUND(SUM(revenue)) AS revenue
        FROM customer_payment
        WHERE cc_payments <> 0
        """
        result = self.db.query(stmt)
        return int(result[0][0])

    def get_percentage_of_customer_purchased_female_items_via_credit_cards(self):
        stmt = """
        SELECT COUNT(*) / (SELECT COUNT(*) FROM customer_payment)::float * 100 AS percentage
        FROM customer_payment
        WHERE cc_payments <> 0 AND female_items <> 0
        """
        result = self.db.query(stmt)
        return result[0][0]

    def get_average_revenue_for_customer_on_platform(self):
        stmt = """
        WITH _avg_revenue_ios_customer AS (
            SELECT 'ios' AS platform, ROUND(AVG(revenue)) AS avg_revenue
            FROM customer_payment
            WHERE ios_orders <> 0
        ), _avg_revenue_android_customer AS (
            SELECT 'android' AS platform, ROUND(AVG(revenue)) AS avg_revenue
            FROM customer_payment
            WHERE android_orders <> 0
        ), _avg_revenue_desktop_customer AS (
            SELECT 'desktop' AS platform, ROUND(AVG(revenue)) AS avg_revenue
            FROM customer_payment
            WHERE desktop_orders <> 0
        )

        SELECT *
        FROM (SELECT * FROM _avg_revenue_ios_customer) AS ios
        UNION (SELECT * FROM _avg_revenue_android_customer)
        UNION (SELECT * FROM _avg_revenue_desktop_customer)
        """
        result = self.db.query(stmt)
        result = {row[0]: int(row[1]) for row in result}
        return result

    def get_list_of_customers_for_men_luxury_brand_campaign(self):
        stmt = """
        SELECT customer_id
        FROM customer_payment
        WHERE male_items <> 0
        """
        result = self.db.query(stmt)
        result = [row[0] for row in result]
        return result
