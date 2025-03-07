import React, { useEffect, useState } from 'react';
import { DndProvider, useDrag, useDrop } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import { toast } from 'react-toastify';
import { getLoanTypeMappingData, updateLoanTypeMapping } from '../../../services/dataIngestionApi';
import { loanTypeConfig, loanTypeMappingStaticData } from '../../../utils/constants/configurationConstants';
import styles from './LoanTypeMapping.module.css';

const ItemType = "ITEM";

const DraggableItem = ({ item, itemAccessKey }) => {
	const [{ isDragging }, drag] = useDrag(() => ({
		type: ItemType,
		item: { name: item },
		collect: (monitor) => ({
			isDragging: !!monitor.isDragging()
		})
	}));

	return (
		<div
			ref={drag}
			style={{
				padding: "3px 5px",
				margin: "4px",
				backgroundColor: "lightblue",
				cursor: "grab",
				opacity: isDragging ? 0.5 : 1,
				minWidth: "175px",
				borderRadius: '5px'
				// maxHeight: "35px"
			}}
		>
			{item && item[itemAccessKey]}
		</div>
	);
};

const DroppableList = ({ title, items, allLists, setAllLists, itemAccessKey }) => {
	const [{ isOver }, drop] = useDrop(() => ({
		accept: ItemType,
		drop: async (draggedItem) => {
			try {
				const mappingData = {
					'master_loan_type': title.master_loan_type,
					'loan_type': draggedItem.name.unmapped_loan_type
				};
				const res = await updateLoanTypeMapping(mappingData);
				console.info('---', res);
			} catch (err) {
				console.error(err);
				toast.error(err?.response?.data?.message);
			}

			setAllLists((prevLists) => {
				const newLists = { ...prevLists };
				console.info('--- map test', newLists, title, draggedItem);
				newLists['unmapped_loan_types'] = newLists['unmapped_loan_types'].filter(
					(item) => item.unmapped_loan_type !== draggedItem.name.unmapped_loan_type
				);

				const item = {
					'loan_type': draggedItem.name.unmapped_loan_type,
					'master_loan_type': title.master_loan_type,
					'master_loan_type_id': title.master_loan_type_id
				};

				newLists['mapped_loan_types'] = [...newLists['mapped_loan_types'], item];
				return newLists;
			});
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
					<DraggableItem key={item[itemAccessKey]} itemAccessKey={itemAccessKey} item={item} />
				))
			) : (
				<div className={styles.emptyDiv}>
					Drop items here
				</div>
			)}
		</div>
	);
};

export const LoanTypeMapping = () => {

	const [loanTypeMappingData, setLoanTypeMappingData] = useState(null);

	useEffect(() => {
		console.info(loanTypeMappingData, 'loan Map data');
	}, [loanTypeMappingData]);

	const getloanTypeMappingInfo = async() => {
		try {
			const res = await getLoanTypeMappingData();
			setLoanTypeMappingData(res.data.result);
		} catch (err) {
			console.error(err);
			toast.error(err?.response?.data?.message);
		}
	};

	useEffect(() => {
		getloanTypeMappingInfo();
	}, []);

	return (
		<div className={styles.loanTypePageContainer}>
			<div className={styles.cardContainer}>
				{loanTypeConfig.cardsData?.map((card) => (
					<div key={card.key} className={styles.loanTypeCard}>
						<div><b>{card.label}</b></div>
						<div className={styles.cardTitle}>{loanTypeMappingData?.all_loan_type_count}</div>
					</div>
				))}
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
								/>
							</div>
						</div>
					))}
				</div>

			</DndProvider>

		</div>
	);
};
