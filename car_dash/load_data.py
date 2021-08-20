import pandas as pd
from datetime import date, timedelta

import car_dash.load_cfg as lc

current_month = date.today().month
current_day = date.today().day
current_year = date.today().year
current_week = date.today().isocalendar()[1]

end_day = (date.today() - timedelta(days=7)).day
end_month = (date.today() - timedelta(days=7)).month
end_year = (date.today() - timedelta(days=7)).year


def load_fuel_data(table, con):
    df = pd.read_sql(f"""SELECT * FROM {table}""", con=con)
    df.loc[df[df['date'].notna()].index, 'date'] = df[df['date'].notna()]['date'].apply(
        lambda x: x.strftime('%d-%m-%Y'))
    df.columns = ['Дата', 'Время', 'Заправлено, л.', 'цена, руб/л.', 'Итого', 'Заправка', 'Адрес заправки', 'Пробег',
                  'Пробег за период', 'Ср. расход, л/100 км.', 'Примечания']
    return df


def get_filtered_df(table_name, start_date, end_date, month, month_year, week, week_year, type_period):
    """
    Синтаксис:
    ----------
    **get_filtered_df** (table_name, start_date, end_date, ch_month, ch_week, type_period)

    Описание:
    ----------
    Функция принимает на вход наименование таблицы, в которой содержаться данные по техподдержки в БД и параметры
    фильтрации (тип фильтра, выбранный номер недели, месяца, даты начала/окончания периода). Сделает запрос к БД.
    Возвращает отфильтрованный датафрейм за выбранный период по выбранной таблице (техподдержки).

    Параметры:
    ----------
        **table_name**: *String* - Название таблицы в БД для фильтрации

        **start_date**: *str* - дата начала периода (если фильтрация по произвольному периоду (DateTimeRange))

        **end_date**: *str* - дата окончания периода (если фильтрация по произвольному периоду (DateTimeRange))

        **ch_month**: *int* - номер выбранного месяца (если фильтрация по месяцу)

        **cho_week**: *int* - номер выбранной недели (если фильтрация осуществляется по неделям)

        **type_period**: *str* - Определяет тип фильтрации. Допустимые значения:

            '**m**' - фильтрация по выбранному месяцу.

            '**p**' - фильтрация по произвольному периоду.

            Если параметр не указан, то фильтрация осуществляется по неделям.

    Returns:
    ----------
        **DataFrame**
    """
    if type_period == 'm':
        df = pd.read_sql(f"""
            SELECT * 
            FROM {table_name} 
            WHERE EXTRACT(month from date) = {int(month)}
            AND EXTRACT(year from date) = {int(month_year)}
        """, con=lc.conn_string)
        df.loc[df[df['date'].notna()].index, 'date'] = df[df['date'].notna()]['date'].apply(
            lambda x: x.strftime('%d-%m-%Y'))
        df.columns = ['Дата', 'Время', 'Заправлено, л.', 'цена, руб/л.', 'Итого', 'Заправка', 'Адрес заправки',
                      'Пробег',
                      'Пробег за период', 'Ср. расход, л/100 км.', 'Примечания']

        return df

    elif type_period == 'p':
        df = pd.read_sql(f"""
            SELECT * 
            FROM {table_name} 
            WHERE date >= '{start_date} 00:00:00' 
                AND date <='{end_date} 23:59:59'
        """, con=lc.conn_string)
        df.loc[df[df['date'].notna()].index, 'date'] = df[df['date'].notna()]['date'].apply(
            lambda x: x.strftime('%d-%m-%Y'))
        df.columns = ['Дата', 'Время', 'Заправлено, л.', 'цена, руб/л.', 'Итого', 'Заправка', 'Адрес заправки',
                      'Пробег',
                      'Пробег за период', 'Ср. расход, л/100 км.', 'Примечания']

        return df
    else:
        df = pd.read_sql(f"""
            SELECT * 
            FROM {table_name} 
            WHERE EXTRACT(year from date) = {week_year}
            AND EXTRACT(week from date) = {week}
        """, con=lc.conn_string)
        df.loc[df[df['date'].notna()].index, 'date'] = df[df['date'].notna()]['date'].apply(
            lambda x: x.strftime('%d-%m-%Y'))
        df.columns = ['Дата', 'Время', 'Заправлено, л.', 'цена, руб/л.', 'Итого', 'Заправка', 'Адрес заправки',
                      'Пробег',
                      'Пробег за период', 'Ср. расход, л/100 км.', 'Примечания']
        return df


def get_start_params(table, con):
    df = pd.read_sql(f"""SELECT date FROM {table}""", con=con)
    start_period = (df['date'].min().week, df['date'].min().month, df['date'].min().year)
    finish_period = (df['date'].max().week, df['date'].max().month, df['date'].max().year)

    return start_period, finish_period


def get_param(field, table, con):
    return pd.read_sql(f'select {field} from {table} order by {field} desc limit 1', con=con)[f'{field}'].values[0]


def prepare_df_to_calc(table, con):
    df = pd.read_sql(f"""SELECT "Наименование товара", Пробег FROM {table}""", con=con)
    df['Пробег'] = df['Пробег'].fillna(0)
    df['Пробег'] = df['Пробег'].apply(lambda x: str(x)[2:] if str(x)[0] == '~' else x)
    df['Пробег'] = df['Пробег'].apply(lambda x: str(x).replace(' ', ''))
    df.loc[df[df['Пробег'] == '-'].index, 'Пробег'] = 0
    df['Пробег'] = df['Пробег'].astype(int)
    return df


def last_change_engine_oil(df):
    df['Межсервис_ДВС'] = df[(df['Наименование товара'].str.contains('амена масла')) | (
        df['Наименование товара'].str.contains('ТО'))]['Пробег'].diff()
    mask = df[((df['Наименование товара'].str.contains('амена масла')) | (df['Наименование товара'].str.contains(
        'ТО'))) & (df['Межсервис_ДВС'].isna())].index
    df.loc[mask, 'Межсервис_ДВС'] = 0
    return df[df['Межсервис_ДВС'].notna()].tail(1)['Пробег'].values[0]


def last_change_air_filter(df):
    df['Замена ВФ'] = df[df['Наименование товара'].str.contains('амена воздушного фильтра')]['Пробег'].diff()
    mask = df[(df['Наименование товара'].str.contains('амена воздушного фильтра')) & (df['Замена ВФ'].isna())].index
    df.loc[mask, 'Замена ВФ'] = 0

    return df[df['Замена ВФ'].notna()].tail(1)['Пробег'].values[0]


def last_change_cabin_filter(df):
    df['Замена_ФС'] = df[df['Наименование товара'].str.contains('амена фильтра салона')]['Пробег'].diff()
    mask = df[(df['Наименование товара'].str.contains('амена фильтра салона')) & (df['Замена_ФС'].isna())].index
    df.loc[mask, 'Замена_ФС'] = 0

    return df[df['Замена_ФС'].notna()].tail(1)['Пробег'].values[0]


def last_change_brake_fluid(df):
    df['Замена_ТЖ'] = df[df['Наименование товара'].str.contains('амена тормозной жидкости')]['Пробег'].diff()
    mask = df[(df['Наименование товара'].str.contains('амена тормозной жидкости')) & (df['Замена_ТЖ'].isna())].index
    df.loc[mask, 'Замена_ТЖ'] = 0

    return df[df['Замена_ТЖ'].notna()].tail(1)['Пробег'].values[0]


def last_change_rubbers(df):
    df['Замена_РС'] = df[df['Наименование товара'].str.contains('амена резинок стеклоочистителей')]['Пробег'].diff()
    mask = df[
        (df['Наименование товара'].str.contains('амена резинок стеклоочистителей')) & (df['Замена_РС'].isna())].index
    df.loc[mask, 'Замена_РС'] = 0
    return df[df['Замена_РС'].notna()].tail(1)['Пробег'].values[0]


def last_tune_valves(df):
    df['Регулировка_клапанов'] = df[df['Наименование товара'].str.contains('егулировка клапанов')]['Пробег'].diff()
    mask = df[
        (df['Наименование товара'].str.contains('егулировка клапанов')) & (df['Регулировка_клапанов'].isna())].index
    df.loc[mask, 'Регулировка_клапанов'] = 0
    return df[df['Регулировка_клапанов'].notna()].tail(1)['Пробег'].values[0]
