function isDateValid(dateStr) {
	return !isNaN(new Date(dateStr));
}

export const fmtDisplayVal = (value) => {
	let temp = value;
	// console.log("value is number", typeof(value), value, isNaN(value));
	if (typeof (value) === 'number' || !isNaN(value)) {
		temp = parseFloat(value).toFixed(1).replace(/\d(?=(\d{3})+\.)/g, '$&,');
	} else if (isDateValid(value)) {
		temp = (new Date(value)).toLocaleDateString('en-US');
	}
	return temp;
};