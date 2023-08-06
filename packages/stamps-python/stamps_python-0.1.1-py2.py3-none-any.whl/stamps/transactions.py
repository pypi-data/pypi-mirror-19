from .base_api import BaseAPI


class Transactions(BaseAPI):

    def add(self, user=None, total_value=None,
            invoice_number=None, created=None, items=None,
            require_email_notification=None, **kwargs):
        url = self.client.base_url + "/transactions/add"

        payload = {
            'token': self.client.token,
            'merchant': self.client.merchant_id,
            'store': self.client.store_id,
            'user': user,
            'invoice_number': invoice_number,
            'total_value': total_value,
            'created': created,
            'require_email_notification': require_email_notification,
        }

        if items:
            payload["items"] = items

        payload.update(kwargs)
        return self.client._call('POST', url, payload)

    def cancel(self, id=None, cancel_related_redemptions=False,
               require_email_notification=None, **kwargs):
        payload = {
            'token': self.client.token,
            'merchant': self.client.merchant_id,
            'id': id,
            'cancel_related_redemptions': cancel_related_redemptions,
            'require_email_notification': require_email_notification,
        }
        payload.update(kwargs)
        url = self.client.base_url + "/transactions/cancel"
        return self.client._call('POST', url, payload)
