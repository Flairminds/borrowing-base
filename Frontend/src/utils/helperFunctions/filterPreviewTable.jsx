export const filterPreviewTable = (array, obligorValue, securityValue) => {
	if (!Array.isArray(array)) {
		console.error("Invalid data array");
		return [];
	}
	if (obligorValue.length === 0 && securityValue.length > 0) {
		const securityFilter = array.filter(item => securityValue.includes(item.security_name.display_value));
		return securityFilter;
	} else if (securityValue.length === 0 && obligorValue.length > 0) {
		const obligorFilter = array.filter(item => obligorValue.includes(item.obligor_name.display_value));
		return obligorFilter;
	} else if (obligorValue.length > 0 && securityValue.length > 0) {
		const combinedFilter = array.filter(item =>
			obligorValue.includes(item.obligor_name.display_value) &&
			securityValue.includes(item.security_name.display_value)
		);
		return combinedFilter;
	} else {
		return array;
	}
};
