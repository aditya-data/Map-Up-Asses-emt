import pandas as pd
import numpy as np


def calculate_distance_matrix(df)->pd.DataFrame():
    distance_dict = {}
    last_entered = []
    cur = -1
    for row in df.itertuples():
        start = row[1]
        end = row[2]
        dist = row[3]
        if (start, end) in distance_dict:
            continue
        else:
            distance_dict[(start, end)] = dist
            last = dist
            last_entered.append((start, end))
            cur += 1
            temp = cur - 1
            while temp >= 0:
                if (last_entered[temp][0], end) in distance_dict:
                    temp -= 1
                    continue
                else:
                    distance_dict[(last_entered[temp][0], end)] = distance_dict[(last_entered[temp][0], last_entered[temp][1])] + last
                    last = distance_dict[(last_entered[temp][0], last_entered[temp][1])] + last
                    temp -= 1
    
    
    index = df['id_start']._append(pd.Series(df['id_end'].iloc[-1])).unique()

    temp_df = pd.DataFrame(np.NaN, index=index, columns=index)
    
    for key, value in distance_dict.items():
        temp_df.loc[key[0], key[1]] = value
        temp_df.loc[key[1], key[0]] = value
        
    df = temp_df.fillna(0)
            
    return df



def unroll_distance_matrix(df)->pd.DataFrame():
    # Write your logic here
    
    num_rows = len(df.index)
    num_cols = len(df.columns)
    row_start = 0
    col_start = 1

    indexes =  df.index
    columns = df.columns

    temp = []

    while (row_start < num_rows) and (col_start < num_cols):
        temp.append([indexes[row_start], columns[col_start], df.loc[indexes[row_start], columns[col_start]]])

        row_start += 1
        col_start += 1
        
    df = pd.DataFrame(temp, columns=['id_start', 'id_end', 'distance'])

    return df


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
# Write your logic here
    temp = df['id_start'][df['id_start'].between(reference_id*0.9, reference_id*1.1)].sort_values()

    return temp


def calculate_toll_rate(df)->pd.DataFrame():
    # Wrie your logic here
    df['moto'] = df['distance'] * 0.8

    df['car'] = df['distance'] * 1.2

    df['rv'] = df['distance'] * 1.5

    df['bus'] = df['distance'] * 2.2

    df['truck'] = df['distance'] * 3.6
    
    df.drop('distance', axis=1, inplace=True)


    return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    additional_data = {
    'start_day': ['Monday', 'Tuesday', 'Wednesday', 'Saturday'],
    'start_time': ['00:00:00', '10:00:00', '18:00:00', '00:00:00'],
    'end_day': ['Friday', 'Saturday', 'Sunday', 'Sunday'],
    'end_time': ['10:00:00', '18:00:00', '23:59:59', '23:59:59']
    }

    additional_df = pd.DataFrame(additional_data)
    df = df.merge(additional_df, how='cross')[['id_start', 'id_end', 'distance', 'start_day', 'start_time', 'end_day', 'end_time', 'moto', 'car', 'rv', 'bus', 'truck']]
    df.loc[(df['start_day'] == 'Saturday') & (df['end_day'] == 'Sunday'), ['moto', 'car', 'rv', 'bus', 'truck']] *= 0.7
    df.loc[((df['start_time'] == '00:00:00') & (df['end_time'] == '10:00:00')) & ~(df['start_day'] == 'Saturday') & (df['end_day'] == 'Sunday'), ['moto', 'car', 'rv', 'bus', 'truck']] *= 0.8
    df.loc[((df['start_time'] == '10:00:00') & (df['end_time'] == '18:00:00')) & ~(df['start_day'] == 'Saturday') & (df['end_day'] == 'Sunday'), ['moto', 'car', 'rv', 'bus', 'truck']] *= 1.2
    df.loc[((df['start_time'] == '18:00:00') & (df['end_time'] == '23:59:59')) & ~(df['start_day'] == 'Saturday') & (df['end_day'] == 'Sunday'), ['moto', 'car', 'rv', 'bus', 'truck']] *= 0.8

    return df