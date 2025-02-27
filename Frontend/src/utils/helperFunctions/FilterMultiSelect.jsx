import { Select } from "antd";
import React, { useState } from "react";

export const FilterMultiSelect = ({ data = [], columns = [], onFilterChange }) => {
	const [selectedFilters, setSelectedFilters] = useState({});
	const getFilterOptions = (key) => {
		if (!data) return [];
		const uniqueValues = [...new Set(data.map((item) => item[key]))];
		return uniqueValues.map((value) => ({ value, label: value }));
	};

	const handleFilterChange = (key, values) => {
		setSelectedFilters((prev) => {
			const updatedFilters = { ...prev, [key]: values };
			const isAllEmpty = Object.values(updatedFilters).every((val) => val.length === 0);
			const newFilteredData = isAllEmpty
				? data
				: data.filter((item) =>
					Object.entries(updatedFilters).every(([filterKey, filterValues]) =>
						filterValues.length === 0 ? true : filterValues.includes(item[filterKey])
					)
				);

			onFilterChange(newFilteredData);
			return updatedFilters;
		});
	};

	return (
		<div style={{ display: "flex", gap: "10px", flexWrap: "wrap" }}>
			{columns.map((column) => (
				<Select
					key={column.key}
					mode="multiple"
					allowClear
					style={{
						width: "250px",
						maxHeight: "150px",
						overflowY: "auto",
						flexGrow: 1
					}}
					placeholder={`Filter by ${column.label}`}
					onChange={(values) => handleFilterChange(column.key, values)}
					options={getFilterOptions(column.key)}
				/>
			))}
		</div>
	);
};