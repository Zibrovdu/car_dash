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
        msg = f'ВНИМАНИЕ! Необходимо заменить {msg_warning}, в течении ' \
              f'{(int(last_change_odometer) + 15000) - current_odometer} километров'
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
    delta = delta.total_seconds()/86400/365
    if delta < 1:
        return "".join([str(round((delta % 1) * 365)), ' дн.'])
    else:
        return "".join([str(int(delta // 1)), ' г. ', str(round((delta % 1) * 365)), ' дн.'])
