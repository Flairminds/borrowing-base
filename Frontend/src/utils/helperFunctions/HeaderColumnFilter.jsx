export const filterData = (data, key = null, order = null) => {

	if (!key || (order !== 'asc' && order !== 'desc')) {
		return data;
	}
	const sortedData = data.sort((a, b) => {
		if (order === 'asc') {
			return a[key] > b[key] ? 1 : a[key] < b[key] ? -1 : 0;
		} else if (order === 'desc') {
			return a[key] < b[key] ? 1 : a[key] > b[key] ? -1 : 0;
		}
	});

	return sortedData;
};