from dash.dependencies import Input, Output, State

import car_dash.load_data as ld
import car_dash.load_cfg as lc
import car_dash.date_cfg as dc
import car_dash as cd


def register_callbacks(app):
    @app.callback(
        Output('period_choice', 'disabled'),
        Output('month_choice', 'disabled'),
        Output('week_choice', 'disabled'),
        Output('avg_liters', 'children'),
        Output('avg_price', 'children'),
        Output('fuel_flow', 'children'),
        Output('main_fuel_table', 'data'),
        Output('main_fuel_table', 'columns'),
        [Input('period_choice', 'start_date'),
         Input('period_choice', 'end_date'),
         Input('month_choice', 'value'),
         Input('week_choice', 'value'),
         Input('choice_type', 'value')],
    )
    def update_fuel_statistic_table(start_date_user, end_date_user, choosen_month, choosen_week, choice_type_period):

        week, week_year = int(choosen_week[:2]), int(choosen_week[3:])
        if len(choosen_month) == 6:
            month, month_year = int(choosen_month[:1]), int(choosen_month[2:])
        else:
            month, month_year = int(choosen_month[:2]), int(choosen_month[3:])
        period_choice, week_choice, month_choice = dc.choosen_type(type_period=choice_type_period,
                                                                   start_date=start_date_user,
                                                                   end_date=end_date_user,
                                                                   ch_month=month,
                                                                   ch_week=week)

        filtered_fuel_data_df = ld.get_filtered_df(table_name=lc.fuel_data_table,
                                                   month=month,
                                                   month_year=month_year,
                                                   week=week,
                                                   week_year=week_year,
                                                   start_date=start_date_user,
                                                   end_date=end_date_user,
                                                   type_period=choice_type_period)

        avg_liters = round(filtered_fuel_data_df['Заправлено, л.'].sum(), 2)
        avg_price = round(filtered_fuel_data_df['цена, руб/л.'].mean(), 2)
        fuel_flow = round(filtered_fuel_data_df['Ср. расход, л/100 км.'].mean(), 1)
        fuel_columns = cd.fuel_data_columns(df=filtered_fuel_data_df)

        return (period_choice, month_choice, week_choice, avg_liters, avg_price, fuel_flow,
                filtered_fuel_data_df.to_dict('records'), fuel_columns)

    @app.callback(
        Output('lbl_change_oil', 'children'),
        Output('change_oil_div', 'style'),
        Output('lbl_change_oil', 'style'),
        Output('curr_odo', 'style'),
        Output('tb_oil_dvs_curr_odo', 'children'),
        Output('tb_oil_dvs_prev_odo', 'children'),
        Output('tb_oil_kpp_curr_odo', 'children'),
        Output('tb_filter_dvs_curr_odo', 'children'),
        Output('tb_filter_salon_curr_odo', 'children'),
        Output('tb_rubbers_curr_odo', 'children'),
        Output('tb_brake_fluid_curr_odo', 'children'),
        Output('tb_valves_curr_odo', 'children'),
        Output('row_1', 'style'),
        Input('submit_odometr_btn', 'n_clicks'),
        State('curr_odometr_input', 'value')
    )
    def need_change_engine_oil(clicks, value):
        last_fuel_odometer = ld.get_param(
            field=lc.odometer_total_field,
            table=lc.fuel_data_table,
            con=lc.conn_string)
        last_odometer_service = ld.last_odometer_service(
            table=lc.repair_data_table,
            con=lc.conn_string,
            data_field=lc.odometer,
            filter_field=lc.service_odometer)
        current_odometer = last_fuel_odometer

        if clicks:
            if int(value) > int(last_fuel_odometer):
                current_odometer = value

        if current_odometer < (int(last_odometer_service) + 7000):
            style_div = dict(backgroundColor='#c9e5ab')
            style_label = dict(color='#1b511a', fontWeight='bold')
            style_label_tbl = dict(color='#1b511a', fontWeight='bold', background='#c9e5ab')
            return f'Следующая замена масла в двигателе через ' \
                   f'{(int(last_odometer_service) + 7000) - current_odometer} километров', style_div, style_label, \
                   style_label, current_odometer, last_odometer_service, current_odometer, current_odometer,\
                   current_odometer, current_odometer, current_odometer, current_odometer, style_label_tbl
        elif (int(last_odometer_service) + 7000) <= current_odometer < (int(last_odometer_service) + 15000):
            style_div = dict(backgroundColor='#efca66')
            style_label = dict(color='#6f2205', fontWeight='bold')
            style_label_tbl = dict(color='#6f2205', fontWeight='bold', background='#efca66')
            return f'ВНИМАНИЕ! Необходимо заменить масло в двигателе, в течении ' \
                   f'{(int(last_odometer_service) + 15000) - current_odometer} километров', style_div, \
                   style_label, style_label, current_odometer, last_odometer_service, current_odometer, \
                   current_odometer, current_odometer, current_odometer, current_odometer, current_odometer, style_label_tbl
        else:
            style_div = dict(backgroundColor='rgb(223, 3, 38)')
            style_label = dict(color='white', fontWeight='bold', fontSize='18px')
            style_label_tbl = dict(color='white', fontWeight='bold', background='rgb(223, 3, 38)')
            return f'ВНИМАНИЕ! ПЕРЕПРОБЕГ {current_odometer - (int(last_odometer_service) + 15000)} КИЛОМЕТРОВ! ' \
                   f'СРОЧНО ЗАМЕНИТЕ МАСЛО В ДВИГАТЕЛЕ!!!', style_div, style_label, style_label, current_odometer,\
                   last_odometer_service, current_odometer, current_odometer, current_odometer, current_odometer, \
                   current_odometer, current_odometer, style_label_tbl
