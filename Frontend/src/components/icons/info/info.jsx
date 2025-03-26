import React from 'react';
// import { CiCircleInfo } from "react-icons/ci";
import { FaInfoCircle } from "react-icons/fa";
import { THEME } from '../../../utils/styles';
// import { IoInformationCircleOutline } from "react-icons/io5";

export const InfoIcon = ({ size = null, title = 'info', style = {}}) => {
	return (
		<FaInfoCircle size={size || 18} title={title} style={{cursor: 'pointer', margin: '0 5px', color: THEME.PRIMARY_BG_COLOR, ...style}} />
	);
};