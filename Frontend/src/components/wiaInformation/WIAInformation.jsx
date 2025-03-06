import React from 'react'
import ButtonStyles from "../../components/uiComponents/Button/ButtonStyle.module.css";
import { UIComponents } from '../uiComponents';

export const WIAInformation = ({baseFile, whaIfAnalsisData, isSetDescriptionModal}) => {
	return (
		<div  style={{backgroundColor:"#F7E0B4", display:"flex" ,justifyContent:"space-between",alignItems:"centre" , padding:"7px"}}>
			<div style={{textAlign:"center", flex:"1", paddingLeft:"2.2rem"}}>
				<p style={{marginBottom:"0px", marginRight:'2px'}}>What if analysis of {baseFile?.name} with {whaIfAnalsisData?.analysisValue} {whaIfAnalsisData?.typeOfAnalysis}</p>
			</div>
			<div style={{textAlign:"right"}}> 
				<UIComponents.Button onClick={() => isSetDescriptionModal(true)} isFilled={true} text={'Save'} />
			</div>
		</div>
	);
};
