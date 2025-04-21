import  numpy as np

class Others:
    def __init__(self, calculator_info):
        self.calculator_info = calculator_info

    def advance_rate_definition(self):
        # =IF(G17="","-",IF(T17="Ineligible","Ineligible",IF(OR(T17="Last Out",T17="Second Lien",T17="Recurring Revenue"),T17,CONCATENATE(T17," ",ER17))))
        def advance_rate_definition_helper(row):
            if row['Borrower'] == "":
                return "-"
            elif row["Calculated Loan Type post AA Discretion"] == "Ineligible":
                return "Ineligible"
            elif row["Calculated Loan Type post AA Discretion"] == "Last Out" or row["Calculated Loan Type post AA Discretion"] == "Second Lien" or row["Calculated Loan Type post AA Discretion"] == "Recurring Revenue":
                return row["Calculated Loan Type post AA Discretion"]
            else:
                return row["Calculated Loan Type post AA Discretion"] + " " + row["Advance Rate Class"]


        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Advance Rate Definition"] = portfolio_df.apply(advance_rate_definition_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
        
    def vae_trigger(self):
        # =IF(OR(DW11="Yes",DX11="Yes",DY11="Yes",DZ11="Yes",EA11="Yes",EB11="Yes",EC11="Yes",ED11="Yes",EE11="Yes",EF11="Yes",EG11="Yes",EH11="Yes",EI11="Yes",EJ11="Yes",EQ11="Yes",EK11="Yes",EL11="Yes"),"Yes","No")

        def vae_trigger_helper(row):
            if row["Cash Interest Coverage Ratio Test"] == "Yes" or row["Net Senior Leverage Ratio Test"] == "Yes" or row["Recurring Revenue Multiple"] == "Yes" or row["Recurring Revenue Multiple"] == "Yes" or row["Liquidity Credit Quality Deterioration"] == "Yes" or row["Obligor Payment Default"] == "Yes" or row["Exercise Rights and Remedies"] == "Yes" or row["Reduces/Waives Principal"] == "Yes" or row["Extends Maturity Date"] == "Yes" or row["Reduces/Waives Interest"] == "Yes" or row["Subordinates Loan(s)"] == "Yes" or row["Releases Collateral/Lien"] == "Yes" or row["Amends Covenants"] == "Yes" or row["Amends Definitions (Permitted Lien/Indebtedness)"] == "Yes" or row["Insolvency Event"] == "Yes" or row["Waives or Extends Due Date of Financial Reports"] == "Yes" or row["Reporting Failure Event"] == "Yes":
                return "Yes"
            else:
                return "No"
            
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["VAE Trigger"] = portfolio_df.apply(vae_trigger_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
        
    def vae_recorded_on_vae_tab(self):
        # =IF(COUNTIFS(VAE!$C$5:$C$114,G11,VAE!$F$5:$F$114,"<="&Availability!$F$12)>=1,"Yes","-")

        def vae_recorded_on_vae_tab_helper(row):
            borrower = row["Borrower"]
            return (
                "Yes"
                if not vae_df[
                    (vae_df['Obligor'] == borrower) & 
                    (vae_df['Date of VAE Decision'] <= cutoff)
                ].empty else "-"
            )
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        vae_df = self.calculator_info.intermediate_calculation_dict['VAE']
        availability_df = self.calculator_info.intermediate_calculation_dict['Availability']
        cutoff = availability_df.query("Terms == 'Measurement Date:'")["Values"].iloc[0]
        portfolio_df["VAE (Recorded on VAE Tab)"] = portfolio_df.apply(vae_recorded_on_vae_tab_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def vae_effective_date(self):
        # =ARRAY_CONSTRAIN(ARRAYFORMULA(IF(MAX(IF(VAE!$C$5:$C$114=G11,IF(VAE!$F$5:$F$114<=Availability!$F$12,VAE!$F$5:$F$114)))=0,"-",MAX(IF(VAE!$C$5:$C$114=G11,IF(VAE!$F$5:$F$114<=Availability!$F$12,VAE!$F$5:$F$114))))), 1, 1)

        def vae_effective_date_helper(row):
            g_value = row['Borrower']
    
            filtered = vae_df[(vae_df['Obligor'] == g_value) & (vae_df['Date of VAE Decision'] <= cutoff)]
            
            if filtered.empty:
                return "-"
            else:
                return filtered['Date of VAE Decision'].max()
        
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        vae_df = self.calculator_info.intermediate_calculation_dict['VAE']
        availability_df = self.calculator_info.intermediate_calculation_dict['Availability']
        cutoff = availability_df.query("Terms == 'Measurement Date:'")["Values"].iloc[0]
        portfolio_df["VAE Effective Date"] = portfolio_df.apply(vae_effective_date_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def event_type(self):
        # =ARRAY_CONSTRAIN(ARRAYFORMULA(IFERROR(IF(AL11="Yes",INDEX(VAE!$D$5:$D$114,MATCH(G11&AN11,VAE!$C$5:$C$114&VAE!$F$5:$F$114,0),MATCH("Event Type",VAE!$D$4,0)),"-"),0)), 1, 1)

        def event_type_helper(row):
            if row['VAE (Recorded on VAE Tab)'] != "Yes":
                return "-"
            
            g_val = row['Borrower']
            an_val = row['VAE Effective Date']
            
            match = vae_df[(vae_df['Obligor'] == g_val) & (vae_df['Date of VAE Decision'] == an_val)]
            
            if not match.empty:
                return match.iloc[0]['Event Type']
            else:
                return 0
    
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        vae_df = self.calculator_info.intermediate_calculation_dict['VAE']
        availability_df = self.calculator_info.intermediate_calculation_dict['Availability']
        cutoff = availability_df.query("Terms == 'Measurement Date:'")["Values"].iloc[0]
        portfolio_df["Event Type"] = portfolio_df.apply(event_type_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
    
    def agent_assigned_value(self):
        # =ARRAY_CONSTRAIN(ARRAYFORMULA(IFERROR(IF(AL11="Yes",INDEX(VAE!$R$5:$R$114,MATCH(G11&AN11,VAE!$C$5:$C$114&VAE!$F$5:$F$114,0),MATCH("Assigned Value",VAE!$R$4,0)),"-"),0)), 1, 1)

        def agent_assigned_value_helper(row):
            if row['VAE (Recorded on VAE Tab)'] != "Yes":
                return "-"
            
            g_val = row['Borrower']
            an_val = row['VAE Effective Date']
            
            match = vae_df[(vae_df['Obligor'] == g_val) & (vae_df['Date of VAE Decision'] == an_val)]
            
            if not match.empty:
                return match.iloc[0]['Assigned Value']
            else:
                return 0
            
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        vae_df = self.calculator_info.intermediate_calculation_dict['VAE']
        availability_df = self.calculator_info.intermediate_calculation_dict['Availability']
        cutoff = availability_df.query("Terms == 'Measurement Date:'")["Values"].iloc[0]
        portfolio_df["Agent Assigned Value"] = portfolio_df.apply(agent_assigned_value_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
        
    def applicable_collateral_value(self):
        
        # =IF(BK11="No",0,IF(T11="First Lien",IF(DH11<Tier_1_1L,Tier_1_ApplicableValue,IF(DH11<Tier_2_1L,Tier_2_ApplicableValue,Tier_3_ApplicableValue)),IF(OR(T11="Second Lien",T11="Last Out"),IF(DI11<Tier_1_2L,Tier_1_ApplicableValue,IF(DI11<Tier_2_2L,Tier_2_ApplicableValue,Tier_3_ApplicableValue)),IF(T11="Recurring Revenue",IF(DN11<Tier_1_RR,Tier_1_ApplicableValue,IF(DN11<Tier_2_RR,Tier_2_ApplicableValue,Tier_3_ApplicableValue))))))

        def applicable_collateral_value_helper(row):
            if row['Eligibility Check'] == "No":
                return 0

            if row['Calculated Loan Type post AA Discretion'] == "First Lien":
                value = row['Current Net Senior']
                if value < Tier_1_1L:
                    return Tier_1_ApplicableValue
                elif value < Tier_2_1L:
                    return Tier_2_ApplicableValue
                else:
                    return Tier_3_ApplicableValue

            elif row['Calculated Loan Type post AA Discretion'] in ["Second Lien", "Last Out"]:
                value = row['Current Net Total']
                if value < Tier_1_2L:
                    return Tier_1_ApplicableValue
                elif value < Tier_2_2L:
                    return Tier_2_ApplicableValue
                else:
                    return Tier_3_ApplicableValue

            elif row['Calculated Loan Type post AA Discretion'] == "Recurring Revenue":
                value = row['Current Multiple']
                if value < Tier_1_RR:
                    return Tier_1_ApplicableValue
                elif value < Tier_2_RR:
                    return Tier_2_ApplicableValue
                else:
                    return Tier_3_ApplicableValue

            return 0

        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        obligor_tiers_map = self.calculator_info.intermediate_calculation_dict['obligor_tiers_map']
        Tier_1_ApplicableValue = obligor_tiers_map.get('tier_1_applicable_value')
        Tier_2_ApplicableValue = obligor_tiers_map.get('tier_2_applicable_value')
        Tier_3_ApplicableValue = obligor_tiers_map.get('tier_3_applicable_value')
        Tier_1_1L = obligor_tiers_map.get('tier_1_1l')
        Tier_1_2L = obligor_tiers_map.get('tier_1_2l')
        Tier_2_1L = obligor_tiers_map.get('tier_2_1l')
        Tier_2_2L = obligor_tiers_map.get('tier_2_2l')
        Tier_1_RR = obligor_tiers_map.get('tier_1_rr')
        Tier_2_RR = obligor_tiers_map.get('tier_2_rr')
        portfolio_df["Applicable Collateral Value"] = portfolio_df.apply(applicable_collateral_value_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def ebitda_greater_than_5MM(self):
        # =IFERROR(IF(CR11>=5000000,"Yes","No"),"-")
        def ebitda_greater_than_5MM_helper(row):
            try:
                if row['Permitted TTM EBITDA (USD)'] > 5000000:
                    return "Yes"
                else:
                    return "No"
            except Exception as e:
                return "-"

        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["EBITDA > $5MM"] = portfolio_df.apply(ebitda_greater_than_5MM_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def second_lien_flloebitda_greater_than_10MM(self):
        # =IFERROR(IF(OR(H11="Second Lien",H11="Last Out"),IF(CR11>=10000000,"Yes","No"),"na"),"-")

        def second_lien_flloebitda_greater_than_10MM_helper(row):
            try:
                if row['Loan Type'] in ["Second Lien", "Last Out"]:
                    if row['Permitted TTM EBITDA (USD)'] > 10000000:
                        return "Yes"
                    else:
                        return "No"
                else:
                    return "na"
            except Exception as e:
                return "-"

        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Second Lien or FLLOEBITDA >$10MM"] = portfolio_df.apply(second_lien_flloebitda_greater_than_10MM_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
    
    def eligible_cov_lite(self):
        # =IF(BM11="Yes",IF(AND(CR11>=50000000,CF11="Yes",CT11>=200000000,CF11="Yes"),"Yes","No"),"na")
        def eligible_cov_lite_helper(row):
            if row['Cov-Lite'] == "Yes":
                if row['Permitted TTM EBITDA (USD)'] >= 50000000 and row['Rated B- or Better'] == "Yes" and row['Initial Gross Senior Debt'] >= 200000000:
                    return "Yes"
                else:
                    return "No"
            else:
                return "na"
            
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Eligible Cov-Lite"] = portfolio_df.apply(eligible_cov_lite_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
    
    def eligible_recurring_revenue(self):
        # =IFERROR(IF(H11="Recurring Revenue",IF(AND(DJ11>=20000000,DL11<=2.5),"Yes","No"),"na"),"-")
        def eligible_recurring_revenue_helper(row):
            try:
                if row['Loan Type'] == "Recurring Revenue":
                    if row['Initial Annualized Recurring Revenue'] >= 20000000 and row['Initial Multiple'] <= 2.5:
                        return "Yes"
                    else:
                        return "No"
                else:
                    return "na"
            except Exception as e:
                return "-"

        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Eligible Recurring Revenue"] = portfolio_df.apply(eligible_recurring_revenue_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
    
    def eligibility_check(self):
        # =IF(BL11="No","No",IF(OR(U11="Ineligible",BU11="No",BV11="No",BW11="No",BX11="No"),"No",IF(CZ11<0,"No","Yes")))

        def eligibility_check_helper(row):
            if row["Eligible Loan Attestation"] == "No":
                return "No"
            else:
                if row["Advance Rate Definition"] == "Ineligible" or row["EBITDA > $5MM"] == "No" or row["Second Lien or FLLOEBITDA >$10MM"] == "No" or row["Eligible Cov-Lite"] == "No" or row["Eligible Recurring Revenue"] == "No":
                    return "No"            
                else:
                    if row["Permitted TTM EBITDA (USD) at relevant test period"] < 0:
                        return "No"
                    else:
                        return "Yes"
                    
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Eligibility Check"] = portfolio_df.apply(eligibility_check_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
        
    def failure_to_deliver_financials_factor(self):
        # =IF(EL11="Yes",IF(EP11<0,0%,IF(EP11<30,15%,IF(AND(EP11>=30,EP11<60),30%,IF(AND(EP11>=60,EP11<90),45%,IF(AND(EP11>=90,EP11<120),60%,IF(AND(EP11>=120,EP11<150),75%,IF(AND(EP11>=150,EP11<180),90%,100%))))))),0)
        
        def failure_to_deliver_financials_factor_helper(row):
            if row["Reporting Failure Event"] == "Yes":
                if row["Day Count"] < 0:
                    return 0.0
                else:
                    if row["Day Count"] < 30:
                        return 0.15
                    else:
                        if row["Day Count"] >= 30 and row["Day Count"] < 60:
                            return 0.30
                        else:
                            if row["Day Count"] >= 60 and row["Day Count"] < 90:
                                return 0.45
                            else:
                                if row["Day Count"] >= 90 and row["Day Count"] < 120:
                                    return 0.60
                                else:
                                    if row["Day Count"] >= 120 and row["Day Count"] < 150:
                                        return 0.75
                                    else:
                                        if row["Day Count"] >= 150 and row["Day Count"] < 180:
                                            return 0.90
                                        else:
                                            return 1.00
            else:
                return 0

        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Failure to Deliver Financials Factor"] = portfolio_df.apply(failure_to_deliver_financials_factor_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def assigned_value(self):
        # =MAX(0,IF(AL11="Yes",MIN(AO11,IF(AJ11<0.95,AJ11,100%),AP11)-IF(EL11="Yes",AR11,0%),MIN(IF(AJ11<0.95,AJ11,100%),AP11)-IF(EL11="Yes",AR11,0%)))

        def assigned_value_helper(row):
            try:
                aj_value = row['Acquisition Price']
                aj_check = aj_value if aj_value < 0.95 else 1.0  # 100% as 1.0 in Python
                min_value = min(aj_check, row['Applicable Collateral Value'])

                if row['VAE (Recorded on VAE Tab)'] == 'Yes':
                    inner_min = min(row['Agent Assigned Value'], min_value)
                else:
                    inner_min = min_value

                subtractor = row['Failure to Deliver Financials Factor'] if row['Reporting Failure Event'] == 'Yes' else 0
                result = inner_min - subtractor

                return max(0, result)
            except:
                return np.nan

        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Assigned Value"] = portfolio_df.apply(assigned_value_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
        
    def amounts_in_excess_of_tier_3_reclassified_as_2nd_lien(self):
        # =IFERROR(IF(OR(T11="Second Lien",T11="Last Out",T11="Recurring Revenue"),0,IF(DH11>Tier_3_1L,((DH11-Tier_3_1L)/DH11)*AF11,0))-AT11,"-")

        def amounts_in_excess_of_tier_3_reclassified_as_2nd_lien_helper(row):
            try:
                if row['Calculated Loan Type post AA Discretion'] in ["Second Lien", "Last Out", "Recurring Revenue"]:
                    return 0 - row['Leverage Amounts in excess of Tier 3 Reclassified as zero value']
                elif row['Current Net Senior'] > tier_3_1l:
                    result = ((row['Current Net Senior'] - tier_3_1l) / row['Current Net Senior']) * row['Borrower Outstanding Principal Balance (USD)']
                    return result - row['Leverage Amounts in excess of Tier 3 Reclassified as zero value']
                else:
                    return 0 - row['Leverage Amounts in excess of Tier 3 Reclassified as zero value']
            except:
                return "-"
        
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        obligor_tiers_map = self.calculator_info.intermediate_calculation_dict['obligor_tiers_map']
        tier_3_1l = obligor_tiers_map['tier_3_1l']
        portfolio_df["Amounts in excess of Tier 3 Reclassified as 2nd Lien"] = portfolio_df.apply(amounts_in_excess_of_tier_3_reclassified_as_2nd_lien_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def leverage_amounts_in_excess_of_tier_3_reclassified_as_zero_value(self):
        # =IFERROR(IF(OR(T11="Second Lien",T11="Last Out",T11="Recurring Revenue"),0,IF(DH11>Tier_3_2L,((DH11-Tier_3_2L)/DH11)*AF11,0)),"-")

        def leverage_amounts_in_excess_of_tier_3_reclassified_as_zero_value_helper(row):
            try:
                if row['Calculated Loan Type post AA Discretion'] in ["Second Lien", "Last Out", "Recurring Revenue"]:
                    return 0
                elif row['Current Net Senior'] > tier_3_2l:
                    return ((row['Current Net Senior'] - tier_3_2l) / row['Current Net Senior']) * row['Borrower Outstanding Principal Balance (USD)']
                else:
                    return 0
            except:
                return np.nan

        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        obligor_tiers_map = self.calculator_info.intermediate_calculation_dict['obligor_tiers_map']
        tier_3_2l = obligor_tiers_map['tier_3_2l']
        portfolio_df["Leverage Amounts in excess of Tier 3 Reclassified as zero value"] = portfolio_df.apply(leverage_amounts_in_excess_of_tier_3_reclassified_as_zero_value_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def first_lien_amount(self):
        # =IFERROR(IF(OR(T11="Second Lien",T11="Last Out",T11="Recurring Revenue"),0,AF11-AS11-AT11),"-")

        def first_lien_amount_helper(row):
            if row["Calculated Loan Type post AA Discretion"] in ["Second Lien", "Last Out", "Recurring Revenue"]:
                return 0
            else:
                try:
                    return row['Borrower Outstanding Principal Balance (USD)'] - row['Amounts in excess of Tier 3 Reclassified as 2nd Lien'] - row['Leverage Amounts in excess of Tier 3 Reclassified as zero value']
                except:
                    return np.nan

        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["First Lien Amount"] = portfolio_df.apply(first_lien_amount_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def first_lien_value(self):
        # =IFERROR(+AQ11*AU11,"-")
        def first_lien_value_helper(row):
            try:
                return row['Assigned Value'] * row['First Lien Amount']
            except:
                return np.nan

        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["First Lien Value"] = portfolio_df.apply(first_lien_value_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
        
    def leverage_metrics_second_lien_value(self):
        # =IFERROR(AS11*AQ11,"-")
        def second_lien_value_helper(row):
            try:
                return row['Amounts in excess of Tier 3 Reclassified as 2nd Lien'] * row['Assigned Value']
            except:
                return np.nan
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Leverage Metrics 2nd Lien Value"] = portfolio_df.apply(second_lien_value_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def amounts_in_excess_of_Tier_3_reclassified_as_zero_value(self):
        # =IFERROR(IF(OR(T11="First Lien",T11="Recurring Revenue"),0,IF(AF11=0,0,IF(DI11>Tier_3_2L,((DI11-Tier_3_2L)/DI11)*AF11,0))),"-")

        def amounts_in_excess_of_Tier_3_reclassified_as_zero_value_helper(row):
            try:
                if row['Calculated Loan Type post AA Discretion'] in ["First Lien", "Recurring Revenue"]:
                    return 0
                if row['Borrower Outstanding Principal Balance (USD)'] == 0:
                    return 0
                if row['Current Net Total'] > tier_3_2l:
                    return ((row['Current Net Total'] - tier_3_2l) / row['Current Net Total']) * row['Current Net Total']
                return 0
            except:
                return "-"
            
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        obligor_tiers_map = self.calculator_info.intermediate_calculation_dict['obligor_tiers_map']
        tier_3_2l = obligor_tiers_map['tier_3_2l']
        portfolio_df["Amounts in excess of Tier 3 Reclassified as zero value"] = portfolio_df.apply(amounts_in_excess_of_Tier_3_reclassified_as_zero_value_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
        
    def last_out_or_2nd_lien_amount(self):
        # =IFERROR(IF(OR(T11="First Lien",T11="Recurring Revenue"),0,(AF11-AX11)),"-")
        def last_out_or_2nd_lien_amount_helper(row):
            try:
                if row["Calculated Loan Type post AA Discretion"] in ["First Lien", "Recurring Revenue"]:
                    return 0
                else:
                    row["Borrower Outstanding Principal Balance (USD)"] - row["Amounts in excess of Tier 3 Reclassified as zero value"]
            except Exception as e:
                return np.nan

        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        obligor_tiers_map = self.calculator_info.intermediate_calculation_dict['obligor_tiers_map']
        tier_3_2l = obligor_tiers_map['tier_3_2l']
        portfolio_df["Last Out or 2nd Lien Amount"] = portfolio_df.apply(last_out_or_2nd_lien_amount_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def fllo_value(self):
        # =IFERROR(IF(T11="Last Out",AY11*AQ11,0),"-")
        def last_out_or_2nd_lien_amount_helper(row):
            try:
                if row["Calculated Loan Type post AA Discretion"] == "Last Out":
                    return row['Last Out or 2nd Lien Amount'] * row['Assigned Value']
                else:
                    return 0
            except Exception as e:
                return np.nan
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["FLLO Value"] = portfolio_df.apply(last_out_or_2nd_lien_amount_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def second_lien_value(self):
        # =IFERROR(IF(T11="Second Lien",AY11*AQ11,0),"-")
        def second_lien_value_helper(row):
            try:
                if row["Calculated Loan Type post AA Discretion"] == "Second Lien":
                    return row['Last Out or 2nd Lien Amount'] * row['Assigned Value']
                else:
                    return 0
            except Exception as e:
                return np.nan

        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["2nd Lien Value"] = portfolio_df.apply(second_lien_value_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
        
    def recurring_revenue_amounts_in_excess_of_tier_3_reclassified_as_zero_value(self):
        # =IF(T11="Recurring Revenue",IF(DN11>Tier_3_RR,((DN11-Tier_3_RR)/DN11)*AF11,0),0)
        def recurring_revenue_amounts_in_excess_of_tier_3_reclassified_as_zero_value_helper(row):
            if row['Calculated Loan Type post AA Discretion'] == "Recurring Revenue":
                if row['Current Multiple'] > tier_3_rr:
                    return ((row['Current Multiple'] - tier_3_rr) / row['Current Multiple']) * row['Borrower Outstanding Principal Balance (USD)']
                else:
                    return 0
            else:
                return 0
            
        obligor_tiers_map = self.calculator_info.intermediate_calculation_dict['obligor_tiers_map']
        tier_3_rr = obligor_tiers_map['tier_3_rr']
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Recurrng Revenue Amounts in excess of Tier 3 Reclassified as zero value"] = portfolio_df.apply(recurring_revenue_amounts_in_excess_of_tier_3_reclassified_as_zero_value_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
        
    def recurring_revenue_amount(self):
        # =IF(T11="Recurring Revenue",AF11-BB11,0)
        def recurring_revenue_amount_helper(row):
            if row['Calculated Loan Type post AA Discretion'] == "Recurring Revenue":
                return row['Borrower Outstanding Principal Balance (USD)'] - row['Recurrng Revenue Amounts in excess of Tier 3 Reclassified as zero value']
            else:
                return 0
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Recurring Revenue Amount"] = portfolio_df.apply(recurring_revenue_amount_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def recurring_evenue_value(self):
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Recurring Revenue Value"] = portfolio_df["Recurring Revenue Amount"]
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
    
    def adjusted_orrowing_value(self):
        # =AV11+AW11+AZ11+BA11+BD11
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Adjusted Borrowing Value"] = portfolio_df["First Lien Value"] + portfolio_df["Leverage Metrics 2nd Lien Value"] + portfolio_df["FLLO Value"] + portfolio_df["2nd Lien Value"] + portfolio_df["Recurring Revenue Value"]
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
    
    def calculate_others(self):
        self.advance_rate_definition() # column 'U'
        self.vae_trigger() # column 'AK'
        self.vae_recorded_on_vae_tab() # column 'AL'
        self.vae_effective_date() # clumn 'AN'
        self.event_type() # column 'AM'
        self.agent_assigned_value() # column 'AO'
        self.ebitda_greater_than_5MM() # column 'BU'
        self.second_lien_flloebitda_greater_than_10MM() # column 'BV'
        self.eligible_cov_lite() # column 'BW'
        self.eligible_recurring_revenue() # column 'BX'
        self.eligibility_check() # column 'BK'
        self.applicable_collateral_value() # column 'AP'
        self.failure_to_deliver_financials_factor() # column 'AR'
        self.assigned_value() # column 'AQ'
        self.leverage_amounts_in_excess_of_tier_3_reclassified_as_zero_value() # column 'AT'
        self.amounts_in_excess_of_tier_3_reclassified_as_2nd_lien() # column 'AS'
        self.first_lien_amount() # column 'AU'
        self.first_lien_value() # column 'AV'
        self.leverage_metrics_second_lien_value() # column 'AW'
        self.amounts_in_excess_of_Tier_3_reclassified_as_zero_value() # column 'AX'
        self.last_out_or_2nd_lien_amount() # column 'AY'
        self.fllo_value() # column 'AZ'
        self.second_lien_value() # column 'BA'
        self.recurring_revenue_amounts_in_excess_of_tier_3_reclassified_as_zero_value() # column 'BB'
        self.recurring_revenue_amount() # column 'BC'
        self.recurring_evenue_value() # column 'BD'
        self.adjusted_orrowing_value() # collumn 'W'