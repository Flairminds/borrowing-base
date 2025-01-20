export const countOccurrencesOfTest = (array, searchString) => {
    const totalCount = array?.length;
    const matchCount = array?.reduce((count, item) => {
        return item.data === searchString ? count + 1 : count;
    }, 0);

    return matchCount;
};