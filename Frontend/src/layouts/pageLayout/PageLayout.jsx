import React from 'react';
import { Outlet } from 'react-router';
import { Navbar } from '../navbar/Navbar';
import { Sidebar } from '../sidebar/Sidebar';

export const PageLayout = () => {
	return (
		<div className='d-flex'>
			<div style={{backgroundColor: 'red'}}>
				<Sidebar />
			</div>
			<div style={{width: '100%'}}>
				<Navbar />
				<div style={{padding: '5px 10px 30px 10px'}}>
					<Outlet />
				</div>
			</div>
		</div>
	);
};
