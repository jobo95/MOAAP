import datetime

import numpy as np
from itertools import product
from dateutil import relativedelta


def create_datetime_lists(first_year, last_year, months=7, correct_last_endtime=True):

    start_year_ar = np.arange(first_year, last_year)
    start_month_ar = [1, 7]
    start_date_list = [datetime.datetime(x, y, 1, 0, 0)
                       for x, y in product(start_year_ar, start_month_ar)]
    end_date_list = [
        x + relativedelta.relativedelta(months=months) for x in start_date_list]

    if correct_last_endtime:
        end_date_list[-1] = end_date_list[-1] - \
            relativedelta.relativedelta(months=1)

    # end_date_list[0].strftime("%Y_%m_%d")
    return start_date_list, end_date_list


def get_datetime_str(datetime):
    return datetime.strftime("%Y_%m_%d")


def load_pkl(output_name):

    with open(output_name+'.pkl', 'rb') as pickle_file:
        ob_dict = pickle.load(pickle_file)
    return ob_dict

def save_as_pkl(dict_, output_name):
                
    with open(output_name+'.pkl', 'wb') as handle:
        pickle.dump(dict_, handle, protocol=pickle.HIGHEST_PROTOCOL)
 
