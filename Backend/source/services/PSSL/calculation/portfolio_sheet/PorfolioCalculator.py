from source.services.PSSL.calculation.portfolio_sheet.EbitdaNetAtDateInclussion import EbitdaNetAtDateInclussion
from source.services.PSSL.calculation.portfolio_sheet.EbitdaNetDebtRelevantTestPeriod import EbitdaNetDebtRelevantTestPeriod
from source.services.PSSL.calculation.portfolio_sheet.LeverageRatiosPermittedTtmEbitda import LeverageRatiosPermittedTtmEbitda
from source.services.PSSL.calculation.portfolio_sheet.RecurringRevenue import RecurringRevenueInterestCoverage
from source.services.PSSL.calculation.portfolio_sheet.ValueAdjustmentEvent import ValueAdjustmentEvent

class PortfolioCalculator:
    def __init__(self, calculator_info):
        self.calculator_info = calculator_info
        exchange_rates_df = calculator_info.intermediate_calculation_dict['Exchange Rates']
        exchange_rate_map = exchange_rates_df.set_index("Currency")["Exchange Rate"].to_dict()
        self.calculator_info.intermediate_calculation_dict['exchange_rate_map'] = exchange_rate_map

    def calculate_portfolio(self):
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
        print('calculation of sheet Portfolio is completed')