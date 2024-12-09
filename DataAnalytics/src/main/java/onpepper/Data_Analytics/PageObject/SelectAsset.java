package onpepper.Data_Analytics.PageObject;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

import onpepper.Data_Analytics.AbstractComponent.AbstractComponent;

public class SelectAsset extends AbstractComponent {
	public WebDriver driver;
	public SelectAsset(WebDriver driver) {
		super(driver);
		this.driver=driver;
		PageFactory.initElements(driver, this);
	}
	
	@FindBy(xpath="//th[text()='+']")
	WebElement SettingBtn;
	@FindBy(xpath="//div[text()='Asset Parameter Selection']")
	WebElement AssetParameterBtn;
	@FindBy(xpath="(//div[contains(@class,'_listContainer')]//input)[1]")
	WebElement IssuerCheckBox;
	@FindBy(xpath="(//div[contains(@class,'_listContainer')]//input)[7]")
	WebElement CostCheckBox;
	@FindBy(xpath="(//div[contains(@class,'_listContainer')]//input)[13]")
	WebElement PIKCheckBox;
	@FindBy(xpath="(//div[contains(@class,'_listContainer')]//input)[5]")
	WebElement  MaturityCheckBox;
	@FindBy(xpath="(//div[contains(@class,'_listContainer')]//input)[6]")
	WebElement  PARCheckBox;
	@FindBy(xpath="//div[contains(@class,'_errorMessage')]")
	WebElement  ErrorMessage;
	@FindBy(xpath="//div[contains(@class,'tableContainer')]//th[1]")
	WebElement  AllCheckBoxBtn;
	@FindBy(xpath="//div[contains(@class,'tableContainer')]//tr[2]//td[1]")
	WebElement  RowCheckBoxBtn;
	@FindBy(xpath="//div[contains(@class,'tableContainer')]//tr[3]//td[1]")
	WebElement  RowCheckBoxBtn1;
	@FindBy(xpath="//button[text()='Set']")
	WebElement  SetBtn;
	@FindBy(xpath="//div[contains(@class,'Toastify__toast-icon')]/following-sibling::div")
	WebElement  getToastMsg;
	@FindBy(xpath="//span[text()='View Results']/parent::button")
	WebElement  ViewResultBtn;
	@FindBy(xpath="//button[@aria-label='close']")
	WebElement  CloseToastBtn;
	
	public void selectAssetCheckbox() throws InterruptedException {
		Thread.sleep(10000);
		Actions act=new Actions(driver);
		//act.click(SettingBtn).perform();
		SettingBtn.click();
	//	AssetParameterBtn.click();
		driver.switchTo().activeElement();
		Thread.sleep(500);
		act.click(PARCheckBox).perform();
		Thread.sleep(500);
		act.click(CostCheckBox).perform();
		Thread.sleep(500);
		act.click(PIKCheckBox).perform();
		Thread.sleep(500);
		act.click(MaturityCheckBox).perform();
		Thread.sleep(500);
	}
	public String getErrorMsg() throws InterruptedException {
		selectAssetCheckbox();
		return ErrorMessage.getText();
	}
	public String clickOnSetBtn() throws InterruptedException {
		SetBtn.click();
		Thread.sleep(2000);
		return getToastMsg.getText();
	}
	public String getLoadToastmsg() throws InterruptedException {
		Thread.sleep(1000);
		return getToastMsg.getText();
	}
	
	public HomePage selectInvestment() throws InterruptedException {
		Thread.sleep(2000);
		CloseToastBtn.click();
		AllCheckBoxBtn.click();
		RowCheckBoxBtn.click();
		RowCheckBoxBtn1.click();
		Actions act=new Actions(driver);
		act.click(ViewResultBtn).perform();
		Thread.sleep(3000);
		HomePage page=new HomePage(driver);
		return page;
	}
	
}
