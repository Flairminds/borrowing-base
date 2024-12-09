package onpepper.Data_Analytics.Tests;

import java.io.IOException;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.List;

import org.openqa.selenium.WebElement;
import org.testng.Assert;
import org.testng.annotations.Test;

import onpepper.Data_Analytics.PageObject.HomePage;
import onpepper.Data_Analytics.TestComponent.BaseTest;

public class Generated_Result_Validation extends BaseTest {

	// As a user I should have different overview cards to see the summarised values
	// of the report on the dashboard.
	@Test()
	public void uploadFile() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		List<WebElement> Cards = homePage.getOverviewCards();
		for (WebElement Card : Cards) {
			Assert.assertTrue(Card.isDisplayed());
		}
	}

	// As a user I should open the overview cards to view intermediate values
	// involved in the calculation of different cards
	@Test()
	public void checkCardName() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		List<WebElement> Cards = homePage.getOverviewCards();
		for (WebElement Card : Cards) {
			Card.click();
			String Cardname = homePage.getCardName();
			Assert.assertNotNull(Cardname, "Card name is not present");
			Thread.sleep(1000);
		}
	}

	//As a user I should I select start and end date to visualize Borrowing Base trends for a particular range
	@Test(enabled = false)
	public void getStartDate() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		String StartDate = "2024-07-02";
		String EndDate = "2024-07-29";
		homePage.selectRangeDate(StartDate, EndDate);
		String ActualStartdate = homePage.getActualStartDate();
		Assert.assertEquals(ActualStartdate, StartDate);
		String ActualEnddate = homePage.getActualEndDate();
		Assert.assertEquals(ActualEnddate, EndDate);
	}
	
	//As a user I should select a date on the calendar to dynamically change the dashboard data to selected date
	@Test
	public void checkdata() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		homePage.selectReportDateData();
		LocalDate today = LocalDate.now();
		DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
		String formattedDate = today.format(formatter);
		String message = homePage.getToastmsg();
		boolean datePresent = message.contains(formattedDate);
		Assert.assertTrue(datePresent, "Data is loaded for today's date");
	}

	//As a user I should view intermediate metrics of Borrowing to validate the calculation
	@Test
	public void checkIntermediateMetrics() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		homePage.clickOnIntermediateMetrics();
		WebElement IntermediateMetrics = homePage.getIntermediateMetricsTable();
		Assert.assertNotNull(IntermediateMetrics, "Intermediate Metrics is present");
	}

	//As a user I should view mathematical formula and values with color codes involved in calculation of intermediate metric to analyze and validate the calculation
	@Test
	public void checkIntermediateMetricsFormula() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		homePage.clickOnIntermediateMetrics();
		List<WebElement> Columns = homePage.getIntermediateMetricsTableData();
		for (WebElement column : Columns) {
			column.click();
			Thread.sleep(1000);
			try {
				Assert.assertNotNull(homePage.getFormulaValue());
			} catch (org.openqa.selenium.NoSuchElementException e) {
				Assert.assertNotNull(homePage.getButtonFormulaValue());
			}
			homePage.closePopup();
		}
	}

	//As a user I should drill-down on the formulas to see the complete calculation involved in the calculation of particular intermediate metric
	@Test(enabled = false)
	public void checkFormuladropdown() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		homePage.clickOnIntermediateMetrics();
		List<WebElement> Columns = homePage.getIntermediateMetricsTableData();
		for (WebElement column : Columns) {
			column.click();
			Thread.sleep(1000);
			try {
				WebElement Popup = homePage.formulaPopup();
				Assert.assertNotNull(Popup);
				homePage.closeFormulaPopup();
				homePage.closePopup();
			} catch (org.openqa.selenium.NoSuchElementException e) {
				homePage.closePopup();
			}
		}
	}

	//As a user I should have a drop-down to perform different types of what-if analysis.
	@Test
	public void checkWhatifDropdown() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		WebElement dropdown = homePage.getWhatIfDropdown();
		Assert.assertNotNull(dropdown);
		List<WebElement> options = homePage.getWhatIfDropdownoptions();
		for(WebElement option :options) {
			Assert.assertNotNull(option);
		}
	}
	

}
