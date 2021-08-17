import pandas as pd
from dash_table.Format import Format, Scheme
from datetime import date, timedelta

import car_dash.log_writer as lw
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
    # df[['total', 'liters', 'price']].float_format = '%.00f'
    df.loc[df[df['date'].notna()].index, 'date'] = df[df['date'].notna()]['date'].apply(
        lambda x: x.strftime('%d-%m-%Y'))
    df.columns = ['Дата', 'Время', 'Заправлено, л.', 'цена, руб/л.', 'Итого', 'Заправка', 'Адрес заправки', 'Пробег',
                  'Пробег за период', 'Ср. расход, л/100 км.', 'Примечания']
    return df


def fuel_data_columns(df):
    list_of_columns = []
    for i, column_type in enumerate(df.dtypes):
        if df.dtypes.index[i] == 'Пробег за период':
            list_of_columns.append(dict(name=df.dtypes.index[i], id=df.dtypes.index[i], type='numeric',
                                        format=Format(precision=1, scheme=Scheme.fixed)))
        elif column_type == 'float64':
            list_of_columns.append(dict(name=df.dtypes.index[i], id=df.dtypes.index[i], type='numeric',
                                        format=Format(precision=2, scheme=Scheme.fixed)))
        else:
            list_of_columns.append(dict(name=df.dtypes.index[i], id=df.dtypes.index[i]))
    return list_of_columns


def get_months(start_month, start_year, finish_month, finish_year):
    """
    Синтаксис:
    ----------
    **get_months** (start_month, start_year, finish_month, finish_year)

    Описание:
    ----------

    Функция принимает на вход период в виде 4-х параметров (номер месяца и год начала, номер месяца и год окончания.
    Возвращает список словарей, содержащих информацию о месяце, годе и номере месяца для последующей загрузки в
    компонент dcc.Dropdown.

    Параметры:
    ----------
        **start_month**: *int* - номер месяца начала периода

        **start_year**: *int* - год начала периода

        **finish_month**: *int* - номер месяца окончания периода

        **finish_year**: *int* - год окончания периода

    Returns:
    ----------
        **List**
    """
    start_period = [
        {"label": f'{get_period_month(year=start_year, month=i)}', "value": "_".join([str(i), str(start_year)])}
        for i in range(start_month, 13)]
    end_period = [
        {"label": f'{get_period_month(year=finish_year, month=i)}', "value": "_".join([str(i), str(finish_year)])}
        for i in range(1, finish_month + 1)]

    if finish_year - start_year <= 1:
        for item in end_period:
            start_period.append(item)
        start_period.reverse()
    else:
        years_list = []
        for count in range(1, finish_year - start_year):
            years_list.insert(count, start_year + count)

        addition_period = []
        for year in years_list:
            addition_period.append(
                [{"label": f'{get_period_month(year=year, month=i)}', "value": "_".join([str(i), str(year)])} for i in
                 range(1, 13)])

        for period in addition_period:
            for item in period:
                start_period.append(item)
        for item in end_period:
            start_period.append(item)
        start_period.reverse()

    return start_period


def get_weeks(start_week, start_year, finish_week, finish_year):
    """
    Синтаксис:
    ----------

    **get_weeks** (start_week, start_year, finish_week, finish_year)

    Описание:
    ----------
    Функция принимает на вход период в виде 4-х параметров (номер недели и год начала, номер недели и год окончания.
    Возвращает список словарей содержащих информацию о номере недели, её периоде, и номере недели для последующей
    загрузки в компонент dcc.Dropdown.

    Параметры:
    ----------
        **start_week**: *int* - номер недели начала периода

        **start_year**: *int* - год начала периода

        **finish_week**: *int* - номер недели окончания периода

        **finish_year**: *int* - год окончания периода

    Returns:
    ----------
        **List**
    """
    last_week_of_start_year = date(start_year, 12, 31).isocalendar()[1]

    start_period = [{"label": f'Неделя {i} ({get_period(year=start_year, week=i)})',
                     "value": "_".join([str(i), str(start_year)])} for i in
                    range(start_week, last_week_of_start_year + 1)]
    end_period = [
        {"label": f'Неделя {i} ({get_period(year=finish_year, week=i)})', "value": "_".join([str(i), str(finish_year)])}
        for i in range(1, finish_week + 1)]

    if finish_year - start_year <= 1:
        for item in end_period:
            start_period.append(item)
        start_period.reverse()
    else:
        years_dict = {}
        for count in range(1, (finish_year - start_year)):
            if date(start_year + count, 12, 31).isocalendar()[2] < 4:
                years_dict[start_year + count] = date(start_year + count, 12, 31 - date(start_year + count, 12, 31).
                                                      isocalendar()[2]).isocalendar()[1]
            else:
                years_dict[start_year + count] = date(start_year + count, 12, 31).isocalendar()[1]

        addition_period = []
        for year in years_dict.keys():
            addition_period.append(
                [{"label": f'Неделя {i} ({get_period(year=year, week=i)})', "value": "_".join([str(i), str(year)])}
                 for i in range(1, years_dict[year] + 1)])

        for period in addition_period:
            for item in period:
                start_period.append(item)
        for item in end_period:
            start_period.append(item)
        start_period.reverse()

    return start_period


def get_period(year, week, output_format='n'):
    """
    Синтаксис:
    ----------

    **get_period** (year, week, output_format='n')

    Описание:
    ---------

    Функция принимает на вход год и номер недели. Возвращает список или строку содержащие начальную и конечную
    даты недели

    Параметры:
    ----------

    **year**: *int* - год

    **week**: *int* - номер недели

    **output_format**: *string*, default 'n'
        Определяет формат вывода данных. Допустимые значения:

        'n' - строка вида 'ДД-ММ-ГГГГ - ДД-ММ-ГГГГ'

        's' - список вида ['ГГГГ-ММ-ДД', 'ГГГГ-ММ-ДД']

        При указании другого параметра вернется список ['1900-01-01', '1900-01-01']

    Returns:
    -------
        **string** or **list of strings**
    """
    first_year_day = date(year, 1, 1)
    if first_year_day.weekday() > 3:
        first_week_day = first_year_day + timedelta(7 - first_year_day.weekday())
    else:
        first_week_day = first_year_day - timedelta(first_year_day.weekday())

    dlt_start = timedelta(days=(week - 1) * 7)
    dlt_end = timedelta(days=(((week - 1) * 7) + 6))

    start_day_of_week = first_week_day + dlt_start
    end_day_of_week = first_week_day + dlt_end

    if output_format == 'n':
        period = ' - '.join([start_day_of_week.strftime("%d-%m-%Y"), end_day_of_week.strftime("%d-%m-%Y")])
    elif output_format == 's':
        period = [start_day_of_week.strftime("%Y-%m-%d"), end_day_of_week.strftime("%Y-%m-%d")]
    else:
        period = ['1900-01-01', '1900-01-01']

    return period


def get_period_month(year, month):
    """
    Синтаксис:
    ----------

    **get_period_month** (year, month)

    Описание:
    ----------
    Функция принимает на вход номер месяца и год. Возвращает строку 'Месяц год'.

    Параметры:
    ----------
        **year**: *int* - год

        **month**: *int* - номер месяца

    Returns:
    ----------
        **String**
    """
    months = ['', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь',
              'Ноябрь', 'Декабрь']
    period = ' '.join([str(months[month]), str(year)])

    return period


def choosen_type(type_period, start_date, end_date, ch_month, ch_week):
    """
    Синтаксис:
    ----------
    **choosen_type** (type_period, start_date, end_date, ch_month, ch_week)

    Описание:
    ----------
    Функция принимает на вход тип фильтра и параметры фильтрации (номер недели, месяца, даты начала/окончания периода).
    В зависимости от выбранного типа фильтра отключает другие компоненты (например если выбрана фильтрация по неделям,
    остальные компоненты фильтрации (выбор месяца и произвольного периода) будут отключены). Также функция записывает в
    лог-файл выбранный тип фильтрации и его значение (номер недели/месяца или период)

    Параметры:
    ----------
        **type_period**: *str*
            Определяет тип фильтрации. Допустимые значения:

            '**m**' - фильтрация по выбранному месяцу.

            '**p**' - фильтрация по произвольному периоду.

            Если параметр не указан, то фильтрация осуществляется по неделям.

        **start_date**: *str* - дата начала периода (если фильтрация по произвольному периоду (DateTimeRange))

        **end_date**: *str* - дата окончания периода (если фильтрация по произвольному периоду (DateTimeRange))

        **ch_month**: *int* - номер выбранного месяца (если фильтрация по месяцу)

        **ch_week**: *int* - номер выбранной недели (если фильтрация осуществляется по неделям)

    Returns:
    ----------
        **Tuple**
    """
    if type_period == 'm':
        period_choice = True
        week_choice = True
        month_choice = False
        lw.log_writer(log_msg=f'Пользователь выбрал месяц, "выбранный месяц - {ch_month}"')

    elif type_period == 'p':
        period_choice = False
        week_choice = True
        month_choice = True
        lw.log_writer(log_msg=f'Пользователь выбрал произвольный период "период с {start_date}, по {end_date}"')

    else:
        period_choice = True
        week_choice = False
        month_choice = True
        lw.log_writer(log_msg=f'Пользователь выбрал неделя "выбранная неделя - {ch_week} '
                              f'({get_period(year=current_year, week=ch_week)})"')

    return period_choice, week_choice, month_choice


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
