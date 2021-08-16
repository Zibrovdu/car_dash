from dash.dependencies import Input, Output

import car_dash.load_data as ld
import car_dash.load_cfg as lc


def register_callbacks(app):
    @app.callback(
        Output('avg_liters', 'children'),
        Output('avg_price', 'children'),
        Output('mileage', 'children'),
        [Input('period_choice', 'start_date'),
         Input('period_choice', 'end_date'),
         Input('month_choice', 'value'),
         Input('week_choice', 'value'),
         Input('choice_type', 'value')],
    )
    def update_fuel_statistic_table(start_date_user, end_date_user, choosen_month, choosen_week, choice_type_period):
        print(choosen_week)
        week, year = int(choosen_week[:2]), int(choosen_week[3:])
        print(week, year)
        period_choice, week_choice, month_choice = ld.choosen_type(type_period=choice_type_period,
                                                                   start_date=start_date_user,
                                                                   end_date=end_date_user,
                                                                   ch_month=choosen_month,
                                                                   ch_week=week)

        filtered_fuel_data_df = ld.get_filtered_df(table_name=lc.fuel_data_table,
                                                   ch_month=choosen_month,
                                                   ch_week=week,
                                                   ch_week_year=year,
                                                   start_date=start_date_user,
                                                   end_date=end_date_user,
                                                   type_period=choice_type_period)
        print(filtered_fuel_data_df)
        avg_liters = round(filtered_fuel_data_df['liters'].sum(), 2)
        avg_price = round(filtered_fuel_data_df['price'].mean(), 2)
        mileage = round(filtered_fuel_data_df['odometr'].sum())

        return avg_liters, avg_price, mileage
