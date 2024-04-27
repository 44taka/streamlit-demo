from st_supabase_connection import SupabaseConnection


class Auth:
    __conn: SupabaseConnection

    def __init__(self, conn: SupabaseConnection):
        self.__conn = conn

    def sign_in_with_password(self, email: str, password: str) -> None:
        self.__conn.auth.sign_in_with_password({
            'email': email,
            'password': password,
        })

    def is_signed_in(self, jwt: str) -> bool:
        return self.__conn.auth.get_user(jwt) is not None

    def get_access_token(self) -> str:
        return self.__conn.auth.get_session().access_token
