import { DatePicker, Dropdown } from "antd";
import React from "react";
import inputStyles from './DynamicInputComponent.module.css';

export const DynamicInputComponent = (
	{
		inputType = "text",
		placeholder = "Enter value",
		inputValue = "",
		onInputChange = () => {},
		dropDownOptions = [],
		autoFocusInput = false
	}
) => {

	return (
		<>
			{
				inputType === 'number' ?
					<input type='number' value={inputValue} onChange={onInputChange} placeholder={placeholder} className={inputStyles.input} />
					:
					inputType === 'dropdown' ?
						<Dropdown
							options = {dropDownOptions}
						/>
						:
						inputType === 'date' ?
							<DatePicker onChange={onInputChange} value={inputValue} />
							:
							<input type="text" value={inputValue} onChange={onInputChange} placeholder={placeholder} className={inputStyles.input} autoFocus={autoFocusInput} />
			}
		</>
	);
};
