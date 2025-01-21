export const filterDataByDateRange = (data, startDate, endDate) => {
	// Convert the start and end dates to Date objects for comparison
	const start = new Date(startDate);
	const end = new Date(endDate);

	// Filter the data array, including only entries within the date range
	return data.filter(item => {
		const itemDate = new Date(item.date);
		return itemDate >= start && itemDate <= end;
	});
};