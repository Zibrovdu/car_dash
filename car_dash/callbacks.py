
from dash.dependencies import Input, Output

import car_dash.load_data as ld
import car_dash.load_cfg as lc


def register_callbacks(app):
    @app.callback(
        Output('avg_liters', 'children'),
        [Input('week_choice', 'value')],
    )
    def update_fuel_statistic_table(choosen_week):
        # period_choice, week_choice, month_choice = ld.choosen_type(type_period=choice_type_period,
        #                                                            start_date=start_date_user,
        #                                                            end_date=end_date_user,
        #                                                            ch_month=choosen_month,
        #                                                            ch_week=choosen_week)
        #
        # filtered_fuel_data_df = ld.get_filtered_df(table_name=lc.fuel_data_table,
        #                                            ch_month=choosen_month,
        #                                            ch_week=choosen_week,
        #                                            start_date=start_date_user,
        #                                            end_date=end_date_user,
        #                                            type_period=choice_type_period)
        # print(filtered_fuel_data_df)
        # avg_liters = round(filtered_fuel_data_df['liters'].mean(), 2)
        # avg_price = round(filtered_fuel_data_df['price'].mean(), 2)
        print(choosen_week)
        return choosen_week
