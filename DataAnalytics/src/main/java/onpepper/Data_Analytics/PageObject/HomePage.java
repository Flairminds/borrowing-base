package onpepper.Data_Analytics.PageObject;

import java.io.IOException;
import java.lang.StackWalker.Option;
import java.util.List;

import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

import onpepper.Data_Analytics.AbstractComponent.AbstractComponent;

public class HomePage extends AbstractComponent{
	public WebDriver driver;
	public HomePage(WebDriver driver) {
		super(driver);
		this.driver=driver;
		PageFactory.initElements(driver, this);
	}

	@FindBy(xpath="((//nav//following-sibling::div)[3]//img)[3]")
	WebElement OptionBtn;
	@FindBy(xpath="//div[contains(text(),'Import File')]")
	WebElement ImportFileOption;
	@FindBy(xpath="//div[contains(text(),'Intermediate Metrics')]")
	WebElement IntermediateMetricsOption;
	@FindBy(xpath="//div[@class='dropzone']//div//span")
	WebElement DragandDropField;
	@FindBy(xpath="//div[contains(@class,'_container')]//input[@placeholder='Report Date']")
	WebElement ReportDateField;
	@FindBy(xpath="//a[contains(text(),'Today')]")
	WebElement TodaysDate;
	@FindBy(xpath="//span[text()='Load']/parent::button")
	WebElement LoadBtn;
	@FindBy(xpath="((//div[@class='ant-modal-content'])[2]//div[@class='ant-modal-header']//div)[4]")
	WebElement OverWritngText;
	@FindBy(xpath="//span[text()='Yes']/parent::button")
	WebElement YesBtn;
	@FindBy(xpath="//h6/following-sibling::ul//li")
	WebElement SheetModificationText;
	@FindBy(xpath="//div[@class='ant-modal-content']//table//tr//td[1]")
	List<WebElement> existingFileNames;
	@FindBy(xpath="(//div[@class='ant-modal-content']//table//tr//td[3])[1]")
	WebElement UseBtn1;
	@FindBy(xpath="//div[contains(@class,'Toastify__toast-icon')]/following-sibling::div")
	WebElement  ToastMsg;
	@FindBy(xpath="//div[contains(@class,'_tabsParent')]//div[contains(@class,'_tabsDiv')]")
	List<WebElement> OverViewCards;
	@FindBy(xpath="//div[contains(@class,'_cardHeader')]//div")
	WebElement  CardName;
	@FindBy(xpath="//input[@placeholder='Start date']")
	WebElement  StartDateField;
	@FindBy(xpath="//input[@placeholder='End date']")
	WebElement  EndDateField;
	@FindBy(xpath="(//*[local-name()='text'])[1]")
	WebElement  StartDateonChart;
	@FindBy(xpath="(//*[local-name()='text'])[3]")
	WebElement  EndDateonChart;
	@FindBy(xpath="//label[@for='reportDatePicker']")
	WebElement  ReportDate;
	@FindBy(xpath="//div[contains(@class,'_tabsContainer')]/following-sibling::div")
	WebElement  IntermediateMetricsTable;
	@FindBy(xpath="//div[contains(@class,'_tabsContainer')]/following-sibling::div//tr[1]//td")
	List<WebElement> FirstRowData;
	@FindBy(xpath="(//div[contains(@class,'_formulaDiv')])[1]//span[1]")
	WebElement FormulaName;
	@FindBy(xpath="(//div[contains(@class,'_formulaDiv')])[1]//span[2]")
	WebElement FormulaValue;
	@FindBy(xpath="//span[text()='Formula']/parent::div/parent::div/parent::div//button[@aria-label='Close']")
	WebElement CloseFormulaBtn;
	@FindBy(xpath="(//div[@class=\"ant-modal-content\"])[3]")
	WebElement FormulaPopup;
	@FindBy(xpath="(//div[contains(@class,'_formulaDiv')])[1]//button")
	List<WebElement> ButtonFormulaValue;
	@FindBy(xpath="(//div[@class='ant-modal-content'])[3]//button")
	WebElement CloseFormulaPopup;
	@FindBy(xpath="//span[text()='What if Analysis']/parent::div")
	WebElement WhatIfDropdown;
	@FindBy(xpath="//div[@class='ant-select-item-option-content']")
	List<WebElement> WhatIfDropdownOptions;
	@FindBy(xpath="//div[text()='Add New Asset']")
	WebElement AddNewAssetOption;
	@FindBy(xpath="//button[text()='Save']")
	WebElement SaveBtn;
	@FindBy(xpath="//span[text()='Save']/parent::button")
	WebElement SaveBtn2;
	@FindBy(xpath="(//div[@class='dropzone']//div//span)[1]")
	WebElement DragandDropField1;
	@FindBy(xpath="//button[text()='Asset Selection']")
	WebElement AssetSelectionBtn;
	@FindBy(xpath="(//th[text()='Investment Name']/parent::tr/parent::thead/parent::table//*[local-name()='svg'])[1]")
	WebElement EditAssetOption;
	@FindBy(xpath="//button[text()='Create Asset']")
	WebElement CreateAssetBtn;
	@FindBy(xpath="//button[text()='Modify Asset']")
	WebElement ModifyAssetBtn;
	@FindBy(xpath="//th[text()='Investment Name']/parent::tr/parent::thead/parent::table//tbody//tr")
	List<WebElement> AssetRows;
	@FindBy(xpath="//input[@placeholder='Notes']")
	WebElement NotesField;
	@FindBy(xpath="//button[text()=' Create Asset ']")
	WebElement CreateAssetBtn1;
	@FindBy(xpath="//th[text()='Investment Name']/parent::tr/parent::thead/parent::table//thead//tr//th//input[@type='checkbox']")
	WebElement AllAssetCheckbox;
	@FindBy(xpath="(//th[text()='Investment Name']/parent::tr/parent::thead/parent::table//tbody//tr//td[1]//input[@type='checkbox'])[1]")
	WebElement AssetCheckbox1;
	@FindBy(xpath="(//th[text()='Investment Name']/parent::tr/parent::thead/parent::table//tbody//tr//td[1]//input[@type='checkbox'])[2]")
	WebElement AssetCheckbox2;
	@FindBy(xpath="//button[text()=' Submit']")
	WebElement Submitbtn;
	@FindBy(xpath="//input[@placeholder='Untitled']")
	WebElement UntitledField;
	@FindBy(xpath="//div[text()='Update Parameters']")
	WebElement UpdateParameterOption;
	@FindBy(xpath="//span[text()='EBITDA']/preceding-sibling::input")
	WebElement EbitdaRadioBtn;
	@FindBy(xpath="//span[text()='Leverage']/preceding-sibling::input")
	WebElement LeverageRadioBtn;
	@FindBy(xpath="(//th[text()='Investment Name']/parent::tr/parent::thead/following-sibling::tbody//tr//td[1]//input[@type='checkbox'])[3]")
	WebElement ParameterCheckbox1;
	@FindBy(xpath="(//th[text()='Investment Name']/parent::tr/parent::thead/following-sibling::tbody//tr//td[1]//input[@type='checkbox'])[4]")
	WebElement ParameterCheckbox2;
	@FindBy(xpath="//input[contains(@placeholder,'Range:')]")
	WebElement RangeField;
	@FindBy(xpath="(//input[contains(@placeholder,'Range:')]/following-sibling::button)[1]")
	WebElement AcceptBtn;
	@FindBy(xpath="(//th[text()='Investment Name']/parent::tr/parent::thead/following-sibling::tbody//tr//td[4])[3]")
	WebElement UpdatedValueField;
	@FindBy(xpath="(//th[text()='Investment Name']/parent::tr/parent::thead/following-sibling::tbody//tr//td[5])[3]")
	WebElement UpdatedText1;
	@FindBy(xpath="(//th[text()='Investment Name']/parent::tr/parent::thead/following-sibling::tbody//tr//td[6])[3]")
	WebElement UpdatedText2;
	@FindBy(xpath="(//th[text()='Investment Name']/parent::tr/parent::thead/following-sibling::tbody//tr//td[5])[4]")
	WebElement UpdatedText3;
	@FindBy(xpath="(//th[text()='Investment Name']/parent::tr/parent::thead/following-sibling::tbody//tr//td[6])[4]")
	WebElement UpdatedText4;
	@FindBy(xpath="//div[text()='What if analysis library']")
	WebElement WhatifanalysisOption;
	@FindBy(xpath="//button[text()='Use']")
	WebElement UseBtn;
	@FindBy(xpath="//th[text()='Name']/parent::tr/parent::thead//th")
	List<WebElement> HeadNames;
	@FindBy(xpath="//th[text()='Name']/parent::tr/parent::thead/following-sibling::tbody//tr[1]//td[1]//input")
	WebElement BaseFileRadio1;
	
	
	public void retriveBasefile() throws InterruptedException {
		clickWhatifanalysisOption();
		Actions act=new Actions(driver);
		act.click(BaseFileRadio1).perform();
		UseBtn.click();
	}
	public void clickWhatifanalysisOption() throws InterruptedException {
		Actions act=new Actions(driver);
		act.click(OptionBtn).perform();
		WhatifanalysisOption.click();
	}
	public List<WebElement> getHeadNames() throws InterruptedException {
		clickWhatifanalysisOption();
		driver.switchTo().activeElement();
		Thread.sleep(1000);
		return HeadNames;
	}
	public void updateMultipleFieldValue() {
	ParameterCheckbox1.click();
	ParameterCheckbox2.click();
	RangeField.sendKeys("80");
	AcceptBtn.click();
	}
	public void selectEBITDARadio() {
		EbitdaRadioBtn.click();
	}
	public void selectLeverageRadioBtn() {
		LeverageRadioBtn.click();
	}
	public void updateFieldValue() {
		UpdatedValueField.click();
		Actions act=new Actions(driver);
        act.moveToElement(UpdatedValueField).click().build().perform();
        act.sendKeys("80").build().perform();
	}
	public String getUpdatedText1value() throws InterruptedException {
		Thread.sleep(500);
		return UpdatedText1.getText();
	}
	public String getUpdatedText2value() throws InterruptedException {
		Thread.sleep(500);
		return UpdatedText2.getText();
	}
	public String getUpdatedText3value() throws InterruptedException {
		Thread.sleep(500);
		return UpdatedText3.getText();
	}
	public String getUpdatedText4value() throws InterruptedException {
		Thread.sleep(500);
		return UpdatedText4.getText();
	}
	public void selectUpdateParameterOption() {
		WhatIfDropdown.click();
		UpdateParameterOption.click();
	}
	public void updateUniqueEBITDAValue() {
		selectEBITDARadio();
		updateFieldValue();		
	}
	public void sendUntitledField() {
		UntitledField.sendKeys("Test1");
		
	}
	public void editAssetRow() throws InterruptedException, IOException {
		WhatIfDropdown.click();
		AddNewAssetOption.click();
		uploadAssetExcelSheet1();
		Thread.sleep(500);
		AssetSelectionBtn.click();
	}
	public void clickAllAssetCheckbox() {
		AllAssetCheckbox.click();
	}
	public void clickAssetCheckbox() {
		AssetCheckbox1.click();
		AssetCheckbox2.click();
	}
	public void selectAsset() throws InterruptedException, IOException {
		editAssetRow();
		clickAllAssetCheckbox();
		clickAssetCheckbox();
		Submitbtn.click();
		LoadBtn.click();
		sendUntitledField();
		clickSaveButton();
		clickSaveButton2();
	}
	public void clickEditAssetOption() {
		EditAssetOption.click();
	}
	public int getAssetRowCount() {
		int count=AssetRows.size();
		return count;
	}
	public void clickCreateAssetBtn1() throws InterruptedException {
		CreateAssetBtn1.click();
		Thread.sleep(2000);
		CreateAssetBtn.click();
	}
	public void clickCreateAssetBtn() throws InterruptedException {
		clickEditAssetOption();
		Thread.sleep(2000);
		CreateAssetBtn.click();
	}
	public void clickModifyAssetBtn() throws InterruptedException {
		clickEditAssetOption();
		Thread.sleep(2000);
		ModifyAssetBtn.click();
	}
	public void clickSaveButton() {
		SaveBtn.click();
	}
	public void clickSaveButton2() throws InterruptedException {
		Thread.sleep(2000);
		driver.switchTo().activeElement();
		NotesField.sendKeys("Test");
		SaveBtn2.click();
	}
	
	public void UploadAssetFile() throws InterruptedException, IOException {
		WhatIfDropdown.click();
		AddNewAssetOption.click();
		uploadAssetExcelSheet1();
		LoadBtn.click();
		clickSaveButton();
		clickSaveButton2();
		
	}
	
	public void uploadAssetExcelSheet1() throws InterruptedException, IOException {
		Actions act=new Actions(driver);
		act.click(DragandDropField1).perform();
		Thread.sleep(3000);
		Runtime.getRuntime().exec("C:\\Users\\USER\\Documents\\Flairminds\\fileupload-Onpeper\\Asset fileupload.exe");
		Thread.sleep(2000);
	}
	public List<WebElement> getWhatIfDropdownoptions() {
		WhatIfDropdown.click();
		return WhatIfDropdownOptions;
	}
	public WebElement getWhatIfDropdown() {
		return WhatIfDropdown;
	}
	public void selectReportDateData() throws InterruptedException {
		Actions act=new Actions(driver);
		Thread.sleep(500);
		act.click(ReportDate).perform();
		Thread.sleep(500);
		TodaysDate.click();
	}
	public String getToastmsg() throws InterruptedException {
		Thread.sleep(3000);
		return ToastMsg.getText();
	}
	public SelectAsset clickUseBtn() throws InterruptedException {
		Thread.sleep(1000);
		UseBtn1.click();
		Thread.sleep(1000);
		SelectAsset select=new SelectAsset(driver);
		return select;
		
	}
	public void clickOnImportFileOption() {
		Actions act=new Actions(driver);
		act.click(OptionBtn).perform();
		ImportFileOption.click();
	}
	public String getDragandDropFieldText() throws InterruptedException {
		Thread.sleep(1000);
		return DragandDropField.getText();
	}
	public void uploadExcelSheet() throws InterruptedException, IOException {
		DragandDropField.click();
		Thread.sleep(3000);
		Runtime.getRuntime().exec("C:\\Users\\USER\\Documents\\Flairminds\\fileupload-Onpeper\\mainfileupload.exe");
		Thread.sleep(2000);
	}
	public void selectReportDate() throws InterruptedException {
		Thread.sleep(500);
		ReportDateField.click();
		Thread.sleep(500);
		TodaysDate.click();
	}
	public String getUpdatedHTML() throws InterruptedException {
		Thread.sleep(1000);
		 return ReportDateField.getAttribute("outerHTML");
	}
	public void clickOnLoadBtn() throws InterruptedException {
		LoadBtn.click();
		Thread.sleep(4000);
	}
	public String getOverWritingText() throws InterruptedException {
		Thread.sleep(1000);
		return OverWritngText.getText();
	}
	public void uploadErrorExcelSheet() throws InterruptedException, IOException {
		DragandDropField.click();
		Thread.sleep(3000);
		Runtime.getRuntime().exec("C:\\Users\\USER\\Documents\\Flairminds\\fileupload-Onpeper\\errorfileupload.exe");
		Thread.sleep(2000);
	}
	public void clickYesBtn() throws InterruptedException {
		Thread.sleep(1000);
		Actions act=new Actions(driver);
		act.click(YesBtn).perform();
	}
	public String getSheetModificationText() throws InterruptedException {
		Thread.sleep(2000);
		return SheetModificationText.getText();
	}
	public SelectAsset NavigatetoSelectAsset() {
		YesBtn.click();
		SelectAsset select=new SelectAsset(driver);
		return select;	
	}
	public List<WebElement> getUploadedFileNames() {
		return existingFileNames;
	}
	public List<WebElement> getOverviewCards() {
		return OverViewCards;
	}
	public String getCardName() {
		return CardName.getText();
	}
	public void selectRangeDate(String StartDate,String EndDate)  {
		StartDateField.sendKeys(StartDate);
		Actions act=new Actions(driver);
		act.sendKeys(Keys.ENTER).perform();
		EndDateField.sendKeys(EndDate);
		act.sendKeys(Keys.ENTER).perform();
	}
	public String getActualStartDate() {
		return StartDateonChart.getText();
	}
	public String getActualEndDate() {
		return EndDateonChart.getText();
	}
	public void clickOnIntermediateMetrics() throws InterruptedException {
		Actions act=new Actions(driver);
		act.click(OptionBtn).perform();
		Thread.sleep(500);
		IntermediateMetricsOption.click();
	}
	public WebElement getIntermediateMetricsTable() {
		return IntermediateMetricsTable;
	}
	public List<WebElement> getIntermediateMetricsTableData() {
		return FirstRowData;
	}
	public void closePopup() {
		CloseFormulaBtn.click();
	}
	public String getFormulaValue() {
		return FormulaValue.getText();
	}
	public String getButtonFormulaValue() {
		int numberofBtn = ButtonFormulaValue.size();
		StringBuilder buttonTexts = new StringBuilder();
		for (int i=1;i<=numberofBtn;i++) {
			String path="(//div[contains(@class,'_formulaDiv')])[1]//button["+i+"]";
			WebElement button = driver.findElement(By.xpath(path));
			String buttonText = button.getText().trim();
		    buttonTexts.append(buttonText).append(" ");
		}
		return buttonTexts.toString().trim();
		
	}
	public WebElement formulaPopup() {
		String path="(//div[contains(@class,'_formulaDiv')])[1]//button[1]";
		WebElement button = driver.findElement(By.xpath(path));
		Actions act=new Actions(driver);
		act.click(button).perform();
		return FormulaPopup;
	}
	public void closeFormulaPopup() {
		Actions act=new Actions(driver);
		act.click(CloseFormulaPopup).perform();
	}
	public WebElement getToastpopup() {
		return ToastMsg;
	}
	
	
	
	
	
	
	
	
}
