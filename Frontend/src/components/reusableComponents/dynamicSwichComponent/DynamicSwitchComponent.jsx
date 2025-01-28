import { Switch } from 'antd';
import React from 'react';
import styles from './DynamicSwitchComponent.module.css';

export const DynamicSwitchComponent = ({switchOnText, switchOffText, switchOnChange = (value) => console.info(value), switchSize = "small"}) => {
	return (
		<div className={styles.switchContainer}>
			<span className={styles.switchText} >{switchOffText}</span>
			<Switch size={switchSize} className={styles.switch} onChange={switchOnChange} />
			<span className={styles.switchText}>{switchOnText}</span>
		</div>
	);
};
