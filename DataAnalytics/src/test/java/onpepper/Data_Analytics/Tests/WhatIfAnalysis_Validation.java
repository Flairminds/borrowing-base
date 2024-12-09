package onpepper.Data_Analytics.Tests;

import java.io.IOException;
import java.util.List;

import org.openqa.selenium.WebElement;
import org.testng.Assert;
import org.testng.annotations.Test;

import onpepper.Data_Analytics.PageObject.HomePage;
import onpepper.Data_Analytics.TestComponent.BaseTest;
import onpepper.Data_Analytics.TestComponent.Retry;

public class WhatIfAnalysis_Validation extends BaseTest {

	// As a user I should upload a file to perform what-if analysis by adding assets
	@Test(retryAnalyzer = Retry.class)
	public void uploadFile() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		homePage.UploadAssetFile();
		String Expectedmsg = homePage.getToastmsg();
		String Actualmsg = "Saved";
		Assert.assertEquals(Actualmsg, Expectedmsg);
	}

	// As a user I should upload a file to perform what-if analysis by adding assets
	@Test(retryAnalyzer = Retry.class)
	public void CopyAssetRow() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		homePage.editAssetRow();
		int OldRowCount = homePage.getAssetRowCount();
		homePage.clickCreateAssetBtn();
		int NewRowCount = homePage.getAssetRowCount();
		Assert.assertNotEquals(OldRowCount, NewRowCount);
	}

	// As a user I should edit parameters of asset to modify the asset before
	// selection
	@Test(retryAnalyzer = Retry.class)
	public void ModifyAssetRow() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		homePage.editAssetRow();
		int OldRowCount = homePage.getAssetRowCount();
		homePage.clickModifyAssetBtn();
		int NewRowCount = homePage.getAssetRowCount();
		Assert.assertEquals(OldRowCount, NewRowCount);
	}

	// As a user I should open a blank form to create a completely new assets
	@Test(retryAnalyzer = Retry.class)
	public void CreateAssetRow() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		homePage.editAssetRow();
		int OldRowCount = homePage.getAssetRowCount();
		homePage.clickCreateAssetBtn1();
		int NewRowCount = homePage.getAssetRowCount();
		Assert.assertNotEquals(OldRowCount, NewRowCount);
	}

	// As a user I should select the assets to perform what-if analysis using only
	// required assets
	@Test(retryAnalyzer = Retry.class)
	public void selectAsset() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		homePage.selectAsset();
		String Expectedmsg = homePage.getToastmsg();
		String Actualmsg = "Saved";
		Assert.assertEquals(Actualmsg, Expectedmsg);
	}

	// As a user I should add name to what-if analysis results to maintain unique
	// identity
	@Test(retryAnalyzer = Retry.class)
	public void uploadFileName() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		homePage.UploadAssetFile();
		String Expectedmsg = homePage.getToastmsg();
		String Actualmsg = "Saved";
		Assert.assertEquals(Actualmsg, Expectedmsg);
	}

	// As a user I should add name to what-if analysis results to maintain unique
	// identity
	@Test(retryAnalyzer = Retry.class)
	public void updateEBITDAParameter() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		homePage.selectUpdateParameterOption();
		homePage.selectEBITDARadio();
		String OldUpdatedText1 = homePage.getUpdatedText1value();
		String OldUpdatedText2 = homePage.getUpdatedText2value();
		homePage.updateFieldValue();
		String NewUpdatedText1 = homePage.getUpdatedText1value();
		String NewUpdatedText2 = homePage.getUpdatedText2value();
		Assert.assertNotEquals(OldUpdatedText1, NewUpdatedText1);
		Assert.assertNotEquals(OldUpdatedText2, NewUpdatedText2);
	}

	// As a user I should add name to what-if analysis results to maintain unique
	// identity
	@Test(retryAnalyzer = Retry.class)
	public void updateLevarageParameter() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		homePage.selectUpdateParameterOption();
		homePage.selectLeverageRadioBtn();
		String OldUpdatedText1 = homePage.getUpdatedText1value();
		String OldUpdatedText2 = homePage.getUpdatedText2value();
		homePage.updateFieldValue();
		String NewUpdatedText1 = homePage.getUpdatedText1value();
		String NewUpdatedText2 = homePage.getUpdatedText2value();
		Assert.assertNotEquals(OldUpdatedText1, NewUpdatedText1);
		Assert.assertNotEquals(OldUpdatedText2, NewUpdatedText2);
	}

	// As a user I should select some assets and add changed percentage value to
	// automate some tasks
	@Test(retryAnalyzer = Retry.class)
	public void updateMultipleEBITDAParameter() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		homePage.selectUpdateParameterOption();
		homePage.selectEBITDARadio();
		String OldUpdatedText1 = homePage.getUpdatedText1value();
		String OldUpdatedText2 = homePage.getUpdatedText2value();
		String OldUpdatedText3 = homePage.getUpdatedText3value();
		String OldUpdatedText4 = homePage.getUpdatedText4value();
		homePage.updateMultipleFieldValue();
		String NewUpdatedText1 = homePage.getUpdatedText1value();
		String NewUpdatedText2 = homePage.getUpdatedText2value();
		String NewUpdatedText3 = homePage.getUpdatedText3value();
		String NewUpdatedText4 = homePage.getUpdatedText4value();
		Assert.assertNotEquals(OldUpdatedText1, NewUpdatedText1);
		Assert.assertNotEquals(OldUpdatedText2, NewUpdatedText2);
		Assert.assertNotEquals(OldUpdatedText3, NewUpdatedText3);
		Assert.assertNotEquals(OldUpdatedText4, NewUpdatedText4);
		System.out.println(OldUpdatedText3 + "*****" + NewUpdatedText3);
		System.out.println(OldUpdatedText4 + "*****" + NewUpdatedText4);
	}

	// As a user I should select some assets and add changed percentage value to
	// automate some tasks
	@Test(retryAnalyzer = Retry.class)
	public void updateMultipleLeaverageParameter() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		homePage.selectUpdateParameterOption();
		homePage.selectLeverageRadioBtn();
		String OldUpdatedText1 = homePage.getUpdatedText1value();
		String OldUpdatedText2 = homePage.getUpdatedText2value();
		String OldUpdatedText3 = homePage.getUpdatedText3value();
		String OldUpdatedText4 = homePage.getUpdatedText4value();
		homePage.updateMultipleFieldValue();
		String NewUpdatedText1 = homePage.getUpdatedText1value();
		String NewUpdatedText2 = homePage.getUpdatedText2value();
		String NewUpdatedText3 = homePage.getUpdatedText3value();
		String NewUpdatedText4 = homePage.getUpdatedText4value();
		Assert.assertNotEquals(OldUpdatedText1, NewUpdatedText1);
		Assert.assertNotEquals(OldUpdatedText2, NewUpdatedText2);
		Assert.assertNotEquals(OldUpdatedText3, NewUpdatedText3);
		Assert.assertNotEquals(OldUpdatedText4, NewUpdatedText4);
		System.out.println(OldUpdatedText3 + "*****" + NewUpdatedText3);
		System.out.println(OldUpdatedText4 + "*****" + NewUpdatedText4);
	}

	// As a user I should click on view simulations to see name, note, base file,
	// create date of the save results (OBPD-37)
	@Test(retryAnalyzer = Retry.class)
	public void CheckTableHeaders() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		List<WebElement> headers = homePage.getHeadNames();
		String Expectedheader2 = "Name";
		String Expectedheader3 = "Created Date";
		String Expectedheader4 = "Note";
		String Expectedheader5 = "Base File Name";
		String Actualheader2 = headers.get(1).getText();
		String Actualheader3 = headers.get(2).getText();
		String Actualheader4 = headers.get(3).getText();
		String Actualheader5 = headers.get(4).getText();
		Assert.assertEquals(Expectedheader2, Actualheader2);
		Assert.assertEquals(Expectedheader3, Actualheader3);
		Assert.assertEquals(Expectedheader4, Actualheader4);
		Assert.assertEquals(Expectedheader5, Actualheader5);
	}

	// As a user I should have a use button to retrieve the saved what-if analysis
	@Test(retryAnalyzer = Retry.class)
	public void RetriveBaseFile() throws IOException, InterruptedException {
		HomePage homePage = page.goTo();
		homePage.retriveBasefile();
		String Acualtext=homePage.getToastmsg();
		String Expectedtext="Assets imported Successfully";
		Boolean status=(Acualtext.contains(Expectedtext));
		Assert.assertTrue(status, "File is not get imported");
	}
}