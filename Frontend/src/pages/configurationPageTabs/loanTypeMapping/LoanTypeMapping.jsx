import { CloseCircleOutlined } from '@ant-design/icons';
import { Select } from 'antd';
import React, { useEffect, useState } from 'react';
import { DndProvider, useDrag, useDrop } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import { toast } from 'react-toastify';
import { UIComponents } from '../../../components/uiComponents';
import { AddLoanTypeMasterModal } from '../../../modal/configurationPageModals/addLoanTypeMasterModal/AddLoanTypeMasterModal';
import { deleteLoanTypeMapping, getLoanTypeMappingData, updateLoanTypeMapping } from '../../../services/dataIngestionApi';
import { fundOptionsArray } from '../../../utils/constants/constants';
import { showToast } from '../../../utils/helperFunctions/toastUtils';
import styles from './LoanTypeMapping.module.css';

const ItemType = "ITEM";

const DraggableItem = ({ item, itemAccessKey, title,getloanTypeMappingInfo,  selectedFundType }) => {
	const [{ isDragging }, drag] = useDrag(() => ({
		type: ItemType,
		item: { name: item },
		collect: (monitor) => ({
			isDragging: !!monitor.isDragging()
		})
	}));

	const handleDeleteMapping = async (deleteItem) => {
		try {
			const res = await deleteLoanTypeMapping(deleteItem.mapping_id);
			showToast('success', res.data.message);
			getloanTypeMappingInfo(selectedFundType);
		} catch (err) {
			console.error(err);
		}
	};

	return (
		<div
			ref={drag}
			style={{
				padding: "3px 7px",
				margin: "4px",
				backgroundColor: "#d3d3d3",
				cursor: "grab",
				opacity: isDragging ? 0.5 : 1,
				minWidth: "175px",
				borderRadius: '5px'
				// maxHeight: "35px"
			}}
		>
			{item && item[itemAccessKey]}
			{title != 'unmapped_loan_types' && <CloseCircleOutlined style={{margin: "0px 10px"}} onClick={() => handleDeleteMapping(item)} />}
		</div>
	);
};

const DroppableList = ({ title, items, allLists, setAllLists, itemAccessKey, getloanTypeMappingInfo, selectedFundType }) => {
	const [{ isOver }, drop] = useDrop(() => ({
		accept: ItemType,
		drop: async (draggedItem) => {
			if (title == 'unmapped_loan_types') return;
			console.info("master", title, items, '//', draggedItem);

			let mappingData = {};
			if (draggedItem.name.mapping_id) {
				mappingData = {
					'master_loan_type_id': title.master_loan_type_id,
					'mapping_id': draggedItem.name.mapping_id
				};
			} else {
				mappingData = {
					'master_loan_type_id': title.master_loan_type_id,
					'loan_type': draggedItem.name.unmapped_loan_type
				};
			}

			try {
				const res = await updateLoanTypeMapping(mappingData);
				showToast('success', res.data.message);
				getloanTypeMappingInfo(selectedFundType);
			} catch (err) {
				console.error(err);
				toast.error(err?.response?.data?.message);
			}
		},
		collect: (monitor) => ({
			isOver: !!monitor.isOver()
		})
	}));

	return (
		<div
			ref={drop}
			className={title == "unmapped_loan_types" ? styles.unmappedLoantypeList : styles.mappedTypesList}
		>
			{items && items.length > 0 ? (
				items.map((item) => (
					<DraggableItem key={item[itemAccessKey]} itemAccessKey={itemAccessKey} item={item} title={title} getloanTypeMappingInfo={getloanTypeMappingInfo} selectedFundType={selectedFundType} />
				))
			) : (
				<div className={styles.emptyDiv}>
					{title == "unmapped_loan_types" ? <> No data </> : <>Drop items here</>}
				</div>
			)}
		</div>
	);
};

export const LoanTypeMapping = () => {

	const [loanTypeMappingData, setLoanTypeMappingData] = useState(null);
	const [selectedFundType, setSelectedFundType] = useState("PFLT");
	const [addMasterPopupOpen, setAddMasterPopupOpen] = useState(false);


	const getloanTypeMappingInfo = async(fund) => {
		try {
			const res = await getLoanTypeMappingData(fund);
			setLoanTypeMappingData(res.data.result);
		} catch (err) {
			console.error(err);
			showToast('error', err?.response?.data?.message);
		}
	};

	const handleFundChange = (value) => {

		let fundType = "";
		if (value == 1) {
			fundType = "PCOF";
		} else if (value === 2) {
			fundType = "PFLT";
		}

		setSelectedFundType(fundType);
		getloanTypeMappingInfo(fundType);
	};


	useEffect(() => {
		getloanTypeMappingInfo(selectedFundType);
	}, []);

	return (
		<div className={styles.loanTypePageContainer}>
			<div className={styles.mappingTitle}>
				<div className={styles.cardContainer}>
					<div className={styles.loanTypeCard}>
						<div><b>All Loan Types</b></div>
						<div className={styles.cardTitle}>{loanTypeMappingData?.unmapped_loan_types.length + loanTypeMappingData?.mapped_loan_types.length}</div>
					</div>
					<div className={styles.loanTypeCard}>
						<div><b>Unmapped Loan Types</b></div>
						<div className={styles.cardTitle}>{loanTypeMappingData?.unmapped_loan_types.length}</div>
					</div>
				</div>
				<div className={styles.dropdownContainer}>
					<Select
						options={fundOptionsArray}
						defaultValue={fundOptionsArray[0].label}
						value={selectedFundType}
						style={{ width: 150, borderRadius: '8px', margin: "0.5rem 0rem" }}
						onChange={handleFundChange}
					/>

					<UIComponents.Button text='Add Master Type' isFilled={true} onClick={() => setAddMasterPopupOpen(true)} />

				</div>
			</div>


			<DndProvider backend={HTML5Backend}>
				<div className={styles.unmappedLoanTypesContainer}>
					<div style={{textAlign: 'left', margin: "10px 20px 0px 20px"}}><b>Unmapped Loan Types</b></div>
					<div className={styles.unmappedLoantypeListContainer}>
						<DroppableList
							title={'unmapped_loan_types'}
							items={loanTypeMappingData?.unmapped_loan_types}
							itemAccessKey={'unmapped_loan_type'}
							allLists={loanTypeMappingData}
							setAllLists={setLoanTypeMappingData}
						/>
					</div>
				</div>

				<div style={{display: "flex"}}>
					<div className={styles.mappingHeading}>Loan Type Master</div>
					<div className={styles.mappingHeading}>Mapped Loan Type</div>
				</div>
				<div className={styles.loanMasterMappingContainer}>
					{loanTypeMappingData?.master_loan_types.map((loanType) => (
						<div key={loanType} className={styles.loanMasterMapContainer}>
							<div className={styles.loanMasterTab}><div className={styles.loanMaster}>{loanType?.master_loan_type}</div></div>
							<div className={`${styles.loanMasterTab} ${styles.loanMasterList}`}>
								<DroppableList
									title={loanType}
									items={loanTypeMappingData?.mapped_loan_types && loanTypeMappingData.mapped_loan_types?.filter(type => loanType.master_loan_type_id == type.master_loan_type_id)}
									itemAccessKey={'loan_type'}
									allLists={loanTypeMappingData}
									setAllLists={setLoanTypeMappingData}
									getloanTypeMappingInfo={getloanTypeMappingInfo}
									selectedFundType={selectedFundType}
								/>
							</div>
						</div>
					))}
				</div>

			</DndProvider>

			<AddLoanTypeMasterModal
				isOpen={addMasterPopupOpen}
				setIsOpen={setAddMasterPopupOpen}
				fundType={selectedFundType}
				getloanTypeMappingInfo={getloanTypeMappingInfo}
				selectedFundType={selectedFundType}
			/>

		</div>
	);
};
