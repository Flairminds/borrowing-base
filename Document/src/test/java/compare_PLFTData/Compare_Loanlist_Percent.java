package compare_PLFTData;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

import document.Original_Loanlist_percent;
import document.TestValue;

public class Compare_Loanlist_Percent {
	public static void main(String[] args) {
		String originalExcelFilePath = "D:\\Users\\USER\\Documents\\Flairminds\\fileupload-Onpeper\\CompareFiles\\PLFT\\30-06\\onppeper main result_30-06.xlsx";
		String sheetName = "Loan List";
		String exportedExcelFilePath = "D:\\Users\\USER\\Downloads\\PFLT-Borrowing_Base_Report.xlsx";
		String sheetName1 = "Loan List";
		String mainData = null;
		String actualData = null;
		List<TestValue> testValues = new ArrayList<>();

		testValues.add(new TestValue("Advance Rate", 21, 78));
		testValues.add(new TestValue("Applicable Recovery Rate", 20, 104));
		testValues.add(new TestValue("Greater of Base Rate and Floor", 49,121));

		Object[][] testValuesArray = new Object[testValues.size()][3];

		for (int i = 0; i < testValues.size(); i++) {
			testValuesArray[i][0] = testValues.get(i).getColumnName(); 
			testValuesArray[i][1] = testValues.get(i).getActualColumnNumber();
			testValuesArray[i][2] = testValues.get(i).getMainColumnNumber();
		}
		for (Object[] testValue : testValuesArray) {
			String columnName = (String) testValue[0];
			int actualColumnNumber = (int) testValue[1];
			int MainColumnNumber = (int) testValue[2];
			try {
				mainData = Original_Loanlist_percent.readExcelAndConvertToJson(originalExcelFilePath, sheetName,MainColumnNumber);

			} catch (IOException e) {
				e.printStackTrace();
			}

			try {
				actualData = Original_Loanlist_percent.readExcelAndConvertToJson(exportedExcelFilePath, sheetName1,
						actualColumnNumber);

			} catch (IOException e) {
				e.printStackTrace();
			}
			
			try {
				ObjectMapper objectMapper = new ObjectMapper();

				List<Map<String, Object>> mainDataList = objectMapper.readValue(mainData,
						new TypeReference<List<Map<String, Object>>>() {
						});
				List<Map<String, Object>> actualDataList = objectMapper.readValue(actualData,
						new TypeReference<List<Map<String, Object>>>() {
						});

				if (mainDataList.size() != actualDataList.size()) {
					System.out.println("Data lists are of different sizes.");
					return;
				}

				boolean allPassed = true;

				for (int i = 0; i < mainDataList.size(); i++) {
					Map<String, Object> mainEntry = mainDataList.get(i);
					Map<String, Object> actualEntry = actualDataList.get(i);

					Object mainTermValue = mainEntry.get("Term Value");
					Object actualTermValue = actualEntry.get("Term Value");

					Object mainObligorName = mainEntry.get("Obligor Name");
					Object actualObligorName = actualEntry.get("Obligor Name");
					
					boolean termValuesMatch = (mainTermValue != null && mainTermValue.equals(actualTermValue)) || 
	                          (mainTermValue == null && actualTermValue == null);

	boolean obligorNamesMatch = (mainObligorName != null && mainObligorName.equals(actualObligorName)) || 
	                            (mainObligorName == null && actualObligorName == null);

					/*if (!mainTermValue.equals(actualTermValue) || !mainObligorName.equals(actualObligorName)) {
						System.out.println(columnName + " column is Mismatch at row " + i + ": Obligor Name=" + mainObligorName+ " Expected: Value=" + mainTermValue + ", Actual: Value=" + actualTermValue);
						allPassed = false;
					}*/
	if (!termValuesMatch || !obligorNamesMatch) {
	    System.out.println(columnName + " column is Mismatch at row " + i + ": Obligor Name=" + mainObligorName + 
	        " Expected: Value=" + mainTermValue + ", Actual: Value=" + actualTermValue);
	    allPassed = false;
	}
	
				}

				if (allPassed) {
					System.out.println("All data matches for " + columnName + " column");
				}

			} catch (Exception e) {
				e.printStackTrace();
			}

		}

	}
}
