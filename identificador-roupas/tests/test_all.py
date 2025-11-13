import tempfile
from pathlib import Path
import json
from core.user import UserStore
from core.purchases import PurchaseStore
from core.recognizer import Recognizer


def test_recognizer_basic():
    users = []
    purchases = []
    us = UserStore(users)
    ps = PurchaseStore(purchases)
    # create two users
    u1 = us.create_user('Alice')
    u2 = us.create_user('Bob')
    # user1 buys many red t-shirts
    ps.create_purchase(u1['id'], 'camiseta', 'vermelho', 50)
    ps.create_purchase(u1['id'], 'camiseta', 'vermelho', 60)
    # user2 buys blue pants
    ps.create_purchase(u2['id'], 'calça', 'azul', 120)
    r = Recognizer(us, ps, threshold=0.5)
    # new purchase similar to user1
    match = r.recognize_by_purchase({'item': 'camiseta', 'color': 'vermelho', 'price': 55})
    assert match == u1['id']
    # new purchase different
    match2 = r.recognize_by_purchase({'item': 'calça', 'color': 'azul', 'price': 130})
    assert match2 == u2['id']


def test_public_view_anonymization():
    users = []
    purchases = []
    us = UserStore(users)
    ps = PurchaseStore(purchases)
    u1 = us.create_user('Carol')
    ps.create_purchase(u1['id'], 'jaqueta', 'preto', 200)
    r = Recognizer(us, ps)
    public = r.public_view()
    assert len(public) == 1
    assert 'Cliente Estilo #' in public[0]
