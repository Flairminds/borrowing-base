import { saveAs } from "file-saver";
import * as XLSX from "xlsx";

export const exportToExcel = (data, fileName = "data.xlsx") => {
	console.info("Entered", data);
	const cleanedData = data.map(row => {
		return Object.fromEntries(
			Object.entries(row).map(([key, value]) => [key, value === null || value === undefined || value === "NaN" || Number.isNaN(value) ? "" : value])
		);
	});

	const worksheet = XLSX.utils.json_to_sheet(cleanedData);
	const workbook = XLSX.utils.book_new();
	XLSX.utils.book_append_sheet(workbook, worksheet, "Sheet1");
	const excelBuffer = XLSX.write(workbook, { bookType: "xlsx", type: "array" });
	const blob = new Blob([excelBuffer], { type: "application/octet-stream" });
	saveAs(blob, fileName);
};
