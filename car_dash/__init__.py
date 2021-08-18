from dash_table.Format import Format, Scheme


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