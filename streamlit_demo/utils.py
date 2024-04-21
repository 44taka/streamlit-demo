from datetime import datetime


class Util:
    @staticmethod
    def create_month_list(start_year: int, start_month: int) -> list:
        current_year = datetime.now().year
        current_month = datetime.now().month

        year_months = []
        year = start_year
        month = start_month

        while year < current_year or (year == current_year and month <= current_month):
            year_months.append(f"{year}年{month}月")
            month += 1
            if month > 12:
                month = 1
                year += 1
        # 逆順に
        year_months.reverse()
        return year_months

    @staticmethod
    def create_fund_name_list() -> tuple:
        return (
            'ニッセイ－＜購入・換金手数料なし＞ニッセイ外国株式インデックスファンド',
            'ニッセイ－ニッセイ日経２２５インデックスファンド',
        )
