import { useEffect } from 'preact/hooks';
import React, { useState } from 'react';
import FailTestIcon from '../../assets/ConcentrationTest/FailTestIcon.svg';
import PassTestIcon from '../../assets/ConcentrationTest/PassTestIcon.svg';
import TotalTestIcon from '../../assets/ConcentrationTest/TotalTestIcon.svg';
import upDownArrow from "../../assets/sortArrows/up-and-down-arrow.svg";
import upArrowIcon from "../../assets/sortArrows/up.svg";
import { ConcentrationTableModal } from '../../modal/concentrationTableModal/ConcentrationTableModal';
import { HairCutTestModal } from '../../modal/hairCutTestModal/HairCutTestModal';
import { TableViewModal } from '../../modal/TableView/TableViewModal';
import { getConentrationData } from '../../services/api';
import { countOccurrencesOfTest } from '../../utils/helperFunctions/CountOfTestStatus';
import { sortData } from '../../utils/helperFunctions/sortTableData';
import Styles from "./TableComponent.module.css";

const ConcentrationTestCount = ({imageSrc, testCountText, backgroundColor}) => {

	const style = {
		backgroundColor: backgroundColor,
		padding: '5px 10px',
		borderRadius: '30px',
		color: 'white',
		fontWeight: 400,
		margin: '0.3rem 0rem'
	};

	return (
		<div style={style}>
			<img style={{marginBottom: '5px', marginRight: '5px'}} src={imageSrc} alt={imageSrc} />
			{testCountText}
		</div>
	);

};



export const TableComponent = ({ data, columns, showviewMore, heading, isConcentrationTest = false, showObligationTotal = true, baseFile, setTablesData, setWhatIfAnalysisListData }) => {
	const [openModal, setOpenModal] = useState(false);
	const [displayData, setDisplayData] = useState();
	const [isHairCutTestModalOpen, setIsHairCutTestModalOpen] = useState(false);
	const [hairCutTestData, setHairCutTestData] = useState();
	const [concentrationTestTableData, setConcentrationTestTableData] = useState();
	const [concentrationTestModalOpen, setConentrationTestModalOpen] = useState(false);
	const [hairCutArray, setHairCutArray] = useState();

	const len = data && data[columns[0]]?.length;
	const dataMappingArray = Array(len > 6 && showviewMore !== false ? 6 : len).fill('');

	const [selectedSort, setSelectedSort] = useState({
		name: '',
		type: ''
	});

	const totalTests = data?.Result?.length;
	const passedTests = countOccurrencesOfTest(data?.Result, 'Pass');
	const failedTests = countOccurrencesOfTest(data?.Result, 'Fail');


	useEffect(() => {
		if (data) {
			setDisplayData(data);
		}
	}, [data]);

	const ModalOpen = () => {
		setOpenModal(true);
	};

	const handleHairCutTestModal = async() => {
		try {
			const res = await getConentrationData(1, baseFile.id);
			setHairCutTestData(res.data.table);
			setIsHairCutTestModalOpen(true);
		} catch (err) {
			console.error(err);
		}
	};

	const handleSortArrowClick = (columnName) => {
		if (selectedSort.name == columnName) {
			if (selectedSort.type == 'asc') {
				const sortedData = sortData(data, columnName, 'desc');
				setDisplayData(sortedData);
				setSelectedSort({name: columnName, type: "desc"});
			} else if (selectedSort.type == 'desc') {
				setDisplayData(data);
				setSelectedSort({name: columnName, type: "nosort"});
			} else {
				const sortedData = sortData(data, columnName, 'asc');
				setDisplayData(sortedData);
				setSelectedSort({name: columnName, type: "asc"});
			}
		} else {
			const sortedData = sortData(data, columnName, 'asc');
			setDisplayData(sortedData);
			setSelectedSort({name: columnName, type: "asc"});
		}

	};

	return (
		<div>
			{
				!isConcentrationTest ?
					<h5 className='my-3'>{heading}</h5>
					:
					<div style={{display: 'flex', gap: 5}}>
						{/* <span style={{fontWeight: '500', fontSize: '16px', padding: '0 0 0 3%'}}>Concentration Test</span> */}
						<span style={{fontSize: '1.5rem', margin: '0rem 1rem'}} >{heading}</span>
						{totalTests !== undefined && totalTests !== null &&
            <ConcentrationTestCount backgroundColor="#6873C7" testCountText={totalTests} imageSrc={TotalTestIcon} />
						}
						{
							passedTests !== undefined && passedTests !== null &&
            <ConcentrationTestCount backgroundColor="#248900" testCountText={passedTests} imageSrc={PassTestIcon} />
						}
						{failedTests !== undefined && failedTests !== null &&
            <ConcentrationTestCount backgroundColor="#EB5757" testCountText={failedTests} imageSrc={FailTestIcon} />
						}
					</div>
			}
			<div className={Styles.tableContainer}>
				{dataMappingArray && Object.keys(dataMappingArray).length > 0 ? (
					<table className={Styles.table}>
						<thead>
							<tr className={Styles.headRow}>
								{columns?.map((columnName, index) => (
									<>
										{columnName != 'Result' ?
											(
												<th key={index} className={Styles.th}>
													{columnName}
													{
														selectedSort.name == columnName && selectedSort.type == 'asc' ?
															<img onClick={() => handleSortArrowClick(columnName)} style={{ paddingLeft: "5px", paddingBottom: "2px", margin: '0px 5px' }} src={upArrowIcon} alt="up" />
															:
															selectedSort.name == columnName && selectedSort.type == 'desc' ?
																<img onClick={() => handleSortArrowClick(columnName)} style={{ paddingLeft: "5px", paddingBottom: "2px", transform: "rotate(180deg)", margin: '0px 5px' }} src={upArrowIcon} alt="up" />
																:
																<img onClick={() => handleSortArrowClick(columnName)} style={{ paddingLeft: "5px", paddingBottom: "2px", height: '13px', width: '14px' }} src={upDownArrow} alt="up" />
													}
												</th>
											) : null
										}
									</>
								))}
							</tr>
						</thead>
						<tbody>
							{dataMappingArray?.map((el, i) => (
								<tr key={i}>
									{columns?.map((ed, j) => (
										<>
											{displayData && displayData[ed] ? (
												showObligationTotal ?
													<>

														{ed == "Actual" && displayData['Result'][i]?.data == "Fail" ? (
															<td
																className={`${Styles.td} ${Styles.failDiv}`}
																// onClick={handleHairCutTestModal}
															>
																<div>
																	{displayData[ed][i]?.data}
																</div>
															</td>
														)
															:
															ed == "Actual" && displayData['Result'][i]?.data == "Pass" ? (
																<td
																	className={`${Styles.td} ${Styles.passDiv}`}
																	// onClick={handleHairCutTestModal}
																>
																	<div>
																		{displayData[ed][i]?.data}
																	</div>
																</td>
															)
																:
																ed == "Actual" && displayData['Result'][i]?.data == "N/A" ? (
																	<td
																		className={`${Styles.td} ${Styles.naDatadiv}`}
																		// onClick={handleHairCutTestModal}
																	>
																		<div>
																			{displayData[ed][i]?.data}
																		</div>
																	</td>
																)
																	:
																	ed == "Actual" ? (
																		<td
																			className={`${Styles.td} ${Styles.resultDiv}`}
																			// onClick={handleHairCutTestModal}
																		>
																			<div>
																				{displayData[ed][i]?.data}
																			</div>
																		</td>
																	)
																		:
																		ed != 'Result' ?
																			(<td key={j} className={Styles.td}>
																				{displayData[ed][i]?.data}
																			</td>)
																			:
																			null
														}
													</>

													:
													( i != len - 1 ?
														<td key={j} className={Styles.td}>
															{displayData[ed][i]?.data}
														</td>
														: null
													)
											) : ''}
										</>
									))}
								</tr>
							))}
							{(len >= 8 && showviewMore !== false) && (
								<tr className={Styles.tr}>
									<td colSpan={columns.length}>
										<button style={{ border: "none", backgroundColor: "transparent", color: "#3B7DDD", textDecoration: "underline", margin: '0.3rem 0.2rem' }}
											onClick={ModalOpen}>
											View other +{data[columns[0]].length - 6}
										</button>
										<TableViewModal setOpenModal={setOpenModal} openModal={openModal} data={data} columns={columns} heading={heading} />
									</td>
								</tr>
							)}
						</tbody>
						{data && data?.Total ?

							<tr className={Styles.lastRow}>
								{columns?.map((ed, k) => (
									<td key={k} className={Styles.totalRow}>
										{data[ed] && data ? data?.Total?.data[ed] : null}
									</td>
								)
								)}
							</tr>
							: null
						}
					</table>
				) : (
					<p className={Styles.PTag}>No data available to display.</p>
				)}
			</div>
			<HairCutTestModal
				isHairCutTestModalOpen={isHairCutTestModalOpen}
				setIsHairCutTestModalOpen={setIsHairCutTestModalOpen}
				hairCutTestData={hairCutTestData}
				setHairCutTestData={setHairCutTestData}
				baseFile={baseFile}
				setConcentrationTestTableData={setConcentrationTestTableData}
				setConentrationTestModalOpen={setConentrationTestModalOpen}
				setHairCutArray={setHairCutArray}
				concentrationTestTableData={concentrationTestTableData}
			/>

			<ConcentrationTableModal
				concentrationTestModalOpen={concentrationTestModalOpen}
				concentrationTestTableData={concentrationTestTableData}
				setConcentrationTestTableData={setConcentrationTestTableData}
				setConentrationTestModalOpen={setConentrationTestModalOpen}
				setIsHairCutTestModalOpen={setIsHairCutTestModalOpen}
				baseFile={baseFile}
				setHairCutTestData={setHairCutTestData}
				hairCutArray={hairCutArray}
				setTablesData={setTablesData}
				setWhatIfAnalysisListData={setWhatIfAnalysisListData}
			/>

		</div>
	);
};
