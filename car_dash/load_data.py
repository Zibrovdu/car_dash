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


def last_odometer_service(table, con, **kwargs):
    if not kwargs:
        return 0
    if len(kwargs) == 2:
        return pd.read_sql(f"select {kwargs['data_field']} from {table} where {kwargs['filter_field']} IS NOT NULL",
                           con=con).tail(1)[f'{kwargs["data_field"]}'].values[0]


