import { useEffect } from 'preact/hooks';
import React, { useState } from 'react';
import upDownArrow from "../../assets/sortArrows/up-and-down-arrow.svg";
import upArrowIcon from "../../assets/sortArrows/up.svg";
import { TableViewModal } from '../../modal/TableView/TableViewModal';
import { fmtDisplayVal } from '../../utils/helperFunctions/formatDisplayData';
import { sortData } from '../../utils/helperFunctions/sortTableData';
import { Graphs } from '../graphs';
import { UIComponents } from '../uiComponents';
import Styles from './TableGraph.module.css';


export const TableGraph = ({title, tableData, tableColumns, chartsData, yAxis}) => {

	const [openModal, setOpenModal] = useState(false);
	const [displayData, setDisplayData] = useState();
	const len = tableData && tableData[tableColumns[0]]?.length;
	const dataMappingArray = Array(len > 9 ? 6 : len).fill('');
	const [selectedSort, setSelectedSort] = useState({
		name: '',
		type: ''
	});

	useEffect(() => {
		if (tableData) {
			setDisplayData(tableData);
		}
	}, [tableData]);

	const ModalOpen = () => {
		setOpenModal(true);
	};

	const handleSortArrowClick = (columnName) => {
		if (selectedSort.name == columnName) {
			if (selectedSort.type == 'asc') {
				const sortedData = sortData(tableData, columnName, 'desc');
				setDisplayData(sortedData);
				setSelectedSort({name: columnName, type: "desc"});
			} else if (selectedSort.type == 'desc') {
				setDisplayData(tableData);
				setSelectedSort({name: columnName, type: "nosort"});
			} else {
				const sortedData = sortData(tableData, columnName, 'asc');
				setDisplayData(sortedData);
				setSelectedSort({name: columnName, type: "asc"});
			}
		} else {
			const sortedData = sortData(tableData, columnName, 'asc');
			setDisplayData(sortedData);
			setSelectedSort({name: columnName, type: "asc"});
		}
	};

	return (
		<div className={Styles.tableGraphContainer}>
			<div style={{fontSize: '18px', fontWeight: 500, margin: '0.8rem 0.4rem'}}>{title}</div>
			<div className='d-flex'>
				<div className={`${Styles.tableContainer}`}>
					<table className={Styles.table}>
						<thead>
							<tr>
								{tableColumns?.map((columnName, index) => (
									<th key={index} className={Styles.th}>
										{columnName ? columnName : null}
										{selectedSort.name == columnName && selectedSort.type == 'asc' ?
											<img onClick={() => handleSortArrowClick(columnName)} style={{ paddingLeft: "5px", paddingBottom: "2px", margin: '0px 5px' }} src={upArrowIcon} alt="up" />
											:
											selectedSort.name == columnName && selectedSort.type == 'desc' ?
												<img onClick={() => handleSortArrowClick(columnName)} style={{ paddingLeft: "5px", paddingBottom: "2px", transform: "rotate(180deg)", margin: '0px 5px' }} src={upArrowIcon} alt="up" />
												:
												<img onClick={() => handleSortArrowClick(columnName)} style={{ paddingLeft: "5px", paddingBottom: "2px", height: '13px', width: '14px' }} src={upDownArrow} alt="up" />
										}
									</th>
								))}
							</tr>
						</thead>
						<tbody>
							{dataMappingArray?.map((el, i) => (
								<tr key={i}>
									{tableColumns?.map((ed, j) => (
										<td key={j} className={Styles.td}>
											{displayData && displayData[ed] ? displayData[ed][i]?.data : ''}
											{displayData && displayData[ed] && displayData[ed][i]?.changeInValue ? <div className={Styles.GreenText}>Change in value</div> : null}
											<div>
												{displayData && displayData[ed] ? <spna className={Styles.updatedText}>{displayData[ed][i]?.prevValue} {displayData[ed] && (displayData[ed][i]?.prevValue || displayData[ed][i]?.prevValue == 0) && ed != 'Industry' ? '|' : null} </spna> : null}
												{displayData && displayData[ed] && displayData[ed][i]?.percentageChange ? <span className={`${Styles.GreenText} ${Styles.updatedText} `}>{displayData[ed][i]?.percentageChange}</span> : null}
											</div>
										</td>
									)
									)}
								</tr>
							))}
							{(len > 9) && (
								<tr>
									<td colSpan={tableColumns.length} className={Styles.td}>
										<UIComponents.Button onClick={ModalOpen} text={`View other +${tableData[tableColumns[0]].length - 6 }`} asLink={true} />
										<TableViewModal openModal={openModal} setOpenModal={setOpenModal} data={tableData} columns={tableColumns} heading={''} />
									</td>
								</tr>
							)}
						</tbody>
						<tr>
							{tableColumns?.map((ed, i) => (
								<td key={i} className={Styles.totalRow}>
									{tableData && tableData[ed]
										? ed === "% Borrowing Base"
											? fmtDisplayVal(tableData?.Total?.data[ed], 2)
											: tableData?.Total?.data[ed]
										: null}
								</td>
							)
							)}
						</tr>

					</table>
				</div>
				<div className={Styles.chartContainer}>
					<Graphs.BarGraph chartsData={chartsData} yAxis={yAxis} />
					{/* <StackedBarGraph StackedGraphData={StackedGraphData} /> */}
				</div>
			</div>
		</div>
	);
};