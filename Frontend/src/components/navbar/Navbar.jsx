import React from 'react'
import Logo from "../../assets/NavbarIcons/Logo.svg"
// import help from "../../assets/NavbarIcons/help.svg"
import profile from "../../assets/NavbarIcons/profile.svg"
import { Link } from "react-router-dom";
import NotificationIcon from '../../assets/NavbarIcons/NotificationIcon.svg'
import helpIcon from "../../assets/NavbarIcons/question.svg"
import AddIcon from '../../assets/NavbarIcons/AddIcon.svg'
import SearchIcon from '../../assets/NavbarIcons/SearchIcon.svg'
import Styles from './Navbar.module.css'
import UserDemo from '../../assets/pdfFolder/Portfolio Dashboard User Guide Manual.pdf'
import { Avatar, Popover, Tooltip } from 'antd';
import { SettingOutlined } from '@ant-design/icons';

import { useEffect, useState } from 'preact/hooks';
import { ColumnSelectionPopup } from '../../modal/columnSelectionPopup/ColumnSelectionPopup';


export const Navbar = () => {
  const [guidePopupOpen, setGuidePopupOpen] = useState(false)

  useEffect(() => {
    setTimeout(() => {
      setGuidePopupOpen(false)
    }, 2000);
    setGuidePopupOpen(true)
  },[])

  const customizationContent = (
    <div>
      <div>Asset Parameter Selection</div>
    </div>
  )

  return (
    <nav className="navbar navbar-expand-lg d-flex flex-row w-100"  style={{borderBottom :'1px solid #DEDDDC'
    //  ,height:'7%'
     }}>
      <div className="container-fluid"  >
    <div  style={{display:"flex",alignItems:"center"}}>
    <Link className="navbar-brand d-flex flex-row" to='/' style={{  }}>
          <img  src={Logo} className="d-inline-block align-text-top" alt="Logo" style={{alignItems:"center", marginRight:"10px"}} />
          <p className='m-0 p-0' style={{fontFamily:"Inter, sans-serif", fontWeight:"600",alignItems:"center"}}>Pepper</p>
        </Link>
        <div>
          {/* <Tabs/> */}
        </div>
    </div>
    
    {/* <div className={Styles.searchDiv}>
        <img src={SearchIcon} alt="Search Icon" className='mx-2 mb-1' />
        <input type="text" name="" id="" placeholder='Search' className={Styles.inputBox} />
    </div> */}
     
    <div style={{display:'flex' , alignItems:'center'}}>
      <Popover  placement="bottomRight" open={guidePopupOpen} content={<>Refer to user guide</>} >
        <a href={UserDemo} rel="noreferrer" target="_blank">
          <img style={{ cursor: "pointer" }} className="me-2" src={helpIcon} alt="Help Icon" />
        </a>
      </Popover>
        {/* <img  style={{cursor:"pointer"}} src={AddIcon} alt="Add Icon" className='me-3' /> */}
        <img src={NotificationIcon} alt="Notification icon" className='me-1' />
        {/* <img  src={profile} className='me-3' /> */}
        <Popover content={customizationContent} placement="bottomLeft"  title="">
          {/* <Button type="primary">Hover me</Button> */}
          {/* <SettingOutlined style={{ fontSize: '25px'}} /> */}
        </Popover>

        <Avatar size={36} style={{ backgroundColor: '#EAAE4E', color: 'white', fontSize:'17px', margin :'0rem 0.9rem' ,padding:'1rem' }}>GS</Avatar>


    </div>
    </div>
    </nav>
  )
}