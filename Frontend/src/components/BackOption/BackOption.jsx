import 'antd/dist/reset.css';
import React from 'react';
import { UIComponents } from "../uiComponents";

export const BackOption = ({
	text = '<- Back',
	onClick = () => {}
}) => {
	return (
		<span onClick={onClick} style={{color: 'blue'}}>{text}</span>
	);
};
