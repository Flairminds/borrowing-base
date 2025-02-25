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

export const LoaderFullPage = () => (
	<div style={{position: 'absolute', top: '0', left: '0', backgroundColor: 'white', opacity: '0.4', width: '100vw', height: '100vh', zIndex: '5000'}}>
		{/* <Spin indicator={<LoadingOutlined spin />} size="small" /> */}
		{/* <Spin indicator={<LoadingOutlined spin />} /> */}
		{/* <Spin indicator={<LoadingOutlined spin />} size="large" /> */}
		<div style={{marginTop: '15%', opacity: '1'}}>
			<Spin indicator={<LoadingOutlined style={{ fontSize: 48 }} spin />} />
		</div>
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