import { LoadingOutlined } from '@ant-design/icons';
import { Flex, Spin } from 'antd';
import React from 'react';

export const Loader = () => (
	<div>
		{/* <Spin indicator={<LoadingOutlined spin />} size="small" /> */}
		{/* <Spin indicator={<LoadingOutlined spin />} /> */}
		{/* <Spin indicator={<LoadingOutlined spin />} size="large" /> */}
		<Spin indicator={<LoadingOutlined style={{ fontSize: 48 }} spin />} />
	</div>
);

export const LoaderSmall = () => (
	<div>
		{/* <Spin indicator={<LoadingOutlined spin />} size="small" /> */}
		<Spin indicator={<LoadingOutlined spin />} />
		{/* <Spin indicator={<LoadingOutlined spin />} size="large" /> */}
		{/* <Spin indicator={<LoadingOutlined style={{ fontSize: 48 }} spin />} /> */}
	</div>
);