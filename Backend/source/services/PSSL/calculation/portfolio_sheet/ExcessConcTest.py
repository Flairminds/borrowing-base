import numpy as np

class ExcessConcTest:
    def __init__(self, calculator_info):
        self.calculator_info = calculator_info

    def pre_excess_concentration_adjusted_borrowing_value(self):
        # =W11
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Pre-Excess Concentration Adjusted Borrowing Value"] = portfolio_df["Adjusted Borrowing Value"]
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    

    def obligor(self):
        # =SUMIF($G:$G,$G11,$ES:$ES)
        def obligor_helper(row):
            matching_rows = portfolio_df[portfolio_df['Borrower'] == row['Borrower']]
            return matching_rows['Pre-Excess Concentration Adjusted Borrowing Value'].sum()
        
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Obligor"] = portfolio_df.apply(obligor_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def remove_dupes(self):
        # =IF(MATCH($G11,$G:$G,0)=ROW(),$EU11,0)
        def remove_dupes_helper(row):
            first_index = portfolio_df[portfolio_df['Borrower'] == row['Borrower']].index[0]
            if row.name == first_index:
                return row['Obligor']
            else:
                return 0

        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Remove Dupes"] = portfolio_df.apply(remove_dupes_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def rank_2(self):
        # =IF(EV11>0,RANK(EV11,$EV$11:$EV$90)+COUNTIF($EV$11:$EV11,EV11)-1,0)
        def rank_2_helper(row):
            if row['Remove Dupes'] <= 0:
                return 0
            ev_val = row['Remove Dupes']
            rank = portfolio_df[portfolio_df['Remove Dupes'] > 0]['Remove Dupes'].rank(method='min', ascending=False)[row.name]
            count_dup = portfolio_df.loc[:row.name, 'Remove Dupes'].eq(ev_val).sum()
            return int(rank + count_dup - 1)

        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Rank 2"] = portfolio_df.apply(rank_2_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def rank(self):
        # =INDEX(EX$10:EX$90,MATCH(G11,G$10:G$90,0))
        def rank_helper(row):
            match_index = portfolio_df[portfolio_df['Borrower'] == row['Borrower']].index[0]
            return portfolio_df.loc[match_index, 'Rank 2']
    
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Rank"] = portfolio_df.apply(rank_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df


    def qualifies(self):
        # =IF(AND(OR(T11="Last Out",T11="Second Lien", CZ11<10000000),EW11<4),"yes","no")
        def qualifies_helper(row):
            if (row["Calculated Loan Type post AA Discretion"] == "Last Out" or row["Calculated Loan Type post AA Discretion"] == "Second Lien" or row["Permitted TTM EBITDA in Local Currency at relevant test period"] < 10000000) and row["Rank"] < 4:
                return "yes"
            else:
                return "no"

        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Qualifies?"] = portfolio_df.apply(qualifies_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def fllosllnitto_excess(self):
        # =IFERROR(IF(ET11="yes",(EU11-INDEX($EU$11:$EU$211-0.01,MATCH(4,$EW$11:$EW$90,0)))*(ES11/SUMIF($G:$G,G11,$ES:$ES)),0),0)

        def fllosllnitto_excess_helper(row):
            try:
                if str(row['Qualifies?']).lower() == "yes":
                    matched_idx = portfolio_df[portfolio_df['Rank'] == 4].index[0]
                    base_value = portfolio_df.loc[matched_idx, 'Obligor'] - 0.01
                    
                    group_sum = portfolio_df[portfolio_df['Borrower'] == row['Borrower']]['Pre-Excess Concentration Adjusted Borrowing Value'].sum()
                    
                    return (row['Obligor'] - base_value) * (row['Pre-Excess Concentration Adjusted Borrowing Value'] / group_sum)
                else:
                    return 0
            except Exception as e:
                return 0
            
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["First Lien Last Out, Second Lien Loan not in Top Three Obligors Excess"] = portfolio_df.apply(fllosllnitto_excess_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def fllosllnitto_revised_value(self):
        # =MAX(0,ES11-EY11)
        def fllosllnitto_revised_value_helper(row):
            return max(0, row['Pre-Excess Concentration Adjusted Borrowing Value'] - row['First Lien Last Out, Second Lien Loan not in Top Three Obligors Excess'])
        
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["First Lien Last Out, Second Lien Loan not in Top Three Obligors Revised Value"] = portfolio_df.apply(fllosllnitto_revised_value_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
        
    def top_3_max(self):
        # ='Concentration Limits'!$J$40

        conc_limit_df = self.calculator_info.intermediate_calculation_dict['Concentration Limits']
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']

        applicable_limit = conc_limit_df.loc[conc_limit_df['test_name'] == 'First Lien Three Largest Obligors (each)', 'Applicable Limit'].iloc[0]
        portfolio_df["Top 3 Max"] = applicable_limit
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def others_max(self):
        # ='Concentration Limits'!$J$41
        
        conc_limit_df = self.calculator_info.intermediate_calculation_dict['Concentration Limits']
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']

        applicable_limit = conc_limit_df.loc[conc_limit_df['test_name'] == 'Other Obligors', 'Applicable Limit'].iloc[0]
        portfolio_df["Others Max"] = applicable_limit
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def largest_obligor_obligor(self):
        # =SUMIF($G:$G,$G11,$EZ:$EZ)

        def largest_obligor_obligor_helper(row):
            return portfolio_df[portfolio_df['Borrower'] == row['Borrower']]['First Lien Last Out, Second Lien Loan not in Top Three Obligors Revised Value'].sum()

        conc_limit_df = self.calculator_info.intermediate_calculation_dict['Concentration Limits']
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Largest Obligor Obligor"] = portfolio_df.apply(largest_obligor_obligor_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def largest_obligor_remove_dupes(self):
        # =IF(MATCH($G11,$G:$G,0)=ROW(),$FC11,0)

        def largest_obligor_remove_dupes_helper(row):
            try:
                first_index = portfolio_df[portfolio_df['Borrower'] == row['Borrower']].index[0]
                if row.name == first_index:
                    return row['Largest Obligor Obligor']
                else:
                    return 0
            except Exception as e:
                return 0

        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Largest Obligor Remove Dupes"] = portfolio_df.apply(largest_obligor_remove_dupes_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def largest_obligor_rank_2(self):
        # =IF(FD11>0,RANK(FD11,$FD$11:$FD$90)+COUNTIF($FD$11:FD11,FD11)-1,0)

        def largest_obligor_rank_2_helper(row):
            if row['Largest Obligor Remove Dupes'] <= 0:
                return 0
            remove_dups = row['Largest Obligor Remove Dupes']
            rank = portfolio_df[portfolio_df['Largest Obligor Remove Dupes'] > 0]['Largest Obligor Remove Dupes'].rank(method='min', ascending=False)[row.name]
            count_dup = portfolio_df.loc[:row.name, 'Largest Obligor Remove Dupes'].eq(remove_dups).sum()
            return int(rank + count_dup - 1)
        # 
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Largest Obligor Rank 2"] = portfolio_df.apply(largest_obligor_rank_2_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df


    def largest_obligor_rank(self):
        # =INDEX(FF$10:FF$90,MATCH(G11,G$10:G$90,0))
        def largest_obligor_rank_helper(row):
            try:
                match_index = portfolio_df[portfolio_df['Borrower'] == row['Borrower']].index[0]
                return portfolio_df.loc[match_index, 'Largest Obligor Rank 2']
            except Exception as e:
                return 0

        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Largest Obligor Rank"] = portfolio_df.apply(largest_obligor_rank_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    
    def top_3_excess(self):
        # =IFERROR(IF(FE11<4,IF(FC11>FA11,(FC11-FA11)*(EZ11/SUMIF($G:$G,G11,$EZ:$EZ)),0),0),0)

        def top_3_excess_helper(row):
            try:
                if row['Largest Obligor Rank'] < 4:
                    if row['Largest Obligor Obligor'] > row['Top 3 Max']:
                        # Sum of EZ where G matches current row's G
                        total_ez = portfolio_df.loc[portfolio_df['Borrower'] == row['Borrower'], 'First Lien Last Out, Second Lien Loan not in Top Three Obligors Revised Value'].sum()
                        if total_ez != 0:
                            return (row['Largest Obligor Obligor'] - row['Top 3 Max']) * (row['First Lien Last Out, Second Lien Loan not in Top Three Obligors Revised Value'] / total_ez)
                return 0
            except:
                return 0
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Top 3 Excess"] = portfolio_df.apply(top_3_excess_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def other_excess(self):
        # =IFERROR(IF(FE11>3,IF(FC11>FB11,(FC11-FB11)*(EZ11/(SUMIF($G:$G,$G11,$EZ:$EZ))),0),0),0)

        def other_excess_helper(row):
            try:
                if row['Largest Obligor Rank'] > 3:
                    if row['Largest Obligor Obligor'] > row['Others Max']:
                        total_ez = portfolio_df.loc[portfolio_df['Borrower'] == row['Borrower'], 'First Lien Last Out, Second Lien Loan not in Top Three Obligors Revised Value'].sum()
                        if total_ez != 0:
                            return (row['Largest Obligor Obligor'] - row['Others Max']) * (row['First Lien Last Out, Second Lien Loan not in Top Three Obligors Revised Value'] / total_ez)
                return 0
            except:
                return 0
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Other Excess"] = portfolio_df.apply(other_excess_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
        
    def largest_obligor_revised_value(self):
        # =MAX(0,EZ11-FG11-FH11)

        def largest_obligor_revised_value_helper(row):
            return max(0, row['First Lien Last Out, Second Lien Loan not in Top Three Obligors Revised Value'] - row['Top 3 Excess'] - row['Other Excess'])
        
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Largest Obligor Revised Value"] = portfolio_df.apply(largest_obligor_revised_value_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
        
    def largest_industry_max(self):
        # ='Concentration Limits'!$J$42
        conc_limit_df = self.calculator_info.intermediate_calculation_dict['Concentration Limits']
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']

        applicable_limit = conc_limit_df.loc[conc_limit_df['test_name'] == 'Largest Industry', 'Applicable Limit'].iloc[0]
        portfolio_df["Largest Industry Max"] = applicable_limit
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def largest_industry_loan_limit(self):
        # =SUMIF($BZ:$BZ,$BZ11,FI:FI)
        def largest_industry_loan_limit_helper(row):
            matching_rows = portfolio_df[portfolio_df['Borrower'] == row['Borrower']]
            return matching_rows['Largest Obligor Revised Value'].sum()
        
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Largest Industry Loan Limit"] = portfolio_df.apply(largest_industry_loan_limit_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def largest_industry(self):
        # =VLOOKUP(BZ11,'Concentration Limits'!$E$64:$I$132,4,FALSE)
        def largest_industry_loan_limit_helper(row):
            industry_name = row['Approved Industry']
            total_bb = portfolio_df_copy["Adjusted Borrowing Value"].sum()
            if industry_name in grouped_df['Approved Industry'].values:
                rank = grouped_df[grouped_df['Approved Industry'] == industry_name]['Rank'].values[0]
                # percent_bb = (industry_bb / total_bb) * 100
                return rank
            else:
                return 0

        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df_copy = portfolio_df.copy(deep=True)
        portfolio_df_copy[["Adjusted Borrowing Value"]] = portfolio_df_copy[["Adjusted Borrowing Value"]].fillna(0)

    
        grouped_df = portfolio_df_copy.groupby('Approved Industry')['Adjusted Borrowing Value'].sum().reset_index()
        ranks = grouped_df['Adjusted Borrowing Value'].rank(method='min', ascending=False)
        grouped_df['Rank'] = grouped_df['Adjusted Borrowing Value'].apply(lambda x: 0 if x == 0 else int(ranks.loc[grouped_df['Adjusted Borrowing Value'] == x].iloc[0]))

        portfolio_df["Largest Industry"] = portfolio_df.apply(largest_industry_loan_limit_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def largest_industry_excess(self):
        # =IF(FL11=1, MAX(0, (FK11-FJ11)*(FI11/SUMIF($BZ:$BZ,BZ11,FI:FI))), 0)
        def largest_industry_excess_helper(row):
            try:
                if row['Largest Industry'] == 1:
                    total_fi = portfolio_df.loc[portfolio_df['Approved Industry'] == row['Approved Industry'], 'Largest Obligor Revised Value'].sum()
                    return max(0, (row['Largest Industry Loan Limit'] - row['Largest Industry Max']) * (row['Largest Obligor Revised Value'] / total_fi))
                else:
                    return 0
            except:
                return 0
            
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Largest Industry Excess"] = portfolio_df.apply(largest_industry_excess_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def largest_industry_revised_value(self):
        # =MAX(0,FI11-FM11)
        def largest_industry_revised_value_helper(row):
            return max(0, row['Largest Obligor Revised Value'] - row['Largest Industry Excess'])
        
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Largest Industry Revised Value"] = portfolio_df.apply(largest_industry_revised_value_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def second_largest_industry_max(self):
        # ='Concentration Limits'!$J$43
        conc_limit_df = self.calculator_info.intermediate_calculation_dict['Concentration Limits']
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']

        applicable_limit = conc_limit_df.loc[conc_limit_df['test_name'] == 'Second Largest Industry', 'Applicable Limit'].iloc[0]
        portfolio_df["Second Largest Industry Max"] = applicable_limit
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def second_largest_industry_loan_limit(self):
        # =SUMIF($BZ:$BZ,$BZ11,FN:FN)
        def second_largest_industry_loan_limit_helper(row):
            matching_rows = portfolio_df[portfolio_df['Borrower'] == row['Borrower']]
            return matching_rows['Largest Industry Revised Value'].sum()
        
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Second Largest Industry Loan Limit"] = portfolio_df.apply(second_largest_industry_loan_limit_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def second_largest_industry(self):
        # =F11
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["2nd Largest Industry"] = portfolio_df["Largest Industry"]
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def second_largest_industry_excess(self): 
    # =MAX(0,IF(FQ11=2,(FP11-FO11)*(FN11/SUMIF($BZ:$BZ,BZ11,FN:FN)),0))
        def second_largest_industry_excess_helper(row):
            if row['2nd Largest Industry'] != 2:
                return 0
            try:
                group_sum = portfolio_df[portfolio_df['Approved Industry'] == row['Approved Industry']]['Largest Industry Revised Value'].sum()
                if group_sum == 0:
                    return 0
                value = (row['Second Largest Industry Loan Limit'] - row['Second Largest Industry Max']) * (row['Largest Industry Revised Value'] / group_sum)
                return max(0, value)
            except:
                return 0

        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Second Largest Industry Excess"] = portfolio_df.apply(second_largest_industry_excess_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
    

    def second_largest_industry_revised_value(self):
        # =MAX(0,FN11-FR11)
        def second_largest_industry_revised_value_helper(row):
            return max(0, row['Largest Industry Revised Value'] - row['Second Largest Industry Excess'])
        
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Second Largest Industry Revised Value"] = portfolio_df.apply(second_largest_industry_revised_value_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def third_largest_industry_max(self):
        # ='Concentration Limits'!$J$44
        conc_limit_df = self.calculator_info.intermediate_calculation_dict['Concentration Limits']
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']

        applicable_limit = conc_limit_df.loc[conc_limit_df['test_name'] == 'Third Largest Industry', 'Applicable Limit'].iloc[0]
        portfolio_df["Third Largest Industry Max"] = applicable_limit
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def third_largest_industry_loan_limit(self):
        # =SUMIF($BZ:$BZ,$BZ11,FS:FS)
        def third_largest_industry_loan_limit_helper(row):
            matching_rows = portfolio_df[portfolio_df['Borrower'] == row['Borrower']]
            return matching_rows['Second Largest Industry Revised Value'].sum()
        
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Third Largest Industry Loan Limit"] = portfolio_df.apply(third_largest_industry_loan_limit_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def third_largest_industry(self):
        # =FL11
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Third Largest Industry"] = portfolio_df["Largest Industry"]
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def third_largest_industry_excess(self):
        # =MAX(0,IF(FV11=3,(FU11-FT11)*(FS11/SUMIF($BZ:$BZ,BZ11,FS:FS)),0))
        def third_largest_industry_excess_helper(row):
            if row['Third Largest Industry'] != 3:
                return 0
            try:
                group_sum = portfolio_df[portfolio_df['Approvd Industry'] == row['Approvd Industry']]['FS'].sum()
                if group_sum == 0:
                    return 0
                value = (row['Third Largest Industry Loan Limit'] - row['Third Largest Industry Max']) * (row['Second Largest Industry Revised Value'] / group_sum)
                return max(0, value)
            except:
                return 0

        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Third Largest Industry Excess"] = portfolio_df.apply(third_largest_industry_excess_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def third_largest_industry_revised_value(self):
        # =MAX(0,FS11-FW11)
        def third_largest_industry_revised_value_helper(row):
            return max(0, row['Second Largest Industry Revised Value'] - row['Third Largest Industry Excess'])
        
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Third Largest Industry Revised Value"] = portfolio_df.apply(third_largest_industry_revised_value_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def other_industry_max(self):
        # ='Concentration Limits'!$J$45
        conc_limit_df = self.calculator_info.intermediate_calculation_dict['Concentration Limits']
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']

        applicable_limit = conc_limit_df.loc[conc_limit_df['test_name'] == 'Other Industry', 'Applicable Limit'].iloc[0]
        portfolio_df["Other Industry Max"] = applicable_limit
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def other_industry_loan_limit(self):
        # =SUMIF($BZ:$BZ,$BZ11,FX:FX)
        def other_industry_loan_limit_helper(row):
            matching_rows = portfolio_df[portfolio_df['Borrower'] == row['Borrower']]
            return matching_rows['Third Largest Industry Revised Value'].sum()
        
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Other Industry Loan Limit"] = portfolio_df.apply(other_industry_loan_limit_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def other_industries(self):
        # =FL11
        def other_industries_helper(row):
            return row['Largest Industry']

        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Other Industries"] = portfolio_df.apply(other_industries_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def other_industry_excess(self):
        # =IF(FX11=0,0,MAX(0,IF(GA11<4,0,(FZ11-FY11)*($FX11/SUMIF($BZ:$BZ,BZ11,FX:FX)))))
        def other_industry_excess_helper(row):
            if row['Third Largest Industry Revised Value'] == 0:
                return 0
            if row['Other Industries'] < 4:
                return 0
            try:
                fx_group_sum = portfolio_df[portfolio_df['Approved Industries'] == row['Approved Industries']]['Third Largest Industry Revised Value'].sum()
                if fx_group_sum == 0:
                    return 0
                value = (row['Other Industry Loan Limit'] - row['Other Industry Max']) * (row['Third Largest Industry Revised Value'] / fx_group_sum)
                return max(0, value)
            except:
                return np.nan
            
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Other Industries Excess"] = portfolio_df.apply(other_industry_excess_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def other_industries_revised_value(self):
        # =MAX(0,FX11-GB11)
        def other_industries_revised_value_helper(row):
            return max(0, row['Third Largest Industry Revised Value'] - row['Other Industries'])
        
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Other Industries Revised Value"] = portfolio_df.apply(other_industries_revised_value_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def ebitda_less_than_10mm_max(self):
        # ='Concentration Limits'!$J$46
        conc_limit_df = self.calculator_info.intermediate_calculation_dict['Concentration Limits']
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']

        applicable_limit = conc_limit_df.loc[conc_limit_df['test_name'] == 'EBITDA < $10MM', 'Applicable Limit'].iloc[0]
        portfolio_df["EBITDA Less Than $10MM Max"] = applicable_limit
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def calculate_excess_concentrations(self):
        self.pre_excess_concentration_adjusted_borrowing_value() # column 'ES'
        # First Lien Last Out, Second Lien Loan not in Top Three Obligors
        self.obligor() # column 'EU'
        self.remove_dupes() # column 'EV'
        self.rank_2() # column 'EX'
        self.rank() # self.rank() # column 'EW'
        self.qualifies() # column 'ET'
        self.fllosllnitto_excess() # column 'EY'
        self.fllosllnitto_revised_value() # column 'EZ'

        # (b) & (c) Largest Obligor
        self.top_3_max() # column 'FA'
        self.others_max() # column 'FB'
        self.largest_obligor_obligor() # column 'FC'
        self.largest_obligor_remove_dupes() # column 'FD'
        self.largest_obligor_rank_2() # column 'FF'
        self.largest_obligor_rank() # column 'FE'
        self.top_3_excess() # column 'FG'
        self.other_excess() # column 'FH'
        self.largest_obligor_revised_value() # column 'FI'

        # (d)(a) Largest Industry
        self.largest_industry_max() # column 'FJ'
        self.largest_industry_loan_limit() # column 'FK'
        self.largest_industry() # column 'FL'
        self.largest_industry_excess() # column 'FM'
        self.largest_industry_revised_value() # column 'FN'

        # (d)(b) 2nd Largest Industry
        self.second_largest_industry_max() # column 'FO'
        self.second_largest_industry_loan_limit() # column 'FP'
        self.second_largest_industry() # column 'FQ'
        self.second_largest_industry_excess() # column 'FR'
        self.second_largest_industry_revised_value() # column 'FS'

        # (d)(c) 3rd Largest Industry
        self.third_largest_industry_max() # column 'FT'
        self.third_largest_industry_loan_limit() # column 'FU'
        self.third_largest_industry() # column 'FV'
        self.third_largest_industry_excess() # column 'FW'
        self.third_largest_industry_revised_value() # column 'FX'

        # (d)(d) All Other Industry Classifications
        self.other_industry_max() # column 'FY'
        self.other_industry_loan_limit() # column 'FZ'
        self.other_industries() # column 'GA'
        self.other_industry_excess() # column 'GB'
        self.other_industries_revised_value() # column 'GC'

