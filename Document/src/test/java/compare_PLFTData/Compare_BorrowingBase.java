package compare_PLFTData;

import java.io.IOException;
import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

import document.Original_BorrowingBase;

public class Compare_BorrowingBase {
	public static void main(String[] args) {
        String originalExcelFilePath = "D:\\Users\\USER\\Documents\\Flairminds\\fileupload-Onpeper\\CompareFiles\\PLFT\\30-06\\onppeper main result_30-06.xlsx";
        String sheetName = "Borrowing Base";
        String exportedExcelFilePath = "D:\\Users\\USER\\Downloads\\PFLT-Borrowing_Base_Report.xlsx";
        String sheetName1 = "Borrowing Base"; 
        String mainData = null; 
        String actualData = null;

        try {
             mainData = Original_BorrowingBase.readExcelAndConvertToJson(originalExcelFilePath, sheetName);
        } catch (IOException e) {
            e.printStackTrace();
        }
        
        try {
             actualData = Original_BorrowingBase.readExcelAndConvertToJson(exportedExcelFilePath, sheetName1);
        } catch (IOException e) {
            e.printStackTrace();
        }
        
        
        try {
        	ObjectMapper objectMapper = new ObjectMapper();

        	List<Map<String, Object>> mainDataList = objectMapper.readValue(mainData, new TypeReference<List<Map<String, Object>>>() {});
        	List<Map<String, Object>> actualDataList = objectMapper.readValue(actualData, new TypeReference<List<Map<String, Object>>>() {});

        	boolean allPassed = true;

        	for (int i = 0; i < mainDataList.size(); i++) {
        	Map<String, Object> mainDataEntry = mainDataList.get(i);
        	Map<String, Object> actualDataEntry = actualDataList.get(i);

        	String term = (String) mainDataEntry.get("Terms");
        	Object mainValue = mainDataEntry.get("Values");
        	Object actualValue = actualDataEntry.get("Values");

        	if (!mainValue.equals(actualValue)) {
        	System.out.println("Failed: " + term + " - Expected: " + mainValue + ", Actual: " + actualValue);
        	allPassed = false;
        	}
        	}

        	if (allPassed) {
        	System.out.println("All are passed.");
        	}

        	} catch (Exception e) {
        	e.printStackTrace();
        	}
        
        
        
    }


}
