import { Button } from "antd";
import 'antd/dist/reset.css';
import React, { useState } from 'react';
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
	const [isActive, setIsActive] = useState(false);
	const handleMouseDown = () => setIsActive(true);
	const handleMouseUp = () => setIsActive(false);

	return (
		<Button
			key={key}
			onClick={onClick}
			className={`${ButtonStyle.btn} ${btnDisabled ? `${ButtonStyle.disabledBtn}` : ''} ${!isFilled ? `${ButtonStyle.outlinedBtn}` : ''} ${asLink ? `${ButtonStyle.textBtn}` : ''}`}
			// style={{...customStyle, boxShadow: isActive ? 'none' : '1px 1px 2px 0.5px grey'}}
			style={{...customStyle}}
			htmlType={type}
			loading={loading}
			disabled={btnDisabled}
			onMouseDown={handleMouseDown}
			onMouseUp={handleMouseUp}
			title={title}
			size={size}
		>
			<span>{loading ? loadingText : text}</span>
		</Button >
	);
};
