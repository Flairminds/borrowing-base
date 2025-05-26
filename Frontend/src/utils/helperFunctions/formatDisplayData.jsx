export function isDateValid(dateStr) {
	const startsWithAlphabet = /^[a-zA-Z]/.test(dateStr);
	const isPercentage = /%{1}$/.test(dateStr);

	if (isPercentage) {
		return false;
	}

	if (startsWithAlphabet) {
		try {
			const startsWithDay = dateStr.startsWith("Mon") || dateStr.startsWith("Tue") || dateStr.startsWith("Wed") || dateStr.startsWith("Thu") || dateStr.startsWith("Fri") || dateStr.startsWith("Sat") || dateStr.startsWith("Sun");
			if (!startsWithDay) {
				return false;
			}
		} catch (error) {
			return false;
		}
	}
	return !isNaN(new Date(dateStr));
}

export const fmtDisplayVal = (value, decimals = 2) => {
	let temp = value;
	if (!temp) return temp;
	// console.log("value is number", typeof(value), value, isNaN(value));
	if (typeof (value) === 'number' || !isNaN(value)) {
		temp = parseFloat(value).toFixed(decimals).replace(/\d(?=(\d{3})+\.)/g, '$&,');
	} else if (isDateValid(value)) {
		const dt = new Date(value);
		const month = (dt.getMonth() + 1).toString().padStart(2, '0');
		const day = dt.getDate().toString().padStart(2, '0');
		const year = dt.getFullYear();
		temp = `${month}-${day}-${year}`;
		// temp = (new Date(value)).toLocaleDateString('en-US');
	} else if (typeof value === 'string' && value.endsWith('%')) {
		temp = parseFloat(value.replace('%', ''));
		temp = `${temp.toFixed(decimals)}%`;
	}
	return temp;
};

export const fmtDateValue = (value) => {
	const temp = value;
	if (!temp) return temp;
	if (typeof temp === 'number' || !isNaN(value)) {
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


export function formatCellValue(value) {
	if (value instanceof Date) return value;

	if (typeof value === 'string' && value.trim().endsWith('%')) {
		return value;
	}

	const num = parseFloat(value);
	if (isNaN(num)) return value;

	if (Math.abs(num) >= 1_000_000_000) {
		return (num / 1_000_000_000).toFixed(1).replace(/\.0$/, '') + 'B';
	} else if (Math.abs(num) >= 1_000_000) {
		return (num / 1_000_000).toFixed(1).replace(/\.0$/, '') + 'M';
	} else if (Math.abs(num) >= 1_000) {
		return (num / 1_000).toFixed(1).replace(/\.0$/, '') + 'K';
	} else {
		return num.toString();
	}
}
