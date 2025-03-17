import React from 'react';
import { Outlet } from 'react-router';
import { Navbar } from '../navbar/Navbar';
import { Sidebar } from '../sidebar/Sidebar';

export const PageLayout = () => {
	return (
		<div className='d-flex'>
			<Sidebar />
			<div className='w-100'>
				<Navbar />
				<Outlet />
			</div>
		</div>
	);
};
