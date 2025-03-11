import React from "react";
import styles from "./statsCard.module.css";

export const StatsCard = ({ cardData, value = null }) => {
	return (
		<div key={cardData.key} className={styles.loanTypeCard}>
			<div><b>{cardData.label}</b></div>
			<div className={styles.cardTitle}>{cardData?.value || value}</div>
		</div>
	);
};