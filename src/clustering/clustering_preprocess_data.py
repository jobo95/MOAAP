"""
    Preprocess geopotential heigth data for clustering according to Fabiano 2021:
    - CNRM-ICON_control
    - NorESM-ICON_control
    - CNRM-ICON_ssp
    - NorESM-ICON_ssp
    - ERA5
"""

from pathlib import Path

from cdo import Cdo

from src.Enumerations import Experiments, Season

for EXP in Experiments:
    # for EXP in [Experiments.ERA5]:
    print(EXP.name)

    exp = EXP.value
    outpath = exp.clustering_data_path
    Path(outpath).mkdir(parents=True, exist_ok=True)
    for season_ in Season:
        # for season_ in [Season.DJF]:
        print(season_.name)

        season = season_
        months = ",".join(map(str, season.value))
        level = 70000
        year_start = exp.year_start
        year_end = exp.year_end

        # general output file name
        out_string = f"{outpath}{exp.exp_name}_gph{level}_{year_start}_{year_end}_reglonlat_-90_90_20_88_1deg_{season.name}"

        cdo = Cdo()
        # merge raw files, select years and months, select level,remap to target grid
        if exp.exp_name == "ERA5":
            cdo.remapbil(
                exp.clustering_target_grid,
                input=f"-selmon,{months}  -selyear,{year_start}/{year_end}  -fillmiss -mergetime  " + " ".join(exp.gph_files_raw_gcm),
                output=f"{out_string}.nc",
            )
        else:
            cdo.remapbil(
                exp.clustering_target_grid,
                input=f"-selmon,{months}  -selyear,{year_start}/{year_end} -fillmiss -sellevel,{level} -mergetime  " + " ".join(exp.gph_files_raw_gcm),
                output=f"{out_string}.nc",
            )

        # compute field mean over NH
        cdo.fldmean(input=f"{out_string}.nc", output=f"{out_string}_fldmean.nc")

        # compute trend of field mean
        cdo.trend(
            input=f"{out_string}_fldmean.nc",
            output=f"{out_string}_fldmean_trenda.nc {out_string}_fldmean_trendb.nc",
        )

        # map field mean trends to target grid
        cdo.enlarge(
            f"{out_string}.nc",
            input=f"{out_string}_fldmean_trenda.nc",
            output=f"{out_string}_fldmean_trendaa.nc",
        )

        cdo.enlarge(
            f"{out_string}.nc",
            input=f"{out_string}_fldmean_trendb.nc",
            output=f"{out_string}_fldmean_trendbb.nc",
        )

        # subtract field mean trend from original file
        cdo.subtrend(
            input=f"{out_string}.nc {out_string}_fldmean_trendaa.nc {out_string}_fldmean_trendbb.nc",
            output=f"{out_string}_fldmean_detrend.nc",
        )

        # compute annual cycle
        cdo.ydaymean(
            input=f"{out_string}_fldmean_detrend.nc",
            output=f"{out_string}_fldmean_detrend_ydaymean.nc",
        )

        # subtract annual cycle from detrended data
        cdo.sub(
            input=f"{out_string}_fldmean_detrend.nc {exp.control_aac_file}{season.name}_fldmean_detrend_ydaymean.nc",
            output=f"{out_string}_fldmean_detrend_aac.nc",
        )

        # compute annual cycle without 29feb
        cdo.ydaymean(
            input=f"-del29feb {out_string}_fldmean_detrend.nc",
            output=f"{out_string}_fldmean_detrend_ydaymean_del29feb.nc",
        )

        cdo.del29feb(
            input=f"{out_string}_fldmean_detrend.nc",
            output=f"{out_string}_fldmean_detrend_del29feb.nc",
        )

        # subtract annual cycle from detrended data without 29feb
        print(f"{exp.control_aac_file_del29feb}{season.name}_fldmean_detrend_ydaymean_del29feb.nc")
        cdo.sub(
            input=f"  {out_string}_fldmean_detrend_del29feb.nc {exp.control_aac_file_del29feb}{season.name}_fldmean_detrend_ydaymean_del29feb.nc",
            output=f"{out_string}_fldmean_detrend_del29feb_aac.nc",
        )
