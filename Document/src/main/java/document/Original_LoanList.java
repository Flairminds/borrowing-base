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

public class Original_LoanList {
	

public static void main(String[] args) {
String excelFilePath = "D:\\Users\\USER\\Documents\\Flairminds\\fileupload-Onpeper\\CompareFiles\\PLFT\\30-06\\onppeper main result_30-06.xlsx";
//String excelFilePath1 = "C:\\Users\\USER\\Downloads\\PFLT-Borrowing_Base_Report.xlsx";
String sheetName = "Loan List";
int comparecellvalue=97;

try {
String jsonData = readExcelAndConvertToJson(excelFilePath, sheetName, comparecellvalue);
System.out.println(jsonData);
} catch (IOException e) {
e.printStackTrace();
}
}

public static String readExcelAndConvertToJson(String excelFilePath, String sheetName,int comparecellvalue) throws IOException {
FileInputStream fis = new FileInputStream(excelFilePath);
Workbook workbook = new XSSFWorkbook(fis);
Sheet sheet = workbook.getSheet(sheetName);

List<Map<String, Object>> sheetData = convertSheetToArray(sheet,comparecellvalue);

ObjectMapper objectMapper = new ObjectMapper();
String mainArray = objectMapper.writerWithDefaultPrettyPrinter().writeValueAsString(sheetData);

workbook.close();
fis.close();

return mainArray;
}

public static List<Map<String, Object>> convertSheetToArray(Sheet sheet,int comparecellvalue) {
List<Map<String, Object>> resultArray = new ArrayList<>();

// Loop through rows starting from row 1 (assuming headers in row 0)
for (int i = 1; i <= sheet.getLastRowNum(); i++) {
Row row = sheet.getRow(i);
if (row != null) {
Map<String, Object> rowMap = new HashMap<>();

// Assuming "Obligor Name" is in the first column
Cell obligorCell = row.getCell(0);

// Assuming the correct numeric "Loan Number" is in a different column (adjust index as needed)
Cell loanNumberCell = row.getCell(comparecellvalue); // Assuming loan number is in the 3rd column

rowMap.put("Obligor Name", getCellValue(obligorCell));
rowMap.put("Term Value", getCellValue(loanNumberCell));

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
return Math.round(cell.getNumericCellValue()); // Round numeric values if needed
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
