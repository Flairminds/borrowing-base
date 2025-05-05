from source.services.PSSL.calculation.portfolio_sheet.EbitdaNetAtDateInclussion import EbitdaNetAtDateInclussion
from source.services.PSSL.calculation.portfolio_sheet.EbitdaNetDebtRelevantTestPeriod import EbitdaNetDebtRelevantTestPeriod
from source.services.PSSL.calculation.portfolio_sheet.LeverageRatiosPermittedTtmEbitda import LeverageRatiosPermittedTtmEbitda
from source.services.PSSL.calculation.portfolio_sheet.RecurringRevenue import RecurringRevenueInterestCoverage
from source.services.PSSL.calculation.portfolio_sheet.ValueAdjustmentEvent import ValueAdjustmentEvent
from source.services.PSSL.calculation.portfolio_sheet.RevolverValidationCheckAndBorrower import RevolverValidationCheckAndBorrower
from source.services.PSSL.calculation.portfolio_sheet.Others import Others
from source.services.PSSL.calculation.portfolio_sheet.ExcessConcTest import ExcessConcTest
from source.services.PSSL.calculation.concentrations_limits_sheet.ConcentrationLimits import ConcentrationLimits
from source.services.concTestService.concTestService import ConcentrationTestExecutor

class PortfolioCalculator:
    def __init__(self, calculator_info):
        self.calculator_info = calculator_info
        exchange_rates_df = calculator_info.intermediate_calculation_dict['Exchange Rates']
        exchange_rate_map = exchange_rates_df.set_index("Currency")["Exchange Rate"].to_dict()
        self.calculator_info.intermediate_calculation_dict['exchange_rate_map'] = exchange_rate_map

        obligor_tiers_df = calculator_info.intermediate_calculation_dict['Obligor Tiers']
        obligor_tiers_map = {
            'tier_1_applicable_value': obligor_tiers_df.query("Obligor == 'Tier 1'")['Applicable Collateral Value'][0],
            'tier_2_applicable_value': obligor_tiers_df.query("Obligor == 'Tier 2'")['Applicable Collateral Value'][1],
            'tier_3_applicable_value': obligor_tiers_df.query("Obligor == 'Tier 3'")['Applicable Collateral Value'][2],
            'tier_1_1l': obligor_tiers_df.query("Obligor == 'Tier 1'")['First Lien Loans'][0],
            'tier_1_2l': obligor_tiers_df.query("Obligor == 'Tier 1'")['FLLO/2nd Lien Loans'][0],
            'tier_2_1l': obligor_tiers_df.query("Obligor == 'Tier 2'")['First Lien Loans'][1],
            'tier_2_2l': obligor_tiers_df.query("Obligor == 'Tier 2'")['FLLO/2nd Lien Loans'][1],
            'tier_3_1l': obligor_tiers_df.query("Obligor == 'Tier 3'")['First Lien Loans'][2],
            'tier_3_2l': obligor_tiers_df.query("Obligor == 'Tier 3'")['FLLO/2nd Lien Loans'][2],
            'tier_1_rr': obligor_tiers_df.query("Obligor == 'Tier 1'")['Recurring Revenue'][0],
            'tier_2_rr': obligor_tiers_df.query("Obligor == 'Tier 2'")['Recurring Revenue'][1],
            'tier_3_rr': obligor_tiers_df.query("Obligor == 'Tier 3'")['Recurring Revenue'][2],
        }
        self.calculator_info.intermediate_calculation_dict['obligor_tiers_map'] = obligor_tiers_map

    def calculate_portfolio(self):
        try:
            ebitda_net_at_date_inclussion = EbitdaNetAtDateInclussion(self.calculator_info)
            ebitda_net_at_date_inclussion.calculate_ENADI()
            ebitda_net_debt_relevant_test_period = EbitdaNetDebtRelevantTestPeriod(self.calculator_info)
            ebitda_net_debt_relevant_test_period.claculate_ENDRTP()
            leverage_ratios_permitted_ttm_ebitda = LeverageRatiosPermittedTtmEbitda(self.calculator_info)
            leverage_ratios_permitted_ttm_ebitda.calculate_LRPTE()
            recurring_revenue = RecurringRevenueInterestCoverage(self.calculator_info)
            recurring_revenue.calculate_RRIC()
            value_adjustment_event = ValueAdjustmentEvent(self.calculator_info)
            value_adjustment_event.calculate_vae()
            revolver_validation_check_borrower = RevolverValidationCheckAndBorrower(self.calculator_info)
            revolver_validation_check_borrower.calculate_RVCBB()
            other = Others(self.calculator_info)
            other.calculate_others()
            concentration_limits = ConcentrationLimits(self.calculator_info)
            concentration_limits.calculate_concentration()
            excess_conc_test = ExcessConcTest(self.calculator_info)
            excess_conc_test.calculate_excess_concentrations()

            portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
            calculated_df_map = {
            "Portfolio": portfolio_df
            }
            concentration_test_executor = ConcentrationTestExecutor(calculated_df_map, "PSSL")
            concentration_test_df = concentration_test_executor.executeConentrationTest()
            self.calculator_info.intermediate_calculation_dict['Concentration Test'] = concentration_test_df
            print('calculation of sheet Portfolio is completed')
        except Exception as e:
            raise Exception(e)