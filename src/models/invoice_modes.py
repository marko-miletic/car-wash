from sqlalchemy import Integer, Column, ForeignKey

from src.models import BaseClass


class InvoiceModes(BaseClass):
    id = Column(Integer, primary_key=True, index=True)

    invoice_id = Column(Integer, ForeignKey('invoice.id'))
    mode_id = Column(Integer, ForeignKey('mode.id'))

    def __init__(self, invoice_id: int, mode_id: int):
        self.invoice_id = invoice_id
        self.mode_id = mode_id

    def __repr__(self):
        return f'Invoice(id={self.id}, invoice_id={self.invoice_id}, mode_id={self.mode_id})'
