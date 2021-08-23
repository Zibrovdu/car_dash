import configparser
from sqlalchemy import create_engine

cfg_parser = configparser.ConfigParser()
cfg_parser.read(r'settings/settings.ini', encoding="utf-8")

db_username = cfg_parser['connect']['username']
db_password = cfg_parser['connect']['password']
db_name = cfg_parser['connect']['db']
db_host = cfg_parser['connect']['host']
db_port = cfg_parser['connect']['port']
db_dialect = cfg_parser['connect']['dialect']

fuel_data_table = cfg_parser['tables']['fuel_data_table']
repair_data_table = cfg_parser['tables']['repair_data_table']

odometer_total_field = cfg_parser['fields']['odometer_total']

ok_msg_engine_oil = cfg_parser['messages']['oil_dvs_msg_ok']
warning_msg_engine_oil = cfg_parser['messages']['oil_dvs_msg_warning']
ok_msg_air_filter = cfg_parser['messages']['air_filter_msg_ok']
warning_msg_air_filter = cfg_parser['messages']['air_filter_msg_warning']
ok_msg_cabin_filter = cfg_parser['messages']['cabin_filter_msg_ok']
warning_msg_cabin_filter = cfg_parser['messages']['cabin_filter_msg_warning']


min_km_oil_change = cfg_parser['repair_km']['min_km_oil_change']
max_km_oil_change = cfg_parser['repair_km']['max_km_oil_change']
min_km_change_air_filter = cfg_parser['repair_km']['min_km_change_air_filter']
max_km_change_air_filter = cfg_parser['repair_km']['max_km_change_air_filter']
min_km_change_cabin_filter = cfg_parser['repair_km']['min_km_change_cabin_filter']
max_km_change_cabin_filter = cfg_parser['repair_km']['max_km_change_cabin_filter']
min_km_change_rubbers = cfg_parser['repair_km']['min_km_change_rubbers']
max_km_change_rubbers = cfg_parser['repair_km']['max_km_change_rubbers']
min_km_tune_valves = cfg_parser['repair_km']['min_km_tune_valves']
max_km_tune_valves = cfg_parser['repair_km']['max_km_tune_valves']

min_date_month_oil_change = cfg_parser['repair_date']['min_date_month_oil_change']
max_date_month_oil_change = cfg_parser['repair_date']['max_date_month_oil_change']
min_date_month_change_air_filter = cfg_parser['repair_date']['min_date_month_change_air_filter']
max_date_month_change_air_filter = cfg_parser['repair_date']['max_date_month_change_air_filter']

conn_string = create_engine(f'{db_dialect}://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}')
