import streamlit as st
from st_supabase_connection import SupabaseConnection

from streamlit_demo.auth.auth import Auth


# initialize
auth = Auth(conn=st.connection("supabase", type=SupabaseConnection))

st.header('44takaの投資信託')

email = st.text_input("メールアドレス")
password = st.text_input("パスワード", type="password")

if st.button("ログイン"):
    try:
        auth.sign_in_with_password(email, password)
        st.session_state['token'] = auth.get_access_token()
        st.switch_page('app.py')
    except Exception:
        st.error("無効なユーザー名またはパスワードです。")
