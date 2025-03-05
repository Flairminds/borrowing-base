import { Select, Switch, Button } from 'antd';
import React, { useState, useEffect } from 'react';
import {toast} from 'react-toastify';
import buttonStyles from '../../components/Buttons/ButtonStyle.module.css';
import { StyledSelectConcTest } from '../../components/elements/styledSelectConcTest/StyledSelectConcTest';
import { changeConcentrationTestMasterData, getConcentrationTestMasterData } from '../../services/api';
import { defaultFund, ConctestMasterdropdownValues } from '../../utils/configurations/fundsDetails';
import { convertToDropdownOptions, getConcTestChnages, styledDropdownOptions } from '../../utils/helperFunctions/concentrationMasterData';
import styles from './ConcentrationTestMaster.module.css';
import { FUND_BG_COLOR } from '../../utils/styles';

export const ConcentrationTestMaster = () => {
	const [tableData, setTableData] = useState([]);
	const [displayTableData, setDisplayTableData] = useState([]);
	const [sortedData, setSortedData] = useState([]);
	const [submitBtnLoading, setSubmitBtnLoading] = useState(false);
	const [activeRowFundData, setActiveRowFundData] = useState({
		hightlightType: "",
		hightlightIds: []
	});
	const [optionsArray, setoptionsArray] = useState([]);

	const handleDropdownChange = async(value) => {
		const res = await getConcentrationTestMasterData(value);
		const deepCopyData = JSON.parse(JSON.stringify(res.data));
		setTableData(deepCopyData);
		setDisplayTableData(deepCopyData);
	};

	const handleLimitInputChange = (e, fundId) => {
		const displaydata = JSON.parse(JSON.stringify(displayTableData.data));
		let index = -1;
		for (let i = 0; i < displaydata.length; i++) {
			if ( displaydata[i].test_id == fundId ) {
				index = i;
				break;
			}
		}
		displaydata[index].limit_percentage = e.target.value;

		setDisplayTableData((prevState) => ({
			...prevState,
			data: displaydata
		}));

		setActiveRowFundData({
			hightlightType: "editedRowsData",
			hightlightIds: [...activeRowFundData.hightlightIds, fundId]
		});
	};

	const submitChnages = async() => {
		setSubmitBtnLoading(true);
		const changes = getConcTestChnages(tableData, displayTableData);
		setActiveRowFundData({
			hightlightType: "",
			hightlightIds: []
		});
		try {
			const res = await changeConcentrationTestMasterData(changes);
			if (res.status == 200) {
				toast.success(res.data.message);
			}
			setSubmitBtnLoading(false);
		} catch (err) {
			toast.error(err.response.data.message);
			console.error(err);
			setSubmitBtnLoading(false);
		}
	};

	const onVisibilityChange = (checked, fundId) => {
		const displaydata = JSON.parse(JSON.stringify(displayTableData.data));

		let index = -1;
		for (let i = 0; i < displaydata.length; i++) {
			if (displaydata[i].test_id == fundId) {
				index = i;
				break;
			}
		}

		displaydata[index].show_on_dashboard = checked;

		setDisplayTableData((prevState) => ({
			...prevState,
			data: displaydata
		}));

		setActiveRowFundData({
			hightlightType: "editedRowsData",
			hightlightIds: [...activeRowFundData.hightlightIds, fundId]
		});
	};

	useEffect(() => {
		if (!displayTableData || displayTableData.length <= 0) return;
		console.info(displayTableData, 'test -123' );
		const sorted = [...(displayTableData?.data ?? [])]
			.sort((a, b) => b.show_on_dashboard - a.show_on_dashboard)
			.sort((a, b) => {
				if (a.show_on_dashboard === b.show_on_dashboard) {
					return a.test_name.localeCompare(b.test_name);
				}
				return 0;
			});
		setSortedData(sorted);

		const optionResult = styledDropdownOptions(displayTableData?.data);
		setoptionsArray(optionResult);
	}, [displayTableData]);

	const handleTestSelect = (value) => {
		const fundID = parseInt(value.split('||')[1]);
		setActiveRowFundData({
			hightlightType: "testHightlight",
			hightlightIds: [fundID]
		});
	};

	useEffect(() => {
		handleDropdownChange(defaultFund);
	}, []);

	return (
		<>
			<div style={{display: 'flex', width: '100%'}}>
				<div className={styles.dropDownHeading}>
					Fund Type
					<Select
						defaultValue={defaultFund}
						style={{ width: "150px", margin: '0 0.5rem'}}
						onChange={handleDropdownChange}
						options={convertToDropdownOptions(ConctestMasterdropdownValues)}
					/>
				</div>
				<div className={styles.dropDownHeading}>
					Concentration Test
					<div style={{display: 'inline-block'}}>
						<StyledSelectConcTest optionsArray={optionsArray} onChange={handleTestSelect} />
					</div>
				</div>
			</div>


			<div className={styles.tableContainer}>
				<table className={styles.table}>
					<thead className={styles.stickyHeader}>
						<tr className={styles.headRow}>
							{displayTableData?.columns?.map((column, index) => (
								<th key={index} className={styles.th}>{column.title}</th>
							))}
						</tr>
					</thead>
					<tbody>
						{sortedData?.map((row, rowIndex) => (
							<tr
								key={rowIndex}
								className={
									activeRowFundData?.hightlightIds.includes(row.test_id) ?
										activeRowFundData?.hightlightType == 'testHightlight' ?
											`${styles.testActiveRow} ${styles.td}`
											:
											`${styles.editStatusRows} ${styles.td}`
										:
										styles.td
								}
							>
								{displayTableData?.columns.map((column, colIndex) => (
									<>
										<td key={colIndex} className={styles.td}>
											{column.key == "limit_percentage" ?
												<div className={styles.inputDiv}><input className={styles.input} value={row[column.key]} onChange={(e) => handleLimitInputChange(e, row.test_id)} /><span>{row.unit == 'percentage' ? '%' : ''}</span></div>
												:
												column.key == "eligible_funds" ?
													<>
														{row[column.key]?.map((el) => (
															<span key={el} className={styles.fundNameTag} style={{backgroundColor: FUND_BG_COLOR[el]}}>{el}</span>
														))}
													</>
													:
													column.key == "show_on_dashboard" ?
														<Switch style={{zIndex: 1}} value={row[column.key]} onChange={(cheked) => onVisibilityChange(cheked, row.test_id)} />
														:
														<>{row[column.key]}</>
											}
										</td>
									</>
								))}
							</tr>
						))}
						{/* {displayTableData?.data?.map((row, rowIndex) => (
						<tr key={rowIndex} className={styles.td}>
							{displayTableData?.columns.map((column, colIndex) => (
							<>
							{!row.show_on_dashboard && <td key={colIndex} className={styles.td}>
								{column.key == "limit_percentage" ?
								<input className={styles.input} value={row[column.key]} onChange={(e) => handleLimitInputChange(e, rowIndex)} />
								:
								<>
								{row[column.key]}
								</>
								}
								{column.key == "show_on_dashboard" &&
								<Switch value={row[column.key]} onChange={(cheked) => onVisibilityChange(cheked,rowIndex)}  />}
								</td>}
							</>
							))}
						</tr>
						))} */}
					</tbody>
				</table>
			</div>

			<div className={styles.updateBtn}>
				<Button onClick={submitChnages} loading={submitBtnLoading} className={buttonStyles.filledBtn}>{submitBtnLoading ? 'Updating' : 'Update'}</Button>
			</div>

		</>
	);
};