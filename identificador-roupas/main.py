import json
from core.user import UserStore
from core.purchases import PurchaseStore
from core.recognizer import Recognizer
from pathlib import Path

DB_PATH = Path('data/database.json')


def ensure_db():
    if not DB_PATH.exists():
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        with DB_PATH.open('w', encoding='utf-8') as f:
            json.dump({'users': [], 'purchases': []}, f, indent=2)


def load_stores():
    with DB_PATH.open('r', encoding='utf-8') as f:
        data = json.load(f)
    user_store = UserStore(data['users'])
    purchase_store = PurchaseStore(data['purchases'])
    return user_store, purchase_store


def save_stores(user_store, purchase_store):
    with DB_PATH.open('w', encoding='utf-8') as f:
        json.dump({'users': user_store.to_list(), 'purchases': purchase_store.to_list()}, f, indent=2)


def menu():
    ensure_db()
    user_store, purchase_store = load_stores()
    recognizer = Recognizer(user_store, purchase_store)

    while True:
        print('\n=== Identificador Anônimo de Compradores ===')
        print('1) Cadastrar usuário')
        print('2) Registrar compra (associar a um usuário existente)')
        print('3) Registrar compra (sem informar usuário — uso do reconhecedor automático)')
        print('4) Listar compras públicas (anônimas)')
        print('5) Sair')
        choice = input('Escolha: ').strip()
        if choice == '1':
            name = input('Nome (não será exibido publicamente): ').strip()
            user = user_store.create_user(name=name)
            save_stores(user_store, purchase_store)
            print(f'Usuário criado com id: {user["id"]}')
        elif choice == '2':
            uid = input('ID do usuário: ').strip()
            if not user_store.get_user(uid):
                print('Usuário não encontrado')
                continue
            item = input('Item (ex: camiseta, calça): ').strip()
            color = input('Cor: ').strip()
            price = float(input('Preço: ').strip())
            purchase = purchase_store.create_purchase(user_id=uid, item=item, color=color, price=price)
            save_stores(user_store, purchase_store)
            print('Compra registrada.')
        elif choice == '3':
            item = input('Item (ex: camiseta, calça): ').strip()
            color = input('Cor: ').strip()
            price = float(input('Preço: ').strip())
            matched_uid = recognizer.recognize_by_purchase({'item': item, 'color': color, 'price': price})
            if matched_uid:
                print(f'Compra associada ao usuário (anônimo) id: {matched_uid}')
                purchase_store.create_purchase(user_id=matched_uid, item=item, color=color, price=price)
            else:
                new_user = user_store.create_user(name='[anon]')
                purchase_store.create_purchase(user_id=new_user['id'], item=item, color=color, price=price)
                print(f'Nenhum perfil compatível. Novo perfil criado: {new_user["id"]}')
            save_stores(user_store, purchase_store)
        elif choice == '4':
            public = recognizer.public_view()
            print('\n-- Compras públicas --')
            for p in public:
                print(p)
        elif choice == '5':
            print('Saindo...')
            break
        else:
            print('Opção inválida')
            
if __name__ == '__main__':
    menu()