from dash.dependencies import Input, Output, State

import car_dash.load_data as ld
import car_dash.load_cfg as lc
import car_dash.date_cfg as dc
import car_dash.processing_data as prd
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
        Output('tb_engine_oil_date', 'children'),
        Output('tb_engine_oil_prev_odo', 'children'),
        Output('tb_engine_oil_km', 'children'),
        Output('tb_engine_oil_delta', 'children'),
        Output('tb_engine_oil_descr', 'children'),
        # Output('engine_oil_row', 'style'),
        # Output('tb_transmission_oil_date', 'children'),
        # Output('tb_transmission_oil_odo', 'children'),
        # Output('tb_transmission_oil_km', 'children'),
        # Output('tb_transmission_oil_delta', 'children'),
        # Output('tb_transmission_oil_descr', 'children'),
        # Output('transmission_oil_row', 'style'),
        Output('tb_air_filter_date', 'children'),
        Output('tb_air_filter_prev_odo', 'children'),
        Output('tb_air_filter_km', 'children'),
        Output('tb_air_filter_delta', 'children'),
        # Output('tb_air_filter_descr', 'children'),
        # Output('air_filter_row', 'style'),
        Output('tb_cabin_filter_date', 'children'),
        Output('tb_cabin_filter_prev_odo', 'children'),
        Output('tb_cabin_filter_km', 'children'),
        Output('tb_cabin_filter_delta', 'children'),
        # Output('tb_cabin_filter_descr', 'children'),
        # Output('cabin_filter_row', 'style'),
        Output('tb_change_rubbers_date', 'children'),
        Output('tb_change_rubbers_prev_odo', 'children'),
        Output('tb_change_rubbers_km', 'children'),
        Output('tb_change_rubbers_delta', 'children'),
        # Output('tb_change_rubbers_descr', 'children'),
        # Output('change_rubbers_row', 'style'),
        Output('tb_brake_fluid_date', 'children'),
        Output('tb_brake_fluid_prev_odo', 'children'),
        Output('tb_brake_fluid_km', 'children'),
        Output('tb_brake_fluid_delta', 'children'),
        # Output('tb_brake_fluid_descr', 'children'),
        # Output('brake_fluid_row', 'style'),
        Output('tb_tune_valves_date', 'children'),
        Output('tb_tune_valves_prev_odo', 'children'),
        Output('tb_tune_valves_km', 'children'),
        Output('tb_tune_valves_delta', 'children'),
        # Output('tb_tune_valves_descr', 'children'),
        # Output('valves_row', 'style'),
        Input('submit_odometr_btn', 'n_clicks'),
        State('curr_odometr_input', 'value')
    )
    def need_change_engine_oil(clicks, value):
        last_fuel_odometer = ld.get_param(
            field=lc.odometer_total_field,
            table=lc.fuel_data_table,
            con=lc.conn_string)
        repair_df = ld.prepare_df_to_calc(
            table=lc.repair_data_table,
            con=lc.conn_string,
        )
        last_change_engine_oil_date, last_change_engine_oil_km = ld.last_change_engine_oil(
            df=repair_df
        )
        last_change_air_filter_date, last_change_air_filter_km = ld.last_change_air_filter(
            df=repair_df
        )
        last_change_cabin_filter_date, last_change_cabin_filter_km = ld.last_change_cabin_filter(
            df=repair_df
        )
        last_change_rubbers_date, last_change_rubbers_km = ld.last_change_rubbers(
            df=repair_df
        )
        last_change_brake_fluid_date, last_change_brake_fluid_km = ld.last_change_brake_fluid(
            df=repair_df
        )
        last_tune_valves_date, last_tune_valves_km = ld.last_tune_valves(
            df=repair_df
        )

        current_odometer = last_fuel_odometer

        odometer_change_engine_oil = int(current_odometer) - int(last_change_engine_oil_km)
        # odometer_change_air_filter = int(current_odometer) - int(last_change_air_filter_km)
        odometer_change_air_filter = int(current_odometer) - int(last_change_air_filter_km)
        odometer_change_cabin_filter = int(current_odometer) - int(last_change_cabin_filter_km)
        odometer_change_rubbers = int(current_odometer) - int(last_change_rubbers_km)
        odometer_change_brake_fluid = int(current_odometer) - int(last_change_brake_fluid_km)
        odometer_tune_valves = int(current_odometer) - int(last_tune_valves_km)

        tb_engine_oil_delta = prd.calc_delta(from_date=last_change_engine_oil_date)
        # tb_engine_oil_delta = prd.calc_delta(from_date=last_change_engine_oil_date)
        tb_change_air_filter_delta = prd.calc_delta(from_date=last_change_air_filter_date)
        tb_change_cabin_filter_delta = prd.calc_delta(from_date=last_change_cabin_filter_date)
        tb_change_rubbers_delta = prd.calc_delta(from_date=last_change_rubbers_date)
        tb_change_brake_fluid_delta = prd.calc_delta(from_date=last_change_brake_fluid_date)
        tb_tune_valves_delta = prd.calc_delta(from_date=last_tune_valves_date)

        if clicks:
            if int(value) > int(last_fuel_odometer):
                current_odometer = value

        msg_engine_oil, style_change_oil_div, style_lbl_change_oil, style_label_tbl = prd.calc_change_engine_oil(
            current_odometer=current_odometer,
            last_change_odometer=last_change_engine_oil_km,
            msg_ok=lc.ok_msg_engine_oil,
            msg_warning=lc.warning_msg_engine_oil,
        )

        return (msg_engine_oil, style_change_oil_div, style_lbl_change_oil, style_lbl_change_oil,  # Upper banner
                # -------- ENGINE OIL ----------
                last_change_engine_oil_date, last_change_engine_oil_km, odometer_change_engine_oil, tb_engine_oil_delta,
                msg_engine_oil,
                # -------- TRANSMISSION OIL ----------
                # -------- AIR FILTER ----------
                last_change_air_filter_date, last_change_air_filter_km, odometer_change_air_filter,
                tb_change_air_filter_delta,
                # -------- CABIN FILTER ----------
                last_change_cabin_filter_date, last_change_cabin_filter_km, odometer_change_cabin_filter,
                tb_change_cabin_filter_delta,
                # -------- RUBBERS ----------
                last_change_rubbers_date, last_change_rubbers_km, odometer_change_rubbers, tb_change_rubbers_delta,
                # -------- BRAKE FLUID ----------
                last_change_brake_fluid_date, last_change_brake_fluid_km, odometer_change_brake_fluid,
                tb_change_brake_fluid_delta,
                # -------- TUNE VALVES ----------
                last_tune_valves_date, last_tune_valves_km, odometer_tune_valves, tb_tune_valves_delta
                )
