import { Button } from 'antd';
import React, { useState } from 'react';
import { toast } from 'react-toastify';
import aboutIcon from "../../assets/NavbarIcons/aboutIcon.png";
import search from "../../assets/NavbarIcons/SearchIcon.svg";
import threeBoxIcon from "../../assets/NavbarIcons/threeSquares.svg";
import ButtonStyles from "../../components/Buttons/ButtonStyle.module.css";
import Styles from "../../components/Tables/TableComponent.module.css";
import { getSelectedWIAAsstes, getWhatIfAnalysisData } from '../../services/api';
import { WiaSimulationInfo } from '../WiaSimulationInfoModal/WiaSimulationInfo';

export const WhatifTable = ({simulationType, setSimulationType, data, columns, setTablesData, setTableModal, setWhatifAnalysisPerformed, selectedRow, setSelectedRow }) => {
	const [selectedWIA, setSelectedWIA] = useState("");
	const [wiaSimulationModal, isWiaSimulationModal] = useState(false);
	const [searchInput, setSearchInput] = useState("");
	if (!columns?.length || !data?.length) {
		return <div>No Data Available</div>;
	}

	const handleUseBtn = async () => {
		if (selectedRow) {
			try {
				const response = await getWhatIfAnalysisData(selectedRow.what_if_analysis_id);
				if (response.status === 200) {
					toast.success(`${selectedRow.name} imported Successfully`);
					setWhatifAnalysisPerformed(true);

					setTablesData(response.data.what_if_analysis);
				}
			} catch (err) {
				console.error(err);
			}
			setTableModal(false);
		} else {
			toast.error("Please select a row first");
		}
	};

	const truncateText = (text, maxLength) => {
		if (text.length > maxLength) {
			return text.substring(0, maxLength - 3) + '...';
		} else {
			return text;
		}
	};

	const handleAboutIcon = async (id, whatIfAnalysisType ) => {
		try {
			const response = await getSelectedWIAAsstes(id, whatIfAnalysisType);
			setSimulationType(response.data.simulation_type);
			setSelectedWIA(response.data.result);
			isWiaSimulationModal(true);
		} catch (err) {
			console.error(err);
		}
	};

	const handleRowSelection = (row) => {
		setSelectedRow(selectedRow === row ? null : row);
	};

	const handleSearchChange = (e) => {
		setSearchInput(e.target.value);
	};

	const filteredData = data.filter(row =>
		row.name.toLowerCase().includes(searchInput.toLowerCase())
	);

	return (
		<div>
			<div className={Styles.inputSearch}>
				<img style={{paddingLeft: "5px"}} src={search} alt="search" />
				<input
					type="text"
					placeholder="Search by file name"
					className={Styles.searchinputTag}
					value={searchInput}
					onChange={handleSearchChange}
				/>
			</div>

			<div className={Styles.tableContainer}>
				<table className={Styles.table}>
					<thead>
						<tr className={Styles.headRow}>
							<th className={Styles.th}></th>
							{columns.map((col, index) => (
								<th key={index} className={Styles.th}>
									{col.label}
								</th>
							))}
							<th className={Styles.th}></th>
						</tr>
					</thead>
					<tbody>
						{filteredData.length > 0 ? (
							filteredData.map((row, rowIndex) => (
								<tr key={rowIndex} onClick={() => handleRowSelection(row)}>
									<td className={Styles.td}>
										<input
											type="radio"
											value={rowIndex}
											checked={selectedRow === row}
											onChange={() => {}}
										/>
									</td>
									{columns.map((col, colIndex) => (
										<td key={col.key} className={Styles.td}>
											{colIndex === 2 ? (
												<Button
													style={{ backgroundColor: "white", color: "black", textDecoration: "none", border: "none", boxShadow: "none" }}
													type="primary"
													title={row[col.key]}
												>
													<span className={Styles.baseFilename}>
														{truncateText(row[col.key], 15)}
													</span>
												</Button>
											) : (
												<span>{row[col.key]?.replace("_", " ")}</span>
											)}
										</td>
									))}
									<td className={Styles.td}>
										<img
											src={threeBoxIcon}
											alt='about'
											style={{ height: "2.9vh", margin: "0rem 0.2rem", cursor: "pointer" }}
											onClick={() => handleAboutIcon(row.what_if_analysis_id, row.simulation_type)}
										/>
									</td>
								</tr>
							))
						) : (
							<tr>
								<td colSpan={columns.length + 2} className={Styles.td}>No Data Found</td>
							</tr>
						)}
					</tbody>
				</table>
				<WiaSimulationInfo simulationType={simulationType} isWiaSimulationModal={isWiaSimulationModal} wiaSimulationModal={wiaSimulationModal} selectedWIA={selectedWIA} />
			</div>
			<div style={{display: "flex", justifyContent: "end", paddingRight: "1.2rem", paddingTop: "1rem"}}>
				<button onClick={handleUseBtn} className={ButtonStyles.filledBtn}>Use</button>
			</div>
		</div>
	);
};
