from cdo import Cdo
from dateutil import relativedelta

from src.Enumerations import Month
from src.utils import get_datetime_str, load_pkl, save_as_pkl


def correct_nc_file(
    path,
    output_file_name_temp,
    file_start_date,
    file_end_date,
    last_processed_date,
) -> None:

    input_file_name = f"ObjectMasks_{output_file_name_temp}_{get_datetime_str(file_start_date)}-{get_datetime_str(file_end_date)}"

    if file_end_date != last_processed_date:
        file_end_date = file_end_date - relativedelta.relativedelta(months=1)

    output_file_name = f"ObjectMasks_{output_file_name_temp}_{get_datetime_str(file_start_date)}-{get_datetime_str(file_end_date)}_corrected"

    cdo = Cdo()

    if file_start_date.month == Month.JANUARY:
        print(f"correct nc-file with \n cdo -selmon,1,2,3,4,5,6 {path}{input_file_name}.nc {path}{output_file_name}.nc")
        cdo.selmon(
            "1,2,3,4,5,6",
            input=f"{path}{input_file_name}.nc",
            output=f"{path}{output_file_name}.nc",
            options="-f nc4c -z zip_5",
        )

    elif file_start_date.month == Month.JULY:
        print(f"correct nc-file with \n cdo -selmon,6,7,8,9,10,11,12 {path}{input_file_name}.nc {path}{output_file_name}.nc")

        cdo.selmon(
            "7,8,9,10,11,12",
            input=f"{path}{input_file_name}.nc",
            output=f"{path}{output_file_name}.nc",
            options="-f nc4c -z zip_5",
        )


def cleanup_dicts(
    output_path,
    output_file_name_temp,
    file_start_date,
    file_end_date,
    last_processed_date,
    type_,
) -> None:

    input_name = f"{output_path}{type_}_{output_file_name_temp}_{get_datetime_str(file_start_date)}-{get_datetime_str(file_end_date)}"

    if file_end_date != last_processed_date:
        file_end_date = file_end_date - relativedelta.relativedelta(months=1)

    obj_dict = load_pkl(input_name)
    dict_bak = dict(obj_dict)

    print(f"clean up {output_path}{type_}_{output_file_name_temp}_{get_datetime_str(file_start_date)}-{get_datetime_str(file_end_date)}.pkl")

    for i, key in enumerate(dict_bak.keys()):
        obj_start_date = dict_bak[key]["times"][0]
        obj_end_date = dict_bak[key]["times"][-1]

        if obj_start_date < file_end_date:
            continue

        if obj_start_date == file_start_date and obj_start_date != last_processed_date:
            del obj_dict[key]

        if obj_end_date > file_end_date and obj_start_date > file_end_date:
            del obj_dict[key]

        output_name = f"{output_path}{type_}_{output_file_name_temp}_{get_datetime_str(file_start_date)}-{get_datetime_str(file_end_date)}"

    print("clean up finished")
    save_as_pkl(obj_dict, output_name=output_name + "_corrected")


# print("remove old pickle file")


# os.remove(f'{input_name}.pkl')
