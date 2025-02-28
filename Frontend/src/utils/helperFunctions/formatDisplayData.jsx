function isDateValid(dateStr) {
	return !isNaN(new Date(dateStr));
}

export const fmtDisplayVal = (value, decimals = 1) => {
	let temp = value;
	if (!temp) return temp;
	// console.log("value is number", typeof(value), value, isNaN(value));
	if (typeof (value) === 'number' || !isNaN(value)) {
		temp = parseFloat(value).toFixed(decimals).replace(/\d(?=(\d{3})+\.)/g, '$&,');
	} else if (isDateValid(value)) {
		temp = (new Date(value)).toLocaleDateString('en-US');
	}
	return temp;
};