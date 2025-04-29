import * as XLSX from "xlsx";
import { isDateValid } from "./formatDisplayData";

export const exportToExcel = (data, columns = [], fileName = "data.xlsx") => {
	console.info("Entered", data);
	const cleanedData = data.map(row => {
		return Object.fromEntries(
			Object.entries(row).map(([key, value]) => [key, value === null || value === undefined || value === "NaN" || Number.isNaN(value) ? "" : value])
		);
	});
	const worksheet = XLSX.utils.json_to_sheet(cleanedData);
	function columnNumberToLetter(colNum) {
		let letter = '';
		while (colNum >= 0) {
			letter = String.fromCharCode((colNum % 26) + 65) + letter;
			colNum = Math.floor(colNum / 26) - 1;
		}
		return letter;
	}

	if (columns.length > 0) {
		columns.forEach((col, colIndex) => {
			if (col.unit === 'percent') {
				for (let rowIndex = 2; rowIndex <= data.length + 1; rowIndex++) {
					worksheet[`${columnNumberToLetter(colIndex)}${rowIndex}`].z = "0.00%";
				// Skip header row (start at 2)
					// const cellRef = XLSX.utils.encode_cell({ r: rowIndex - 1, c: colIndex }); // 0-based index
					// if (worksheet[cellRef]) {
					// 	worksheet[cellRef].z = "0.00%";
					// }
				}
			}
			if (col.unit === 'date') {
				for (let rowIndex = 2; rowIndex <= data.length + 1; rowIndex++) {
					if (!worksheet[`${columnNumberToLetter(colIndex)}${rowIndex}`].v || !isDateValid(worksheet[`${columnNumberToLetter(colIndex)}${rowIndex}`].v)) {
						worksheet[`${columnNumberToLetter(colIndex)}${rowIndex}`].v = "";
						worksheet[`${columnNumberToLetter(colIndex)}${rowIndex}`].t = "s"; // type 'd' for date
					} else {
						worksheet[`${columnNumberToLetter(colIndex)}${rowIndex}`].t = "d"; // type 'd' for date
					}
					worksheet[`${columnNumberToLetter(colIndex)}${rowIndex}`].z = "mm/dd/yyyy"; // or your desired format
				}
			}
		});
	}

	const workbook = XLSX.utils.book_new();
	XLSX.utils.book_append_sheet(workbook, worksheet, "Sheet1");
	XLSX.writeFile(workbook, fileName);
	// const excelBuffer = XLSX.write(workbook, { bookType: "xlsx", type: "array" });
	// const blob = new Blob([excelBuffer], { type: "application/octet-stream" });
	// saveAs(blob, fileName);
};
