import pandas as pd
from sqlalchemy import text



def rename_duplicate_columns(df):
    """Rename duplicate columns by appending incremental suffixes."""
    cols = pd.Series(df.columns)
    for dup in cols[cols.duplicated()].unique():
        new_names = [dup if i == 0 else f"{dup}_{i}" for i in range(sum(cols == dup))]
        cols[cols[cols == dup].index.values.tolist()] = new_names
    df.columns = cols
    return df

def base_data_mapping(cf, engine, bs = None):
    try:
        with engine.connect() as connection:
            base_data_map = pd.DataFrame(connection.execute(text('select * from "base_data_mapping"')).fetchall())
        data = []
        # new_dict = {}
        for i, r in base_data_map.iterrows():
            # if r['bd_column_name'] == 'Stretch Senior Loan (Y/N)':
            # if bs is not None and r['rd_column_name'] in bs:
            #     if isinstance((bs[r["rd_column_name"]]), pd.core.series.Series):
            #         data.append(bs[r["rd_column_name"]].astype("string"))
            #     else:
            #         data.append(bs[r["rd_column_name"]])
            if r["rd_column_name"] in cf and cf[r['rd_column_name']] is not None:
                # print("here", r['rd_column_name'], cf[r['rd_column_name']])
                if isinstance((cf[r["rd_column_name"]]), pd.core.series.Series):
                    data.append(cf[r["rd_column_name"]].astype("string"))
                else:
                    data.append(cf[r["rd_column_name"]])
            else:
                data.append(None)
        return data
    except Exception as e:
        print({
                    "error": str(e),
                    "error_type": str(type(e).__name__),
                    "error_file_details": f"error on line {e.__traceback__.tb_lineno} inside {__file__}",
                })

def soi_mapping(engine, master_comp_file_details, cash_file_details):
    try:
        with engine.connect() as connection:
            # soi_data = pd.DataFrame(connection.execute(text('select * from "SOI Mapping"')).fetchall())
            # master_comp = pd.DataFrame(connection.execute(text('select * from "Borrower Stats (Quarterly)" bs join "Securities Stats" ss on ss."Family Name" = bs."Company" join "PFLT Borrowing Base" pbb on pbb."Security" = ss."Security"')).fetchall())
            # master_comp = rename_duplicate_columns(master_comp)
            cash_file = pd.DataFrame(connection.execute(text('select * from "US Bank Holdings" usbh left join "Client Holdings" ch on ch."Issuer/Borrower Name" = usbh."Issuer/Borrower Name" and ch."Current Par Amount (Issue Currency) - Settled" = usbh."Current Par Amount (Issue Currency) - Settled" left join "SOI Mapping" sm on sm."Cashfile Security Name" = usbh."Security/Facility Name" left join "Securities Stats" ss on ss."Security" = sm."Master_Comp Security Name" left join "PFLT Borrowing Base" pbb on pbb."Security" = ss."Security" left join "Borrower Stats (Quarterly)" bsq on bsq."Company" = ss."Family Name" where usbh.source_file_id= :cash_file_id AND ch.source_file_id= :cash_file_id AND ss.source_file_id= :master_comp_file_id AND pbb.source_file_id= :master_comp_file_id AND bsq.source_file_id= :master_comp_file_id'), {'cash_file_id': cash_file_details.id, 'master_comp_file_id':master_comp_file_details.id}).fetchall())
            cash_file = rename_duplicate_columns(cash_file)
            base_data_map = pd.DataFrame(connection.execute(text('select * from "base_data_mapping"')).fetchall())
            # securities_stats = pd.DataFrame(connection.execute(text('select * from "Securities Stats"')).fetchall())
            # dataframe = pd.DataFrame(output)
        # d = {
        #     "Delayed Draw Term Loan": ['(DDTL)', 'DD T/L'],
        #     "Term Loan": ['(TL)', '(Term Loan)', 'T/L'],
        #     "Revolver": ['(Revolver)'],
        #     "Common Equity": ['(Common Equity)']
        # }
        new_dict = {}
        matched = False
        for i, cf in cash_file.iterrows():
            # type = None
            print(i)
            if (cf['Security/Facility Name'] is None):
                continue
            # for key in d:
            #     if key in cf['Security/Facility Name']:
            #         type = key
            #         break
            # if (type is None):
            #     continue
            # for j, sm in soi_data.iterrows():
            #     if (sm['Cashfile Security Name'] is None):
            #         continue
            #     if (sm['Cashfile Security Name'] == cf['Security/Facility Name']):
            #         for k, bs in master_comp.iterrows():
            #             res = None
            #             if (bs["Security"] is None):
            #                 continue
            #             if (bs['Security'] == sm['Master_Comp Security Name']):
            #                 res = base_data_mapping(cf, bs)
            #                 matched = True
            #             # else:
            #             #     c = None
            #             #     b = None
            #             #     for t in d[type]:
            #             #         if t in bs['Security']:
            #             #             temp1 = bs['Security'].split(t)
            #             #             c = temp1[0]
            #             #             break
            #             #     for t in d[type]:
            #             #         # print(t, sm['[G] Security Name'], k, j)
            #             #         if t in sm['[G] Security Name']:
            #             #             temp2 = sm['[G] Security Name'].split(t)
            #             #             b = temp2[0]
            #             #             break
            #             #     if (c is not None and b is not None and c == b):
            #             #         res = base_data_mapping(bs, cf)
            #             if res is not None:
            #                 print(res[1])
            #                 new_dict[i] = res
            #                 # df = pd.DataFrame([res])
            #                 # pd.concat([dfo, df])
            #                 break
            # if matched is False:
            res = base_data_mapping(cf, engine=engine)
            print(res[1])
            new_dict[i] = res
        df = pd.DataFrame.from_dict(new_dict, orient='index', columns = list(base_data_map['bd_column_name']))
        df = rename_duplicate_columns(df)
        df["company_id"] = master_comp_file_details.company_id
        df["report_date"] = master_comp_file_details.report_date
        # df.to_csv('file1.csv')
        df.to_sql("base_data", con=engine, if_exists='append', index=False, method='multi')
        

    except Exception as e:
        print(e)