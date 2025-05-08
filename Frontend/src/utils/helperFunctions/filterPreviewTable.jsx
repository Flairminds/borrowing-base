export const filterPreviewTable = (array, col1Value = [], col2Value = [], fundType) => {
	if (!Array.isArray(array)) {
		console.error("Invalid data array");
		return [];
	}

	let cols = ['obligor_name', 'security_name'];
	switch (fundType) {
	case 'PFLT': cols = ['obligor_name', 'security_name']; break;
	case 'PCOF': cols = ['investment_name', 'issuer']; break;
	case 'PSSL': cols = ['borrower']; break;
	default: break;
	}

	return array.filter(item => {
		const col1 = item[cols[0]]?.display_value;
		const col1Match = col1Value.length === 0 || col1Value.includes(col1);

		if (cols.length > 1) {
			const col2 = item[cols[1]]?.display_value;
			const col2Match = col2Value.length === 0 || col2Value.includes(col2);
			return col1Match && col2Match;
		}
		return col1Match;
	});
};
