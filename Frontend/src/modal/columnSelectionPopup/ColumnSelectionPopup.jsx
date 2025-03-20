import { Modal } from 'antd';
import { useEffect, useState } from 'preact/hooks';
import React from 'react';
import { toast } from 'react-toastify';
import ButtonStyles from '../../components/uiComponents/Button/ButtonStyle.module.css';
import { assetSelectionList, setConfigurations } from '../../services/api';
import { parametersForSelection } from '../../utils/parameterSelectionData';
import Styles from './ColumnSelectionPopup.module.css';
import { ModalComponents } from '../../components/modalComponents';

export const ColumnSelectionPopup = ({setAssetSelectionData, assetSelectionData, baseFile, columnSelectionPopupOpen, setColumnSelectionPopupOpen, fundType}) => {

	const [selectedColumns, setSelectedColumns] = useState([]);
	const [checkBoxesDisabled, setCheckBoxesDisabled] = useState(false);

	const handleCheckBoxClick = (key) => {
		setSelectedColumns((prevSelectedKeys) =>
			prevSelectedKeys.includes(key)
				? prevSelectedKeys.filter((selectedKey) => selectedKey !== key)
				: [...prevSelectedKeys, key]
		);
	};
	useEffect(() => {
		if (selectedColumns.length < 4) {
			setCheckBoxesDisabled(false);
		} else {
			setCheckBoxesDisabled(true);
		}
	}, [selectedColumns]);

	const setConfiguration = async() => {

		const payload = {
			user_id: 1,
			assets_selection_columns: selectedColumns
		};
		try {
			const res = await setConfigurations(payload);
			assestSelection();
			toast.success('Configurations Set Successfully');
		} catch (err) {
			console.error(err);
		}
		setColumnSelectionPopupOpen(false);
	};

	const handleCancel = () => {
		setColumnSelectionPopupOpen(false);
	};
	const assestSelection = async() => {
		try {
			const res = await assetSelectionList(baseFile.id);
			setAssetSelectionData(res.data.assets_list);
			setAssetSelectionData({...assetSelectionData, 'assetSelectionList': res.data
			});
			getTrendGraphData(fundType);
			setDate(null);
		} catch (err) {
			console.error(err);
		}
	};

	return (
		<>
			<Modal
				title={<ModalComponents.Title title={'Select Parameters for Asset Selection'} description={'*Select upto 4 Paramerts'} showDescription={true} />}
				centered
				open={columnSelectionPopupOpen}
				onOk={setConfiguration}
				onCancel={handleCancel}
				width={'70%'}
				footer={[
					<ModalComponents.Footer key="footer-buttons" showCancel={false} onClickSubmit={setConfiguration} submitText={'Set'} />
				]}
			>
				<>
					<div className={Styles.popUpContainer}>
						<div className={Styles.errorMessage}>{checkBoxesDisabled == true ? <>*Only 4 columns allowded</> : null }</div>
						<div className={Styles.listContainer}>
							{parametersForSelection.map((parameter, index) => (
								<>
									<div key={index} className={Styles.listItem}>
										<input disabled={checkBoxesDisabled && !selectedColumns.includes(parameter.key)} type="checkbox" style={{margin: '0px 5px'}} onClick={() => handleCheckBoxClick(parameter.key)} />
										{parameter.label}
									</div>
								</>
							))
							}
						</div>

					</div>

				</>
			</Modal>
		</>
	);
};