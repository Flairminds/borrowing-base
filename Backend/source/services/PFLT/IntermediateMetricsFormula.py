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

def formula_info(loan_list_df, row_name, col_name):
    colors = [
        "#d91421",
        "#14d9ab",
        "#51db2e",
        "#f57842",
        "#144fd9",
        "#d914be",
        "#476b6b",
    ]

    row_idx = loan_list_df[loan_list_df["Security Name"] == row_name].index[0]

    if col_name == "Obligor Name":
        # commit 2
        values = {
            "obligor_name": loan_list_df["Obligor Name"].iloc[row_idx],
            'final_obligor_name': loan_list_df["Obligor Name"].iloc[row_idx]
        }

        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)

        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>Obligor Name</span> = <span id='{ids_list[1]}'>'Loan List'!Obligor Name</span>",
            "formula_variable_data": [
                {
                    "key": ids_list[0], 
                    "value": "Obligor Name", 
                    "color": colors[0]
                },
                {
                    "key": ids_list[1],
                    "value": "'Loan List'!Obligor Name",
                    "color": colors[1],
                },
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['obligor_name']}</span> = <span id='{span_ids_list[1]}'>{values['final_obligor_name']}</span>",
            "formula_values_data": [
                {
                    "key": span_ids_list[0],
                    "value": values['obligor_name'],
                    "color": colors[0],
                },
                {
                    "key": span_ids_list[1],
                    "value": values['final_obligor_name'],
                    "color": colors[1],
                },
            ],
        }

    if col_name == "Company":
        # commit 2
        values = {
            "security_name": loan_list_df["Security Name"].iloc[row_idx],
            'final_security_name': loan_list_df["Security Name"].iloc[row_idx]
        }

        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)

        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>Company</span> = <span id='{ids_list[1]}'>'Loan List'!Security Name</span>",
            "formula_variable_data": [
                {
                    "key": ids_list[0], 
                    "value": "Security Name", 
                    "color": colors[0]
                },
                {
                    "key": ids_list[1],
                    "value": "'Loan List'!Security Name",
                    "color": colors[1],
                },
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['security_name']}</span> = <span id='{span_ids_list[1]}'>{values['final_security_name']}</span>",
            "formula_values_data": [
                {
                    "key": span_ids_list[0],
                    "value": values['security_name'],
                    "color": colors[0],
                },
                {
                    "key": span_ids_list[1],
                    "value": values['final_security_name'],
                    "color": colors[1],
                },
            ],
        }

    if col_name == "Total Commitment (Issue Currency)":
        # commit 2
        values = {
            "total_commitment_issue_currency": loan_list_df["Total Commitment (Issue Currency)"].iloc[row_idx],
            'final_total_commitment_issue_currency': loan_list_df["Total Commitment (Issue Currency)"].iloc[row_idx]
        }

        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)

        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>Total Commitment (Issue Currency)</span> = <span id='{ids_list[1]}'>'Loan List'!Total Commitment (Issue Currency)</span>",
            "formula_variable_data": [
                {
                    "key": ids_list[0], 
                    "value": "Total Commitment (Issue Currency)", 
                    "color": colors[0]
                },
                {
                    "key": ids_list[1],
                    "value": "'Loan List'!Total Commitment (Issue Currency)",
                    "color": colors[1],
                },
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['total_commitment_issue_currency']}</span> = <span id='{span_ids_list[1]}'>{values['final_total_commitment_issue_currency']}</span>",
            "formula_values_data": [
                {
                    "key": span_ids_list[0],
                    "value": values['total_commitment_issue_currency'],
                    "color": colors[0],
                },
                {
                    "key": span_ids_list[1],
                    "value": values['final_total_commitment_issue_currency'],
                    "color": colors[1],
                },
            ],
        }

    if col_name == "Outstanding Principal Balance (Issue Currency)":
        # commit 2
        values = {
            "outstanding_principal_balance_issue_currency": loan_list_df["Outstanding Principal Balance (Issue Currency)"].iloc[row_idx],
            'final_outstanding_principal_balance_issue_currency': loan_list_df["Outstanding Principal Balance (Issue Currency)"].iloc[row_idx]
        }

        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)

        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>Outstanding Principal Balance (Issue Currency)</span> = <span id='{ids_list[1]}'>'Loan List'!Outstanding Principal Balance (Issue Currency)</span>",
            "formula_variable_data": [
                {
                    "key": ids_list[0], 
                    "value": "Outstanding Principal Balance (Issue Currency)", 
                    "color": colors[0]
                },
                {
                    "key": ids_list[1],
                    "value": "'Loan List'!Outstanding Principal Balance (Issue Currency)",
                    "color": colors[1],
                },
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['outstanding_principal_balance_issue_currency']}</span> = <span id='{span_ids_list[1]}'>{values['final_outstanding_principal_balance_issue_currency']}</span>",
            "formula_values_data": [
                {
                    "key": span_ids_list[0],
                    "value": values['outstanding_principal_balance_issue_currency'],
                    "color": colors[0],
                },
                {
                    "key": span_ids_list[1],
                    "value": values['final_outstanding_principal_balance_issue_currency'],
                    "color": colors[1],
                },
            ],
        }

    if col_name == "Lien Type":
        # commit 2
        values = {
            "lien_type": loan_list_df['Lien Type (First Lien / Split First Lien / Split Lien / Second Lien / Tier 1 Split Lien / Tier 2 Split Lien)'].iloc[row_idx],
            'final_lien_type': loan_list_df['Lien Type (First Lien / Split First Lien / Split Lien / Second Lien / Tier 1 Split Lien / Tier 2 Split Lien)'].iloc[row_idx]
        }

        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)

        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>Lien Type</span> = <span id='{ids_list[1]}'>'Loan List'!Lien Type</span>",
            "formula_variable_data": [
                {
                    "key": ids_list[0], 
                    "value": "Lien Type", 
                    "color": colors[0]
                },
                {
                    "key": ids_list[1],
                    "value": "'Loan List'!Lien Type",
                    "color": colors[1],
                },
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['lien_type']}</span> = <span id='{span_ids_list[1]}'>{values['final_lien_type']}</span>",
            "formula_values_data": [
                {
                    "key": span_ids_list[0],
                    "value": values['lien_type'],
                    "color": colors[0],
                },
                {
                    "key": span_ids_list[1],
                    "value": values['final_lien_type'],
                    "color": colors[1],
                },
            ],
        }

    if col_name == "Exchange Rate":
        # commit 2
        values = {
            "exchange_rate": loan_list_df["Exchange Rate"].iloc[row_idx],
            'final_exchange_rate': loan_list_df["Exchange Rate"].iloc[row_idx]
        }

        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)

        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>Exchange Rate</span> = <span id='{ids_list[1]}'>'Loan List'!Exchange Rate</span>",
            "formula_variable_data": [
                {
                    "key": ids_list[0], 
                    "value": "Exchange Rate", 
                    "color": colors[0]
                },
                {
                    "key": ids_list[1],
                    "value": "'Loan List'!Exchange Rate",
                    "color": colors[1],
                },
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['exchange_rate']}</span> = <span id='{span_ids_list[1]}'>{values['final_exchange_rate']}</span>",
            "formula_values_data": [
                {
                    "key": span_ids_list[0],
                    "value": values['exchange_rate'],
                    "color": colors[0],
                },
                {
                    "key": span_ids_list[1],
                    "value": values['final_exchange_rate'],
                    "color": colors[1],
                },
            ],
        }

    if col_name == "Total Commitment (USD)":
        # commit 2
        values = {
            "total_commitment_usd": loan_list_df["Total Commitment (USD)"].iloc[row_idx],
            'total_commitment_issue_currency': loan_list_df["Total Commitment (Issue Currency)"].iloc[row_idx],
            'exchange_rate': loan_list_df["Exchange Rate"].iloc[row_idx]
        }

        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)

        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>Total Commitment (USD)</span> = <button id={ids_list[1]}>Total Commitment (Issue Currency)<button> * <button id={ids_list[2]}>Exchange Rate<button>)",
            "formula_variable_data": [
                {
                    "key": ids_list[0], 
                    "value": "Total Commitment (USD)", 
                    "color": colors[0]
                },
                {
                    "key": ids_list[1],
                    "value": "Total Commitment (Issue Currency)",
                    "color": colors[1],
                },{
                    "key": ids_list[2],
                    "value": "Exchange Rate",
                    "color": colors[2],
                }
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['total_commitment_usd']}</span> = <span id={span_ids_list[1]}>{values['total_commitment_issue_currency']}<span> * <span id={span_ids_list[2]}>{values['exchange_rate']}<span>)",
            "formula_values_data": [
                {
                    "key": span_ids_list[0],
                    "value": values['total_commitment_usd'],
                    "color": colors[0],
                },
                {
                    "key": span_ids_list[1],
                    "value": values['total_commitment_issue_currency'],
                    "color": colors[1],
                },
                {
                    "key": span_ids_list[2],
                    "value": values['exchange_rate'],
                    "color": colors[2],
                }
            ],
        }
    
    if col_name == "Outstanding Principal Balance (USD)":
        values = {
            "outstanding_principal_balance_usd": loan_list_df["Outstanding Principal Balance (USD)"].iloc[row_idx],
            'outstanding_principal_balance_issue_currency': loan_list_df["Outstanding Principal Balance (Issue Currency)"].iloc[row_idx],
            'exchange_rate': loan_list_df["Exchange Rate"].iloc[row_idx]
        }

        values = format_values_with_comma(values)
        ids_list = get_ids_list(values, row_name)
        span_ids_list = get_span_ids_list(values, row_name)

        drill_down_dict = {
            "col_name": col_name,
            "row_name": row_name,
            "formula_variable_string": f"<span id='{ids_list[0]}'>Outstanding Principal Balance (USD)</span> = <button id={ids_list[1]}>Outstanding Principal Balance (Issue Currency)<button> * <button id={ids_list[2]}>Exchange Rate<button>)",
            "formula_variable_data": [
                {
                    "key": ids_list[0], 
                    "value": "Outstanding Principal Balance (USD)", 
                    "color": colors[0]
                },
                {
                    "key": ids_list[1],
                    "value": "Outstanding Principal Balance (Issue Currency)",
                    "color": colors[1],
                },{
                    "key": ids_list[2],
                    "value": "Exchange Rate",
                    "color": colors[2],
                }
            ],
            "formula_values_string": f"<span id='{span_ids_list[0]}'>{values['outstanding_principal_balance_usd']}</span> = <span id={span_ids_list[1]}>{values['outstanding_principal_balance_issue_currency']}<span> * <span id={span_ids_list[2]}>{values['exchange_rate']}<span>)",
            "formula_values_data": [
                {
                    "key": span_ids_list[0],
                    "value": values['outstanding_principal_balance_usd'],
                    "color": colors[0],
                },
                {
                    "key": span_ids_list[1],
                    "value": values['outstanding_principal_balance_issue_currency'],
                    "color": colors[1],
                },
                {
                    "key": span_ids_list[2],
                    "value": values['exchange_rate'],
                    "color": colors[2],
                }
            ],
        }
    return drill_down_dict
