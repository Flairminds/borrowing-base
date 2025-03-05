import numpy as np
import pandas as pd
import uuid


def get_ids_list(values, row_name):
    ids_list = []

    for term in values.keys():
        # id_name = row_name + "_" + term
        id_name = str(uuid.uuid4())
        ids_list.append(id_name)
    return ids_list


def get_span_ids_list(values, row_name):
    span_ids_list = []

    for term in values.keys():
        # id_name = row_name + "_" + term + "_value"
        id_name = str(uuid.uuid4()) + "_value"
        span_ids_list.append(id_name)
    return span_ids_list


def format_values_with_comma(values_dict):
    for key, value in values_dict.items():
        if isinstance(value, (int, float)):
            values_dict[key] = "{:,.2f}".format(value)
    return values_dict


def formula_info(df_PL_BB_Build, df_PL_BB_Output, row_name, col_name):
    colors = [
        "#d91421",
        "#14d9ab",
        "#51db2e",
        "#f57842",
        "#144fd9",
        "#d914be",
        "#476b6b",
    ]
    row_idx = df_PL_BB_Build[df_PL_BB_Build["Investment Name"] == row_name].index[0]

    if col_name == "Company":
        # commit 2
        values = {
            "invetsment_name": df_PL_BB_Output["Company"].iloc[row_idx],
            "final_invetsment_name": df_PL_BB_Build["Investment Name"].iloc[row_idx],
        }

        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)

        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>Company</span> = <span id='{ids_list[1]}'>'PL BB Build'!Investment Name</span>",
            "formula_variable_data": [
                {"key": ids_list[0], "value": "Company", "color": colors[0]},
                {
                    "key": ids_list[1],
                    "value": "'PL BB Build'!Investment Name",
                    "color": colors[1],
                },
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['invetsment_name']}</span> = <span id='{span_ids_list[1]}'>{values['final_invetsment_name']}</span>",
            "formula_values_data": [
                {
                    "key": span_ids_list[0],
                    "value": values["invetsment_name"],
                    "color": colors[0],
                },
                {
                    "key": span_ids_list[1],
                    "value": values["final_invetsment_name"],
                    "color": colors[1],
                },
            ],
        }

    if col_name == "Eligible":
        values = {
            "eligible": df_PL_BB_Output["Eligible"].iloc[row_idx],
            "final_eligible": df_PL_BB_Build["Final Eligible"].iloc[row_idx],
        }

        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)

        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>Eligible</span> = <span id='{ids_list[1]}'>'PL BB Build'!Final Eligible</span>",
            "formula_variable_data": [
                {"key": ids_list[0], "value": "Eligible", "color": colors[0]},
                {
                    "key": ids_list[1],
                    "value": "PL BB Build'!Final Eligible",
                    "color": colors[1],
                },
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['eligible']}</span> = <span id='{span_ids_list[1]}'>{values['final_eligible']}</span>",
            "formula_values_data": [
                {
                    "key": span_ids_list[0],
                    "value": values["eligible"],
                    "color": colors[0],
                },
                {
                    "key": span_ids_list[1],
                    "value": values["final_eligible"],
                    "color": colors[1],
                },
            ],
        }

    if col_name == "Maturity":
        values = {
            "maturity": df_PL_BB_Output["Maturity"].iloc[row_idx].strftime("%Y-%m-%d"),
            "investment_maturity": df_PL_BB_Build["Investment Maturity"]
            .iloc[row_idx]
            .strftime("%Y-%m-%d"),
        }

        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)

        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>Maturity</span> = <span id='{ids_list[1]}'>'PL BB Build'!Investment Maturity</span>",
            "formula_variable_data": [
                {"key": ids_list[0], "value": "Maturity", "color": colors[0]},
                {
                    "key": ids_list[1],
                    "value": "PL BB Build'!Investment Maturity",
                    "color": colors[1],
                },
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['maturity']}</span> = <span id='{span_ids_list[1]}'>{values['investment_maturity']}</span>",
            "formula_values_data": [
                {
                    "key": span_ids_list[0],
                    "value": values["maturity"],
                    "color": colors[0],
                },
                {
                    "key": span_ids_list[1],
                    "value": values["investment_maturity"],
                    "color": colors[1],
                },
            ],
        }

    if col_name == "Industry":
        values = {
            "industry": df_PL_BB_Output["Industry"].iloc[row_idx],
            "investment_industry": df_PL_BB_Build["Investment Industry"].iloc[row_idx],
        }

        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)

        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>Industry</span> = <span id='{ids_list[1]}'>'PL BB Build'!Investment Industry</span>",
            "formula_variable_data": [
                {"key": ids_list[0], "value": "Industry", "color": colors[0]},
                {
                    "key": ids_list[1],
                    "value": "PL BB Build'!Investment Industry",
                    "color": colors[1],
                },
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['industry']}</span> = <span id='{span_ids_list[1]}_value'>{values['investment_industry']}</span>",
            "formula_values_data": [
                {
                    "key": span_ids_list[0],
                    "value": values["industry"],
                    "color": colors[0],
                },
                {
                    "key": span_ids_list[1],
                    "value": values["investment_industry"],
                    "color": colors[1],
                },
            ],
        }

    if col_name == "Quoted / Unquoted":
        values = {
            "quoted_unquoted": df_PL_BB_Output["Quoted / Unquoted"].iloc[row_idx],
            "classifications_quoted_unquoted": df_PL_BB_Build[
                "Classifications Quoted / Unquoted"
            ].iloc[row_idx],
        }

        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)

        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>Quoted / Unquoted</span> = <span id='{ids_list[1]}'>'PL BB Build'!Classifications Quoted / Unquoted</span>",
            "formula_variable_data": [
                {"key": ids_list[0], "value": "Quoted / Unquoted", "color": colors[0]},
                {
                    "key": ids_list[1],
                    "value": "PL BB Build'!Classifications Quoted / Unquoted",
                    "color": colors[1],
                },
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['quoted_unquoted']}</span> = <span id='{span_ids_list[1]}'>{values['classifications_quoted_unquoted']}</span>",
            "formula_values_data": [
                {
                    "key": span_ids_list[0],
                    "value": values["quoted_unquoted"],
                    "color": colors[0],
                },
                {
                    "key": span_ids_list[1],
                    "value": values["classifications_quoted_unquoted"],
                    "color": colors[1],
                },
            ],
        }

    if col_name == "Security":
        values = {
            "security": df_PL_BB_Output["Security"].iloc[row_idx],
            "classification_adj_adjusted_type": df_PL_BB_Build[
                "Classification Adj. Adjusted Type"
            ].iloc[row_idx],
        }

        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)

        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>Security</span> = <span id='{ids_list[1]}'>'PL BB Build'!Classification Adj. Adjusted Type</span>",
            "formula_variable_data": [
                {"key": ids_list[0], "value": "Security", "color": colors[0]},
                {
                    "key": ids_list[1],
                    "value": "PL BB Build'!Classification Adj. Adjusted Type",
                    "color": colors[1],
                },
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['security']}</span> = <span id='{span_ids_list[1]}'>{values['classification_adj_adjusted_type']}</span>",
            "formula_values_data": [
                {
                    "key": span_ids_list[0],
                    "value": values["security"],
                    "color": colors[0],
                },
                {
                    "key": span_ids_list[1],
                    "value": values["classification_adj_adjusted_type"],
                    "color": colors[1],
                },
            ],
        }

    if col_name == "Cost":
        values = {
            "cost": df_PL_BB_Output["Cost"].iloc[row_idx],
            "investment_cost": df_PL_BB_Build["Investment Cost"].iloc[row_idx],
        }
        values = format_values_with_comma(values)

        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)

        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>Cost</span> = <span id='{ids_list[1]}'>'PL BB Build'!Investment Cost</span>",
            "formula_variable_data": [
                {"key": ids_list[0], "value": "Cost", "color": colors[0]},
                {
                    "key": ids_list[1],
                    "value": "PL BB Build'!Investment Cost",
                    "color": colors[1],
                },
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['cost']}</span> = <span id='{span_ids_list[1]}'>{values['investment_cost']}</span>",
            "formula_values_data": [
                {"key": span_ids_list[0], "value": values["cost"], "color": colors[0]},
                {
                    "key": span_ids_list[1],
                    "value": values["investment_cost"],
                    "color": colors[1],
                },
            ],
        }

    if col_name == "FMV":
        values = {
            "pl_bb_build!investment_fmv": df_PL_BB_Build["Investment FMV"].iloc[
                row_idx
            ],
            "fmv": df_PL_BB_Output["FMV"].iloc[row_idx],
        }

        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)

        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>FMV</span> = <button id='{ids_list[1]}'>'PL BB Build'!Investment FMV</button>",
            "formula_variable_data": [
                {"key": ids_list[0], "value": "FMV", "color": colors[0]},
                {
                    "key": ids_list[1],
                    "value": "'PL BB Build'!Investment FMV",
                    "color": colors[1],
                },
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['fmv']}</span> = <span id='{span_ids_list[1]}'>{values['pl_bb_build!investment_fmv']}</span>",
            "formula_values_data": [
                {"key": span_ids_list[0], "value": values["fmv"], "color": colors[0]},
                {
                    "key": span_ids_list[1],
                    "value": values["pl_bb_build!investment_fmv"],
                    "color": colors[1],
                },
            ],
        }

    if col_name == "'PL BB Build'!Investment FMV":
        values = {
            "pl_bb_build!investment_fmv": df_PL_BB_Build["Investment FMV"].iloc[
                row_idx
            ],
            "pl_bb_build!par": df_PL_BB_Build["Investment Par"].iloc[row_idx],
            "pl_bb_build!external_valuation": df_PL_BB_Build[
                "Investment External Valuation"
            ].iloc[row_idx],
            "pl_bb_build!internal_valuation": "-"
            if df_PL_BB_Build["Investment Internal Valuation"].iloc[row_idx] == 0.00
            else "nan",
        }
        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)

        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>'PL BB Build'!Investment FMV</span>= MIN(<span id='{ids_list[1]}'>'PL BB Build'!Investment Par</span>,<span id='{ids_list[2]}'>'PL BB Build'!Investment External Valuation</span>,<span id='{ids_list[3]}'>'PL BB Build'!Investment Internal Valuation</span>)",
            "formula_variable_data": [
                {
                    "key": ids_list[0],
                    "value": "'PL BB Build'!Investment FMV",
                    "color": colors[0],
                },
                {
                    "key": ids_list[1],
                    "value": "'PL BB Build'!Investment Par",
                    "color": colors[1],
                },
                {
                    "key": ids_list[2],
                    "value": "'PL BB Build'!Investment External Valuation",
                    "color": colors[2],
                },
                {
                    "key": ids_list[3],
                    "value": "'pl_bb_build'!internal_valuation",
                    "color": colors[3],
                },
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['pl_bb_build!investment_fmv']}</span>= MIN(<span id='{span_ids_list[1]}'>{values['pl_bb_build!par']}</span>,<span id='{span_ids_list[2]}'>{values['pl_bb_build!external_valuation']}</span>,<span id='{span_ids_list[3]}'>{values['pl_bb_build!internal_valuation']}</span>)",
            "formula_values_data": [
                {
                    "key": span_ids_list[0],
                    "value": values["pl_bb_build!investment_fmv"],
                    "color": colors[0],
                },
                {
                    "key": span_ids_list[1],
                    "value": values["pl_bb_build!par"],
                    "color": colors[1],
                },
                {
                    "key": span_ids_list[2],
                    "value": values["pl_bb_build!external_valuation"],
                    "color": colors[2],
                },
                {
                    "key": span_ids_list[3],
                    "value": values["pl_bb_build!internal_valuation"],
                    "color": colors[3],
                },
            ],
        }

    if col_name == "Ineligible Investments":
        values = {
            "ineligible_investments": df_PL_BB_Output["Ineligible Investments"].iloc[
                row_idx
            ],
            "eligible investments": df_PL_BB_Output["Eligible Investments"].iloc[
                row_idx
            ],
            "fmv": df_PL_BB_Output["FMV"].iloc[row_idx],
        }

        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)

        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>Ineligible Investments</span> = <button id='{ids_list[1]}'>Eligible Investments</button> - <button id='{ids_list[2]}'>FMV</buttoon>",
            "formula_variable_data": [
                {
                    "key": ids_list[0],
                    "value": "Ineligible Investments",
                    "color": colors[0],
                },
                {
                    "key": ids_list[1],
                    "value": "Eligible Investments",
                    "color": colors[1],
                },
                {"key": ids_list[2], "value": "FMV", "color": colors[2]},
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['ineligible_investments']}</span> = <span id='{span_ids_list[1]}'>{values['eligible investments']}</span>-<span id='{span_ids_list[2]}'>{values['fmv']}</span>",
            "formula_values_data": [
                {
                    "key": span_ids_list[0],
                    "value": values["ineligible_investments"],
                    "color": colors[0],
                },
                {
                    "key": span_ids_list[1],
                    "value": values["eligible investments"],
                    "color": colors[1],
                },
                {"key": span_ids_list[2], "value": values["fmv"], "color": colors[2]},
            ],
        }

    if col_name == "Eligible Investments":
        values = {
            "eligible_investments": df_PL_BB_Output["Eligible Investments"].iloc[
                row_idx
            ],
            "portfolio_eligible_amount": df_PL_BB_Build[
                "Portfolio Eligible Amount"
            ].iloc[row_idx],
        }

        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)

        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>Eligible Investments</span> = <button id='{ids_list[1]}'>'PL BB Build'!Portfolio Eligible Amount</button>",
            "formula_variable_data": [
                {
                    "key": ids_list[0],
                    "value": "Eligible Investments",
                    "color": colors[0],
                },
                {
                    "key": ids_list[1],
                    "value": "'PL BB Build'!Portfolio Eligible Amount",
                    "color": colors[1],
                },
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['eligible_investments']}</span> = <span id='{span_ids_list[1]}'>{values['portfolio_eligible_amount']}</span>",
            "formula_values_data": [
                {
                    "key": span_ids_list[0],
                    "value": values["eligible_investments"],
                    "color": colors[0],
                },
                {
                    "key": span_ids_list[1],
                    "value": values["portfolio_eligible_amount"],
                    "color": colors[1],
                },
            ],
        }

    if col_name == "Concentration Limit Adjustments":
        values = {
            "adjustments": df_PL_BB_Output["Adjustments"].iloc[row_idx],
            "concentration_adjustment": df_PL_BB_Build["Concentration Adjustment"].iloc[
                row_idx
            ],
        }

        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)

        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>Concentration Limit Adjustments</span> = <button id='{ids_list[1]}'>'PL BB Build'!Concentration Adjustment</button>",
            "formula_variable_data": [
                {
                    "key": ids_list[0],
                    "value": "Concentration Limit Adjustments",
                    "color": colors[0],
                },
                [
                    {
                        "key": ids_list[1],
                        "value": "PL BB Build'!Concentration Adjustment",
                        "color": colors[1],
                    }
                ],
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['adjustments']}</span> = <span id='{span_ids_list[1]}'>{values['concentration_adjustment']}</span>",
            "formula_values_data": [
                {
                    "key": span_ids_list[0],
                    "value": values["adjustments"],
                    "color": colors[0],
                },
                {
                    "key": span_ids_list[1],
                    "value": values["concentration_adjustment"],
                    "color": colors[1],
                },
            ],
        }

    if col_name == "Adj. Eligible Investments":
        values = {
            "adj_eligible_investments": df_PL_BB_Output[
                "Adj. Eligible Investments"
            ].iloc[row_idx],
            "eligible_investments": df_PL_BB_Output["Eligible Investments"].iloc[
                row_idx
            ],
            "adjustments": df_PL_BB_Output["Adjustments"].iloc[row_idx],
        }

        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)

        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>Adj. Eligible Investments</span> = <button id='{ids_list[1]}'>Eligible Investments</button> + <button id='{ids_list[2]}'>Adjustments</button>",
            "formula_variable_data": [
                {
                    "key": ids_list[0],
                    "value": "Adj. Eligible Investments",
                    "color": colors[0],
                },
                {
                    "key": ids_list[1],
                    "value": "Eligible Investments",
                    "color": colors[1],
                },
                {"key": ids_list[2], "value": "Adjustments", "color": colors[2]},
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['adj_eligible_investments']}</span> = <span id='{span_ids_list[1]}'>{values['eligible_investments']}</span> + <span id='{span_ids_list[2]}'>{values['adjustments']}</span>",
            "formula_values_data": [
                {
                    "key": span_ids_list[0],
                    "value": values["adj_eligible_investments"],
                    "color": colors[0],
                },
                {
                    "key": span_ids_list[1],
                    "value": values["eligible_investments"],
                    "color": colors[1],
                },
                {
                    "key": span_ids_list[2],
                    "value": values["adjustments"],
                    "color": colors[2],
                },
            ],
        }

    if col_name == "Adj. Advance Rate":
        values = {
            "pl_bb_build!first_lien_adj._advance_rate": df_PL_BB_Build[
                "First Lien Adj. Advance Rate"
            ].iloc[row_idx],
            "adj._advance_rate": df_PL_BB_Output["Adj. Advance Rate"].iloc[row_idx],
        }

        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)

        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>Adj. Advance Rate</span> = <button id='{ids_list[1]}'>'PL BB Build'!First Lien Adj. Advance Rate</button>",
            "formula_variable_data": [
                {"key": ids_list[0], "value": "Adj. Advance Rate", "color": colors[0]},
                {
                    "key": ids_list[1],
                    "value": "'PL BB Build'!First Lien Adj. Advance Rate",
                    "color": colors[1],
                },
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['adj._advance_rate']}</span> = <span id='{span_ids_list[1]}'>{values['pl_bb_build!first_lien_adj._advance_rate']}</span>",
            "formula_values_data": [
                {
                    "key": span_ids_list[0],
                    "value": values["adj._advance_rate"],
                    "color": colors[0],
                },
                {
                    "key": span_ids_list[1],
                    "value": values["pl_bb_build!first_lien_adj._advance_rate"],
                    "color": colors[1],
                },
            ],
        }

    if col_name == "'PL BB Build'!First Lien Adj. Advance Rate":
        # =IF(AE7="Warehouse First Lien",(CY7*CZ7)+((1-CY7)*CR7),IF(CT7<>0,((CT7*CU7)+((1-CT7)*CR7)),CR7))
        values = {
            "pl_bb_build!first_lien_adj._advance_rate": float(
                df_PL_BB_Build["First Lien Adj. Advance Rate"].iloc[row_idx]
            ),
            "pl_bb_build!classifications_classification_for_bb": str(
                df_PL_BB_Build["Classifications Classification for BB"].iloc[row_idx]
            ),
            "pl_bb_build!warehouse_second_lien_share": float(
                df_PL_BB_Build["Warehouse Second Lien Share"].iloc[row_idx]
            ),
            "pl_bb_build!warehouse_second_lien_rate": float(
                df_PL_BB_Build["Warehouse Second Lien Rate"].iloc[row_idx]
            ),
            "pl_bb_build!revolver_adj._advance_rate": float(
                df_PL_BB_Build["Revolver Adj. Advance Rate"].iloc[row_idx]
            ),
            "pl_bb_build!first_lien_second_lien_share": float(
                df_PL_BB_Build["First Lien Second Lien Share"].iloc[row_idx]
            ),
            "pl_bb_build!first_lien_second_lien_rate": float(
                df_PL_BB_Build["First Lien Second Lien Rate"].iloc[row_idx]
            ),
        }

        # Format values with comma if necessary
        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)

        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": (
                f"<span id='{ids_list[0]}'>'PL BB Build'!First Lien Adj. Advance Rate</span> = "
                f"IF(<button id='{ids_list[1]}'>'PL BB Build'!Classifications Classification for BB</button> = Warehouse First Lien, "
                f"(<button id='{ids_list[2]}'>'PL BB Build'!Warehouse Second Lien Share</button> * "
                f"<button id='{ids_list[3]}'>'PL BB Build'!Warehouse Second Lien Rate</button>) + "
                f"((1- <button id='{ids_list[2]}'>'PL BB Build'!Warehouse Second Lien Share</button>) * "
                f"<button id='{ids_list[4]}'>'PL BB Build'!Revolver Adj. Advance Rate</button>), "
                f"IF(<button id='{ids_list[5]}'>'PL BB Build'!First Lien Second Lien Share</button> <> 0, "
                f"((<button id='{ids_list[5]}'>'PL BB Build'!First Lien Second Lien Share</button> * "
                f"<button id='{ids_list[6]}'>'PL BB Build'!First Lien Second Lien Rate</button>) + "
                f"((1 - <button id='{ids_list[5]}'>'PL BB Build'!First Lien Second Lien Share</button>) * "
                f"<button id='{ids_list[4]}'>'PL BB Build'!Revolver Adj. Advance Rate</button>)), "
                f"<button id='{ids_list[4]}'>'PL BB Build'!Revolver Adj. Advance Rate</button>))"
            ),
            "formula_variable_data": [
                {
                    "key": ids_list[0],
                    "value": "'PL BB Build'!First Lien Adj. Advance Rate",
                    "color": colors[0],
                },
                {
                    "key": ids_list[1],
                    "value": "'PL BB Build'!Classifications Classification for BB",
                    "color": colors[1],
                },
                {
                    "key": ids_list[2],
                    "value": "'PL BB Build'!Warehouse Second Lien Share",
                    "color": colors[2],
                },
                {
                    "key": ids_list[3],
                    "value": "'PL BB Build'!Warehouse Second Lien Rate",
                    "color": colors[3],
                },
                {
                    "key": ids_list[4],
                    "value": "'PL BB Build'!Revolver Adj. Advance Rate",
                    "color": colors[4],
                },
                {
                    "key": ids_list[5],
                    "value": "'PL BB Build'!First Lien Second Lien Share",
                    "color": colors[5],
                },
                {
                    "key": ids_list[6],
                    "value": "'PL BB Build'!First Lien Second Lien Rate",
                    "color": colors[6],
                },
            ],
            "formula_values_string": (
                f"<span id='{span_ids_list[0]}'>{values['pl_bb_build!first_lien_adj._advance_rate']}</span> = "
                f"IF(<span id='{span_ids_list[1]}'>{values['pl_bb_build!classifications_classification_for_bb']}</span> = Warehouse First Lien, "
                f"(<span id='{span_ids_list[2]}'>{values['pl_bb_build!warehouse_second_lien_share']}</span> * "
                f"<span id='{span_ids_list[3]}'>{values['pl_bb_build!warehouse_second_lien_rate']}</span>) + "
                f"((1 - <span id='{span_ids_list[2]}'>{values['pl_bb_build!warehouse_second_lien_share']}</span>) * "
                f"<span id='{span_ids_list[4]}'>{values['pl_bb_build!revolver_adj._advance_rate']}</span>), "
                f"IF(<span id='{span_ids_list[5]}'>{values['pl_bb_build!first_lien_second_lien_share']}</span> <> 0, "
                f"((<span id='{span_ids_list[5]}'>{values['pl_bb_build!first_lien_second_lien_share']}</span> * "
                f"<span id='{span_ids_list[6]}'>{values['pl_bb_build!first_lien_second_lien_rate']}</span>) + "
                f"((1 - <span id='{span_ids_list[5]}'>{values['pl_bb_build!first_lien_second_lien_share']}</span>) * "
                f"<span id='{span_ids_list[4]}'>{values['pl_bb_build!revolver_adj._advance_rate']}</span>)), "
                f"<span id='{span_ids_list[4]}'>{values['pl_bb_build!revolver_adj._advance_rate']}</span>))"
            ),
            "formula_values_data": [
                {
                    "key": span_ids_list[0],
                    "value": values["pl_bb_build!first_lien_adj._advance_rate"],
                    "color": colors[0],
                },
                {
                    "key": span_ids_list[1],
                    "value": values[
                        "pl_bb_build!classifications_classification_for_bb"
                    ],
                    "color": colors[1],
                },
                {
                    "key": span_ids_list[2],
                    "value": values["pl_bb_build!warehouse_second_lien_share"],
                    "color": colors[2],
                },
                {
                    "key": span_ids_list[3],
                    "value": values["pl_bb_build!warehouse_second_lien_rate"],
                    "color": colors[3],
                },
                {
                    "key": span_ids_list[4],
                    "value": values["pl_bb_build!revolver_adj._advance_rate"],
                    "color": colors[4],
                },
                {
                    "key": span_ids_list[5],
                    "value": values["pl_bb_build!first_lien_second_lien_share"],
                    "color": colors[5],
                },
                {
                    "key": span_ids_list[6],
                    "value": values["pl_bb_build!first_lien_second_lien_rate"],
                    "color": colors[6],
                },
            ],
        }

    # if col_name == 'Adj. Advance Rate':
    #     values = {
    #         "adj_eligible_investments" : df_PL_BB_Output['Adj. Eligible Investments'].iloc[row_idx],
    #         "eligible_investments" : df_PL_BB_Output['Eligible Investments'].iloc[row_idx],
    #         "adjustments": df_PL_BB_Output['Adjustments'].iloc[row_idx],

    #     }

    #     values = format_values_with_comma(values)
    #     ids_list = get_ids_list(values, row_name)
    #     span_ids_list = get_span_ids_list(values, row_name)

    #     drill_down_dict = {
    #         "col_name" : col_name,
    #         "row_name" : row_name,

    #         "formula_variable_string" : f"<button id='{ids_list[0]}'>Adj. Advance Rate</button> = <button id='{ids_list[1]}'>Eligible Investments</button> + <button id='{ids_list[2]}'>Adjustments</button>",

    #         "formula_variable_data": [{"key": ids_list[0], "value": 'Adj. Advance Rate', "color": colors[0]}, {"key": ids_list[1], "value": 'Eligible Investments', "color": colors[1]}, {"key": ids_list[2], "value": 'Adjustments', "color": colors[2]}],

    #         "formula_values_string" : f"<span  id='{span_ids_list[0]}'>{values['adj_eligible_investments']}</span> = <span id='{span_ids_list[1]}'>{values['eligible_investments']}</span> + <span id='{span_ids_list[2]}'>{values['adjustments']}</span>",

    #         "formula_values_data": [{"key": span_ids_list[0], "value": values['adj_eligible_investments'], "color": colors[0]}, {"key": span_ids_list[1], "value": values['eligible_investments'], "color": colors[1]}, {"key": span_ids_list[2], "value": values['adjustments'], "color": colors[2]}]

    #     }

    if col_name == "Contribution":
        values = {
            "contribution": df_PL_BB_Output["Contribution"].iloc[row_idx],
            "adj_eligible_investments": df_PL_BB_Output[
                "Adj. Eligible Investments"
            ].iloc[row_idx],
            "adj_advance_rate": df_PL_BB_Output["Adj. Advance Rate"].iloc[row_idx],
        }

        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)
        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>Contribution</span> = IFERROR(<button id='{ids_list[1]}'>Adj. Eligible Investments</button>*<button id='{ids_list[2]}'>Adj. Advance Rate</button>,0)",
            "formula_variable_data": [
                {"key": ids_list[0], "value": "Contribution", "color": colors[0]},
                {
                    "key": ids_list[1],
                    "value": "Adj. Eligible Investments",
                    "color": colors[1],
                },
                {"key": ids_list[2], "value": "Adj. Advance Rate", "color": colors[2]},
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['contribution']}</span> = IFERROR(<span id='{span_ids_list[1]}'>{values['adj_eligible_investments']}</span>*<span id='{span_ids_list[2]}'>{values['adj_advance_rate']}</span>,0)",
            "formula_values_data": [
                {
                    "key": span_ids_list[0],
                    "value": values["contribution"],
                    "color": colors[0],
                },
                {
                    "key": span_ids_list[1],
                    "value": values["adj_eligible_investments"],
                    "color": colors[1],
                },
                {
                    "key": span_ids_list[2],
                    "value": values["adj_advance_rate"],
                    "color": colors[2],
                },
            ],
        }

    if col_name == "Adjustments":
        # ='PL BB Build'!DK7+'PL BB Build'!DM7+'PL BB Build'!DN7

        values = {
            "adjustments": df_PL_BB_Output["Adjustments"].iloc[row_idx],
            "borrowing_base_onw_Adjustment": df_PL_BB_Build[
                "Borrowing Base ONW Adjustment"
            ].iloc[row_idx],
            "borrowing_base_other_adjustment": df_PL_BB_Build[
                "Borrowing Base Other Adjustment"
            ].iloc[row_idx],
            "borrowing_base_industry_concentration": df_PL_BB_Build[
                "Borrowing Base Industry Concentration"
            ].iloc[row_idx],
        }

        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)
        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>Adjustments</span> = <button id='{ids_list[1]}'>'PL BB Build'!Borrowing Base ONW Adjustment</button> + <button id='{ids_list[2]}'>'PL BB Build'!Borrowing Base Other Adjustment</button> + <button id='{ids_list[3]}'>'PL BB Build'!Borrowing Base Industry Concentration</button>",
            "formula_variable_data": [
                {"key": ids_list[0], "value": "Adjustments", "color": colors[0]},
                {
                    "key": ids_list[1],
                    "value": "'PL BB Build'!Borrowing Base ONW Adjustment",
                    "color": colors[1],
                },
                {
                    "key": ids_list[2],
                    "value": "'PL BB Build'!Borrowing Base Other Adjustment",
                    "color": colors[2],
                },
                {
                    "key": ids_list[3],
                    "value": "'PL BB Build'!Borrowing Base Industry Concentration",
                    "color": colors[3],
                },
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['adjustments']}</span> = <span id='{span_ids_list[1]}'>{values['borrowing_base_onw_Adjustment']}</span> + <span id='{span_ids_list[2]}'>{values['borrowing_base_onw_Adjustment']}</span> + <span id='{span_ids_list[3]}'>{values['borrowing_base_onw_Adjustment']}</span>",
            "formula_values_data": [
                {
                    "key": ids_list[0],
                    "value": values["adjustments"],
                    "color": colors[0],
                },
                {
                    "key": span_ids_list[1],
                    "value": values["borrowing_base_onw_Adjustment"],
                    "color": colors[1],
                },
                {
                    "key": span_ids_list[2],
                    "value": values["borrowing_base_onw_Adjustment"],
                    "color": colors[2],
                },
                {
                    "key": span_ids_list[3],
                    "value": values["borrowing_base_onw_Adjustment"],
                    "color": colors[3],
                },
            ],
        }

    # if col_name == "'PL BB Build'!Borrowing Base ONW Adjustment":
    # # DK of PL BB Build
    # # =DL7-CW7

    #     values = {
    #         "pl_bb_build!Borrowing Base ONW Adjustment": df_PL_BB_Build['Borrowing Base ONW Adjustment'].iloc[row_idx],
    #         "pl_bb_build!Borrowing Base Adj. Contribution": df_PL_BB_Build['Borrowing Base Adj. Contribution'].iloc[row_idx],
    #         "pl_bb_build!First Lien Contribution": df_PL_BB_Build['First Lien Contribution'].iloc[row_idx],
    #     }

    #     values = format_values_with_comma(values)
    #     ids_list = get_ids_list(values, row_name)
    #     span_ids_list = get_span_ids_list(values, row_name)

    #     drill_down_dict = {
    #         "col_name": col_name,
    #         "row_name": row_name,

    #         "formula_variable_string": f"<span id='{ids_list[0]}'>'PL BB Build'!Borrowing Base ONW Adjustment</span> = <button id='{ids_list[1]}'>'PL BB Build'!Borrowing Base Adj. Contribution</button> + <button id='{ids_list[2]}'>PL BB Build'!First Lien Contribution</button>",

    #         "formula_variable_data": [
    #             {"key": ids_list[0], "value": "'PL BB Build'!Borrowing Base ONW Adjustment", "color": colors[0]},
    #             {"key": ids_list[1], "value": "'PL BB Build'!Borrowing Base Adj. Contribution", "color": colors[1]},
    #             {"key": ids_list[2], "value": "PL BB Build'!First Lien Contribution", "color": colors[2]}
    #         ],

    #         "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['pl_bb_build!Borrowing Base ONW Adjustment']}</span> = <span id='{span_ids_list[1]}'>{values['pl_bb_build!Borrowing Base Adj. Contribution']}</span> + <span id='{span_ids_list[2]}'>{values['pl_bb_build!First Lien Contribution']}</span>",

    #         "formula_values_data": [
    #             {"key": span_ids_list[0], "value": values["pl_bb_build!Borrowing Base ONW Adjustment"], "color": colors[0]},
    #             {"key": span_ids_list[1], "value": values['pl_bb_build!Borrowing Base Adj. Contribution'], "color": colors[1]},
    #             {"key": span_ids_list[2], "value": values['pl_bb_build!First Lien Contribution'], "color": colors[2]}
    #         ]
    #     }

    if col_name == "'PL BB Build'!Borrowing Base Adj. Contribution":
        # DK of PL BB Build
        # =IFERROR(((CJ7-DD7-DE7)*CV7)+DI7,0)

        values = {
            "pl_bb_build!Borrowing Base Adj. Contribution": df_PL_BB_Build[
                "Borrowing Base Adj. Contribution"
            ].iloc[row_idx],
            "pl_bb_build!Concentration Adj. Elig. Amount": df_PL_BB_Build[
                "Concentration Adj. Elig. Amount"
            ].iloc[row_idx],
            "pl_bb_build!ONW Adjustments > 7.5% ONC Share": df_PL_BB_Build[
                "ONW Adjustments > 7.5% ONC Share"
            ].iloc[row_idx],
            "pl_bb_build!ONW Adjustments > 10% ONC Share": df_PL_BB_Build[
                "ONW Adjustments > 10% ONC Share"
            ].iloc[row_idx],
            "pl_bb_build!First Lien Adj. Advance Rate": df_PL_BB_Build[
                "First Lien Adj. Advance Rate"
            ].iloc[row_idx],
            "pl_bb_build!ONW Adjustments Concentration BB Adj. Contribution": df_PL_BB_Build[
                "ONW Adjustments Concentration BB Adj. Contribution"
            ].iloc[
                row_idx
            ],
        }

        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)

        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>'PL BB Build'!Borrowing Base Adj. Contribution</span> = IFERROR(((<button id='{ids_list[1]}'>'PL BB Build'!Concentration Adj. Elig. Amount</button> - <button id='{ids_list[2]}'>ONW Adjustments > 7.5% ONC Share</button> - <button id='{ids_list[3]}'>ONW Adjustments > 10% ONC Share</button>) * <button id='{ids_list[4]}'>First Lien Adj. Advance Rate</button>) + <button id='{ids_list[5]}'>ONW Adjustments Concentration BB Adj. Contribution</button>, 0)",
            "formula_variable_data": [
                {
                    "key": ids_list[0],
                    "value": "'PL BB Build'!Borrowing Base Adj. Contribution",
                    "color": colors[0],
                },
                {
                    "key": ids_list[1],
                    "value": "'PL BB Build'!Concentration Adj. Elig. Amount",
                    "color": colors[1],
                },
                {
                    "key": ids_list[2],
                    "value": "'PL BB Build'!ONW Adjustments > 7.5% ONC Share",
                    "color": colors[2],
                },
                {
                    "key": ids_list[3],
                    "value": "'PL BB Build'!ONW Adjustments > 10% ONC Share",
                    "color": colors[3],
                },
                {
                    "key": ids_list[4],
                    "value": "'PL BB Build'!First Lien Adj. Advance Rate",
                    "color": colors[4],
                },
                {
                    "key": ids_list[5],
                    "value": "'PL BB Build'!ONW Adjustments Concentration BB Adj. Contribution",
                    "color": colors[5],
                },
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['pl_bb_build!Borrowing Base Adj. Contribution']}</span> = IFERROR(((<span id='{span_ids_list[1]}'>{values['pl_bb_build!Concentration Adj. Elig. Amount']}</span> - <span id='{span_ids_list[2]}'>{values['pl_bb_build!ONW Adjustments > 7.5% ONC Share']}</span> - <span id='{span_ids_list[3]}'>{values['pl_bb_build!ONW Adjustments > 10% ONC Share']}</span>) * <span id='{span_ids_list[4]}'>{values['pl_bb_build!First Lien Adj. Advance Rate']}</span>) + <span id='{span_ids_list[5]}'>{values['pl_bb_build!ONW Adjustments Concentration BB Adj. Contribution']}</span>, 0)",
            "formula_values_data": [
                {
                    "key": span_ids_list[0],
                    "value": values["pl_bb_build!Borrowing Base Adj. Contribution"],
                    "color": colors[0],
                },
                {
                    "key": span_ids_list[1],
                    "value": values["pl_bb_build!Concentration Adj. Elig. Amount"],
                    "color": colors[1],
                },
                {
                    "key": span_ids_list[2],
                    "value": values["pl_bb_build!ONW Adjustments > 7.5% ONC Share"],
                    "color": colors[2],
                },
                {
                    "key": span_ids_list[3],
                    "value": values["pl_bb_build!ONW Adjustments > 10% ONC Share"],
                    "color": colors[3],
                },
                {
                    "key": span_ids_list[4],
                    "value": values["pl_bb_build!First Lien Adj. Advance Rate"],
                    "color": colors[4],
                },
                {
                    "key": span_ids_list[5],
                    "value": values[
                        "pl_bb_build!ONW Adjustments Concentration BB Adj. Contribution"
                    ],
                    "color": colors[5],
                },
            ],
        }

    if col_name == "'PL BB Build'!First Lien Contribution":
        # DK of PL BB Build
        # =IFERROR(CJ7*CV7,0)

        values = {
            "pl_bb_build!First Lien Contribution": df_PL_BB_Build[
                "First Lien Contribution"
            ].iloc[row_idx],
            "pl_bb_build!Concentration Adj. Elig. Amount": df_PL_BB_Build[
                "Concentration Adj. Elig. Amount"
            ].iloc[row_idx],
            "pl_bb_build!First Lien Adj. Advance Rate": df_PL_BB_Build[
                "First Lien Adj. Advance Rate"
            ].iloc[row_idx],
        }

        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)

        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>'PL BB Build'!First Lien Contribution</span> = IFERROR(<button id='{ids_list[1]}'>'PL BB Build'!Concentration Adj. Elig. Amount</button> * <button id='{ids_list[2]}'>First Lien Adj. Advance Rate</button>, 0)",
            "formula_variable_data": [
                {
                    "key": ids_list[0],
                    "value": "'PL BB Build'!First Lien Contribution",
                    "color": colors[0],
                },
                {
                    "key": ids_list[1],
                    "value": "'PL BB Build'!Concentration Adj. Elig. Amount",
                    "color": colors[1],
                },
                {
                    "key": ids_list[2],
                    "value": "'PL BB Build'!First Lien Adj. Advance Rate",
                    "color": colors[2],
                },
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['pl_bb_build!First Lien Contribution']}</span> = IFERROR(<span id='{span_ids_list[1]}'>{values['pl_bb_build!Concentration Adj. Elig. Amount']}</span> * <span id='{span_ids_list[2]}'>{values['pl_bb_build!First Lien Adj. Advance Rate']}</span>, 0)",
            "formula_values_data": [
                {
                    "key": span_ids_list[0],
                    "value": values["pl_bb_build!First Lien Contribution"],
                    "color": colors[0],
                },
                {
                    "key": span_ids_list[1],
                    "value": values["pl_bb_build!Concentration Adj. Elig. Amount"],
                    "color": colors[1],
                },
                {
                    "key": span_ids_list[2],
                    "value": values["pl_bb_build!First Lien Adj. Advance Rate"],
                    "color": colors[2],
                },
            ],
        }

    # if col_name == "'PL BB Build'!Borrowing Base Other Adjustment":
    # # DK of PL BB Build
    # # =IFERROR(CJ7*CV7,0)

    #     values = {
    #         "pl_bb_build!Borrowing Base Other Adjustment": df_PL_BB_Build['Borrowing Base Other Adjustment'].iloc[row_idx],
    #         "pl_bb_build!Borrowing Base Adj. Contribution": df_PL_BB_Build['Borrowing Base Adj. Contribution'].iloc[row_idx],
    #         "pl_bb_build!First Lien Contribution": df_PL_BB_Build['First Lien Contribution'].iloc[row_idx]
    #     }

    #     ids_list = get_ids_list(values, row_name)
    #     span_ids_list = get_span_ids_list(values, row_name)

    #     drill_down_dict = {
    #         "col_name": col_name,
    #         "row_name": row_name,

    #         "formula_variable_string": f"<button id={ids_list[0]}>'PL BB Build'!Borrowing Base Other Adjustment</button> = IFERROR(<button id={ids_list[1]}>'PL BB Build'!Borrowing Base Adj. Contribution</button> * <button id={ids_list[2]}>PL BB Build'!First Lien Contribution</button>, 0)",

    #         "formula_variable_data": [
    #             {"key": ids_list[0], "value": "'PL BB Build'!Borrowing Base Other Adjustment", "color": colors[0]},
    #             {"key": ids_list[1], "value": "'PL BB Build'!Borrowing Base Adj. Contribution", "color": colors[1]},
    #             {"key": ids_list[2], "value": "PL BB Build'!First Lien Contribution", "color": colors[2]}
    #         ],

    #         "formula_values_string": f"<span id={span_ids_list[0]}>{values['pl_bb_build!Borrowing Base Other Adjustment']}</span> = IFERROR(<span id={span_ids_list[1]}>{values['pl_bb_build!Borrowing Base Adj. Contribution']}</span> * <span id={span_ids_list[2]}>{values['pl_bb_build!First Lien Contribution']}</span>, 0)",

    #         "formula_values_data": [
    #             {"key": span_ids_list[0], "value": values["pl_bb_build!Borrowing Base Other Adjustment"], "color": colors[0]},
    #             {"key": span_ids_list[1], "value": values['pl_bb_build!Borrowing Base Adj. Contribution'], "color": colors[1]},
    #             {"key": span_ids_list[2], "value": values['pl_bb_build!First Lien Contribution'], "color": colors[2]}
    #         ]
    #     }

    # if col_name == "'PL BB Build'!Borrowing Base Industry Concentration":
    #     # DK of PL BB Build
    #     # =IFERROR(CJ7*CV7,0)

    #     values = {
    #                 "pl_bb_build!Borrowing Base Industry Concentration" : df_PL_BB_Build['Borrowing Base Industry Concentration'].iloc[row_idx]
    #     }

    #     ids_list = get_ids_list(values, row_name)
    #     span_ids_list = get_span_ids_list(values, row_name)

    #     drill_down_dict = {
    #         "col_name" : col_name,
    #         "row_name" : row_name,

    #         "formula_variable_string" : f"<button id={ids_list[0]}>'PL BB Build'!Borrowing Base ONW Adjustment</button> = <button id={ids_list[1]}>'PL BB Build'!Borrowing Base Adj. Contribution</button> +<button id={ids_list[2]}>PL BB Build'!First Lien Contribution</button>",

    #         "formula_variable_data": [{"key": ids_list[0], "value": "'PL BB Build'!Borrowing Base ONW Adjustment", "color": colors[0]}, {"key": ids_list[1], "value": "'PL BB Build'!Borrowing Base Adj. Contribution", "color": colors[1]}, {"key": ids_list[2], "value": "PL BB Build'!First Lien Contribution", "color": colors[2]}],

    #         "formula_values_string" : f"<span id={span_ids_list[0]}>{values['pl_bb_build!Borrowing Base ONW Adjustment']}</span> = <span id={span_ids_list[1]}>{values['pl_bb_build!Borrowing Base Adj. Contribution']}</span> +<span id={span_ids_list[2]}>{values['PL BB Build!First Lien Contribution']}</span>, <span id={span_ids_list[3]}",

    #         "formula_values_data": [
    #             {"key": span_ids_list[0], "value": values["pl_bb_build!Borrowing Base ONW Adjustment"], "color": colors[0]},
    #             {"key": span_ids_list[1], "value": values['pl_bb_build!Borrowing Base Adj. Contribution'], "color": colors[1]},
    #             {"key": span_ids_list[2], "value": values['pl_bb_build!First Lien Contribution'], "color": colors[2]}
    #         ]
    #     }

    if col_name == "Borrowing Base":
        # =SUM(Q6:R6)

        values = {
            "borrowing_base": df_PL_BB_Output["Borrowing Base"].iloc[row_idx],
            "contribution": df_PL_BB_Output["Contribution"].iloc[row_idx],
            "adjustments": df_PL_BB_Output["Adjustments"].iloc[row_idx],
        }

        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)
        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>Borrowing Base</span> = <button id='{ids_list[1]}'>Contribution</button> + <button id='{ids_list[2]}'>Adjustments</button>",
            "formula_variable_data": [
                {"key": ids_list[0], "value": "Borrowing Base", "color": colors[0]},
                {"key": ids_list[1], "value": "Contribution", "color": colors[1]},
                {"key": ids_list[2], "value": "Adjustments", "color": colors[2]},
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['borrowing_base']}</span> = <span id='{span_ids_list[1]}'>{values['contribution']}</span> + <span id='{span_ids_list[2]}'>{values['adjustments']}</span>",
            "formula_values_data": [
                {
                    "key": span_ids_list[0],
                    "value": values["borrowing_base"],
                    "color": colors[0],
                },
                {
                    "key": span_ids_list[1],
                    "value": values["contribution"],
                    "color": colors[1],
                },
                {
                    "key": span_ids_list[2],
                    "value": values["adjustments"],
                    "color": colors[2],
                },
            ],
        }

    if col_name == "'PL BB Build'!Portfolio Eligible Amount":
        # BW of PL BB Build
        # =IF($BR7="Yes",MIN(R7,O7,N7),0)

        values = {
            "pl_bb_build!portfolio_eligible_amount": df_PL_BB_Build[
                "Portfolio Eligible Amount"
            ].iloc[row_idx],
            "pl_bb_build!eligible": df_PL_BB_Build["Final Eligible"].iloc[row_idx],
            "pl_bb_build!investment_fmv": df_PL_BB_Build["Investment FMV"].iloc[
                row_idx
            ],
            "pl_bb_build!cost": df_PL_BB_Build["Investment Cost"].iloc[row_idx],
            "pl_bb_build!par": df_PL_BB_Build["Investment Par"].iloc[row_idx],
        }

        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)

        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>'PL BB Build'!Portfolio Eligible Amount</span> = IF(<button id='{ids_list[1]}'>'PL BB Build'!Final Eligible</button> ='Yes',MIN(<button id='{ids_list[2]}'>'PL BB Build'!Investment FMV</button>, <span id='{ids_list[3]}'>'PL BB Build'!Cost</span>, <span id='{ids_list[4]}'>'PL BB Build'!Par</span>),0)",
            "formula_variable_data": [
                {
                    "key": ids_list[0],
                    "value": "'PL BB Build'!Portfolio Eligible Amount",
                    "color": colors[0],
                },
                {
                    "key": ids_list[1],
                    "value": "'PL BB Build'!Final Eligible",
                    "color": colors[1],
                },
                {
                    "key": ids_list[2],
                    "value": "'PL BB Build'!Investment FMV",
                    "color": colors[2],
                },
                {"key": ids_list[3], "value": "'PL BB Build'!Cost", "color": colors[3]},
                {"key": ids_list[4], "value": "'PL BB Build'!Par", "color": colors[4]},
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['pl_bb_build!portfolio_eligible_amount']}</span> = IF(<span id='{span_ids_list[1]}'>{values['pl_bb_build!eligible']}</span> = 'Yes', MIN(<span id='{span_ids_list[2]}'>{values['pl_bb_build!investment_fmv']}</span>, <span id='{span_ids_list[3]}'>{values['pl_bb_build!cost']}</span>, <span id='{span_ids_list[4]}'>{values['pl_bb_build!par']})</span>, 0)",
            "formula_values_data": [
                {
                    "key": span_ids_list[0],
                    "value": values["pl_bb_build!portfolio_eligible_amount"],
                    "color": colors[0],
                },
                {
                    "key": span_ids_list[1],
                    "value": values["pl_bb_build!eligible"],
                    "color": colors[1],
                },
                {
                    "key": span_ids_list[2],
                    "value": values["pl_bb_build!investment_fmv"],
                    "color": colors[2],
                },
                {
                    "key": span_ids_list[3],
                    "value": values["pl_bb_build!cost"],
                    "color": colors[3],
                },
                {
                    "key": span_ids_list[4],
                    "value": values["pl_bb_build!par"],
                    "color": colors[4],
                },
            ],
        }

    if col_name == "'PL BB Build'!Final Eligible":
        # =IF(OR(AS7="No",BK7="No",BP7="No"),"No","Yes")

        values = {
            "pl_bb_build!final_eligible": df_PL_BB_Build["Final Eligible"].iloc[
                row_idx
            ],
            "pl_bb_build!classification_eligible": df_PL_BB_Build[
                "Classification Eligible"
            ].iloc[row_idx],
            "pl_bb_build!test_1_pass": df_PL_BB_Build["Test 1 Pass"].iloc[row_idx],
            "pl_bb_build!final_eligibility_override": "No"
            if df_PL_BB_Build["Final Eligibility Override"].iloc[row_idx] == 0.00
            else "Yes",
        }

        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)

        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>'PL BB Build'!Final_Eligible</span> = IF(OR(<span id='{ids_list[1]}'>'PL BB Build'!Classification Eligible</span> = No, <span id='{ids_list[2]}'>'PL BB Build'!Test 1 Pass</span> = No, <span id='{ids_list[3]}'>'PL BB Build'!Final Eligibility Override</span> = No), No, Yes)",
            "formula_variable_data": [
                {
                    "key": ids_list[0],
                    "value": "'PL BB Build'!Final_Eligible",
                    "color": colors[0],
                },
                {
                    "key": ids_list[1],
                    "value": "'PL BB Build'!Classification Eligible",
                    "color": colors[1],
                },
                {
                    "key": ids_list[2],
                    "value": "'PL BB Build'!Test 1 Pass",
                    "color": colors[2],
                },
                {
                    "key": ids_list[3],
                    "value": "'PL BB Build'!Final Eligibility Override",
                    "color": colors[3],
                },
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['pl_bb_build!final_eligible']}</span> = IF(OR(<span id='{span_ids_list[1]}'>{values['pl_bb_build!classification_eligible']}</span> == No, <span id='{span_ids_list[2]}'>{values['pl_bb_build!test_1_pass']}</span> == No, <span id='{span_ids_list[3]}'>{values['pl_bb_build!final_eligibility_override']}</span> == No), No, Yes)",
            "formula_values_data": [
                {
                    "key": span_ids_list[0],
                    "value": values["pl_bb_build!final_eligible"],
                    "color": colors[0],
                },
                {
                    "key": span_ids_list[1],
                    "value": values["pl_bb_build!classification_eligible"],
                    "color": colors[1],
                },
                {
                    "key": span_ids_list[2],
                    "value": values["pl_bb_build!test_1_pass"],
                    "color": colors[2],
                },
                {
                    "key": span_ids_list[3],
                    "value": values["pl_bb_build!final_eligibility_override"],
                    "color": colors[3],
                },
            ],
        }

    return drill_down_dict
