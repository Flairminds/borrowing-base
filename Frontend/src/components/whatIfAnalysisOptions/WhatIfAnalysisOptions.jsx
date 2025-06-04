import { Select } from 'antd';
import React, { useState } from 'react';
// import { updateAssetData } from '../../utils/updateAssetData';
import { toast } from 'react-toastify';
import { getUpdateAssetData } from '../../services/api';
import { wiaOptions } from '../../utils/configurations/wiaOptions';
import { DEFAULT_SHEET_NAME } from '../../utils/constants/constants';
import { LoaderSmall } from '../uiComponents/loader/loader';

export const WhatIfAnalysisOptions = ({
	selectedOption,
	setSelectedOption,
	setIsModalVisible,
	setEbitdaModalOpen,
	setIsupdateAssetModalOpen,
	setUpdateAssetTableData,
	baseFile,
	whatIfAnalysisId,
	setWhatIfAnalysisId,
	setSaveBtn,
	fundType
}) => {

	const [isLoading, setIsLoading] = useState(false);

	const handleDropdownChange = (value) => {
		setSaveBtn(false);
		setWhatIfAnalysisId(null);
		if (value == 1) {
			setIsModalVisible(true);
		} else if (value == 2) {
			setEbitdaModalOpen(true);
		} else if (value == 3) {
			getUpdateAssetSheetData();
		// setUpdateAssetTableData(updateAssetData)
		}
	};

	const getUpdateAssetSheetData = async() => {
		const defaultsheetName = DEFAULT_SHEET_NAME[fundType];
		const basefileid = baseFile.id;
		try {
			setIsLoading(true);
			const res = await getUpdateAssetData(basefileid, defaultsheetName);
			setUpdateAssetTableData(res.data.result);
			setIsupdateAssetModalOpen(true);
		} catch (err) {
			toast.error("something went wrong");
			console.error(err);
		} finally {
			setIsLoading(false);
			setSelectedOption(0);
		}
	};

	return (
		<>

			<div style={{ display: "flex", flex: "1", alignItems: "center" }}>
				<Select
				// className={ButtonStyles.filledBtn}
					defaultValue="-- What if Analysis --"
					style={{ width: 180, borderRadius: '8px', border: '1px solid #6D6E6F' }}
					onChange={handleDropdownChange}
					value={selectedOption}
					onSelect={(value) => setSelectedOption(value)}
					options={wiaOptions[fundType]}
				/>
				{isLoading && <span style={{padding: "0 5px"}}> <LoaderSmall /></span>}
			</div>
			<div>
				{/* <AboutModal isAboutModalState={isAboutModalState} aboutModalState={aboutModalState}  /> */}
				{/* Preveiw */}
			</div>

		</>
	);
};
