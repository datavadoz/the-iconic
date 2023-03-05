from iconic.model.customer_payment import CustomerPaymentModel
from iconic.service.base import BaseService


class CustomerPaymentService(BaseService):
    @staticmethod
    def get_customer_payment_schema():
        return CustomerPaymentModel.get_schema_dict()

    def upsert_df(self, df):
        self.db.upsert_df(df, CustomerPaymentModel)
