import { Button } from "antd";
import 'antd/dist/reset.css';
import React from 'react';
import styles from './backoption.module.css';

export const BackOption = ({
	text = '<- Back',
	onClick = () => {},
	loading = false,
	loadingText = 'Loading...',
	customStyle = {},
	btnDisabled = false
}) => {
  	return (
		<div>
			<Button onClick={onClick} loading={loading}
				className={styles.filledBtn}
				style={customStyle}
				disabled={btnDisabled}
			>
				{loading ? loadingText : text}
			</Button >
		</div>
	);
};
