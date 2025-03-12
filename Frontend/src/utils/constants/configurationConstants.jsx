import React from "react";
import { LoanTypeMapping } from "../../pages/configurationPageTabs/loanTypeMapping/LoanTypeMapping";

export const configurationTabs = [
	{
		key: "1",
		label: "Security Mapping",
		children: "Security Mapping UI"
	},
	{
		key: "2",
		label: "Loan Type Mapping",
		children: <LoanTypeMapping />
	},
	{
		key: "3",
		label: "Lien Type Mapping",
		children: "Lien Type UI"
	}
];

export const loanTypeConfig = {
	cardsData: [{
		key: 'all_loan_types',
		label: "All Loan Types"
	}, {
		key: 'unmapped_loan_types',
		label: "Unmapped Loan Types"
	}]
};

