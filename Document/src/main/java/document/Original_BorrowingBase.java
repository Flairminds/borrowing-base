package document;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.DateUtil;
import org.apache.poi.ss.usermodel.Row;

import com.fasterxml.jackson.databind.ObjectMapper;

public class Original_BorrowingBase {
	public static void main(String[] args) {
		String excelFilePath = "C:\\Users\\USER\\Downloads\\PFLT-Borrowing_Base_Report.xlsx";
		String sheetName = "Borrowing Base"; 

		try {
		String jsonData = readExcelAndConvertToJson(excelFilePath, sheetName);
		System.out.println(jsonData);
		} catch (IOException e) {
		e.printStackTrace();
		}
		}

		public static String readExcelAndConvertToJson(String excelFilePath, String sheetName) throws IOException {
		FileInputStream fis = new FileInputStream(excelFilePath);
		Workbook workbook = new XSSFWorkbook(fis);
		Sheet sheet = workbook.getSheet(sheetName);

		List<Map<String, Object>> sheetData = convertSheetToArray(sheet);

		ObjectMapper objectMapper = new ObjectMapper();
		String MainArray = objectMapper.writerWithDefaultPrettyPrinter().writeValueAsString(sheetData);

		workbook.close();
		fis.close();

		return MainArray; 
		}

		public static List<Map<String, Object>> convertSheetToArray(Sheet sheet) {
		List<Map<String, Object>> resultArray = new ArrayList<>();

		for (int i = 1; i <= sheet.getLastRowNum(); i++) {
		Row row = sheet.getRow(i);
		if (row != null) {
		Map<String, Object> rowMap = new HashMap<>();
		Cell termCell = row.getCell(0);
		Cell valueCell = row.getCell(1);

		rowMap.put("Terms", getCellValue(termCell));
		rowMap.put("Values", getCellValue(valueCell));

		resultArray.add(rowMap);
		}
		}

		return resultArray;
		}

		public static Object getCellValue(Cell cell) {
		if (cell == null) {
		return null;
		}
		switch (cell.getCellType()) {
		case STRING:
		return cell.getStringCellValue();
		case NUMERIC:
		if (DateUtil.isCellDateFormatted(cell)) {
		return cell.getDateCellValue();
		} else {
		return Math.round(cell.getNumericCellValue());
		}
		case BOOLEAN:
		return cell.getBooleanCellValue();
		case BLANK:
		return "";
		default:
		return cell.toString();
		}
		}
		
}
