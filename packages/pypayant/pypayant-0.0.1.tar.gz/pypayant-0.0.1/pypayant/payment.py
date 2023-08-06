from pypayant.base import BasePayantAPI


class Payment(BasePayantAPI):
    def __init__(self, auth_key):
        super(Payment, self).__init__(auth_key)
        self.base_payment_key = "payments"

    def add(self, reference_code, date, amount, channel):
        """

        :param reference_code:
        :param date:
        :param amount:
        :param channel:
        :return:
        """
        url = self._path(self.base_payment_key)
        request_data = {
            "reference_code": reference_code,
            "date": date,
            "amount": amount,
            "channel": channel
        }
        response = self._exec_request('POST', url, request_data)
        return response

    def get(self, reference_code):
        """
        Get the details of a payment with the reference_code provided.
        :param reference_code:
        :return:
        """
        url = self._path("{0}/{1}".format(self.base_payment_key,
                                          reference_code))
        return self._exec_request('GET', url)

    def history(self, period, start, end):
        """
        Return invoice history from start to end within specified period
        :param period:
        :param start:
        :param end:
        :return:
        """
        _history_base = "history"
        url = self._path("{0}/{1}/".format(self.base_payment_key,
                                           _history_base))
        request_data = {"period": period, "start": start, "end": end}
        return self._exec_request('GET', url, request_data)