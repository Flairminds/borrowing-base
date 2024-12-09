package compare_PCOFData;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

import document.Exported_PL_BB_Build_percent;
import document.OriginalPL_BB_build_Percent;
import document.TestValue;

public class Compare_PL_BB_Build_Percent {
	
	public static void main(String[] args) {
		String originalExcelFilePath = "D:\\Users\\USER\\Documents\\Flairminds\\fileupload-Onpeper\\CompareFiles\\PCOF\\10-31\\Main Result 10-31.xlsx";
		String sheetName = "PL BB Build";
		String exportedExcelFilePath = "D:\\Users\\USER\\Documents\\Flairminds\\fileupload-Onpeper\\CompareFiles\\PCOF\\10-31\\PCOF-Borrowing_Base_Report (4).xlsx";
		String sheetName1 = "df_PL_BB_Build";
		String mainData = null;
		String actualData = null;
		List<TestValue> testValues = new ArrayList<>();
			
		testValues.add(new TestValue("Investment FMV/Par", 18, 81));
		testValues.add(new TestValue("Investment FMV/cost", 19, 80));
		testValues.add(new TestValue("Investment % of FMV", 20, 79));
		testValues.add(new TestValue("All-In (Cash)", 26, 78));
		testValues.add(new TestValue("All-In", 27, 77));
		testValues.add(new TestValue("Leverage Revolver percent of TEV", 51, 71));
		testValues.add(new TestValue("Eligible % FMV Eligible (excluding cash)", 76, 52));
		testValues.add(new TestValue("Weighted Percent Fixed", 80, 60));
		testValues.add(new TestValue("Weighted Fixed", 81, 61));
		testValues.add(new TestValue("Weighted Percent Floating", 82, 62));
		testValues.add(new TestValue("Weighted Percent Floating", 83, 63));
		testValues.add(new TestValue("Concentration % Adj. Elig. Amount (excluding cash)",88,64));
		testValues.add(new TestValue("Concentration % of ONC", 89, 65));
		testValues.add(new TestValue("Concentration Issuer % of ONC", 90, 87));
		testValues.add(new TestValue("Adv. Adv. Rate", 92, 70));
		testValues.add(new TestValue("Revolver Rev. > 15% TEV", 94, 72));
		testValues.add(new TestValue("Revolver Adj. Advance Rate", 95,73));
		testValues.add(new TestValue("First Lien Second Lien Share", 97, 74));
		testValues.add(new TestValue("First Lien Second Lien Rate", 98, 75));
		testValues.add(new TestValue("First Lien Adj. Advance Rate", 99, 85));
		
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
				mainData = OriginalPL_BB_build_Percent.readExcelAndConvertToJson(originalExcelFilePath, sheetName,
						MainColumnNumber);
			} catch (IOException e) {
				e.printStackTrace();
			}
			
			try {
				actualData = Exported_PL_BB_Build_percent.readExcelAndConvertToJson(exportedExcelFilePath, sheetName1,
						actualColumnNumber);	
			;

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

	                Object mainObligorName = mainEntry.get("Investment Name");
	                Object actualObligorName = actualEntry.get("Investment Name");

	                // Convert null values to 0 for comparison
	                if (mainTermValue == null || "-".equals(mainTermValue) || "N/A".equals(mainTermValue) || "n/a".equals(mainTermValue) || "No".equals(mainTermValue)) {
	                    mainTermValue = 0;
	                }
	                if (actualTermValue == null || "-".equals(actualTermValue) || "N/A".equals(actualTermValue) || "n/a".equals(actualTermValue) || "No".equals(mainTermValue)) {
	                    actualTermValue = 0;
	                }
	                
	                double mainTermValueNumeric = Double.parseDouble(mainTermValue.toString());
	                double actualTermValueNumeric = Double.parseDouble(actualTermValue.toString());

	                if (mainTermValueNumeric != actualTermValueNumeric || !mainObligorName.equals(actualObligorName)) {
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
