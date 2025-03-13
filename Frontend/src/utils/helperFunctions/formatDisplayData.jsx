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

export const fmtDateValue = (value) => {
	const temp = value;
	if (!temp) return temp;

	if (typeof temp === 'number') {
		return value;
	}

	if (/[a-zA-Z]/.test(temp) && /\d/.test(temp)) {
		const isoDatePattern = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?Z$/;
		if (!isoDatePattern.test(temp)) {
			return temp;
		}
	}

	if (isDateValid(temp) || !isNaN(Date.parse(temp))) {
		return new Date(temp).toLocaleDateString('en-US');
	}

	return temp;
};

export const formatColumnName = (name) => {
	return name.replace(/_/g, ' ').replace(/\b\w/g, (char) => char.toUpperCase());
};