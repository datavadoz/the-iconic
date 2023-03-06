import smtplib
import ssl
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd

from iconic.service.resource import ResourceService


class EmailService(ResourceService):
    def __init__(self, sender_email='danhvo.uit@gmail.com'):
        super().__init__()
        self.port = 465
        self.host = 'smtp.gmail.com'
        self.sender_email = sender_email

    def _get_password(self, email_address):
        return self.get_resource_password(email_address)

    def _send_email(self, receiver_email, message):
        context = ssl.create_default_context()
        sender_password = self.get_resource_password(self.sender_email)

        with smtplib.SMTP_SSL(self.host, self.port, context=context) as server:
            server.login(self.sender_email, sender_password)
            server.sendmail(self.sender_email, receiver_email, message.as_string())

    def send_daily_report_email(self, message_input, receiver_email):
        today_str = datetime.today().strftime('%m/%d/%Y')
        message = MIMEMultipart("alternative")
        message["Subject"] = f"[Daily Report] {today_str}"
        message["From"] = self.sender_email
        message["To"] = receiver_email

        html = f"""\
        <html>
            <body>
                <p>Hi,</p>
                <p>Revenue report:</p>
                <table>
                    <tr>
                        <th>Item</th>
                        <th>Revenue</th>
                    </tr>
                    <tr>
                        <td>Credit card</td>
                        <td>$ {message_input['cc_revenue']}</td>
                    </tr>
                    <tr>
                        <td>Average revenue of iOS</td>
                        <td>$ {message_input['avg_each_platform_revenue']['ios']}</td>
                    </tr>
                    <tr>
                        <td>Average revenue of Android</td>
                        <td>$ {message_input['avg_each_platform_revenue']['android']}</td>
                    </tr>
                    <tr>
                        <td>Average revenue of Desktop</td>
                        <td>$ {message_input['avg_each_platform_revenue']['desktop']}</td>
                    </tr>
                </table>
                <p>
                    Percentage of female item purchased by credit card: 
                    <b>{round(message_input['cc_female_item_revenue'], 2)} % </b>
                </p>
                <p>List of customer for men luxury brand campaign is attached in this email.</p>
            </body>
        </html>
        """

        customer_campaign_list = message_input['customer_campaign_list']
        customer_campaign_list_df = pd.DataFrame(columns=['customer_id'],
                                                 data=customer_campaign_list)

        file_name = 'customer_list.csv'
        file_path = f'/tmp/{file_name}'
        customer_campaign_list_df.to_csv(file_path, index=False)
        attachment = MIMEBase("application", "octet-stream")
        with open(file_path, "rb") as f:
            attachment.set_payload(f.read())

        encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", f"attachment; filename={file_name}")

        body = MIMEText(html, "html")
        message.attach(body)
        message.attach(attachment)

        self._send_email(receiver_email, message)
