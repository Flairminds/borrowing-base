
export const filterPreviewData = (array, key) => {
	const uniqueValues = new Set();

	array.forEach(item => {
		if (item.hasOwnProperty(key) && item[key].hasOwnProperty('display_value')) {
			uniqueValues.add(item[key].display_value);
		}
	});

	const resultArray = Array.from(uniqueValues).map(value => ({
		label: value,
		value: value
	}));

	return resultArray;
};


