import React from 'react';
import { useState } from 'react';
import { useNavigate } from 'react-router';
import { Tooltip } from 'antd';
import { sidebarItemsArray } from '../../utils/constants/constants';
import MenuIcon from '../../assets/sideBarIcons/MenuIcon.svg';
import Styles from './Sidebar.module.css';

export const Sidebar = () => {
	const [active, setActive] = useState(1);
	const navigate = useNavigate();

	const handleIconClick = (iconNum, route) => {
		setActive(iconNum);
		navigate(route)
	};

	return (
		<div className={`px-2 ${Styles.sidebarContainer}`}>
			<div className={`p-2 mt-2 mb-4 rounded-3`}>
				<img src={MenuIcon} alt={"Menu"} />
			</div>
			{sidebarItemsArray?.map((item, index) => (
				<React.Fragment key={index}>
					<Tooltip placement="right" title={item.name}>
						<div className={`p-2 my-2 rounded-3`} style={active === index + 1 ? { backgroundColor: '#3A4850' } : {}}
							onClick={() => handleIconClick(index + 1, item.route)}>
							<img src={item.imgSrc} alt={item.imgAlt} />
						</div>
					</Tooltip>
				</React.Fragment>
			))}
		</div>
	)
}