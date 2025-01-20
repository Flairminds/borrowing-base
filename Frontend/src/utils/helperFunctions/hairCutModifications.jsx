export const getLatestEntryOfModification = (data, index) => {

    const filteredEntries = data.filter(entry => entry.rowIndex === index);

    if (filteredEntries.length === 0) {
        return null;
    }
    const latestEntry = filteredEntries[filteredEntries.length - 1];

    const resultString = `${latestEntry.prev_val} | ${latestEntry.percentageChange.toFixed(2)}%`;

    return resultString;
};
