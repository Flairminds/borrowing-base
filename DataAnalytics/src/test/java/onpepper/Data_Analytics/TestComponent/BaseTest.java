package onpepper.Data_Analytics.TestComponent;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.time.Duration;
import java.util.Properties;

import org.apache.commons.io.FileUtils;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.edge.EdgeDriver;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;

import io.github.bonigarcia.wdm.WebDriverManager;
import onpepper.Data_Analytics.PageObject.LandingPage;

public class BaseTest {
	public WebDriver driver;
	public LandingPage page;
	
	public WebDriver initializeDriver() throws IOException {
		Properties prop=new Properties();
		FileInputStream fsi=new FileInputStream((System.getProperty("user.dir")+"//src//main//java//onpepper//Data_Analytics//resources//globaldata.properties"));
		prop.load(fsi);
		String browserName = prop.getProperty("browser");
		if(browserName.equalsIgnoreCase("chrome")) {
		WebDriverManager.chromedriver().setup();
		 driver=new ChromeDriver();
	
		}
		else if(browserName.equalsIgnoreCase("Edge")) {
		WebDriverManager.edgedriver().setup();
		 driver=new EdgeDriver();
		}

		//driver.manage().window().maximize();
		driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
		return driver;	
	}
	@BeforeMethod(alwaysRun = true)
	public LandingPage launchApplication() throws IOException, InterruptedException {
		driver=initializeDriver();
		 page=new LandingPage(driver);
	     page.goTo();
		return page;
	}
	
	public String getScreenshot(String testcasename, WebDriver driver) throws IOException {
		TakesScreenshot ts=(TakesScreenshot)driver;
		File source=ts.getScreenshotAs(OutputType.FILE);
		File file=new File(System.getProperty("user.dir")+"//reports//"+testcasename+".png");
		FileUtils.copyFile(source, file);
		
		return System.getProperty("user.dir")+"//reports//"+testcasename+".png";
	}
	
	
	@AfterMethod(alwaysRun = false)
	public void closeapplication() {
		driver.close();
	}
	
}
