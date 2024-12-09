export const sortData = (originalData, columnName, sortOrder = 'asc') => {

    const data = JSON.parse(JSON.stringify(originalData)); // Clone original data

    // Helper to parse dollar amounts and percentages into sortable numbers
    function parseValue(value) {
        if (typeof value === 'string') {
            if (value.includes('$')) {
                let num = parseFloat(value.replace(/[$,]/g, '')); // Remove dollar signs and commas
                if (value.includes('M')) {
                    return num * 1_000_000; // Convert M to millions
                } else if (value.includes('K')) {
                    return num * 1_000; // Convert K to thousands
                }
                return num; // No suffix means it's a direct number
            } else if (value.endsWith('%')) {
                return parseFloat(value.replace('%', '')); // Remove percentage signs
            }
        }
        return value;
    }

    // Sorting logic
    const indices = data[columnName].map((item, index) => index); // Create an array of indices
    indices.sort((a, b) => {
        const valA = parseValue(data[columnName][a].data);
        const valB = parseValue(data[columnName][b].data);

        // Compare for sorting
        if (valA < valB) {
            return sortOrder === 'asc' ? -1 : 1;
        } else if (valA > valB) {
            return sortOrder === 'asc' ? 1 : -1;
        }
        return 0;
    });

    // Create a new object to store sorted data without modifying the original data
    const sortedData = {};
    for (let key in data) {
        sortedData[key] = indices.map(index => data[key][index]);
    }

    // Create result object keeping columns and total intact
    let result = {};
    for (let key in sortedData) {
        if (key === 'columns' || key === 'Total') {
            result[key] = originalData[key];
        } else {
            result[key] = sortedData[key];
        }
    }

    return result; // Return result with sorted data and columns intact
};
