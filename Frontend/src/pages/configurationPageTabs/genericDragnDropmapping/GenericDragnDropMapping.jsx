import { CloseCircleOutlined } from '@ant-design/icons';
import { Select } from 'antd';
import React, { useEffect, useState } from 'react';
import { DndProvider, useDrag, useDrop } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import { toast } from 'react-toastify';
import { Icons } from '../../../components/icons';
import { UIComponents } from '../../../components/uiComponents';
import { AddLoanTypeMasterModal } from '../../../modal/configurationPageModals/addLoanTypeMasterModal/AddLoanTypeMasterModal';
import { deleteLoanTypeMapping, getLoanTypeMappingData, updateLoanTypeMapping } from '../../../services/dataIngestionApi';
import { fundOptionsArray } from '../../../utils/constants/constants';
import { capitalizeFirstLetter } from '../../../utils/helperFunctions/commonHelperFunctions';
import { showToast } from '../../../utils/helperFunctions/toastUtils';
import styles from './GenericDragnDropMapping.module.css';

const ItemType = "ITEM";

const DraggableItem = ({ item, itemAccessKey, title, getEntryMappingInfo, selectedFundType, activeMappingType }) => {
	const [{ isDragging }, drag] = useDrag(() => ({
		type: ItemType,
		item: { name: item },
		collect: (monitor) => ({
			isDragging: !!monitor.isDragging()
		})
	}));

	const handleDeleteMapping = async (deleteItem) => {
		try {
			const res = await deleteLoanTypeMapping(deleteItem.mapping_id, activeMappingType);
			showToast('success', res.data.message);
			getEntryMappingInfo(selectedFundType);
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
				// minWidth: "175px",
				borderRadius: '5px'
				// maxHeight: "35px"
			}}
		>
			<span title={"Drag around and drop for editing the mapping"}>{item && item[itemAccessKey]}</span>
			{title != `unmapped_${activeMappingType}_types` && <CloseCircleOutlined style={{margin: "0px 10px"}} onClick={() => handleDeleteMapping(item)} title={"Click to delete this mapping"} />}
		</div>
	);
};

const DroppableList = ({ title, items, allLists, setAllLists, itemAccessKey, getEntryMappingInfo, selectedFundType, activeMappingType }) => {
	const [{ isOver }, drop] = useDrop(() => ({
		accept: ItemType,
		drop: async (draggedItem) => {
			if (title == `unmapped_${activeMappingType}_types`) return;
			console.info("master", title, items, '//', draggedItem);

			let mappingData = {};
			if (draggedItem.name.mapping_id) {
				mappingData = {
					[`master_${activeMappingType}_type_id`]: title[`master_${activeMappingType}_type_id`],
					'mapping_id': draggedItem.name.mapping_id
				};
			} else {
				mappingData = {
					[`master_${activeMappingType}_type_id`]: title[`master_${activeMappingType}_type_id`],
					[`${activeMappingType}_type`]: draggedItem.name[`unmapped_${activeMappingType}_type`]
				};
			}

			try {
				const res = await updateLoanTypeMapping(mappingData, activeMappingType);
				showToast('success', res.data.message);
				getEntryMappingInfo(selectedFundType);
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
			className={title == `unmapped_${activeMappingType}_types` ? styles.unmappedLoantypeList : styles.mappedTypesList}
		>
			{items && items.length > 0 ? (
				items.map((item) => (
					<DraggableItem key={item[itemAccessKey]} itemAccessKey={itemAccessKey} item={item} title={title} getEntryMappingInfo={getEntryMappingInfo} selectedFundType={selectedFundType} activeMappingType={activeMappingType} />
				))
			) : (
				<div className={styles.emptyDiv}>
					{title == `unmapped_${activeMappingType}_types` ? <> No data </> : <>Drop items here</>}
				</div>
			)}
		</div>
	);
};

export const GenericDragnDropMapping = ({activeMappingType}) => {

	const [entryMappingData, setEntryMappingData] = useState(null);
	const [selectedFundType, setSelectedFundType] = useState("PFLT");
	const [addMasterPopupOpen, setAddMasterPopupOpen] = useState(false);

	console.info('activeMappingType', activeMappingType);

	const getEntryMappingInfo = async(fund) => {
		try {
			const res = await getLoanTypeMappingData(fund, activeMappingType);
			setEntryMappingData(res.data.result);
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
		getEntryMappingInfo(fundType);
	};


	useEffect(() => {
		getEntryMappingInfo(selectedFundType);
	}, []);

	return (
		<div className={styles.loanTypePageContainer}>
			<div className={styles.mappingTitle}>
				<div className={styles.cardContainer}>
					<div className={styles.loanTypeCard}>
						<div><b>All {capitalizeFirstLetter(activeMappingType)} Types</b></div>
						<div className={styles.cardTitle}>{entryMappingData && entryMappingData[`unmapped_${activeMappingType}_types`]?.length + entryMappingData[`mapped_${activeMappingType}_types`]?.length}</div>
					</div>
					<div className={styles.loanTypeCard}>
						<div><b>Unmapped {capitalizeFirstLetter(activeMappingType)} Types</b></div>
						<div className={styles.cardTitle}>{entryMappingData && entryMappingData[`unmapped_${activeMappingType}_types`]?.length}</div>
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

					<UIComponents.Button text={`Add Master ${capitalizeFirstLetter(activeMappingType)} Type`} isFilled={true} onClick={() => setAddMasterPopupOpen(true)} />

				</div>
			</div>


			<DndProvider backend={HTML5Backend}>
				<div className={styles.unmappedLoanTypesContainer}>
					<div style={{textAlign: 'left', margin: "5px"}}><b>Unmapped {capitalizeFirstLetter(activeMappingType)} Types</b><Icons.InfoIcon title={`The list of ${capitalizeFirstLetter(activeMappingType)} types from the source files which are not mapped to the standardised master ${capitalizeFirstLetter(activeMappingType)} types.' + '\nDrag and drop items in respective master ${capitalizeFirstLetter(activeMappingType)} types for mapping.`} /></div>
					<div className={styles.unmappedLoantypeListContainer}>
						<DroppableList
							title={`unmapped_${activeMappingType}_types`}
							items={entryMappingData && entryMappingData[`unmapped_${activeMappingType}_types`]}
							itemAccessKey={`unmapped_${activeMappingType}_type`}
							allLists={entryMappingData}
							setAllLists={setEntryMappingData}
						/>
					</div>
				</div>

				<div style={{display: "flex", marginTop: '15px'}}>
					<div className={styles.mappingHeading} style={{width: '25%'}}>{capitalizeFirstLetter(activeMappingType)} Type Master</div>
					<div className={styles.mappingHeading} style={{width: '75%'}}>Mapped {capitalizeFirstLetter(activeMappingType)} Type</div>
				</div>
				<div className={styles.loanMasterMappingContainer}>
					{entryMappingData && entryMappingData[`master_${activeMappingType}_types`]?.map((entryType) => (
						<div key={entryType} className={styles.loanMasterMapContainer}>
							<div className={styles.loanMasterTab} style={{width: '25%'}}><div className={styles.loanMaster}>{entryType && entryType[`master_${activeMappingType}_type`]}</div></div>
							<div className={`${styles.loanMasterTab} ${styles.loanMasterList}`} style={{width: '75%'}}>
								<DroppableList
									title={entryType}
									items={entryMappingData && entryMappingData[`mapped_${activeMappingType}_types`]?.filter(type => entryType[`master_${activeMappingType}_type_id`] == type[`master_${activeMappingType}_type_id`])}
									itemAccessKey={`${activeMappingType}_type`}
									allLists={entryMappingData}
									setAllLists={setEntryMappingData}
									getEntryMappingInfo={getEntryMappingInfo}
									selectedFundType={selectedFundType}
									activeMappingType={activeMappingType}
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
				getEntryMappingInfo={getEntryMappingInfo}
				selectedFundType={selectedFundType}
				activeMappingType={activeMappingType}
			/>

		</div>
	);
};
