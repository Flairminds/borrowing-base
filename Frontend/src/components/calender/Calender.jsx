import { DatePicker, Tooltip } from 'antd';
import React from 'react';
import { toast } from 'react-toastify';
import GreenEllipse from '../../assets/GreenEllipse.svg';
import CalendarIcon from '../../assets/NavbarIcons/Calendar.svg';
import { getDateReport } from '../../services/api';
import { LoaderSmall } from '../uiComponents/loader/loader';

export const Calender = ({
	setReportDate,
	setTablesData,
	setDate,
	fileUpload,
	setWhatifAnalysisPerformed,
	setBaseFile,
	availableClosingDates,
	setFundType,
	getTrendGraphData,
	onDateChange = null,
	selectedFund,
	setGettingDashboardData,
	gettingDates,
	setTrendGraphData
}) => {

	const handleDateChange = async (date, dateString) => {
		if (!dateString) {
			setReportDate(null);
			setDate(null);
			setTablesData([]);
			setBaseFile(null);
			setWhatifAnalysisPerformed(false);
			toast.info('Date cleared');
			return;
		}

		if (fileUpload) {
			if (dateString) {
				setWhatifAnalysisPerformed(false);
				setReportDate(dateString);
				setDate(dateString);
			}
		} else {
			if (dateString) {
				try {
					setGettingDashboardData(true)
					setTrendGraphData(null)
					const response = await getDateReport(dateString, null, selectedFund);
					if (response.status === 200) {
						setTablesData(response.data);
						setBaseFile({ name: response.data.file_name, id: response.data.base_data_file_id });
						setWhatifAnalysisPerformed(false);
						setReportDate(dateString);
						setFundType(response.data.fund_name);
						getTrendGraphData(response.data.fund_name);
						toast.info(`Data for ${dateString} imported`);
						setGettingDashboardData(false)
					}
				} catch (err) {
					setGettingDashboardData(false)
					if (err.response && err.response.status === 404) {
						toast.info(err.response.data.message);
					} else {
						console.error(err);
					}
				}
			}
		}
	};


	const cellRender = (current, info) => {
		const style = {};
		const isSpecialDate = availableClosingDates?.includes(current.format('YYYY-MM-DD'));

		if (info && info.type === 'date') {
			return (
				<>
					{isSpecialDate ? (
						<Tooltip title="File Updated">
							<div className="ant-picker-cell-inner" style={style}>
								<div style={{backgroundColor: '#0EB198', borderRadius: '5px', color: 'white'}}>
									{current.date()}

								</div>
								<div style={{visibility: 'hidden', display: 'flex', justifyContent: 'center'}}>
									<img src={GreenEllipse} alt="Data Present" />
								</div>
							</div>
						</Tooltip>
					) : (
						<div className="ant-picker-cell-inner" style={style}>
							{current.date()}
							<div style={{visibility: 'hidden', display: 'flex', justifyContent: 'center'}}>
								<img src={GreenEllipse} alt="Data Present" />
							</div>
						</div>
					)}
				</>
			);
		} else if (info && info.type === 'month') {
			return (
				<div className="ant-picker-cell-inner" style={style}>
					{current.format('MMM')}
				</div>
			);
		} else if (info && info.type === 'year') {
			return (
				<div className="ant-picker-cell-inner" style={style}>
					{current.year()}
				</div>
			);
		}

		return null;
	};


	return (
		<>
			{gettingDates ? <LoaderSmall/> :
				<>
					{/* <DatePicker
					style={{ width: 120 }}
					allowClear={true}
					placeholder='Report Date'
					onChange={handleDateChange}
					/> */}
					<DatePicker
						id={fileUpload ? 'fileuploadDatePicker' : 'reportDatePicker'}
						style={fileUpload ? {width: 130 } : {visibility: 'hidden', width: 3, padding: '0'}}
						suffixIcon={<img src={CalendarIcon}/>}	
						placeholder='Report Date'
						cellRender={cellRender}
						onChange={onDateChange || handleDateChange}
						allowClear={true}
					/>
					{!fileUpload ?
						<label htmlFor={fileUpload ? 'fileuploadDatePicker' : 'reportDatePicker'}>
							<img src={CalendarIcon} alt="Calender Icon" />
						</label>
						:
						null
					}
				</>
			}
		</>
	);
};
