import React, { useEffect, useState } from 'react';
import { DndProvider, useDrag, useDrop } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import { toast } from 'react-toastify';
import { getLoanTypeMappingData, updateLoanTypeMapping } from '../../../services/dataIngestionApi';
import { loanTypeConfig, loanTypeMappingStaticData } from '../../../utils/constants/configurationConstants';
import styles from './LoanTypeMapping.module.css';

const ItemType = "ITEM";

const DraggableItem = ({ item }) => {
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
			{item}
		</div>
	);
};

const DroppableList = ({ title, items, allLists, setAllLists }) => {
	const [{ isOver }, drop] = useDrop(() => ({
		accept: ItemType,
		drop: async (draggedItem) => {
			try {
				const mappingData = {
					'master_loan_type': title,
					'loan_type': draggedItem.name
				};
				const res = await updateLoanTypeMapping(mappingData);
				console.info('---', res);
			} catch (err) {
				console.error(err);
				toast.error(err?.response?.data?.message);
			}

			setAllLists((prevLists) => {
				const newLists = { ...prevLists };
				newLists['unmapped_loan_type_data'] = newLists['unmapped_loan_type_data'].filter(
					(item) => item !== draggedItem.name
				);

				newLists.mapped_loan_type_data[title] = [...newLists.mapped_loan_type_data[title], draggedItem.name];
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
			className={title == "unmapped_loan_type_data" ? styles.unmappedLoantypeList : styles.mappedTypesList}
		>
			{/* <h4>{title}</h4> */}
			{items?.map((item) => (
				<DraggableItem key={item.name} item={item} />
			))}
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
			console.info(res, 'loan map 1');
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
							title={'unmapped_loan_type_data'}
							items={loanTypeMappingData?.unmapped_loan_type_data}
							allLists={loanTypeMappingData}
							setAllLists={setLoanTypeMappingData}
						/>
					</div>
				</div>

				<div className={styles.loanMasterMappingContainer}>
					{loanTypeMappingData?.mapped_loan_types.map((loanType) => (
						<div key={loanType} className={styles.loanMasterMapContainer}>
							<div className={styles.loanMasterTab}><div className={styles.loanMaster}>{loanType}</div></div>
							<div className={`${styles.loanMasterTab} ${styles.loanMasterList}`}>
								<DroppableList
									title={loanType}
									items={loanTypeMappingData?.mapped_loan_type_data && loanTypeMappingData.mapped_loan_type_data[loanType]}
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
