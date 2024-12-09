package compare_PLFTData;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

import document.Original_LoanList;
import document.TestValue;

public class Compare_LoanListData {
	public static void main(String[] args) {
		String originalExcelFilePath = "D:\\Users\\USER\\Documents\\Flairminds\\fileupload-Onpeper\\CompareFiles\\PLFT\\30-06\\onppeper main result_30-06.xlsx";
		String sheetName = "Loan List";
		String exportedExcelFilePath = "D:\\Users\\USER\\Downloads\\PFLT-Borrowing_Base_Report.xlsx";
		String sheetName1 = "Loan List";
		String mainData = null;
		String actualData = null;
		List<TestValue> testValues = new ArrayList<>();

		//testValues.add(new TestValue("Advance Rate", 21, 78));
	testValues.add(new TestValue("Loan Number", 1, 74));
	/*testValues.add(new TestValue("Obligor", 2, 59));
	testValues.add(new TestValue("Exchange Rate", 8, 95));
		testValues.add(new TestValue("Total commintment USD", 9, 97));
		testValues.add(new TestValue("Outstanding Principal Balance	(USD)", 10, 99));
		testValues.add(new TestValue("Eligible Commitment (USD)", 11, 98));
		testValues.add(new TestValue("Eligible Outstanding Principal Balance (USD)", 12, 100));
		testValues.add(new TestValue("Discount Collateral Loan (Y/N)", 18, 94));
		testValues.add(new TestValue("Applicable Recovery Rate", 20, 104));
		testValues.add(new TestValue("Advance Rate", 21, 78));
		testValues.add(new TestValue("Aggregate Collateral Balance (Pre-Eligibility; Excluding Unfunded; Excluding Principal Acct)", 22, 110));
		testValues.add(new TestValue("Tier 1 / Tier 2 Obligor", 39, 77));
		testValues.add(new TestValue("Rem. Term to Maturity", 41, 85));
		testValues.add(new TestValue("Avg Life", 42, 123));
		testValues.add(new TestValue("Greater of Base Rate and Floor", 49,121));
		testValues.add(new TestValue("Partial PIK Loan (Y/N)", 60, 79));
		 testValues.add(new TestValue("Non-Cash PIK Loan (Y/N)",61, 80));
		 testValues.add(new TestValue("Aggregate Funded Spread", 79, 122));
		 testValues.add(new TestValue("Aggregate Unfunded Spread",80,120 ));
		 testValues.add(new TestValue("Aggregate Collateral Balance (Post Eligibility; Including Haircut Ineligible; Excluding Unfunded)", 108, 124));
		 testValues.add(new TestValue("Eligible Unfunded", 109, 125));
		testValues.add(new TestValue("Aggregate Collateral Balance (Post Eligibility; Including Eligible Unfunded)", 110, 126));
		 testValues.add(new TestValue("Concentration Test Balance - OPB + Eligible Unfunded", 111, 127));
		 testValues.add(new TestValue("Revolving Exposure", 112, 128));
		testValues.add(new TestValue("Foreign Currency Loan OC Balance",113, 225));
		 testValues.add(new TestValue("Foreign Currency Variability Factor",114, 73));
		 testValues.add(new TestValue("Foreign Currency Variability Reserve",115, 226));
		testValues.add(new TestValue("Second Lien and Split Lien", 117, 129));
		 testValues.add(new TestValue("Second Lien and Split Lien Net Loan Balance", 119, 131));
		 testValues.add(new TestValue("Second Lien", 120, 132));
		 testValues.add(new TestValue("Second Lien excess", 121, 133));
		 testValues.add(new TestValue("Second Lien Net Loan Balance", 122, 134));
		 testValues.add(new TestValue("DIP Collateral Loans", 123, 135));
		 testValues.add(new TestValue("DIP Collateral Loans excess", 124, 136));
		 testValues.add(new TestValue("DIP Collateral Loans Net Loan Balance", 125, 137));
		 testValues.add(new TestValue("Eligible Foreign Country", 126, 138));
		 testValues.add(new TestValue("Eligible Foreign Country excess", 127, 139));
		 testValues.add(new TestValue("Eligible Foreign Country Net Loan Balance", 128, 140));
		 testValues.add(new TestValue("Partial PIK Loan", 129, 141));
		 testValues.add(new TestValue("Partial PIK Loan excess", 130, 142));
		 testValues.add(new TestValue("Partial PIK Loan Net Loan Balance", 131, 143));
		 testValues.add(new TestValue("Revolving / Delayed Drawdown", 132, 144));
		 testValues.add(new TestValue("Revolving / Delayed Drawdown excess", 133, 145));
		 testValues.add(new TestValue("Revolving / Delayed Drawdown Net Loan Balance", 134, 146));
		 testValues.add(new TestValue("Discount Loans", 135, 147));
		 testValues.add(new TestValue("Discount Loans excess", 136, 148));
		 testValues.add(new TestValue("Discount Loans Net Loan Balance", 137, 149));
		 testValues.add(new TestValue("Credit Improved Loans", 138, 150));
		 testValues.add(new TestValue("Credit Improved Loans excess", 139, 151));
		 testValues.add(new TestValue("Credit Improved Loans Net Loan Balance", 140, 152));
		 testValues.add(new TestValue("Less than Quarterly Pay", 141, 153));
		 testValues.add(new TestValue("Less than Quarterly Pay excess", 142, 154));
		 testValues.add(new TestValue("Less than Quarterly Pay Net Loan Balance", 143, 155));
		 testValues.add(new TestValue("Warrants to Purchase Equity Securities", 144, 156));
		 testValues.add(new TestValue("Warrants to Purchase Equity Securities excess", 145, 157));
		 testValues.add(new TestValue("Warrants to Purchase Equity Securities Net Loan Balance", 146, 158));
		 testValues.add(new TestValue("LBO Loan with Equity to Cap <25%", 147, 159));
		 testValues.add(new TestValue("LBO Loan with Equity to Cap <25% excess", 148, 160));
		 testValues.add(new TestValue("LBO Loan with Equity to Cap <25% Net Loan Balance", 149, 161));
		 testValues.add(new TestValue("Participation Interests", 150, 162));
		 testValues.add(new TestValue("Participation Interests excess", 151, 163));
		 testValues.add(new TestValue("Participation Interests Net Loan Balance", 152, 164));
		 testValues.add(new TestValue("Eligible Covenant Lite Loans", 153, 165));
		 testValues.add(new TestValue("Eligible Covenant Lite Loans excess", 154, 166));
		 testValues.add(new TestValue("Eligible Covenant Lite Loans Net Loan Balance", 155, 167));
		 testValues.add(new TestValue("Fixed Rate Loan", 156, 168));
		 testValues.add(new TestValue("Fixed Rate Loan excess", 157, 169));
		 testValues.add(new TestValue("Fixed Rate Loan Net Loan Balance", 158, 170));
		 testValues.add(new TestValue("Agreed Foreign Currency", 159, 171));
		 testValues.add(new TestValue("Agreed Foreign Currency excess", 160, 172));
		 testValues.add(new TestValue("Agreed Foreign Currency Net Loan Balance", 161, 173));
		 //testValues.add(new TestValue("Obligor", 162, 129));
		 //testValues.add(new TestValue("Obligor excess", 163, 129));
		 //testValues.add(new TestValue("Obligor Net Loan Balance", 164, 131));
		 testValues.add(new TestValue("Obligor Industry", 165, 201));
		 testValues.add(new TestValue("Obligor Industry excess", 166, 202));
		 testValues.add(new TestValue("Obligor Industry Net Loan Balance", 167, 203));
		 testValues.add(new TestValue("Top 5 Obligors", 168, 204));
		 testValues.add(new TestValue("Top 5 Obligors excess", 169, 205));
		 testValues.add(new TestValue("Top 5 Obligors Net Loan Balance", 170, 206));*/


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
				mainData = Original_LoanList.readExcelAndConvertToJson(originalExcelFilePath, sheetName,MainColumnNumber);

			} catch (IOException e) {
				e.printStackTrace();
			}

			try {
				actualData = Original_LoanList.readExcelAndConvertToJson(exportedExcelFilePath, sheetName1,
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
