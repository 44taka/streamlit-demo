from datetime import datetime
from dateutil.relativedelta import relativedelta

import pandas as pd
import streamlit as st
from st_supabase_connection import SupabaseConnection

import database.investment_trust
from utils import Util

from auth.auth import Auth


# Initialize connection.
conn = st.connection("supabase", type=SupabaseConnection)
db = database.investment_trust.InvestmentTrustDB(db=conn, table="investment_trusts")
auth = Auth(conn)

def main():
    # タイトル
    st.header('44takaの投資信託')
    st.subheader("最新情報")

    # データ表示
    with st.spinner('データ取得中...'):
        data = db.find_latest_data()
        col1, col2 = st.columns(2)
        col1.metric(data[0].fund_name, f"{data[0].evaluation_value} 円", f"{data[0].income_price} 円")
        col2.metric(data[1].fund_name, f"{data[1].evaluation_value} 円", f"{data[1].income_price} 円")
        st.caption(f"{data[0].created_at.strftime('%Y年%m月%d日 %H時%M分')} 時点")

    # テーブル
    st.subheader("月別一覧")
    col3, col4 = st.columns(2)
    with col3:
        fund_name_option = st.selectbox(
            '投資信託名を指定してください。',
            Util.create_fund_name_list()
        )
    with col4:
        month_option = st.selectbox(
            '表示月を指定してください。',
            Util.create_month_list(2023, 5)
        )

    with st.spinner('データ取得中...'):
        table_data = db.find_by_name_and_created_at(
            name=fund_name_option,
            begin_date=datetime.strptime(f'{month_option}1日', '%Y年%m月%d日'),
            end_date=datetime.strptime(f'{month_option}1日', '%Y年%m月%d日') + relativedelta(months=1),
        )
        df = pd.DataFrame({
            '日付': [datum.created_at.strftime('%Y年%m月%d日') for datum in table_data],
            'ファンド名': [datum.fund_name for datum in table_data],
            '損益（円）': [datum.income_price for datum in table_data],
            '損益（％）': [datum.income_percent for datum in table_data],
            '評価額（円）': [datum.evaluation_value for datum in table_data],
        })
        st.dataframe(df)


if __name__ == '__main__':
    if 'token' not in st.session_state or st.session_state['token'] is None:
        st.switch_page('./pages/login.py')
    if auth.is_signed_in(jwt=st.session_state['token']) is False:
        st.switch_page('./pages/login.py')
    main()
