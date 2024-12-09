export const previousSelectedAssetsArray = (asssetsList) => {
    let selectedAssetsArray = Array(asssetsList.length);
    for(let i =0 ; i<asssetsList.length ; i++)
    {
        selectedAssetsArray[i] = asssetsList[i].isIncluded;
    }
    return selectedAssetsArray;
}