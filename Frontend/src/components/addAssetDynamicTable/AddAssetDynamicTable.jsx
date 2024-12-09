import React from 'react'
import StylesTable from "./AddAssetDynamicTable.module.css"
import { useEffect, useState } from 'preact/hooks'
import editIcon from '../../assets/editIcon.svg'
import { generateAssetFormData } from '../../utils/helperFunctions/addAssetFormData'
import {MoreOutlined} from '@ant-design/icons';
import { formatNumber } from '../../utils/helperFunctions/numberFormatting'


export const AddAssetDynamicTable = ({data,columns,selectedAssets, setSelectedAssets,setModificationData,setCreateAssetModalOpen,setCreateAssetFormData}) => {

  const [isAllSelected, setIsAllSelected] = useState(true);

  useEffect(() => {
    setIsAllSelected(selectedAssets.every(asset => asset));
}, [selectedAssets]);

  const handleCheckBoxClick = (index) => {
    const newValues = [...selectedAssets];
    newValues[index] = !newValues[index];

    setSelectedAssets(newValues)
    setIsAllSelected(newValues.every(asset => asset));
  }

  const handleSelectAllClick = () => {  
    const newSelectAll = !isAllSelected   ;
    setIsAllSelected(newSelectAll);
    setSelectedAssets(selectedAssets?.map((el =>newSelectAll)));
};

const handleEditAsset = (data, rowIndex) => {
  setModificationData({
      data:data,
      index:rowIndex
    })
    const modifiedData = generateAssetFormData(data);
    setCreateAssetFormData(modifiedData);
    setCreateAssetModalOpen(true)
}



  return (
    <div className={StylesTable.tableContainer}>
      <table className={StylesTable.table}>
        <thead>
          <tr className={StylesTable.headRow}>
            <th className={StylesTable.th}> 
              <input
                  type="checkbox"
                  checked={isAllSelected}
                  onChange={handleSelectAllClick}
              />
            </th>
            {columns?.map((col, index) => (
              <th key={index} className={StylesTable.th}>
                {col.title}
              </th>
            ))}
            <th className={StylesTable.th}></th>
          </tr>
        </thead>
        <tbody>
          {data?.map((row, rowIndex) => (
            <tr key={rowIndex}>
              <td className={StylesTable.td}>
                <input onClick={() => handleCheckBoxClick(rowIndex)} type="checkbox" checked={selectedAssets[rowIndex]} />
              </td>
              {columns.map((col) => (
                <td key={col?.key} className={StylesTable.td}>
                  {row && typeof(row[col?.key]) == 'number' ? formatNumber(row[col?.key]) : row[col?.key]}
                </td>
              ))}
              <td className={`${StylesTable.td} ${StylesTable.lastCol}`} >
                  <MoreOutlined style={{cursor:'pointer', fontSize:'20px'}} onClick={() => handleEditAsset(row, rowIndex)} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
