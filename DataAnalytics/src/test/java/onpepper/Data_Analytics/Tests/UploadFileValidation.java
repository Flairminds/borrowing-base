package onpepper.Data_Analytics.Tests;

import java.io.IOException;
import java.util.List;

import org.openqa.selenium.WebElement;
import org.testng.Assert;
import org.testng.annotations.Test;

import onpepper.Data_Analytics.PageObject.HomePage;
import onpepper.Data_Analytics.PageObject.SelectAsset;
import onpepper.Data_Analytics.TestComponent.BaseTest;
import onpepper.Data_Analytics.TestComponent.Retry;

public class UploadFileValidation extends BaseTest {

	// As a user I should upload the file to perform Borrowing Base Calculations
	@Test(retryAnalyzer = Retry.class)
	public void UploadFile() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		homePage.clickOnImportFileOption();
		driver.switchTo().activeElement();
		String previoustext = homePage.getDragandDropFieldText();
		homePage.uploadExcelSheet();
		String UpdatedText = homePage.getDragandDropFieldText();
		Assert.assertNotSame(previoustext, UpdatedText);
	}

	// As a user I should select the report date to keep borrowing base results
	// unique for the date
	@Test(retryAnalyzer = Retry.class)
	public void SelectReportDate() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		homePage.clickOnImportFileOption();
		driver.switchTo().activeElement();
		homePage.selectReportDate();
		String updatedHtml = homePage.getUpdatedHTML();
		boolean isClearButtonPresent = updatedHtml.contains("ant-picker-clear");
		Assert.assertFalse(isClearButtonPresent, "HTML element is not present");
	}
	@Test(retryAnalyzer = Retry.class)
	public void uploadFile() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		homePage.clickOnImportFileOption();
		driver.switchTo().activeElement();
		homePage.selectReportDate();
		homePage.uploadExcelSheet();
		homePage.clickOnLoadBtn();
	}

	// As a user I should get notification message for selecting existing report to
	// ask permission for over-writing the existing report data
	@Test(dependsOnMethods = "uploadFile",retryAnalyzer = Retry.class)
	public void checkOverwritingText() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		homePage.clickOnImportFileOption();
		driver.switchTo().activeElement();
		homePage.selectReportDate();
		homePage.uploadExcelSheet();
		homePage.clickOnLoadBtn();
		driver.switchTo().activeElement();
		String OverWritingText = homePage.getOverWritingText();
		String text = "Data for the selected date already exists in the system. Do you want to replace it ?";
		Assert.assertEquals(OverWritingText, text);
	}

	// As a user I should get notification message for selecting existing report to
	// ask permission for over-writing the existing report data
	@Test(dependsOnMethods = "uploadFile",retryAnalyzer = Retry.class)
	public void checkSheetModificationText() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		homePage.clickOnImportFileOption();
		driver.switchTo().activeElement();
		homePage.selectReportDate();
		homePage.uploadErrorExcelSheet();
		homePage.clickOnLoadBtn();
		homePage.clickYesBtn();
		String ExpectedText = "PL BB Build is not present in uploaded file";
		String ActualText = homePage.getSheetModificationText();
		System.out.println(ActualText);
		Assert.assertEquals(ExpectedText, ActualText);
	}

	// As a user I should re-upload the file to generate results
	@Test(dependsOnMethods = "uploadFile",retryAnalyzer = Retry.class)
	public void checkReUploadFile() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		homePage.clickOnImportFileOption();
		driver.switchTo().activeElement();
		homePage.selectReportDate();
		homePage.uploadExcelSheet();
		homePage.clickOnLoadBtn();
		homePage.clickYesBtn();
	}

	// As a user I should set the configuration of asset selection table to perform
	// asset selection based on the required parameters
	@Test(dependsOnMethods = "uploadFile",retryAnalyzer = Retry.class)
	public void checkAssetSelection() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		homePage.clickOnImportFileOption();
		driver.switchTo().activeElement();
		SelectAsset asset = homePage.clickUseBtn();
		asset.selectAssetCheckbox();
		String ActualText = asset.clickOnSetBtn();
		String ExpectedText = "Configurations Set Successfully";
		Assert.assertEquals(ActualText, ExpectedText);
	}

	// As a user I should set the configuration of asset selection table to perform
	// asset selection based on the required parameters
	@Test(dependsOnMethods = "uploadFile",retryAnalyzer = Retry.class)
	public void checkAssetErrorMsg() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		homePage.clickOnImportFileOption();
		driver.switchTo().activeElement();
		SelectAsset asset = homePage.clickUseBtn();
		String ExpectedText = "*Only 4 columns allowded";
		String ActualText = asset.getErrorMsg();
		Assert.assertEquals(ActualText, ExpectedText);
	}

	// As a user I should re-use the existing files to modify the Borrowing Base
	// Results of a particular date.
	@Test(dependsOnMethods = "uploadFile",retryAnalyzer = Retry.class)
	public void checkLoadMsg() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		homePage.clickOnImportFileOption();
		driver.switchTo().activeElement();
		SelectAsset asset = homePage.clickUseBtn();
		String ExpectedText = "File Loaded";
		String ActualText = asset.getLoadToastmsg();
		Assert.assertEquals(ActualText, ExpectedText);
	}

	// As a user I should re-use the existing files to modify the Borrowing Base
	// Results of a particular date
	@Test(dependsOnMethods = "uploadFile",retryAnalyzer = Retry.class)
	public void selectInvestment() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		homePage.clickOnImportFileOption();
		driver.switchTo().activeElement();
		SelectAsset asset = homePage.clickUseBtn();
		asset.selectInvestment();
		String ExpectedText = "Results Generated";
		String ActualText = asset.getLoadToastmsg();
		Assert.assertEquals(ActualText, ExpectedText);
	}

	// As a user I should view a table of existing files to get overview of existing data
	@Test(dependsOnMethods = "uploadFile",retryAnalyzer = Retry.class)
	public void checkUploadedFileNames() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		homePage.clickOnImportFileOption();
		driver.switchTo().activeElement();
		List<WebElement> filenames = homePage.getUploadedFileNames();
		for (WebElement filename : filenames) {
			Assert.assertNotNull(filename, "file name is present");
		}
	}
}
