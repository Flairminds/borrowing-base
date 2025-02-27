import dollarMoneyCurrencyIcon from '../../assets/sideBarIcons/dollarMoneyCurrencyIcon.svg';
import DoneCheckIcon from '../../assets/sideBarIcons/DoneCheckIcon.svg';
import GroupUserIcon from '../../assets/sideBarIcons/GroupUserIcon.svg';
import HomeIcon from '../../assets/sideBarIcons/HomeIcon.svg';
import projectDocumentsIcon from '../../assets/sideBarIcons/projectDocumentsIcon.svg';
import suitcasePortfolioIcon from '../../assets/sideBarIcons/suitcasePortfolioIcon.svg';
import ThreeBarIcon from '../../assets/sideBarIcons/ThreeBarIcon.svg';

export const updateAssetDefaultColumnsData = {
	'PL BB Build': 'Investment_Name',
	'Other Metrics': 'Other_Metrics',
	'Availability Borrower': 'A',
	'PL BB Results': 'Concentration_Tests',
	'Subscription BB': 'Investor',
	'PL_BB_Results_Security': 'Security',
	'Inputs ': 'Industries',
	'Pricing': 'Pricing',
	'Portfolio LeverageBorrowingBase': 'Investment_Type',
	'Obligors Net Capital': 'Obligors_Net_Capital',
	'Advance Rates': 'Investor_Type',
	'Concentration Limits': 'Investors',
	'Principle Obligations': 'Principal_Obligations',
	'Loan List': 'Security_Name',
	'Inputs': 'INPUTS',
	'Cash Balance Projections': 'Currency',
	'Credit Balance Projection': 'Currency'

};

export const updateAssetModalData = (fundType) => {
	return fundType === 'PCOF' ? 'PL BB Build' : 'Loan List';
};

export const fundOptionsArray = [
	{ value: 0, label: 'Select Fund' },
	{ value: 1, label: 'PCOF' },
	{ value: 2, label: 'PFLT' }
];

export const sidebarItemsArray = [
	{ imgSrc: HomeIcon, imgAlt: "Home Icon", name: 'Home', route: '/' },
	{ imgSrc: ThreeBarIcon, imgAlt: "ThreeBar Icon", name: 'Concentration Test Setup', route: '/fund-setup' },
	{ imgSrc: projectDocumentsIcon, imgAlt: "projectDocuments Icon", name: 'Data Ingestion', route: '/base-data-list' },
	{ imgSrc: DoneCheckIcon, imgAlt: "DoneCheck Icon" },
	{ imgSrc: suitcasePortfolioIcon, imgAlt: "suitcasePortfolio Icon" },
	{ imgSrc: GroupUserIcon, imgAlt: "GroupUser Icon" },
	{ imgSrc: dollarMoneyCurrencyIcon, imgAlt: "dollarMoneyCurrency Icon" }
];

// AddInfo Functionality
export const PFLTData = {
	input: {
		Header: [
			{
				name: "determination_date",
				label: "Determination Date",
				type: "datePicker"
			},
			{
				name: "minimum_equity_amount_floor",
				label: "Minimum Equity Amount Floor",
				type: "text"
			}
		],
		Column: [
			{
				name: "currency",
				label: "Currency",
				type: "text"
			},
			{
				name: "borrowing",
				label: "Borrowing",
				type: "text"
			},
			{
				name: "exchange_rates",
				label: "Exchange Rate",
				type: "text"
			},
			{
				name: "current_credit_facility_balance",
				label: "Credit Facility Balance",
				type: "text"
			},
			{
				name: "cash_current_and_preborrowing",
				label: "Cash Current And Preborrowing",
				type: "text"
			},
			{
				name: "additional_expenses_1",
				label: "Additional Expenses 1",
				type: "text"
			},
			{
				name: "additional_expenses_2",
				label: "Additional Expenses 2",
				type: "text"
			},
			{
				name: "additional_expenses_3",
				label: "Additional Expenses 3",
				type: "text"
			}
		]
	}
};

export const PCOFData = {
	availability_borrower: {
		Header: [
			{
				name: "borrower",
				label: "Borrower",
				type: "text"
			},
			{
				name: "determination_date",
				label: "Determination Date",
				type: "datePicker"
			},
			{
				name: "revolving_closing_date",
				label: "Revolving Closing Date",
				type: "datePicker"
			},
			{
				name: "commitment_period_(3_years_from_final_closing_date,_as_defined_in_lpa)",
				label: "Commitment Period",
				type: "text"
			},
			{
				name: "(b)_facility_size",
				label: "Facility Size",
				type: "text"
			},
			{
				name: "loans_(usd)",
				label: "Loans (USD)",
				type: "text"
			},
			{
				name: "loans_(cad)",
				label: "Loans (CAD)",
				type: "text"
			}
		]
	},
	principle_obligations: {
		Column: [
			{
				name: "principal_obligations",
				label: "Principal Obligations",
				type: "text"
			},
			{
				name: "currency",
				label: "Currency",
				type: "text"
			},
			{
				name: "amount",
				label: "Amount",
				type: "text"
			},
			{
				name: "spot_rate",
				label: "Spot Rate",
				type: "text"
			}
		]
	},
	subscription_bb: {
		Column: [
			{
				name: "investor",
				label: "Investor",
				type: "text"
			},
			{
				name: "master_or_feeder",
				label: "Master/Feeder",
				type: "text"
			},
			{
				name: "ultimate_investor_parent",
				label: "Ultimate Investor Parent",
				type: "text"
			},
			{
				name: "designation",
				label: "Designation",
				type: "text"
			},
			{
				name: "commitment",
				label: "Commitment",
				type: "text"
			},
			{
				name: "capital_called",
				label: "Capital Called",
				type: "text"
			}
		]
	},
	pricing: {
		Column: [
			{
				name: "pricing",
				label: "Pricing",
				type: "text"
			},
			{
				name: "percent",
				label: "Percent",
				type: "text"
			}
		]
	},
	portfolio_leverageborrowingbase: {
		Column: [
			{
				name: "investment_type",
				label: "Investment Type",
				type: "text"
			},
			{
				name: "unquoted",
				label: "Unquoted",
				type: "text"
			},
			{
				name: "quoted",
				label: "Quoted",
				type: "text"
			}
		]
	},
	advance_rates: {
		Column: [
			{
				name: "investor_type",
				label: "Investor Type",
				type: "text"
			},
			{
				name: "advance_rate",
				label: "Advance Rate",
				type: "text"
			}
		]
	},
	concentration_limits: {
		Column: [
			{
				name: "investors",
				label: "Investors",
				type: "text"
			},
			{
				name: "rank",
				label: "Rank",
				type: "text"
			},
			{
				name: "concentration_limit",
				label: "Concentration Limit",
				type: "text"
			}
		]
	},
	other_metrics: {
		Header: [
			{
				name: "first_lien_leverage_cut-off_point",
				label: "First Lien Leverage Cut-Off Point",
				type: "text"
			},
			{
				name: "warehouse_first_lien_leverage_cut-off",
				label: "Warehouse First Lien Leverage Cut-Off",
				type: "text"
			},
			{
				name: "last_out_attachment_point",
				label: "Last Out Attachment Point",
				type: "text"
			},
			{
				name: "trailing_12-month_ebitda",
				label: "Trailing 12-Month EBITDA",
				type: "text"
			},
			{
				name: "trailing_24-month_ebitda",
				label: "Trailing 24-Month EBITDA",
				type: "text"
			},
			{
				name: "total_leverage",
				label: "Total Leverage",
				type: "text"
			},
			{
				name: "ltv",
				label: "LTV",
				type: "text"
			},
			{
				name: "concentration_test_threshold_1",
				label: "Concentration Test Threshold 1",
				type: "text"
			},
			{
				name: "concentration_test_threshold_2",
				label: "Concentration Test Threshold 2",
				type: "text"
			},
			{
				name: "threshold_1_advance_rate",
				label: "Threshold 1 Advance Rate",
				type: "text"
			},
			{
				name: "threshold_2_advance_rate",
				label: "Threshold 2 Advance Rate",
				type: "text"
			}
		]
	}
};

export const OTHER_INFO_OPTIONS = [
	{ label: 'Enter Data', value: 'add' },
	{ label: 'Upload File', value: 'upload'}
];

export const cloWhatIfData = {
	'PFLT': {
		defaultSelectedColumns: [
			{
				"key": "Security_Name",
				"label": "Security Name"
			},
			{
				"key": "Obligor_Name",
				"label": "Obligor Name"
			},
			{
				"key": "Total_Commitment_(Issue_Currency)",
				"label": "Total Commitment (Issue Currency)"
			},
			{
				"key": "Outstanding_Principal_Balance_(Issue_Currency)",
				"label": "Outstanding Principal Balance (Issue Currency)"
			}
		],
		additionalInputColumns: [
			{
				"key": "Total Commitment (Issue Currency) CLO",
				"label": "Total Commitment (Issue Currency) CLO",
				"initialValue": "0"
			},
			{
				"key": "Outstanding Principal Balance (Issue Currency) CLO",
				"label": "Outstanding Principal Balance (Issue Currency) CLO",
				"initialValue": "0"
			}
		],
		matchingColumns: [
			{
				"key": "Security_Name",
				"label": "Security Name"
			},
			{
				"key": "Obligor_Name",
				"label": "Obligor Name"
			}
		]
	},
	'PCOF': {
		defaultSelectedColumns: [
			{
				"key": "Investment_Name",
				"label": "Investment Name"
			},
			{
				"key": "Issuer",
				"label": "Issuer"
			},
			{
				"key": "Investment_Par",
				"label": "Investment Par"
			}
		],
		additionalInputColumns: [
			{
				"key": "Investment Par CLO",
				"label": "Investment Par CLO",
				"initialValue": "0"
			}
		],
		matchingColumns: [
			{
				"key": "Investment_Name",
				"label": "Investment Name"
			},
			{
				"key": "Issuer",
				"label": "Issuer"
			}
		]}
};