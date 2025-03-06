import { Button, Modal } from 'antd';
import { useState } from 'preact/hooks';
import React from 'react';
import FailTestIcon from '../../assets/ConcentrationTest/FailTestIcon.svg';
import PassTestIcon from '../../assets/ConcentrationTest/PassTestIcon.svg';
import TotalTestIcon from '../../assets/ConcentrationTest/TotalTestIcon.svg';
import ButtonStyles from '../../components/uiComponents/Button/ButtonStyle.module.css';
import { TableComponent } from '../../components/Tables/TableComponent';
import { getConentrationData, lockHairCutTestData } from '../../services/api';
import { countOccurrencesOfTest } from '../../utils/helperFunctions/CountOfTestStatus';
import { ConcentrationTestConfirmationModal } from '../concentrationTestConfirmationModal/ConcentrationTestConfirmationModal';
import Styles from './ConcentrationTableModal.module.css';
import { ModalComponents } from '../../components/modalComponents';

const ConcentrationTestCount = ({imageSrc, testCountText, backgroundColor}) => {

	const style = {
		backgroundColor: backgroundColor,
		padding: '5px 10px',
		borderRadius: '30px',
		color: 'white',
		fontWeight: 400
	};

	return (
		<div style={style}>
			<img className={Styles.image} src={imageSrc} alt={imageSrc} />
			{testCountText}
		</div>
	);

};


export const ConcentrationTableModal = ({
	baseFile,
	concentrationTestModalOpen,
	setConentrationTestModalOpen,
	setConcentrationTestTableData,
	concentrationTestTableData,
	showObligationTotal = true,
	hairCutArray,
	setIsHairCutTestModalOpen,
	setHairCutTestData,
	setTablesData,
	setWhatIfAnalysisListData
}) => {
	const columns = concentrationTestTableData?.columns[0]?.data;
	const len = concentrationTestTableData && concentrationTestTableData[columns[0]]?.length;
	const dataMappingArray = Array(len).fill('');
	const [confirmationModalOpen, setConfirmationModalOpen] = useState(false);

	const handleCancel = () => {
		setConentrationTestModalOpen(false);
	};

	const totalTests = concentrationTestTableData?.Result?.length;
	const passedTests = countOccurrencesOfTest(concentrationTestTableData?.Result, 'Pass');
	const failedTests = countOccurrencesOfTest(concentrationTestTableData?.Result, 'Fail');

	const handleHairCutTestModal = async() => {
		const hairCutpayloadArray = hairCutArray.map(el => Object.values(el)[0]);
		try {
			const res = await getConentrationData(1, baseFile.id, hairCutpayloadArray);
			setHairCutTestData(res.data.table);
			setIsHairCutTestModalOpen(true);
		} catch (err) {
			console.error(err);
		}
		setConentrationTestModalOpen(false);
	};

	return (
		<>
			<Modal
				title={
					<>
						<div className={Styles.titlecontainer}>
							<span className={Styles.title}>Concentration Test</span>
							<ConcentrationTestCount backgroundColor="#6873C7" testCountText={totalTests} imageSrc={TotalTestIcon} />
							<ConcentrationTestCount backgroundColor="#248900" testCountText={passedTests} imageSrc={PassTestIcon} />
							<ConcentrationTestCount backgroundColor="#EB5757" testCountText={failedTests} imageSrc={FailTestIcon} />
						</div>
					</>
				}
				centered
				open={concentrationTestModalOpen}
				onCancel={handleCancel}
				width={'70%'}
				footer={[<ModalComponents.Footer key='footer-buttons' onClickCancel={handleCancel} onClickSubmit={() => setConfirmationModalOpen(true)} submitText={'Lock'} />]}
			>
				<div className={Styles.tableContainer}>
					<table className={Styles.table}>
						<thead>
							<tr className={Styles.headRow}>
								{columns?.map((columnName, index) => (
									columnName !== 'Result' && columnName !== 'Previous Result' ? (
										<th key={index} className={`${Styles.th} ${columnName === 'Actual' ? Styles.minWidth16vh : ''}`}>
											{columnName}
										</th>
									) : null
								))}
							</tr>
						</thead>
						<tbody>
							{dataMappingArray?.map((el, i) => (
								<tr key={i}>
									{columns?.map((ed, j) => (
										concentrationTestTableData && concentrationTestTableData[ed] ? (
											showObligationTotal ? (
												<>
													{ed === "Actual" && concentrationTestTableData['Result'][i]?.data === "Fail" ? (
														<td className={`${Styles.td} ${Styles.failDiv}`} onClick={handleHairCutTestModal}>
															<div>
																{concentrationTestTableData[ed][i]?.data}
															</div>
															{concentrationTestTableData['Previous Result'] ?
																<p className={`${Styles.prevActualData} ${concentrationTestTableData['Previous Result'][i]?.data == "Fail" ? Styles.failprevActual : null} ${concentrationTestTableData['Previous Result'][i]?.data == "Pass" ? Styles.passprevActual : null}`}>
																	{concentrationTestTableData['Previous Actual'][i]?.data}
																</p>
																:
																null
															}
														</td>
													)
														:
														ed == "Actual" && concentrationTestTableData['Result'][i]?.data == "Pass" ? (
															<td className={`${Styles.td} ${Styles.passDiv}`} onClick={handleHairCutTestModal}>
																<div>
																	{concentrationTestTableData[ed][i]?.data}
																</div>
																{concentrationTestTableData['Previous Result'] ?
																	<p className={`
                                ${Styles.prevActualData} 
                                ${concentrationTestTableData['Previous Result'][i]?.data == "Fail" ? Styles.failprevActual : null} 
                                ${concentrationTestTableData['Previous Result'][i]?.data == "Pass" ? Styles.passprevActual : null} 
                                ${concentrationTestTableData['Previous Result'][i]?.data == "N/A" ? Styles.naprevActual : null}`
																	}>
																		{concentrationTestTableData['Previous Actual'][i]?.data}
																	</p>
																	:
																	null
																}
															</td>
														)
															:
															ed == "Actual" && concentrationTestTableData['Result'][i]?.data == "N/A" ? (
																<td className={`${Styles.td} ${Styles.naDatadiv}`} onClick={handleHairCutTestModal}>
																	<div>
																		{concentrationTestTableData[ed][i]?.data}
																	</div>
																	{concentrationTestTableData['Previous Result'] ?
																		<p className={`
                                    ${Styles.prevActualData} 
                                    ${concentrationTestTableData['Previous Result'][i]?.data == "Fail" ? Styles.failprevActual : null} 
                                    ${concentrationTestTableData['Previous Result'][i]?.data == "Pass" ? Styles.passprevActual : null} 
                                    ${concentrationTestTableData['Previous Result'][i]?.data == "N/A" ? Styles.naprevActual : null}`
																		}>
																			{concentrationTestTableData['Previous Actual'][i]?.data}
																		</p>
																		:
																		null
																	}
																</td>
															)

																: ed === "Actual" ? (
																	<td className={`${Styles.td} ${Styles.resultDiv}`} onClick={handleHairCutTestModal}>
																		<div>
																			{concentrationTestTableData[ed][i]?.data}
																		</div>
																	</td>
																) : ed === "Previous Actual" && concentrationTestTableData['Previous Result'][i]?.data === "Fail" ? (
																	<td className={`${Styles.td} ${Styles.prevFailDiv}`} onClick={handleHairCutTestModal}>
																		<div>
																			{concentrationTestTableData[ed][i]?.data}
																		</div>
																	</td>
																) : ed === "Previous Actual" && concentrationTestTableData['Previous Result'][i]?.data === "Pass" ? (
																	<td className={`${Styles.td} ${Styles.prevPassDiv}`} onClick={handleHairCutTestModal}>
																		<div>
																			{concentrationTestTableData[ed][i]?.data}
																		</div>
																	</td>
																) : ed === "Previous Actual" ? (
																	<td className={`${Styles.td} ${Styles.resultDiv}`} onClick={handleHairCutTestModal}>
																		<div>
																			{concentrationTestTableData[ed][i]?.data}
																		</div>
																	</td>
																) : ed !== 'Result' && ed !== 'Previous Result' ? (
																	<td key={j} className={Styles.td}>
																		{concentrationTestTableData[ed][i]?.data}
																	</td>
																) : null}
												</>
											) : (i !== len - 1 ? (
												<td key={j} className={Styles.td}>
													{concentrationTestTableData[ed][i]?.data}
												</td>
											) : null)
										) : ''
									))}
								</tr>
							))}
						</tbody>
					</table>
				</div>
			</Modal>

			<ConcentrationTestConfirmationModal
				confirmationModalOpen={confirmationModalOpen}
				setConfirmationModalOpen={setConfirmationModalOpen}
				baseFile={baseFile}
				hairCutArray={hairCutArray}
				setTablesData={setTablesData}
				setConentrationTestModalOpen={setConentrationTestModalOpen}
				setWhatIfAnalysisListData={setWhatIfAnalysisListData}
			/>
		</>
	);
};
