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
};

export const PCOFData = {
	Header: [
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
			name: "commitment_period",
			label: "Commitment Period",
			type: "text"
		},
		{
			name: "facility_size",
			label: "Facility Size",
			type: "text"
		},
		{
			name: "loans_usd",
			label: "Loans (USD)",
			type: "text"
		},
		{
			name: "loans_cad",
			label: "Loans (CAD)",
			type: "text"
		}
	],
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
		// {
		// 	name: "dollar_equivalent",
		// 	label: "Dollar Equivalent",
		// 	type: "text"
		// }
	]
};

export const OTHER_INFO_OPTIONS = [
	{ label: 'Enter Data', value: 'add' },
	{ label: 'Upload File', value: 'upload'}
];