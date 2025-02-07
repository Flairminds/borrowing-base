import { Select, Space } from 'antd';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router';
import { CustomButton } from '../../components/custombutton/CustomButton';
import { DynamicTableComponents } from '../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';
import { AddAdditionalInformationModal } from '../../modal/addAdditionalInformationModal/AddAdditionalInformationModal';
import { getBaseDataCellDetail, generateBaseDataFile } from '../../services/api';
import { editBaseData, getBaseFilePreviewData } from '../../services/dataIngestionApi';
import { filterPreviewData } from '../../utils/helperFunctions/filterPreviewData';
import { filterPreviewTable } from '../../utils/helperFunctions/filterPreviewTable';
import { showToast } from '../../utils/helperFunctions/toastUtils';
import styles from './BorrowingBasePreviewPage.module.css';

export const BorrowingBasePreviewPage = ({ baseFilePreviewData, setBaseFilePreviewData, previewPageId, previewFundType}) => {
	const navigate = useNavigate();
	const [mapping, setMapping] = useState({});
	const [cellDetail, setCellDetail] = useState({});
	const [isAddFieldModalOpen, setIsAddFieldModalOpen] = useState(false);
	const [triggerBBCalculation, setTriggerBBCalculation] = useState(false);
	const [obligorFliteredValue, setObligorFliteredValue] = useState([]);
	const [securityFilteredValue, setSecurityFilteredValue] = useState([]);
	const [filteredData, setFilteredData] = useState(baseFilePreviewData?.baseData?.data);

	useEffect(() => {
		let col = [];
		if (!baseFilePreviewData.reportDate) {
			showToast('info', 'No report date selected. Redirecting...');
			setTimeout(() => {
				navigate('/base-data-list');
			}, 1500);
		}
		baseFilePreviewData.baseData?.columns.forEach(c => {
			let a = baseFilePreviewData?.baseDataMapping?.find(bd => bd.bd_column_name == c.label);
			if (a) {
				col[a.bd_column_name] = `${a.rd_file_name} -> ${a.rd_sheet_name} -> ${a.rd_column_name}`;
			}
		});
		setMapping(col);
	}, [baseFilePreviewData]);

	const getCellDetail = async (rowIndex, columnKey, columnName, cellValue) => {
		const temp = {
			"title": columnName,
			"data": {
				// 'Base data column name': columnName,
				'Value': cellValue,
				'Source file name': 'Not mapped',
				'Sheet name': 'Not mapped',
				'Column name': 'Not mapped',
				'Formula': 'Not mapped'
			}
		};
		try {
			const response = await getBaseDataCellDetail({ 'ebd_id': baseFilePreviewData.infoId, 'column_key': columnKey, 'data_id': baseFilePreviewData?.baseData?.data[rowIndex]['id']['value'] });
			const detail = response?.data?.result;
			const mappingData = detail?.mapping_data;
			const t = {
				...temp.data,
				'Source file name': mappingData.file_name + mappingData.extension,
				'Sheet name': mappingData.sf_sheet_name,
				'Column name': mappingData.sf_column_name,
				'Formula': mappingData.formula ? mappingData.formula : 'Value same as source column value'
			};
			temp['data'] = t;
			const sourceData = detail?.source_data;
			if (sourceData) {

				temp['htmlRender'] = <table style={{ textAlign: 'center', margin: '15px 0' }}>
					<thead>
						{Object.keys(sourceData[0]).map((h, i) => {
							return (<th key={i} style={{ padding: '3px 10px', border: "1px solid #DCDEDE", backgroundColor: '#DCDEDE' }}>{h}</th>);
						})}
					</thead>
					<tbody>
						{sourceData.map((d, j) => {
							return (
								<tr key={j}>
									{Object.keys(d).map((key, k) => {
										return (
											<td key={k} style={{ padding: '3px', border: "1px solid #DCDEDE" }}>{d[key]}</td>);
									})}
								</tr>
							);
						})}
					</tbody>
				</table>;
			}
			setCellDetail(temp);
		} catch (error) {
			console.error(error.message);
			setCellDetail(temp);
		}
	};

	const handleBaseDataPreview = async () => {
		try {
			const previewDataResponse = await getBaseFilePreviewData(previewPageId);
			const result = previewDataResponse.data?.result;
			if (result)
				setBaseFilePreviewData({
					baseData: result?.base_data_table,
					reportDate: result?.report_date,
					baseDataMapping: result?.base_data_mapping && result.base_data_mapping,
					cardData: result?.card_data && result.card_data[0],
					otherInfo: result.other_info
				});
			setFilteredData(result?.base_data_table?.data);
		} catch (err) {
			showToast("error", err.response.data.message);
		}
	};

	const handleSaveEdit = async (rowIndex, columnkey, inputValue) => {
		const updatedData = [...baseFilePreviewData?.baseData?.data];
		const changes = [{
			id: updatedData[rowIndex].id['value'],
			[columnkey]: inputValue
		}
		];

		try {
			await editBaseData(changes);
			await handleBaseDataPreview();
			updatedData[rowIndex][columnkey] = inputValue;
			setBaseFilePreviewData({
				...baseFilePreviewData,
				'baseData': {
					...baseFilePreviewData.baseData,
					'data': updatedData
				}
			});
			setFilteredData(updatedData);
			// setBaseFilePreviewData({...BorrowingBasePreviewPage.baseData, data: updatedData});
			return { success: "failure", msg: "Update success" };
		} catch (error) {
			// showToast("error", error?.response?.data?.message || "Failed to update data");
			return { success: "failure", msg: error?.response?.data?.message || "Failed to update data" };
		}
	};

	const generateBaseData = async (e) => {
		// e.preventDefault();
		setTriggerBBCalculation(true);
		try {
			let run = false;
			if (baseFilePreviewData?.cardData['Unmapped Securities'] > 0) {
				if (confirm('The calculation will be inaccurate due to some unmapped securities. Do you want to proceed?')) {
					run = true;
				}
			} else {
				run = true;
			}
			if (run) {
				const response = await generateBaseDataFile({ 'bdi_id': baseFilePreviewData.infoId });
				const detail = response?.data;
				showToast('success', detail?.message);
			}
			setTriggerBBCalculation(false);
			return;
		} catch (error) {
			setTriggerBBCalculation(false);
			showToast('error', error.message);
		}
	};

	// const filterData = async(cardTitle) => {
	// 	if (cardTitle == 'Unmapped Securities') {
	// 		const temp = [...baseFilePreviewData?.baseData?.data];
	// 		const updatedData = temp.filter(t => !t.security_name.value);
	// 		setBaseFilePreviewData({
	// 			...baseFilePreviewData,
	// 			'baseData': {
	// 				...baseFilePreviewData.baseData,
	// 				'data': updatedData
	// 			}
	// 		});
	// 	}
	// };

	const handleObligorChange = (value) => {
		setObligorFliteredValue(value);
		const obligorFilterData = filterPreviewTable(baseFilePreviewData?.baseData?.data, value, securityFilteredValue);
		setFilteredData(obligorFilterData);
	};

	const handleSecurityChange = (value) => {
		setSecurityFilteredValue(value);
		const securityFilterData = filterPreviewTable(baseFilePreviewData?.baseData?.data, obligorFliteredValue, value );
		setFilteredData(securityFilterData);
	};


	return (
		<div className={styles.previewPage}>
			<div className={styles.tableContainer}>
				<div style={{ display: 'flex', justifyContent: 'space-between' }}>
					<div>
						<div className={styles.cardContainer}>
							{baseFilePreviewData?.cardData && Object.keys(baseFilePreviewData?.cardData).map((cardTitle, index) => (
								<div key={index} className={styles.card} title={cardTitle == 'Unmapped Securities' ? "Click to go to 'Security mapping'" : ""} onClick={cardTitle == 'Unmapped Securities' ? () => navigate('/security-mapping') : () => {}}>
									<div><b>{cardTitle}</b></div>
									<div className={styles.cardTitle}>{baseFilePreviewData?.cardData[cardTitle]}</div>
								</div>
							))}
						</div>
					</div>
					<div>
						<button onClick={(e) => generateBaseData(e)} style={{ outline: 'none', backgroundColor: '#0EB198', color: 'white', padding: '5px 10px', borderRadius: '5px', border: '0px' }}>{triggerBBCalculation ? '...Calculating' : 'Trigger BB Calculation'}</button>
						<button onClick={() => setIsAddFieldModalOpen(true)} style={{ outline: 'none', backgroundColor: '#0EB198', color: 'white', padding: '5px 10px', borderRadius: '5px', border: '0px ', margin: '0 10px' }}>Add Other Info</button>
					</div>
				</div>
				<div>
					<div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%', maxWidth: '600px', gap: '16px', padding: '5px' }}>
						<Select
							mode="multiple"
							allowClear
							style={{flex: 1}}
							placeholder="Filter by Obligor Name(s)"
							onChange={handleObligorChange}
							options={baseFilePreviewData?.baseData?.data && filterPreviewData(baseFilePreviewData?.baseData?.data, 'obligor_name')}
						/>
						<Select
							mode="multiple"
							allowClear
							style={{flex: 1}}
							placeholder="Filter by Security Name(s)"
							onChange={handleSecurityChange}
							options={baseFilePreviewData?.baseData?.data && filterPreviewData(baseFilePreviewData?.baseData?.data, 'security_name')}
						/>
					</div>
				</div>
				<div>
					<DynamicTableComponents
						data={filteredData}
						columns={baseFilePreviewData?.baseData?.columns}
						enableStickyColumns={true}
						showSettings={true}
						showCellDetailsModal={true}
						enableColumnEditing={true}
						onChangeSave={handleSaveEdit}
						getCellDetailFunc={getCellDetail}
						cellDetail={cellDetail}
						refreshDataFunction={handleBaseDataPreview}
						previewFundType={previewFundType}
					/>
				</div>
			</div>
			<AddAdditionalInformationModal
				isAddFieldModalOpen={isAddFieldModalOpen}
				setIsAddFieldModalOpen={setIsAddFieldModalOpen}
				onClose={() => setIsAddFieldModalOpen(false)}
				dataId={baseFilePreviewData.infoId}
				data={baseFilePreviewData.otherInfo}
				handleBaseDataPreview={handleBaseDataPreview}
				previewFundType={previewFundType}
			/>
		</div>
		// <div>
		//     {Object.keys(mapping)?.map(m => {
		//         return (
		//             <div>{m}</div>
		//         )
		//     })}
		// </div>
	);
};