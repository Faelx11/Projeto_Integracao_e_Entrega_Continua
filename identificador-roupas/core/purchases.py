import uuid
from datetime import datetime, timezone, timedelta

class PurchaseStore:
    def __init__(self, purchases_list=None):
        self.purchases = purchases_list or []

    def create_purchase(self, user_id, item, color, price, date=None):
        pid = str(uuid.uuid4())
        # Formato de data e hora em pt-BR (horário de Brasília)
        now_brazil = datetime.now(timezone(timedelta(hours=-3))).strftime("%d/%m/%Y %H:%M:%S")
        purchase = {
            'id': pid,
            'user_id': user_id,
            'item': item.lower(),
            'color': color.lower(),
            'price': float(price),
            'date': date or now_brazil
        }
        self.purchases.append(purchase)
        return purchase

    def purchases_by_user(self, user_id):
        return [p for p in self.purchases if p['user_id'] == user_id]

    def to_list(self):
        return self.purchases

    def all(self):
        return self.purchases