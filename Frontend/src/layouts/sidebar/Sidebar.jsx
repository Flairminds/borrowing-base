import { Tooltip } from 'antd';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router';
import MenuIcon from '../../assets/sideBarIcons/MenuIcon.svg';
import { sidebarItemsArray } from '../../utils/constants/constants';
import Styles from './Sidebar.module.css';

export const Sidebar = () => {
	const [active, setActive] = useState(1);
	const [collapseSidebar, setCollapseSidebar] = useState(false);
	const navigate = useNavigate();

	const handleIconClick = (iconNum, route) => {
		setActive(iconNum);
		navigate(route);
	};

	useEffect(() => {
		const isCollapsed = localStorage.getItem('sidebar-collapsed');
		if (isCollapsed) {
			setCollapseSidebar(JSON.parse(isCollapsed) ? true : false);
		}
	}, []);

	return (
		<div className={`px-1 ${Styles.sidebarContainer}`} onMouseLeave={() => setActive(-1)}>
			<div className={`p-2 mb-4 rounded-3`} onClick={() => {
				setCollapseSidebar(!collapseSidebar);
				localStorage.setItem('sidebar-collapsed', !collapseSidebar);
			}}>
				<img src={MenuIcon} alt={"Menu"} />
			</div>
			{sidebarItemsArray?.map((item, index) => (
				<React.Fragment key={index}>
					<Tooltip placement="right" title={collapseSidebar ? item.name : ""}>
						<div className={`py-2 px-1 my-2 rounded-3`} style={{backgroundColor: active === index + 1 ? '#919191' : '', textWrap: 'nowrap'}}
							onClick={() => handleIconClick(index + 1, item.route)} onMouseEnter={() => setActive(index + 1)}>
							{item.imgSrc ?
								<img src={item.imgSrc} alt={item.imgAlt} />
								: item.imgIcon}
							{!collapseSidebar ? <span style={{padding: '0 5px'}}>{item.name}</span> : <></>}
						</div>
					</Tooltip>
				</React.Fragment>
			))}
		</div>
	);
};