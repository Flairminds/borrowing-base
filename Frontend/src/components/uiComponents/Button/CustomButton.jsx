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
	asLink = false,
	title = '',
	size = 'default'
}) => {
	return (
		<Button
			key={key}
			onClick={onClick}
			className={`${ButtonStyle.btn} ${btnDisabled ? `${ButtonStyle.disabledBtn}` : ''} ${!isFilled ? `${ButtonStyle.outlinedBtn}` : ''} ${asLink ? `${ButtonStyle.textBtn}` : ''}`}
			style={customStyle}
			htmlType={type}
			loading={loading}
			disabled={btnDisabled}
			title={title}
			size={size}
		>
			<span>{loading ? loadingText : text}</span>
		</Button >
	);
};
