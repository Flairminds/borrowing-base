import { SettingOutlined } from '@ant-design/icons';
import { Avatar, Popover, Tooltip } from 'antd';
import { useEffect, useState } from 'preact/hooks';
import React from 'react';
import { Link, useLocation } from "react-router-dom";
import AddIcon from '../../assets/NavbarIcons/AddIcon.svg';
import Logo from "../../assets/NavbarIcons/Logo.svg";
// import help from "../../assets/NavbarIcons/help.svg"
import NotificationIcon from '../../assets/NavbarIcons/NotificationIcon.svg';
import profile from "../../assets/NavbarIcons/profile.svg";
import helpIcon from "../../assets/NavbarIcons/question.svg";
import SearchIcon from '../../assets/NavbarIcons/SearchIcon.svg';
import UserDemo from '../../assets/pdfFolder/Portfolio Dashboard User Guide Manual.pdf';
import { ColumnSelectionPopup } from '../../modal/columnSelectionPopup/ColumnSelectionPopup';
import Styles from './Navbar.module.css';



export const Navbar = () => {
	const location = useLocation();
	const [guidePopupOpen, setGuidePopupOpen] = useState(false);
	const [pageLocation, setPageLocation] = useState('');

	useEffect(() => {
		setTimeout(() => {
			setGuidePopupOpen(false);
		}, 2000);
		setGuidePopupOpen(true);
	}, []);

	useEffect(() => {
		setPageLocation(window.location.pathname.split('/')[1]);
	}, [location]);

	const customizationContent = (
		<div>
			<div>Asset Parameter Selection</div>
		</div>
	);

	const PAGE_HEADERS = {
		'fund-setup': 'Concentration Test Setup',
		'base-data-list': 'Data Ingestion - Extracted Base Data',
		'ingestions-file-list': 'Ingestion'
	};

	return (
		<nav className="navbar navbar-expand-lg d-flex flex-row w-100" style={{borderBottom: '1px solid #DEDDDC', backgroundColor: 'white'
		//  ,height:'7%'
		}}>
			<div className="container-fluid">
				<div style={{display: "flex", alignItems: "center"}}>
					<Link className="navbar-brand d-flex flex-row" to='/'>
						<img src={Logo} className="d-inline-block align-text-top" alt="Logo" style={{alignItems: "center", marginRight: "10px"}} />
						<p className='m-0 p-0' style={{fontFamily: "Inter, sans-serif", fontWeight: "600", alignItems: "center"}}>Pepper</p>
					</Link>
					{/* {PAGE_HEADERS[pageLocation] && */}
					{/* <span style={{fontSize: 'large'}}> */}
					{/* <b> {PAGE_HEADERS[pageLocation]}</b></span>} */}
					<div>
						{/* <Tabs/> */}
					</div>
				</div>
				{/* <div className={Styles.searchDiv}>
			<img src={SearchIcon} alt="Search Icon" className='mx-2 mb-1' />
			<input type="text" name="" id="" placeholder='Search' className={Styles.inputBox} />
		</div> */}
				<div style={{display: 'flex', alignItems: 'center'}}>
					<Popover placement="bottomRight" open={guidePopupOpen} content={<>Refer to user guide</>} >
						<a href={UserDemo} rel="noreferrer" target="_blank">
							<img style={{ cursor: "pointer" }} className="me-2" src={helpIcon} alt="Help Icon" />
						</a>
					</Popover>
					{/* <img  style={{cursor:"pointer"}} src={AddIcon} alt="Add Icon" className='me-3' /> */}
					<img src={NotificationIcon} alt="Notification icon" className='me-1' />
					{/* <img  src={profile} className='me-3' /> */}
					<Popover content={customizationContent} placement="bottomLeft" title="">
						{/* <SettingOutlined style={{ fontSize: '25px'}} /> */}
					</Popover>

					<Avatar size={36} style={{ backgroundColor: '#EAAE4E', color: 'white', fontSize: '17px', margin: '0rem 0.9rem', padding: '1rem' }}>GS</Avatar>
				</div>
			</div>
		</nav>
	);
};