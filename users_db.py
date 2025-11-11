import bcrypt

#użytkownik admin z hasłem "admin123" i rolą ROLE_ADMIN
hashed_pw = bcrypt.hashpw(b"admin123", bcrypt.gensalt())

USERS_DB = {
    "admin": {
        "password": hashed_pw,
        "roles": ["ROLE_ADMIN"]
    }
}
