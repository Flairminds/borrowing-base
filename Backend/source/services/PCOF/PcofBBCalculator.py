import pickle
import pandas as pd
import json

from source.services.PCOF.calculation.Pcof_response_generator import generate_response
from source.services.PCOF.utility import (
    read_excels,
    get_included_excluded_assets_map_json,
)
from source.services.PCOF.calculation.functionsCall import calculate_bb
from models import BaseDataFile, db


class PcofBBCalculator:
    def get_bb_calculation(self, base_data_file, selected_assets, user_id):
        xl_sheet_df_map = pickle.loads(base_data_file.file_data)
        (
            df_PL_BB_Build,
            df_Inputs_Other_Metrics,
            df_Availability_Borrower,
            df_PL_BB_Results,
            df_subscriptionBB,
            df_security,
            df_industry,
            df_Input_pricing,
            df_Inputs_Portfolio_LeverageBorrowingBase,
            df_Obligors_Net_Capital,
            df_Inputs_Advance_Rates,
            df_Inputs_Concentration_limit,
            df_principle_obligations,
        ) = read_excels(xl_sheet_df_map)

        included_excluded_assets_list_map_json = get_included_excluded_assets_map_json(
            df_PL_BB_Build
        )

        original_PL_BB_Build = df_PL_BB_Build.copy()
        selected_assets_mask = df_PL_BB_Build["Investment Name"].isin(selected_assets)

        df_PL_BB_Build = df_PL_BB_Build[selected_assets_mask].reset_index(drop=True)
        df_PL_BB_Build = df_PL_BB_Build[df_PL_BB_Build["Is Eligible Issuer"] == "Yes"]

        if "Cash" not in selected_assets:
            cash_row = original_PL_BB_Build[
                original_PL_BB_Build["Investment Name"] == "Cash"
            ]
            df_PL_BB_Build = pd.concat([df_PL_BB_Build, cash_row], ignore_index=True)
        else:
            cash_row = original_PL_BB_Build[
                original_PL_BB_Build["Investment Name"] == "Cash"
            ]
            if cash_row["Is Eligible Issuer"].tolist()[0] == "No":
                df_PL_BB_Build = pd.concat(
                    [df_PL_BB_Build, cash_row], ignore_index=True
                )
        # Calculate the result files
        (
            df_PL_BB_Build,
            df_Inputs_Other_Metrics,
            df_Availability_Borrower,
            df_PL_BB_Results,
            df_subscriptionBB,
            df_security,
            df_industry,
            df_Input_pricing,
            df_Inputs_Portfolio_LeverageBorrowingBase,
            df_Obligors_Net_Capital,
            df_Inputs_Advance_Rates,
            df_Inputs_Concentration_limit,
            df_principle_obligations,
            df_segmentation_overview,
            df_PL_BB_Output,
        ) = calculate_bb(
            df_PL_BB_Build,
            df_Inputs_Other_Metrics,
            df_Availability_Borrower,
            df_PL_BB_Results,
            df_subscriptionBB,
            df_security,
            df_industry,
            df_Input_pricing,
            df_Inputs_Portfolio_LeverageBorrowingBase,
            df_Obligors_Net_Capital,
            df_Inputs_Advance_Rates,
            df_Inputs_Concentration_limit,
            df_principle_obligations,
        )

        # Save calculated files to DB
        intermediate_calculation = {
            "df_PL_BB_Build": df_PL_BB_Build,
            "df_Inputs_Other_Metrics": df_Inputs_Other_Metrics,
            "df_Availability_Borrower": df_Availability_Borrower,
            "df_PL_BB_Results": df_PL_BB_Results,
            "df_subscriptionBB": df_subscriptionBB,
            "df_subscriptionBB": df_subscriptionBB,
            "df_security": df_security,
            "df_industry": df_industry,
            "df_Input_pricing": df_Input_pricing,
            "df_Inputs_Portfolio_LeverageBorrowingBase": df_Inputs_Portfolio_LeverageBorrowingBase,
            "df_Obligors_Net_Capital": df_Obligors_Net_Capital,
            "df_Inputs_Advance_Rates": df_Inputs_Advance_Rates,
            "df_Inputs_Concentration_limit": df_Inputs_Concentration_limit,
            "df_principle_obligations": df_principle_obligations,
            "df_segmentation_overview": df_segmentation_overview,
            "df_PL_BB_Output": df_PL_BB_Output,
        }

        pickled_intermediate_calculation = pickle.dumps(intermediate_calculation)
        base_data_file.intermediate_calculation = pickled_intermediate_calculation

        latest_data = (
            BaseDataFile.query.filter(BaseDataFile.user_id == user_id)
            .order_by(BaseDataFile.closing_date.desc())
            .first()
        )
        closing_date = latest_data.closing_date.strftime("%Y-%m-%d")

        (
            card_data,
            segmentation_Overview_data,
            security_data,
            concentration_Test_data,
            principal_obligation_data,
            segmentation_chart_data,
            security_chart_data,
        ) = generate_response(
            df_PL_BB_Results,
            df_security,
            df_segmentation_overview,
            df_principle_obligations,
            df_Availability_Borrower,
        )

        response_data = {
            "card_data": card_data,
            "segmentation_overview_data": segmentation_Overview_data,
            "security_data": security_data,
            "concentration_test_data": concentration_Test_data,
            "principal_obligation_data": principal_obligation_data,
            "segmentation_chart_data": segmentation_chart_data,
            "security_chart_data": security_chart_data,
            "closing_date": closing_date,
        }

        # upsert pickled_response_data
        pickled_response_data = pickle.dumps(response_data)
        base_data_file.response = pickled_response_data

        # update json_include_exclude_map
        included_excluded_assets_list_map = json.loads(
            included_excluded_assets_list_map_json
        )
        all_assets_list = included_excluded_assets_list_map["included_assets"]

        excluded_assets = all_assets_list.copy()
        for included_asset in selected_assets:
            if included_asset in all_assets_list:
                excluded_assets.remove(included_asset)

        included_excluded_assets_map = {
            "included_assets": selected_assets,
            "excluded_assets": excluded_assets,
        }

        json_include_exclude_map = json.dumps(included_excluded_assets_map)
        base_data_file.included_excluded_assets_map = json_include_exclude_map

        db.session.add(base_data_file)
        db.session.commit()
        return response_data
