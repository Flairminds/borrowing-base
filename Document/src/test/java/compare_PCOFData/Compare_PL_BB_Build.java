package compare_PCOFData;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

import document.Exported_PL_BB_Build;
import document.Original_PL_BB_Build;
import document.TestValue;

public class Compare_PL_BB_Build {
	public static void main(String[] args) {
		String originalExcelFilePath = "D:\\Users\\USER\\Documents\\Flairminds\\fileupload-Onpeper\\CompareFiles\\PCOF\\04_30\\PCOF_mainresult_04_30.xlsx";
		String sheetName = "PL BB Build";
		String exportedExcelFilePath = "D:\\Users\\USER\\Documents\\Flairminds\\fileupload-Onpeper\\CompareFiles\\PCOF\\04_30\\PCOF-Borrowing_Base_Report.xlsx";
		String sheetName1 = "df_PL_BB_Build";
		String mainData = null;
		String actualData = null;
		List<TestValue> testValues = new ArrayList<>();

		/*testValues.add(new TestValue("Eligible Issuers", 2, 100));
		testValues.add(new TestValue("Eligible", 6, 82));
		testValues.add(new TestValue("Tenor", 12, 54));
		testValues.add(new TestValue("Investment FMV", 17, 50));
		testValues.add(new TestValue("Classification for BB", 30, 66));
		testValues.add(new TestValue("Classification Eligible", 44, 44));
		testValues.add(new TestValue("Test 1 EBITDA Threshold", 58, 45));
		testValues.add(new TestValue("Test 1 Test Applies?", 59, 56));
		testValues.add(new TestValue("Test 1 Leverage < 4.5x", 60, 46));
		testValues.add(new TestValue("Test 1 LTV < 65%", 61, 47));
		testValues.add(new TestValue("Test 1 Pass", 62, 48));
		testValues.add(new TestValue("Classification Adj. Adjusted Type", 65, 68));		
		testValues.add(new TestValue("Final Eligible", 69, 49));
		testValues.add(new TestValue("Eligible Issuer", 71, 57));
		testValues.add(new TestValue("Eligible Industry", 72, 58));
		testValues.add(new TestValue("Portfolio Type", 73, 69));
		testValues.add(new TestValue("Portfolio Eligible Amount", 74, 51));
		testValues.add(new TestValue("Weighted LTM EBITDA", 78, 53));
		testValues.add(new TestValue("Weighted Maturity", 79, 55));
		testValues.add(new TestValue("Concentration Adj. Elig. Amount", 87, 59));
		testValues.add(new TestValue("First Lien Contribution", 100, 86));
		*/
	
		
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
				mainData = Original_PL_BB_Build.readExcelAndConvertToJson(originalExcelFilePath, sheetName,
						MainColumnNumber);
			} catch (IOException e) {
				e.printStackTrace();
			}
			
			try {
				actualData = Exported_PL_BB_Build.readExcelAndConvertToJson(exportedExcelFilePath, sheetName1,
						actualColumnNumber);	
			;

			} catch (IOException e) {
				e.printStackTrace();
			}
			
			System.out.println(actualData);
			
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

	                Object mainObligorName = mainEntry.get("Investment Name");
	                Object actualObligorName = actualEntry.get("Investment Name");

	                // Convert null values to 0 for comparison
	                if (mainTermValue == null || "-".equals(mainTermValue)) {
	                    mainTermValue = 0;
	                }
	                if (actualTermValue == null || "-".equals(actualTermValue)) {
	                    actualTermValue = 0;
	                }

	                if (!mainTermValue.equals(actualTermValue) || !mainObligorName.equals(actualObligorName)) {
						System.out.println(columnName + " column is Mismatch at row " + i + ": Obligor Name=" + mainObligorName+ " Expected: Value=" + mainTermValue + ", Actual: Value=" + actualTermValue);
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

