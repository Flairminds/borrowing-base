import json
import pickle
import copy

from source.services.PCOF import utility as pcofUtility
from source.services.PCOF.calculation.functionsCall import calculate_bb
from source.services.PCOF.WIA import responseGenerator2
from source.utility.ServiceResponse import ServiceResponse
from models import db

class UpdateAssetAnalyst():

    @staticmethod
    def update_assset(base_data_file, modified_base_data_file):
        try:
            base_data = pickle.loads(base_data_file.file_data)
            pl_bb_build = base_data["PL BB Build"]
            pl_bb_build = pl_bb_build[pl_bb_build["Is Eligible Issuer"] == "Yes"]
            included_asset = json.loads(base_data_file.included_excluded_assets_map)["included_assets"]
            selected_assets_mask = pl_bb_build["Investment Name"].isin(included_asset)
            pl_bb_build = pl_bb_build[selected_assets_mask].reset_index(drop=True)

            initial_base_data = pickle.loads(base_data_file.file_data)
            initial_base_data["PL BB Build"] = pl_bb_build

            new_base_data = copy.deepcopy(initial_base_data)
            modified_data =  pickle.loads(modified_base_data_file.modified_data)

            for sheet in modified_data.keys():
                new_base_data[sheet] = modified_data[sheet]

            intermediate_calculation = pickle.loads(base_data_file.intermediate_calculation)
            intermediate_metrics_data = {"inital_df_PL_BB_Output": intermediate_calculation["df_PL_BB_Output"]}

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
            ) = pcofUtility.read_excels(new_base_data)

            (
                df_PL_BB_Build,
                df_Inputs_Other_Metrics,
                Updated_df_Availability_Borrower,
                Updated_df_PL_BB_Results,
                df_subscriptionBB,
                Updated_df_security,
                df_industry,
                df_Input_pricing,
                df_Inputs_Portfolio_LeverageBorrowingBase,
                df_Obligors_Net_Capital,
                df_Inputs_Advance_Rates,
                df_Inputs_Concentration_limit,
                df_principle_obligations,
                Updated_df_segmentation_overview,
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

            intermediate_metrics_data["modified_df_PL_BB_Output"] = df_PL_BB_Output

            initial_xl_df_map = pickle.loads(base_data_file.intermediate_calculation)
            
            calculated_xl_df_map = {
                "df_PL_BB_Build": df_PL_BB_Build,
                "df_Inputs_Other_Metrics": df_Inputs_Other_Metrics,
                "Updated_df_Availability_Borrower": Updated_df_Availability_Borrower,
                "Updated_df_PL_BB_Results": Updated_df_PL_BB_Results,
                "df_subscriptionBB": df_subscriptionBB,
                "Updated_df_security": Updated_df_security,
                "df_industry": df_industry,
                "df_Input_pricing": df_Input_pricing,
                "df_Inputs_Portfolio_LeverageBorrowingBase": df_Inputs_Portfolio_LeverageBorrowingBase,
                "df_Obligors_Net_Capital": df_Obligors_Net_Capital,
                "df_Inputs_Advance_Rates": df_Inputs_Advance_Rates,
                "df_Inputs_Concentration_limit": df_Inputs_Concentration_limit,
                "df_principle_obligations": df_principle_obligations,
                "Updated_df_segmentation_overview": Updated_df_segmentation_overview,
                "df_PL_BB_Output": df_PL_BB_Output
            }

            (
                card_data,
                segmentation_overview_data,
                security_data,
                concentration_Test_data,
                principal_obligation_data,
                segmentation_chart_data,
                security_chart_data 
            )= responseGenerator2.generate_response(initial_xl_df_map=initial_xl_df_map, calculated_xl_df_map=calculated_xl_df_map)

            response_data = {
                "card_data": card_data,
                "segmentation_overview_data": segmentation_overview_data,
                "security_data": security_data,
                "concentration_test_data": concentration_Test_data,
                "principal_obligation_data": principal_obligation_data,
                "segmentation_chart_data": segmentation_chart_data,
                "security_chart_data": security_chart_data,
                "closing_date": base_data_file.closing_date.strftime("%Y-%m-%d"),
            }

            modified_base_data_file.response = response_data
            modified_base_data_file.intermediate_metrics_data = intermediate_metrics_data

            db.session.add(modified_base_data_file)
            db.session.commit()
            db.session.refresh(modified_base_data_file)
        
            return ServiceResponse.success(data=response_data)
    
        except Exception as e:
            return ServiceResponse.error(message="Internal server error")