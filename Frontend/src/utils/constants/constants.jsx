import dollarMoneyCurrencyIcon from '../../assets/sideBarIcons/dollarMoneyCurrencyIcon.svg';
import DoneCheckIcon from '../../assets/sideBarIcons/DoneCheckIcon.svg';
import GroupUserIcon from '../../assets/sideBarIcons/GroupUserIcon.svg';
import HomeIcon from '../../assets/sideBarIcons/HomeIcon.svg';
import projectDocumentsIcon from '../../assets/sideBarIcons/projectDocumentsIcon.svg';
import settingIcon from '../../assets/sideBarIcons/settingIcon.svg';
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
	{ value: 0, label: '-- Select Fund --' },
	{ value: 1, label: 'PCOF' },
	{ value: 2, label: 'PFLT' }
];

export const PAGE_ROUTES = {
	BASE_DATA_LIST: {
		url: '/data-ingestion/base-data',
		header: 'Extracted Base Data'
	},
	SOURCE_FILES: {
		url: '/data-ingestion/ingestion-files-list',
		header: 'Uploaded Source Files'
	}
};

export const sidebarItemsArray = [
	{ imgSrc: HomeIcon, imgAlt: "Home Icon", name: 'Home', route: '/' },
	{ imgSrc: ThreeBarIcon, imgAlt: "ThreeBar Icon", name: 'Concentration Test Setup', route: '/fund-setup' },
	{ imgSrc: projectDocumentsIcon, imgAlt: "projectDocuments Icon", name: 'Data Ingestion', route: PAGE_ROUTES.BASE_DATA_LIST.url },
	{ imgSrc: settingIcon, imgAlt: "Config Icon", name: 'Configuration', route: '/configuration' }
	// { imgSrc: DoneCheckIcon, imgAlt: "DoneCheck Icon" },
	// { imgSrc: suitcasePortfolioIcon, imgAlt: "suitcasePortfolio Icon" },
	// { imgSrc: GroupUserIcon, imgAlt: "GroupUser Icon" },
	// { imgSrc: dollarMoneyCurrencyIcon, imgAlt: "dollarMoneyCurrency Icon" }
];

// AddInfo Functionality
export const PFLTData = {
	other_sheet: {
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
				name: "master/feeder",
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
				type: "text",
				unit: "percent"
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
				type: "text",
				unit: "percent"
			},
			{
				name: "quoted",
				label: "Quoted",
				type: "text",
				unit: "percent"
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
				type: "text",
				unit: "percent"
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
				type: "text",
				unit: "percent"
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
				type: "text",
				unit: "percent"
			},
			{
				name: "concentration_test_threshold_1",
				label: "Concentration Test Threshold 1",
				type: "text",
				unit: "percent"
			},
			{
				name: "concentration_test_threshold_2",
				label: "Concentration Test Threshold 2",
				type: "text",
				unit: "percent"
			},
			{
				name: "threshold_1_advance_rate",
				label: "Threshold 1 Advance Rate",
				type: "text",
				unit: "percent"
			},
			{
				name: "threshold_2_advance_rate",
				label: "Threshold 2 Advance Rate",
				type: "text",
				unit: "percent"
			}
		]
	}
};

export const OTHER_INFO_OPTIONS = [
	{ label: 'Enter Data manually', value: 'add' },
	{ label: 'Upload file to extract', value: 'upload'}
];

export const cloWhatIfData = {
	'PFLT': {
		defaultSelectedColumns: [
			{
				"key": "Security_Name",
				"label": "Security Name"
			},
			{
				"key": "LoanX_ID",
				"label": "LoanX ID"
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

export const COLUMN_GROUPS = {
	unmapped: [
		{ key: "cashfile_securities", label: "Security/Facility Name" },
		{ key: "issuer_borrower_name", label: "Issuer/Borrower Name" },
		{ key: "facility_category_desc", label: "Facility Category Desc" }
	],
	all: [
		{ key: "soi_name", label: "SOI Name" },
		{ key: "master_comp_security_name", label: "Security Name" },
		{ key: "family_name", label: "Family Name" }

	]
};

export const PFLT_COLUMNS_NAME = {
	"input": {
		"columns_info": [
			{
				"col_name": "inputs",
				"sequence": 1,
				"display_name": "INPUTS"
			},
			{
				"col_name": "values",
				"sequence": 2,
				"display_name": "Values"
			}
		]
	},
	"other_sheet": {
		"columns_info": [
			{
				"col_name": "currency",
				"sequence": 1,
				"display_name": "Currency"
			},
			{
				"col_name": "exchange_rates",
				"sequence": 2,
				"display_name": "Exchange Rates"
			},
			{
				"col_name": "cash_current_and_preborrowing",
				"sequence": 3,
				"display_name": "Cash Current and PreBorrowing"
			},
			{
				"col_name": "borrowing",
				"sequence": 4,
				"display_name": "Borrowing"
			},
			{
				"col_name": "additional_expenses_1",
				"sequence": 5,
				"display_name": "Additional Expenses 1"
			},
			{
				"col_name": "additional_expenses_2",
				"sequence": 6,
				"display_name": "Additional Expenses 2"
			},
			{
				"col_name": "additional_expenses_3",
				"sequence": 7,
				"display_name": "Additional Expenses 3"
			},
			{
				"col_name": "current_credit_facility_balance",
				"sequence": 8,
				"display_name": "Current Credit Facility Balance"
			}
		]
	}
};

export const PCOF_COLUMNS_NAME = {
	"availability_borrower": {
		"columns_info": [
			{
				"col_name": "a",
				"sequence": 1,
				"display_name": "A"
			},
			{
				"col_name": "b",
				"sequence": 2,
				"display_name": "B"
			}
		]
	},
	"principle_obligations": {
		"columns_info": [
			{
				"col_name": "principal_obligations",
				"sequence": 1,
				"display_name": "Principal Obligations"
			},
			{
				"col_name": "currency",
				"sequence": 2,
				"display_name": "Currency"
			},
			{
				"col_name": "amount",
				"sequence": 3,
				"display_name": "Amount"
			},
			{
				"col_name": "spot_rate",
				"sequence": 4,
				"display_name": "Spot Rate"
			},
			{
				"col_name": "dollar_equivalent",
				"sequence": 5,
				"display_name": "Dollar Equivalent"
			}
		]
	},
	"subscription_bb": {
		"columns_info": [
			{
				"col_name": "investor",
				"sequence": 1,
				"display_name": "Investor"
			},
			{
				"col_name": "master/feeder",
				"sequence": 2,
				"display_name": "Master/Feeder"
			},
			{
				"col_name": "ultimate_investor_parent",
				"sequence": 3,
				"display_name": "Ultimate Investor Parent"
			},
			{
				"col_name": "designation",
				"sequence": 4,
				"display_name": "Designation"
			},
			{
				"col_name": "commitment",
				"sequence": 5,
				"display_name": "Commitment"
			},
			{
				"col_name": "capital_called",
				"sequence": 6,
				"display_name": "Capital Called"
			}
		]
	},
	"pricing": {
		"columns_info": [
			{
				"col_name": "pricing",
				"sequence": 1,
				"display_name": "Pricing"
			},
			{
				"col_name": "percent",
				"sequence": 2,
				"display_name": "percent"
			}
		]
	},
	"advance_rates": {
		"columns_info": [
			{
				"col_name": "investor_type",
				"sequence": 1,
				"display_name": "Investor Type"
			},
			{
				"col_name": "advance_rate",
				"sequence": 2,
				"display_name": "Advance Rate"
			}
		]
	},
	"portfolio_leverageborrowingbase": {
		"columns_info": [
			{
				"col_name": "investment_type",
				"sequence": 1,
				"display_name": "Investment Type"
			},
			{
				"col_name": "unquoted",
				"sequence": 2,
				"display_name": "Unquoted"
			},
			{
				"col_name": "quoted",
				"sequence": 3,
				"display_name": "Quoted"
			}
		]
	},
	"concentration_limits": {
		"columns_info": [
			{
				"col_name": "investors",
				"sequence": 1,
				"display_name": "Investors"
			},
			{
				"col_name": "rank",
				"sequence": 2,
				"display_name": "Rank"
			},
			{
				"col_name": "concentration_limit",
				"sequence": 3,
				"display_name": "Concentration Limit"
			}
		]
	},
	"other_metrics": {
		"columns_info": [
			{
				"col_name": "other_metrics",
				"sequence": 1,
				"display_name": "Other Metrics"
			},
			{
				"col_name": "values",
				"sequence": 2,
				"display_name": "values"
			}
		]
	}
};