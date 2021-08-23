import pandas as pd
from datetime import date


def calc_change_engine_oil(current_odometer, last_change_odometer, msg_ok, msg_warning):
    if current_odometer < (int(last_change_odometer) + 7000):
        msg = f'Следующая замена {msg_ok} через {(int(last_change_odometer) + 7000) - current_odometer} ' \
              f'километров'
        style_change_oil_div = dict(backgroundColor='#c9e5ab')
        style_lbl_change_oil = dict(color='#1b511a', fontWeight='bold')
        style_label_tbl = dict(color='#1b511a', fontWeight='bold', background='#c9e5ab')

        return msg, style_change_oil_div, style_lbl_change_oil, style_label_tbl

    elif (int(last_change_odometer) + 7000) <= current_odometer < (int(last_change_odometer) + 15000):
        msg = f'ВНИМАНИЕ! Необходимо заменить {msg_warning}'
        style_change_oil_div = dict(backgroundColor='#efca66')
        style_lbl_change_oil = dict(color='#6f2205', fontWeight='bold')
        style_label_tbl = dict(color='#6f2205', fontWeight='bold', background='#efca66')

        return msg, style_change_oil_div, style_lbl_change_oil, style_label_tbl
    else:
        msg = f'ВНИМАНИЕ! ПЕРЕПРОБЕГ {current_odometer - (int(last_change_odometer) + 15000)} КИЛОМЕТРОВ! СРОЧНО ' \
              f'ЗАМЕНИТЕ {msg_warning.upper()}!!!'
        style_change_oil_div = dict(backgroundColor='rgb(223, 3, 38)')
        style_lbl_change_oil = dict(color='white', fontWeight='bold', fontSize='18px')
        style_label_tbl = dict(color='white', fontWeight='bold', background='rgb(223, 3, 38)')

        return msg, style_change_oil_div, style_lbl_change_oil, style_label_tbl


def calc_delta(from_date):
    delta = pd.to_datetime(date.today()) - pd.to_datetime(from_date, format="%d-%m-%Y")
    delta = delta.total_seconds() / 86400 / 365
    if delta < 1:
        return "".join([str(round((delta % 1) * 365)), ' дн.'])
    else:
        return "".join([str(int(delta // 1)), ' г. ', str(round((delta % 1) * 365)), ' дн.'])


def calc_repairs_km(current_km, last_change_km, min_km, max_km):
    if current_km < (int(last_change_km) + int(min_km)):
        msg = f'Следующее обслуживание через {(int(last_change_km) + int(min_km)) - current_km} километров'
        status = 'ok'

        return msg, status

    elif (int(last_change_km) + int(min_km)) <= current_km < (int(last_change_km) + int(max_km)):
        msg = f'ВНИМАНИЕ! Требуется замена/регулировка'
        status = 'warning'

        return msg, status
    else:
        msg = f'ВНИМАНИЕ! Перепробег {current_km - (int(last_change_km) + int(max_km))} километров! Требуется ' \
              f'срочная замена/регулировка'
        status = 'stop'

        return msg, status


def calc_repairs_date(last_change_date, min_date_month, max_date_month):
    delta = pd.to_datetime(date.today()) - pd.to_datetime(last_change_date, format="%d-%m-%Y")
    delta = delta.total_seconds() / 86400 / 365 * 12
    if delta < (int(min_date_month)):
        if int(min_date_month) - delta < 1:
            msg = f'Следующее обслуживание через {round((min_date_month - delta) * 12)} дн.'
        else:
            msg = f'Следующее обслуживание через {round((min_date_month - delta) // 1)} мес.,' \
                  f' {round((min_date_month - delta) % 1 * 12)} дн.'
        status = 'ok'

        return msg, status

    elif int(min_date_month) <= delta < int(max_date_month):
        msg = f'ВНИМАНИЕ! Требуется замена/регулировка'
        status = 'warning'

        return msg, status
    else:
        msg = f'ВНИМАНИЕ! Перепробег {round((delta - int(max_date_month)))} мес.! Требуется срочная замена/регулировка'
        status = 'stop'

        return msg, status


def analyze_results(msg_km, status_km, msg_date, status_date):
    if status_km == 'ok' and status_date == 'ok':
        return status_km, " ".join([msg_km, 'или', msg_date[29:]])
    elif status_km == 'warning' and status_date == 'warning':
        return status_km, msg_km
    elif status_km == 'stop' and status_date == 'stop':
        return status_km, " ".join([msg_km[:msg_km.find('!', 10)], 'или', msg_date[msg_date.find(' ', 10) + 1:
                                                                                   msg_date.find('!', 10)],
                                    msg_km[msg_km.find('Т'):]])
    elif status_km == 'ok' and (status_date == 'warning' or status_date == 'stop'):
        return status_date, msg_date
    # need add new condition elif warning and stop
    else:
        return status_km, msg_km
