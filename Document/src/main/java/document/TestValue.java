package document;

public class TestValue {
	
	 private String columnName;
	    private int mainColumnNumber;
	    private int actualColumnNumber;

	    public TestValue(String columnName, int mainColumnNumber, int actualColumnNumber) {
	        this.columnName = columnName;
	        this.mainColumnNumber = mainColumnNumber;
	        this.actualColumnNumber = actualColumnNumber;
	    }

	    // Getters and Setters
	    public String getColumnName() {
	        return columnName;
	    }

	    public void setColumnName(String columnName) {
	        this.columnName = columnName;
	    }

	    public int getMainColumnNumber() {
	        return mainColumnNumber;
	    }

	    public void setMainColumnNumber(int mainColumnNumber) {
	        this.mainColumnNumber = mainColumnNumber;
	    }

	    public int getActualColumnNumber() {
	        return actualColumnNumber;
	    }

	    public void setActualColumnNumber(int actualColumnNumber) {
	        this.actualColumnNumber = actualColumnNumber;
	    }

	    @Override
	    public String toString() {
	        return "TestValue{" +
	                "columnName='" + columnName + '\'' +
	                ", mainColumnNumber=" + mainColumnNumber +
	                ", actualColumnNumber=" + actualColumnNumber +
	                '}';
	    }

}
