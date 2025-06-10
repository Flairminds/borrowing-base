import { isDateValid } from "./formatDisplayData";

export const filterData = (data, key = null, order = null) => {

	if (!key || (order !== 'asc' && order !== 'desc')) {
		return data;
	}
	const sortedData = data.sort((a, b) => {
		let t1 = a[key];
		let t2 = b[key];
		if (a[key]['meta_info']) {
			t1 = a[key]['cellActualValue'];
		}
		if (b[key]['meta_info']) {
			t2 = b[key]['cellActualValue'];
		}
		if (order === 'asc') {
			if (isDateValid(t1) && isDateValid(t2)) {
				return new Date(t1) > new Date(t2) ? 1 : new Date(t1) < new Date(t2) ? -1 : 0;
			} else {
				return t1 > t2 ? 1 : t1 < t2 ? -1 : 0;
			}
		} else if (order === 'desc') {
			if (isDateValid(t1) && isDateValid(t2)) {
				return new Date(t1) < new Date(t2) ? 1 : new Date(t1) > new Date(t2) ? -1 : 0;
			} else {
				return t1 < t2 ? 1 : t1 > t2 ? -1 : 0;
			}
		}
	});

	return sortedData;
};