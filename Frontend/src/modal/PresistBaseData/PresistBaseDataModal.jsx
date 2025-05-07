import { Modal, Collapse, Table, Radio, Tag } from 'antd';
import React from 'react';
import { CustomButton } from '../../components/uiComponents/Button/CustomButton';

const { Panel } = Collapse;

export const PersistBaseDataModal = ({ visible, onClose }) => {
	const dataSource = [
		{ key: '1', obligor: 'ACP Falcon Buyer, Inc', security: 'Falcon TL', loanId: 'LX00001', current: 500000, previous: 600000 },
		{ key: '2', obligor: 'ACP 2', security: 'Falcon TL', loanId: 'LX00001', current: 500000, previous: 700000 },
		{ key: '3', obligor: 'ACP 3', security: 'Falcon TL', loanId: 'LX00001', current: null, previous: 800000 }
	];

	const columns = [
		{ title: 'Obligor Name', dataIndex: 'obligor' },
		{ title: 'Security Name', dataIndex: 'security' },
		{ title: 'LoanXID', dataIndex: 'loanId' },
		{
			title: 'Current Value',
			dataIndex: 'current',
			render: (value) => value !== null && value !== undefined ? value : '-',
		},
		{
			title: 'Previous Value',
			dataIndex: 'previous',
			render: (value) => value !== null && value !== undefined ? value : '-',
		},
		{
			title: 'Select Value',
			render: (text, record) => (
				<Radio.Group>
					<Radio value="current">Current</Radio>
					<Radio value="previous">Previous</Radio>
				</Radio.Group>
			)
		}
	];

	return (
		<Modal
			title="Compare values from previous base data"
			open={visible}
			onCancel={onClose}
			footer={null}
			width={900}
		>
			<Collapse defaultActiveKey={['1', '2', '3']}>
				<Panel header="Initial Cash Interest Expense" key="1" extra={<Tag color="gold">Differences in 3 records</Tag>}>
					<div style={{ marginBottom: 10 }}>
						<CustomButton isFilled={true} text="Select All Current"/>
						<CustomButton isFilled={true} text="Select All Previous"/>
						<CustomButton isFilled={false} text="Mark Reviewed"/>
					</div>
					<Table dataSource={dataSource} columns={columns} pagination={false} bordered />
				</Panel>

				<Panel header="Date of Default" key="2" extra={<Tag color="green">Reviewed</Tag>}>
					<p>No differences found. Already reviewed.</p>
				</Panel>

				<Panel header="Total Commitment" key="3" extra={<Tag color="orange">Pending for review</Tag>}>
					<p>Pending data to be reviewed.</p>
				</Panel>
			</Collapse>
		</Modal>
	);
};

