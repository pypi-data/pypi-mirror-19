import datetime
from decimal import Decimal
import uuid

from amaascore.core.amaas_model import AMaaSModel
from amaascore.exceptions import TransactionNeedsSaving
from amaascore.transactions.transaction_children import Reference


class Transaction(AMaaSModel):

    @staticmethod
    def children():
        return ['charges', 'codes', 'references']

    def __init__(self, asset_manager_id, asset_book_id, counterparty_book_id, transaction_action, asset_id, quantity,
                 transaction_date, settlement_date, price, transaction_currency, settlement_currency,
                 asset=None, execution_time=None, transaction_type='Trade', transaction_id=None,
                 transaction_status='New', version=1, charges={}, codes={}, references={}, *args, **kwargs):

        self.asset_manager_id = asset_manager_id
        self.asset_book_id = asset_book_id
        self.counterparty_book_id = counterparty_book_id
        self.transaction_action = transaction_action
        self.asset_id = asset_id  # This is duplicated on the child asset.  Remove?
        self.quantity = quantity
        self.transaction_date = transaction_date
        self.settlement_date = settlement_date
        self.price = price
        self.transaction_currency = transaction_currency
        self.settlement_currency = settlement_currency
        self.transaction_type = transaction_type
        self.transaction_status = transaction_status
        self.version = version

        # Cannot be in method signature or the value gets bound to the constructor call
        self.execution_time = execution_time or datetime.datetime.utcnow()
        self.transaction_id = transaction_id or uuid.uuid4().hex

        self.charges = charges
        self.codes = codes
        self.references = references
        self.references['AMaaS'] = Reference(reference_value=self.transaction_id)  # Upserts the AMaaS Reference

        self.postings = []
        self.asset = asset
        super(Transaction, self).__init__(*args, **kwargs)

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        """
        Force the quantity to always be a decimal
        :param value:
        :return:
        """
        self._quantity = Decimal(value)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        """
        Force the price to always be a decimal
        :param value:
        :return:
        """
        self._price = Decimal(value)

    @property
    def gross_settlement(self):
        if hasattr(self, '_gross_settlement'):
            return self.__gross_settlement
        return self.quantity * self.price

    @gross_settlement.setter
    def gross_settlement(self, gross_settlement):
        """

        :param gross_settlement:
        :return:
        """
        if gross_settlement:
            self._gross_settlement = Decimal(gross_settlement)

    @property
    def net_settlement(self):
        if hasattr(self, '_net_settlement'):
            return self._net_settlement
        return self.gross_settlement - self.charges_net_effect()

    @net_settlement.setter
    def net_settlement(self, net_settlement):
        """

        :param gross_settlement:
        :return:
        """
        if net_settlement:
            self._net_settlement = Decimal(net_settlement)

    def charges_net_effect(self):
        """
        The total effect of the net_affecting charges (note affect vs effect here).

        Currently this is single currency only (AMAAS-110).

        Cast to Decimal in case the result is zero (no net_affecting charges).

        :return:
        """
        return Decimal(sum([charge.charge_value for charge in self.charges.values()
                            if charge.active and charge.net_affecting]))

    def charge_types(self):
        """
        TODO - are these helper functions useful?
        :return:
        """
        return self.charges.keys()

    def code_types(self):
        """
        TODO - are these helper functions useful?
        :return:
        """
        return self.codes.keys()

    def reference_types(self):
        """
        TODO - are these helper functions useful?
        :return:
        """
        return self.references.keys()

    # def __dict__(self):
    #     # Potentially move this into the base class?
    #     transaction_dict = super(Transaction, self).__dict__
    #     for child in self.children():
    #         transaction_dict[child] = getattr(self, child)
    #     return transaction_dict

    def __str__(self):
        return "Transaction object - ID: %s" % self.transaction_id

    @property
    def postings(self):
        if hasattr(self, '_postings'):
            return self._postings
        else:
            raise TransactionNeedsSaving

    @postings.setter
    def postings(self, postings):
        """
        TODO - when do we save this from AMaaS Core?
        :param postings:
        :return:
        """
        if postings:
            self._postings = postings
