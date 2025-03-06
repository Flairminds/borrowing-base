import 'antd/dist/reset.css';
import React from 'react';
import { UIComponents } from "../uiComponents";

export const BackOption = ({
	text = '<- Back',
	onClick = () => {},
	loading = false,
	loadingText = 'Loading...',
	customStyle = {},
	btnDisabled = false
}) => {
	return (
		<UIComponents.Button onClick={onClick} loading={loading} asLink={true} disabled={btnDisabled} text={loading ? loadingText : text} />
	);
};
