import dash
from dash.dependencies import Input, Output, State

import car_dash.load_data as ld
import car_dash.load_cfg as lc


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
        period_choice, week_choice, month_choice = ld.choosen_type(type_period=choice_type_period,
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
        fuel_columns = ld.fuel_data_columns(filtered_fuel_data_df)

        return (period_choice, month_choice, week_choice, avg_liters, avg_price, fuel_flow,
                filtered_fuel_data_df.to_dict('records'), fuel_columns)

    @app.callback(
        Output('lbl_change_oil', 'children'),
        Input('submit_odometr_btn', 'n_clicks'),
        State('curr_odometr_input', 'value')
    )
    def need_change_engine_oil(clicks, value):
        if clicks:
            return value
        return dash.no_update

