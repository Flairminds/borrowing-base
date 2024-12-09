import React from 'react';
import { Outlet } from 'react-router';
import { Navbar } from '../../components/navbar/Navbar';
import { Sidebar } from '../../components/sidebar/Sidebar';

export const Layout = () => {
  return (
    <div className='d-flex'>
        <Sidebar />
        <div className='w-100'
        >
            <Navbar />
            <Outlet />
        </div>

    </div>
  );
};
