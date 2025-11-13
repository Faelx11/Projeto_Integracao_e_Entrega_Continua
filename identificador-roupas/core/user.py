import uuid

class UserStore:
    def __init__(self, users_list=None):
        self.users = users_list or []

    def create_user(self, name):
        uid = str(uuid.uuid4())
        user = {'id': uid, 'name': name}
        self.users.append(user)
        return user

    def get_user(self, uid):
        for u in self.users:
            if u['id'] == uid:
                return u
        return None

    def to_list(self):
        return self.users

    def all_ids(self):
        return [u['id'] for u in self.users]
