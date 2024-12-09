export const getLatestEntryOfModification = (data, index) => {
    
    let filteredEntries = data.filter(entry => entry.rowIndex === index);
    
    if (filteredEntries.length === 0) {
        return null;  
    }
    let latestEntry = filteredEntries[filteredEntries.length - 1];
    
    let resultString = `${latestEntry.prev_val} | ${latestEntry.percentageChange.toFixed(2)}%`;
    
    return resultString;
}
