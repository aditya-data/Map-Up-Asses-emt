import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    # problem of transformation . can be done using pivot function.
    
    df = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)

    return df


def get_type_count(df)->dict:
    # Write your logic here
    df['car_type'] = df['car'].apply(lambda x: 'low' if x <= 15 else ('medium' if x <= 25 else 'high'))

    return dict(sorted(dict(df['car_type'].value_counts()).items(), key=lambda x: x[0]))



def get_bus_indexes(df)->list:
    # Write your logic here

    return list(df[df['bus'] > 2*df['bus'].mean()].index)



def filter_routes(df)->list:
    # Write your logic here
    filtered_df = df.groupby('route').filter(lambda x: x['truck'].mean() > 7)
    
    sorted_routes = sorted(filtered_df['route'].unique())
    
    return list(sorted_routes)

def multiply_matrix(matrix)->pd.DataFrame:
    # Write your logic here
    matrix = matrix.applymap(lambda x: x*0.75 if x > 20 else x*1.25)

    return matrix


def time_check(df)->pd.Series:
    # Write your logic here
    from datetime import datetime, timedelta

    days_map = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
    time_differences = []
    for index, row in df.iterrows():
        start_day_num = days_map[row['startDay']]
        end_day_num = days_map[row['endDay']]
        day_difference = (end_day_num - start_day_num + 7) % 7

        start_time = datetime.strptime(row['startTime'], '%H:%M:%S')
        end_time = datetime.strptime(row['endTime'], '%H:%M:%S')

        time_difference = (day_difference * 24) + ((end_time - start_time).total_seconds() / 3600)
        time_differences.append(time_difference)

    df['time_difference_hours'] = time_differences
    
    
    ### all 7 days 24 hours covered 
    t = (df.groupby(['id', 'id_2'])[['time_difference_hours']].sum() > 24*7).squeeze()

    return pd.Series(t)

