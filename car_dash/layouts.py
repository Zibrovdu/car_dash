import calendar
import datetime

import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt

import car_dash.load_cfg as lc
import car_dash.load_data as ld
import car_dash.date_cfg as dc


def serve_layout():
    start_params = ld.get_start_params(table=lc.fuel_data_table, con=lc.conn_string)

    start_week, start_month, start_year = start_params[0][0], start_params[0][1], start_params[0][2]
    finish_week, finish_month, finish_year = start_params[1][0], start_params[1][1], start_params[1][2]

    choice_type = [dict(label='Неделя', value='w'),
                   dict(label='Месяц', value='m'),
                   dict(label='Произвольный период', value='p')]

    d_month = dc.get_months(start_month=start_month,
                            start_year=start_year,
                            finish_month=finish_month,
                            finish_year=finish_year)

    d_week = dc.get_weeks(start_week=start_week,
                          start_year=start_year,
                          finish_week=finish_week,
                          finish_year=finish_year)

    tab_selected_style = dict(backgroundColor='#dee8ec',
                              fontWeight='bold')

    layout = html.Div([
        html.Div([
            html.H2('HONDA The power of dreams'),
            html.A([
                html.Img(src="assets/pixlr-bg-result.png")
            ], href='#modal-1', className='js-modal-open link')
        ], className="banner"),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Label("Выберите период: ")
                    ],
                        className='wrapper-dropdown-4'
                    )
                ],
                    className='bblock'),
                html.Div([
                    html.Div([
                        dcc.Dropdown(id='choice_type',
                                     options=choice_type,
                                     searchable=False,
                                     clearable=False,
                                     optionHeight=50,
                                     value='w',
                                     disabled=False)
                    ],
                        className='wrapper-dropdown-3',
                        style=dict(width='295px',
                                   display='block')
                    )
                ],
                    className='bblock'),  # choice period dropdown
                html.Div([
                    html.Div([
                        dcc.Dropdown(id='month_choice',
                                     options=d_month,
                                     searchable=False,
                                     clearable=False,
                                     value='_'.join([str(finish_month), str(finish_year)]),
                                     disabled=False
                                     )
                    ],
                        className='wrapper-dropdown-3',
                        style=dict(width='190px')
                    ),
                ],
                    className='bblock'),
            ]),  # Month_choice dropdown
            html.Div([
                html.Div([
                    dcc.Dropdown(id='week_choice',
                                 options=d_week,
                                 searchable=False,
                                 clearable=False,
                                 value='_'.join([str(finish_week), str(finish_year)]),
                                 style=dict(width='100%',
                                            heigth='60px'),
                                 disabled=False)
                ],
                    className='wrapper-dropdown-3',
                    style=dict(width='420px')
                )
            ],
                className='bblock'),  # Week_choice dropdown
            html.Div([
                html.Div([
                    dcc.DatePickerRange(id='period_choice',
                                        display_format='DD-MM-YYYY',
                                        min_date_allowed=datetime.date(start_year, start_month, 1),
                                        max_date_allowed=datetime.date(finish_year, finish_month, calendar.monthrange(
                                            finish_year, finish_month)[1]),
                                        start_date=datetime.date(ld.end_year, ld.end_month, ld.end_day),
                                        end_date=datetime.date(ld.current_year, ld.current_month, ld.current_day),
                                        updatemode='bothdates',
                                        style=dict(background='#b1d5fa'),
                                        clearable=False
                                        )
                ])
            ], className='bblock', style=dict(heigth='45px')),  # Period_choice range picker
        ], style=dict(background='#b1d5fa')),
        html.Div([
            html.Div([
                html.Label(
                    'Текущий пробег:',
                    id='curr_odo'
                ),
                dcc.Input(
                    id='curr_odometr_input',
                    type='number',
                    inputMode='numeric',
                    value=ld.get_param(
                        field=lc.odometer_total_field,
                        table=lc.fuel_data_table,
                        con=lc.conn_string
                    ),
                    minLength=len(str(ld.get_param(
                        field=lc.odometer_total_field,
                        table=lc.fuel_data_table,
                        con=lc.conn_string
                    ))),
                    className='input_curr_odometr'
                ),
                html.Button(
                    id='submit_odometr_btn',
                    n_clicks=0,
                    children='Установить',
                    className='btn_confirm_odometr'
                ),
                html.Label(
                    id='lbl_change_oil',
                    className='wrapper-dropdown-3'
                )
            ])
        ],
            className='div_change_oil',
            id='change_oil_div'
        ),

        html.Div([
            html.Div([
                dcc.Tabs(
                    id='',
                    value='summary',
                    children=[
                        dcc.Tab(
                            id='summary',
                            label='Суммарная информация',
                            value='summary',
                            children=[
                                html.Div([
                                    html.Div([
                                        # html.Table([
                                        #     html.Th([
                                        #         html.Label('Операция')
                                        #     ]),
                                        #     html.Th([
                                        #         html.Label('Дата последней замены')
                                        #     ]),
                                        #     html.Th([
                                        #         html.Label('Километраж')
                                        #     ]),
                                        #     html.Th([
                                        #         html.Label('Пробег с момента замены')
                                        #     ]),
                                        #     html.Th([
                                        #         html.Label('Время с момента замены')
                                        #     ]),
                                        #     html.Th([
                                        #         html.Label('Примечания')
                                        #     ]),
                                        #     html.Tr([
                                        #         html.Td([
                                        #             html.Label('Замена масла в ДВС')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_engine_oil_date')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_engine_oil_prev_odo')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_engine_oil_km')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_engine_oil_delta')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_engine_oil_descr')
                                        #         ])
                                        #     ],
                                        #         id='engine_oil_row'
                                        #     ),
                                        #     html.Tr([
                                        #         html.Td([
                                        #             html.Label('Замена масла в КПП')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_transmission_oil_date')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_transmission_oil_prev_odo')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_transmission_oil_km')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_transmission_oil_delta')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_transmission_oil_descr')
                                        #         ])
                                        #     ],
                                        #         id='transmission_oil_row'
                                        #     ),
                                        #     html.Tr([
                                        #         html.Td([
                                        #             html.Label('Замена воздушного фильтра')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_air_filter_date')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_air_filter_prev_odo')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_air_filter_km')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_air_filter_delta')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_air_filter_descr')
                                        #         ])
                                        #     ],
                                        #         id='air_filter_row'
                                        #     ),
                                        #     html.Tr([
                                        #         html.Td([
                                        #             html.Label('Замена фильтра салона')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_cabin_filter_date')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_cabin_filter_prev_odo')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_cabin_filter_km')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_cabin_filter_delta')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_cabin_filter_descr')
                                        #         ]),
                                        #     ],
                                        #         id='cabin_filter_row'
                                        #     ),
                                        #     html.Tr([
                                        #         html.Td([
                                        #             html.Label('Замена резинок стеклоочистителей')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_change_rubbers_date')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_change_rubbers_prev_odo')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_change_rubbers_km')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_change_rubbers_delta')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_change_rubbers_descr')
                                        #         ]),
                                        #     ],
                                        #         id='change_rubbers_row'
                                        #     ),
                                        #     html.Tr([
                                        #         html.Td([
                                        #             html.Label('Замена тормозной жидкости')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_brake_fluid_date')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_brake_fluid_prev_odo')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_brake_fluid_km')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_brake_fluid_delta')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_brake_fluid_descr')
                                        #         ]),
                                        #     ],
                                        #         id='brake_fluid_row'
                                        #     ),
                                        #     html.Tr([
                                        #         html.Td([
                                        #             html.Label('Регулировка клапанов ДВС')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_tune_valves_date')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_tune_valves_prev_odo')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_tune_valves_km')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_tune_valves_delta')
                                        #         ]),
                                        #         html.Td([
                                        #             html.Label(id='tb_tune_valves_descr')
                                        #         ]),
                                        #     ],
                                        #         id='tune_valves_row'
                                        #     ),
                                        # ]),
                                        html.Div([
                                            dt.DataTable(
                                                id='repair_table',
                                                style_data_conditional=[
                                                    {'if': {'filter_query': f'{{Состояние}} = ok', },
                                                     'backgroundColor': 'lightgreen'
                                                     },
                                                    {'if': {'filter_query': f'{{Состояние}} = warning', },
                                                     'backgroundColor': '#efca66'
                                                     },
                                                    {'if': {'filter_query': f'{{Состояние}} = stop', },
                                                     'backgroundColor': 'rgb(223, 3, 38)', 'color': 'white'
                                                     },
                                                ]
                                            )
                                        ],
                                            style=dict(fontSize='16px')
                                        ),

                                    ], style=dict(padding='40px'))
                                ])

                            ],
                            selected_style=tab_selected_style
                        ),
                        dcc.Tab(
                            id='fuel_tab',
                            label='Топливо',
                            value='fuel',
                            children=[
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Label('Количество литров:', className='label_liters'),
                                            html.Label(id='avg_liters', className='label_value_liters')
                                        ]),
                                    ], className='div_count_liters'),  # Карточка "Количество литров"
                                    html.Div([
                                        html.Div([
                                            html.Label('Средняя стоимость литра, руб:', className='label_price'),
                                            html.Label(id='avg_price', className='label_value_price')
                                        ]),
                                    ], className='div_price'),  # Карточка "Средняя стоимость литра"
                                    html.Div([
                                        html.Div([
                                            html.Label('Средний расход:', className='label_fuel_flow'),
                                            html.Label(id='fuel_flow', className='label_value_fuel_flow')
                                        ])
                                    ], className='div_fuel_flow'),  # Карточка "Средний расход"
                                ], className='div_cards'),
                                html.Div([
                                    dt.DataTable(id='main_fuel_table')
                                ], className='div_fuel_main_table'),
                            ],
                            selected_style=tab_selected_style
                        ),
                        dcc.Tab(
                            id='repair_tab',
                            value='repair',
                            label='Запчасти и работы',
                            children=[],
                            selected_style=tab_selected_style
                        )
                    ], colors=dict(border='#dee8ec',
                                   primary='#df0326',
                                   background='#b1d5fa'))
            ])
        ])
    ])
    return layout
