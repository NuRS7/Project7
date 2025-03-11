class UsersRepository:
    users_db = []

    @classmethod
    def create_user(cls, email, name, password):
        user = {"email": email, "name": name, "password": password}
        cls.users_db.append(user)

    @classmethod
    def get_user_by_email(cls, email):
        return next((user for user in cls.users_db if user["email"] == email), None)
