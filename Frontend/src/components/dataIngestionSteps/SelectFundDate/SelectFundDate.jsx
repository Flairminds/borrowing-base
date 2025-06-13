import { DatePicker, Select } from 'antd';
import React from 'react';
import CalendarIcon from '../../../assets/NavbarIcons/Calendar.svg';
import { fundOptionsArray } from '../../../utils/constants/constants';
import styles from './SelectFundDate.module.css';

const SelectFundDate = ({ selectedFund, setSelectedFund, selectedDate, setSelectedDate }) => {
	return (
		<div className={styles.container}>
			<div className={styles.formGroup}>
				<label className={styles.label}>Select Fund</label>
				<Select
					style={{ width: '100%', borderRadius: '8px', margin: "0.5rem 0rem" }}
					onChange={(value) => setSelectedFund(fundOptionsArray[value].label)}
					value={selectedFund}
					options={fundOptionsArray}
				/>
			</div>
			<div className={styles.formGroup}>
				<label className={styles.label}>Report Date</label>
				<DatePicker
					id="reportDatePicker"
					style={{ width: "100%" }}
					suffixIcon={<img src={CalendarIcon} alt="calendar icon" />}
					placeholder="Report Date"
					allowClear={true}
					onChange={(date) => {
						const localDate = date.startOf('day'); // resets time to 00:00
						setSelectedDate(localDate);
					}}
					value={selectedDate}
				/>
			</div>
		</div>
	);
};

export default SelectFundDate;