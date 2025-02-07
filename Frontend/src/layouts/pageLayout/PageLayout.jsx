import React from 'react';
import { Outlet } from 'react-router';
import { Navbar } from '../../components/navbar/Navbar';
import { Sidebar } from '../../components/sidebar/Sidebar';

export const PageLayout = () => {
	return (
		<div className='d-flex'>
			<Sidebar />
			<div className='w-100' style={{textAlign: 'center'}}>
				<Navbar />
				<Outlet />
			</div>
		</div>
	);
};
