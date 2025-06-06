import { Select, Space } from 'antd';
import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router';
import { DynamicTableComponents } from '../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';
import { AddAdditionalInformationModal } from '../../modal/addAdditionalInformationModal/AddAdditionalInformationModal';
import { getBaseDataCellDetail, generateBaseDataFile } from '../../services/api';
import { editBaseData, getBaseFilePreviewData } from '../../services/dataIngestionApi';
import { filterPreviewData } from '../../utils/helperFunctions/filterPreviewData';
import { filterPreviewTable } from '../../utils/helperFunctions/filterPreviewTable';
import { fmtDisplayVal } from '../../utils/helperFunctions/formatDisplayData';
import { showToast } from '../../utils/helperFunctions/toastUtils';
import styles from './BorrowingBasePreviewPage.module.css';
import { FileUploadModal } from '../../modal/addMoreSecurities/FileUploadModal';
import { PAGE_ROUTES } from '../../utils/constants/constants';
import { UIComponents } from '../../components/uiComponents';
import { ShowEmptyBasedDataValues } from '../../modal/showEmptyBasedDataValues/ShowEmptyBasedDataValues';
import { PersistBaseDataModal } from '../../modal/PresistBaseData/PresistBaseDataModal';
import { VAEModal } from '../../modal/VAEModal/VAEModal';
import { PCOFCashDataModal } from '../../modal/PCOFCashDataModal/PCOFCashDataModal';



export const BorrowingBasePreviewPage = ({ baseFilePreviewData, setBaseFilePreviewData, previewPageId, previewFundType, setPreviewFundType, setTablesData, setPreviewPageId, getborrowingbasedata}) => {
	const navigate = useNavigate();
	// const { infoId } = useParams();
	const [mapping, setMapping] = useState({});
	const [cellDetail, setCellDetail] = useState({});
	const [isAddFieldModalOpen, setIsAddFieldModalOpen] = useState(false);
	const [isShowEmptyBaseDataModalOpen, setIsShowEmptyBaseDataModalOpen] = useState(false);
	// const [triggerBBCalculation, setTriggerBBCalculation] = useState(false);
	const [col1FilteredValue, setCol1FilteredValue] = useState([]);
	const [col2FilteredValue, setCol2FilteredValue] = useState([]);
	const [triggerBBCalculation, setTriggerBBCalculation] = useState(false);
	const [filteredData, setFilteredData] = useState(baseFilePreviewData?.baseData?.data);
	const [selectedFiles, setSelectedFiles] = useState([]);
	const [isOpenFileUpload, setIsOpenFileUpload] = useState(false);
	const [addsecFiles, setAddsecFiles] = useState([]);
	const [loading, setLoading] = useState(false);
	const [isPresistBaseModalVisible, setIsPresistBaseModalVisible] = useState(false);
	const [showVAEModal, setShowVAEModal] = useState(false);
	const [showPCOFCashModal, setShowPCOFCashModal] = useState(false);


	const {infoId} = useParams();

	const showModal = () => {
		setIsOpenFileUpload(true);
	};

	const handleCancel = () => {
		setIsOpenFileUpload(false);
	};

	// console.log("infoId", infoId);

	useEffect(() => {
		let col = [];

		if (!baseFilePreviewData.reportDate) {
			if (!infoId) {
				showToast('info', 'No report date selected. Redirecting...');
				setTimeout(() => {
					navigate('/base-data-list');
				}, 1500);
			} else {
				setPreviewPageId(infoId);
				handleBaseDataPreview(infoId);
			}
		}
		baseFilePreviewData.baseData?.columns.forEach(c => {
			let a = baseFilePreviewData?.baseDataMapping?.find(bd => bd.bd_column_name == c.label);
			if (a) {
				col[a.bd_column_name] = `${a.rd_file_name} -> ${a.rd_sheet_name} -> ${a.rd_column_name}`;
			}
		});
		setMapping(col);
	}, [baseFilePreviewData]);

	const getCellDetail = async (rowId, columnKey, columnName, cellValue) => {
		const temp = {
			"title": columnName,
			"data": {
				// 'Base data column name': columnName,
				'Current Value': fmtDisplayVal(cellValue),
				'Source file name': 'Not mapped',
				'Sheet name': 'Not mapped',
				'Column name': 'Not mapped',
				'Formula': 'Not mapped'
			}
		};
		try {
			const response = await getBaseDataCellDetail({ 'ebd_id': baseFilePreviewData.infoId || infoId, 'column_key': columnKey, 'data_id': rowId });
			const detail = response?.data?.result;
			const mappingData = detail?.mapping_data;
			let t = {
				...temp.data
			};
			if (!detail.is_manual) {
				t = {
					...t,
					'Source file name': mappingData.file_name + mappingData.extension,
					'Sheet name': mappingData.sf_sheet_name,
					'Column name': mappingData.sf_column_name,
					'Formula': mappingData.formula ? mappingData.formula : 'Value same as source column value'
				};
			} else {
				t = {
					...t,
					'Source file name': 'Manually added data',
					'Sheet name': undefined,
					'Column name': undefined,
					'Formula': undefined
				};
			}
			temp['data'] = t;
			const sourceData = detail?.source_data;
			if (sourceData) {

				temp['htmlRender'] = <>
					<p style={{ fontWeight: 'bold', textAlign: 'Left', margin: '15px 0 5px' }}>Source File Value</p>
					<table style={{ textAlign: 'center', margin: '5px 0 15px' }}>
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
												<td key={k} style={{ padding: '3px', border: "1px solid #DCDEDE" }}>{fmtDisplayVal(d[key])}</td>);
										})}
									</tr>
								);
							})}
						</tbody>
					</table>
				</>;
			}
			setCellDetail(temp);
		} catch (error) {
			console.error(error.message);
			setCellDetail(temp);
		}
	};

	const handleBaseDataPreview = async (previewId = null) => {
		try {
			setLoading(true);
			const previewpageId = previewId ? previewId : previewPageId;
			const previewDataResponse = await getBaseFilePreviewData(previewpageId);
			const result = previewDataResponse.data?.result;
			if (result)
				setBaseFilePreviewData({
					baseData: result?.base_data_table,
					reportDate: result?.report_date,
					baseDataMapping: result?.base_data_mapping && result.base_data_mapping,
					cardData: result?.card_data && result.card_data[0],
					otherInfo: result.other_info,
					fundType: result?.fund_type,
					infoId: result?.other_info?.extraction_info_id
				});
			setPreviewFundType(result?.fund_type);
			setFilteredData(result?.base_data_table?.data);
			setLoading(false);
		} catch (err) {
			setLoading(false);
			showToast("error", err.response.data.message);
		}
	};

	const handleSaveEdit = async (rowIndex, columnkey, inputValue, id) => {
		const updatedData = [...filteredData];
		const changes = [{
			id: id,
			[columnkey]: inputValue,
			fundType: previewFundType
		}
		];

		try {
			await editBaseData(changes);
			// await handleBaseDataPreview();
			updatedData[rowIndex][columnkey] = inputValue;
			// setBaseFilePreviewData({
			// 	...baseFilePreviewData,
			// 	'baseData': {
			// 		...baseFilePreviewData.baseData,
			// 		'data': updatedData
			// 	}
			// });
			setFilteredData(updatedData);
			// setBaseFilePreviewData({...BorrowingBasePreviewPage.baseData, data: updatedData});
			return { success: true, msg: "Update success" };
		} catch (error) {
			// showToast("error", error?.response?.data?.message || "Failed to update data");
			return { success: false, msg: error?.response?.data?.message || "Failed to update data" };
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

	const handleCol1Change = (value) => {
		setCol1FilteredValue(value);
		const col1FilterData = filterPreviewTable(baseFilePreviewData?.baseData?.data, value, col2FilteredValue, previewFundType);
		setFilteredData(col1FilterData);
	};

	const handleCol2Change = (value) => {
		setCol2FilteredValue(value);
		const securityFilterData = filterPreviewTable(baseFilePreviewData?.baseData?.data, col1FilteredValue, value, previewFundType);
		setFilteredData(securityFilterData);
	};

	const filterSelections = {
		'PFLT': [{
			placeholder: "Filter by Obligor Name(s)",
			onChange: handleCol1Change,
			options: baseFilePreviewData?.baseData?.data && filterPreviewData(baseFilePreviewData?.baseData?.data, 'obligor_name'),
			value: col1FilteredValue
		}, {
			placeholder: "Filter by Security Name(s)",
			onChange: handleCol2Change,
			options: baseFilePreviewData?.baseData?.data && filterPreviewData(baseFilePreviewData?.baseData?.data, 'security_name'),
			value: col2FilteredValue
		}],
		'PCOF': [{
			placeholder: "Filter by Investment Name(s)",
			onChange: handleCol1Change,
			options: baseFilePreviewData?.baseData?.data && filterPreviewData(baseFilePreviewData?.baseData?.data, 'investment_name'),
			value: col1FilteredValue
		}, {
			placeholder: "Filter by Issuer(s)",
			onChange: handleCol2Change,
			options: baseFilePreviewData?.baseData?.data && filterPreviewData(baseFilePreviewData?.baseData?.data, 'issuer'),
			value: col2FilteredValue
		}],
		'PSSL': [{
			placeholder: "Filter by Borrower(s)",
			onChange: handleCol1Change,
			options: baseFilePreviewData?.baseData?.data && filterPreviewData(baseFilePreviewData?.baseData?.data, 'borrower'),
			value: col1FilteredValue
		}]
	};

	const handleConfirmEmptyBaseModal = () => {
		setIsShowEmptyBaseDataModalOpen(false);
		if (previewFundType == 'PCOF') {
			const cashData = filteredData.find(f => f.investment_name?.value == 'Cash');
			if (!cashData || ((cashData.investment_cost.meta_info && !cashData.investment_cost.value) || (!cashData.investment_cost.meta_info && !cashData.investment_cost)) || ((cashData.investment_external_valuation.meta_info && !cashData.investment_external_valuation.value) || (!cashData.investment_external_valuation.meta_info && !cashData.investment_external_valuation)) || ((cashData.investment_par.meta_info && !cashData.investment_par.value) || (!cashData.investment_par.meta_info && !cashData.investment_par))) {
				setShowPCOFCashModal(true);
			} else {
				setIsAddFieldModalOpen(true);
			}
		} else setIsAddFieldModalOpen(true);
	};

	const handleCancelEmptyBaseModal = () => {
		setIsShowEmptyBaseDataModalOpen(false);
	};


	return (
		<div className={styles.previewPage}>
			{loading ? <UIComponents.Loader /> :
				<div className={styles.tableContainer}>
					<div style={{ display: 'flex', justifyContent: 'space-between' }}>
						<div>
							<div className={styles.cardContainer}>
								{baseFilePreviewData?.cardData && Object.keys(baseFilePreviewData?.cardData).map((cardTitle, index) => (
									<div key={index} className={styles.card} title={cardTitle == 'Unmapped Securities' ? "Click to go to 'Security mapping'" : ""} onClick={cardTitle == 'Unmapped Securities' ? () => navigate('/configuration?tab=security_mapping') : () => {}}>
										<div>{cardTitle}</div>
										<div className={styles.cardTitle}><b>{fmtDisplayVal(baseFilePreviewData?.cardData[cardTitle], 0)}</b></div>
									</div>
								))}
							</div>
						</div>
						<div>
							<UIComponents.Button onClick={showModal} isFilled={true} text='Bulk Update' btnDisabled={previewFundType == 'PSSL' ? false : false} title={previewFundType == 'PSSL' ? 'Work in progress' : 'Add more securities data in the base data'} />
							{previewFundType == 'PSSL' && <UIComponents.Button onClick={() => setShowVAEModal(true)} isFilled={true} text='VAE' title={previewFundType == 'PSSL' ? 'Work in progress' : 'Add more securities data in the base data'} />}
							{/* <UIComponents.Button onClick={() => setIsPresistBaseModalVisible(true)} isFilled={true} text='Compare And Update Previous Base Data'/> */}
							<UIComponents.Button onClick={() => setIsShowEmptyBaseDataModalOpen(true)} isFilled={true} text='Trigger Calculation' loading={triggerBBCalculation} loadingText={'Calculating'} btnDisabled={previewFundType == 'PSSL' ? false : false} />
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
							filterSelections={filterSelections[baseFilePreviewData.fundType]}
							showFilter={true}
							visibleSortHeader={true}
						/>
					</div>
				</div>}
			<AddAdditionalInformationModal
				isAddFieldModalOpen={isAddFieldModalOpen}
				setIsAddFieldModalOpen={setIsAddFieldModalOpen}
				onClose={() => setIsAddFieldModalOpen(false)}
				dataId={baseFilePreviewData.infoId || infoId}
				setTriggerBBCalculation={setTriggerBBCalculation}
				data={baseFilePreviewData.otherInfo}
				previewFundType={previewFundType}
				selectedFiles={selectedFiles}
				setSelectedFiles={setSelectedFiles}
				baseFilePreviewData= {baseFilePreviewData}
				setBaseFilePreviewData={setBaseFilePreviewData}
				previewPageId= {previewPageId}
				setTablesData= {setTablesData}
				getborrowingbasedata= {getborrowingbasedata}
				setLoading= {setLoading}
			/>
			<FileUploadModal
				data={filteredData}
				columns={baseFilePreviewData?.baseData?.columns}
				previewFundType={previewFundType}
				isOpenFileUpload={isOpenFileUpload}
				handleCancel={handleCancel}
				handleBaseDataPreview={handleBaseDataPreview}
				dataId={baseFilePreviewData.infoId || infoId}
				reportId={baseFilePreviewData.reportDate}
				addsecFiles={addsecFiles}
				setAddsecFiles={setAddsecFiles}
			/>
			<ShowEmptyBasedDataValues
				visible={isShowEmptyBaseDataModalOpen}
				columnNames={baseFilePreviewData?.baseData?.columns}
				data={filteredData}
				previewFundType={previewFundType}
				onConfirm={handleConfirmEmptyBaseModal}
				onCancel={handleCancelEmptyBaseModal}
			/>
			<PCOFCashDataModal visible={showPCOFCashModal} onCancel={() => setShowPCOFCashModal(false)} onConfirm={() => {
				setShowPCOFCashModal(false); setIsAddFieldModalOpen(true);
			}} />
			<PersistBaseDataModal
				visible={isPresistBaseModalVisible}
				onClose={() => setIsPresistBaseModalVisible(false)}
			/>
			{previewFundType == 'PSSL' && <VAEModal visible={showVAEModal} onCancel={() => setShowVAEModal(false)} />}
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