import { Button } from "antd";
import 'antd/dist/reset.css';
import React from 'react';
import ButtonStyle from './CustomButton.module.css';

export const CustomButton = ({
	isFilled = false,
	text = 'Button',
	onClick = () => {},
	type = 'button',
	key = 'submit',
	loading = false,
	loadingText = 'Loading...',
	customStyle = {},
	btnDisabled = false,
	asText = false
}) => {
	return (

		<Button
			key={key}
			onClick={onClick}
			className={`${btnDisabled ? `${ButtonStyle.DisabledBtn}` : isFilled ? `${ButtonStyle.filledBtn}` : asText ? `${ButtonStyle.textBtn}` : `${ButtonStyle.outlinedBtn}`}`}
			style={customStyle}
			htmlType={type}
			loading={loading}
			disabled={btnDisabled}
		>
			<span>{loading ? loadingText : text}</span>
		</Button >
	);
};
