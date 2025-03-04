import React, { useEffect, useState } from 'react';
import { DndProvider, useDrag, useDrop } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import { loanTypeConfig, loanTypeMappingStaticData } from '../../../utils/constants/configurationConstants';
import styles from './LoanTypeMapping.module.css';
import { getLoanTypeMappingData } from '../../../services/dataIngestionApi';
import { toast } from 'react-toastify';

export const LoanTypeMapping = () => {

	const getloanTypeMappingInfo = async() => {
		try {
			const res = await getLoanTypeMappingData();
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
						<div className={styles.cardTitle}>{loanTypeMappingStaticData[card.key]}</div>
					</div>
				))}
			</div>

		</div>
	);
};
