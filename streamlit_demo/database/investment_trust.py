from typing import List
from pydantic import TypeAdapter
from st_supabase_connection import SupabaseConnection
from streamlit_demo.domain.investment_trust import InvestmentTrust
from datetime import datetime


class InvestmentTrustDB:
    __db: SupabaseConnection
    __table: str

    def __init__(self, db: SupabaseConnection, table: str) -> None:
        self.__db = db
        self.__table = table

    def find_latest_data(self) -> List[InvestmentTrust] | None:
        rows = self.__db.query("*", table=self.__table, ttl=0) \
            .order("created_at", desc=True) \
            .limit(2) \
            .execute()
        return TypeAdapter(List[InvestmentTrust]).validate_python(rows.data)

    def find_by_name(self, name: str) -> List[InvestmentTrust] | None:
        rows = self.__db.query("*", table=self.__table, ttl=0) \
            .eq("fund_name", name) \
            .execute()
        return TypeAdapter(List[InvestmentTrust]).validate_python(rows.data)

    def find_by_name_and_created_at(self, name: str, begin_date: datetime, end_date: datetime) -> List[InvestmentTrust] | None:
        rows = self.__db.query("*", table=self.__table, ttl=0) \
            .eq("fund_name", name) \
            .gte("created_at", begin_date) \
            .lt("created_at", end_date) \
            .execute()
        return TypeAdapter(List[InvestmentTrust]).validate_python(rows.data)
