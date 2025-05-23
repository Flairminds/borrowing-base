import { Modal } from 'antd';
import { saveAs } from "file-saver";
import React, { useEffect, useState } from 'react';
import * as XLSX from "xlsx";
import { ModalComponents } from '../../../components/modalComponents';
import { CustomButton } from '../../../components/uiComponents/Button/CustomButton';
import { cloWhatIfData } from '../../../utils/constants/constants';
import styles from './ExportAssetFileModal.module.css';

export const ExportAssetFileModal = ({isOpen, setIsOpen, updateAssetTableData, selectedSheetNumber, fundType}) => {

	const [selectedColumns, setSelectedColumns] = useState([]);

	const handleCancel = () => {
		setIsOpen(false);
	};

	const columnsData = updateAssetTableData?.table_data[selectedSheetNumber]?.columns;

	const handleCheckboxClick = (e, columnData) => {
		const columnSelected = selectedColumns.filter(col => col.key == columnData.key).length;
		if (columnSelected > 0) {
			setSelectedColumns(selectedColumns.filter(col => col.key != columnData.key));
		} else {
			setSelectedColumns([...selectedColumns, columnData]);
		}
	};

	const handleFileExtract = () => {
		const excelFileData = updateAssetTableData.table_data[selectedSheetNumber]?.data.map((el) => {
			// const requiredKeys = cloWhatIfData[fundType].defaultSelectedColumns;
			const excelRow = {};
			selectedColumns.forEach(key => excelRow[key.label] = el[key.key]);
			cloWhatIfData[fundType].additionalInputColumns.forEach(info => excelRow[info.label] = info.initialValue);
			return excelRow;
		});
		const ws = XLSX.utils.json_to_sheet(excelFileData);

		const wb = XLSX.utils.book_new();
		XLSX.utils.book_append_sheet(wb, ws, "CLO Data");

		const excelBuffer = XLSX.write(wb, { bookType: "xlsx", type: "array" });
		const blob = new Blob([excelBuffer], { type: "application/octet-stream" });
		saveAs(blob, "CLO data.xlsx");
		setIsOpen(false);
	};

	useEffect(() => {
		if (fundType && isOpen) {
			setSelectedColumns(cloWhatIfData[fundType]?.defaultSelectedColumns);
		}
	}, [isOpen]);

	return (
		<Modal title={<ModalComponents.Title title='Select columns for export' />} open={isOpen} onCancel={handleCancel} footer={null} width={"90%"}>
			<div className={styles.columnsDisplayContainer}>
				{columnsData && columnsData.length > 0 && [...columnsData]?.sort((a, b) => a.label < b.label ? -1 : 1).map((column) => {
					const isselected = selectedColumns?.filter(el => el.label == column.label).length > 0;
					return (
						<div key={column.label} className={styles.columnItem}>
							<input type="checkbox" id={column.key} name={column.key} value={isselected} checked={isselected} onClick={(e) => handleCheckboxClick(e, column)} />
							<label htmlFor={column.key} style={{display: 'inline-block'}}>{column.label}</label>
						</div>
					);
				})}
			</div>
			<div className={styles.popupFooter}>
				<CustomButton isFilled={true} text='Extract File' onClick={handleFileExtract} />
				<CustomButton text='Cancel' onClick={handleCancel} />
			</div>
		</Modal>
	);
};
