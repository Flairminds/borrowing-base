import { Button, Modal, Popover } from 'antd';
import React, { useState } from 'react';
import { toast } from 'react-toastify';
import ButtonStyles from '../../components/uiComponents/Button/ButtonStyle.module.css';
import { EbitdaAnalysis } from '../../services/api';
import { ParameterChange } from '../ParameterChange/ParameterChange';
import style from './UpdateParameterModal.module.css';
import { ModalComponents } from '../../components/modalComponents';

export const UpdateParameterModal = ({
	ebitdaModalOpen,
	handleCancel,
	changeParameterSubmitDisplay,
	handleParameterRadioBtn,
	apiResponseStatusParameter,
	selectedOptionUpdateValue,
	parameterList,
	setParameterList,
	loading,
	setLoading,
	baseFile,
	inputValueUntitled,
	setTablesData,
	setReportDate,
	setEbitdaModalOpen,
	setWhaIfAnalsisData,
	ebitaChangeValue,
	setWhatifAnalysisPerformed,
	setEbitaChangeValue,
	setSaveBtn,
	setInputValueUntitled,
	setSelectedOption,
	setWhatIfAnalysisId,
	setWhatIfAnalysisType
}) => {

	const [selectedIndexes, setSelectedIndexes] = useState([]);
	const [popoverVisible, setPopoverVisible] = useState(false);

	const handleEbitaAnalysis = async () => {
		setLoading(true);
		try {
			const response = await EbitdaAnalysis(baseFile.id, selectedOptionUpdateValue, parameterList.data);
			setWhatIfAnalysisId(response.data.what_if_analysis_id);
			setWhatIfAnalysisType(response.data.what_if_analysis_type);
			setTablesData(response.data);
			if (response.status === 200) {
				setTablesData(response.data);
				setReportDate(response.data.closing_date);
				setEbitdaModalOpen(false);
				toast.success(`${selectedOptionUpdateValue} Changed`);
				setWhaIfAnalsisData({
					typeOfAnalysis: `${selectedOptionUpdateValue} change value`,
					analysisValue: selectedOptionUpdateValue === "Ebitda" ? ebitaChangeValue.ebitaValue : ebitaChangeValue.leverage
				});
				setWhatifAnalysisPerformed(true);
				setEbitaChangeValue({
					ebitaValue: "",
					leverage: ""
				});
				setSaveBtn(true);
			}
		} catch (err) {
			console.error(err);
			setEbitdaModalOpen(false);
			setEbitaChangeValue({
				ebitaValue: "",
				leverage: ""
			});
		}
		setInputValueUntitled('');
		setEbitaChangeValue({
			ebitaValue: "",
			leverage: ""
		});
		setLoading(false);
		setSelectedOption(0);
	};

	const handleContinueClick = () => {
		if (selectedIndexes.length > 0) {
			setPopoverVisible(true);
			setTimeout(() => {
				setPopoverVisible(false);
			}, 3000);
		} else {
			handleEbitaAnalysis();
		}
	};

	return (
		<>
			<Modal
				title={<ModalComponents.Title title={'Update Parameters'} description={'Here you can change EBITDA or Cash leverage of any investment and perform what-if analysis'} showDescription={true} />
					// <div style={{display: "flex", flexDirection: "column"}}>
					// 	<span style={{fontWeight: '700', fontSize: '18px', padding: '0 0 1.2% 4%'}}>Update Parameters</span>
					// 	<span style={{fontWeight: "400", fontSize: "14px", color: "#4B4B4B", padding: "0 0 1.2% 4%"}}>Here you can change EBITDA or Cash leverage of any investment and do what-if analysis.</span>
					// 	<span style={{fontWeight: "500", fontSize: "14px", color: "#A7A7A7", padding: "0 0 0 4%"}}>Choose the metrics</span>
					// </div>
				}
				centered
				open={ebitdaModalOpen}
				onOk={handleContinueClick}
				onCancel={handleCancel}
				width={'70%'}
				footer={
					changeParameterSubmitDisplay === true ? (
						<div key="footer-buttons" style={{marginTop: "0px", paddingRight: "1.5rem"}}>
							<button key="back" onClick={handleCancel} className={ButtonStyles.outlinedBtn}>
								Cancel
							</button>
							<Popover
								content="Please deselect all values before continuing."
								open={popoverVisible}
								trigger={"hover"}
								placement="top"
							>
								<Button
									className={ButtonStyles.filledBtn}
									loading={loading}
									key="submit"
									type="primary"
									// disabled={selectedIndexes.length > 0}
									style={{ backgroundColor: '#0EB198' }}
									onClick={handleContinueClick}
								>
									Continue
								</Button>
							</Popover>
						</div>
					) : null
				}
			>
				<div className={style.updateParameterPopupContainer}>
					<div>
						<div style={{fontWeight: "500", fontSize: "14px"}}>Choose the metrics</div>
						<div className={style.optionDiv}>
							<label>
								<input
									name='UpdateValue'
									checked={selectedOptionUpdateValue === "Ebitda"}
									onClick={() => handleParameterRadioBtn("Ebitda")}
									type="radio"
									value="Ebitda"
								/>
								<span style={{padding: "0 0 1rem 0.1rem"}}>EBITDA</span>
							</label>
							<label>
								<input
									name='UpdateValue'
									checked={selectedOptionUpdateValue === "Leverage"}
									onClick={() => handleParameterRadioBtn("Leverage")}
									type="radio"
									value="Leverage"
								/>
								<span style={{padding: "0 0 1rem 0.1rem"}}>Leverage</span>
							</label>
						</div>
						{apiResponseStatusParameter && selectedOptionUpdateValue === "Ebitda" ? (
							<div className={style.parameterChangeContainer} >
								<span className={style.changeInfo}>Change in EBITDA</span>
								<ParameterChange selectedIndexes={selectedIndexes} setSelectedIndexes={setSelectedIndexes} parameterList={parameterList} selectedOptionUpdateValue={selectedOptionUpdateValue} setParameterList={setParameterList} />
							</div>
						) : null}
						{apiResponseStatusParameter && selectedOptionUpdateValue === "Leverage" ? (
							<div className={style.parameterChangeContainer} >
								<span className={style.changeInfo}>Change in Leverage values</span>
								<ParameterChange selectedIndexes={selectedIndexes} setSelectedIndexes={setSelectedIndexes} parameterList={parameterList} selectedOptionUpdateValue={selectedOptionUpdateValue} setParameterList={setParameterList} />
							</div>
						) : null}
					</div>
				</div>
			</Modal>
		</>
	);
};
