import dollarMoneyCurrencyIcon from '../../assets/sideBarIcons/dollarMoneyCurrencyIcon.svg';
import DoneCheckIcon from '../../assets/sideBarIcons/DoneCheckIcon.svg';
import GroupUserIcon from '../../assets/sideBarIcons/GroupUserIcon.svg';
import HomeIcon from '../../assets/sideBarIcons/HomeIcon.svg';
import projectDocumentsIcon from '../../assets/sideBarIcons/projectDocumentsIcon.svg';
import suitcasePortfolioIcon from '../../assets/sideBarIcons/suitcasePortfolioIcon.svg';
import ThreeBarIcon from '../../assets/sideBarIcons/ThreeBarIcon.svg';

export const updateAssetDefaultColumnsData = {
    'PL BB Build' : 'Investment_Name',
    'Other Metrics' : 'Other_Metrics',
    'Availability Borrower' : 'A',
    'PL BB Results' : 'Concentration_Tests',
    'Subscription BB' : 'Investor',
    'PL_BB_Results_Security' : 'Security',
    'Inputs ' : 'Industries',
    'Pricing' : 'Pricing',
    'Portfolio LeverageBorrowingBase' : 'Investment_Type',
    'Obligors Net Capital' : 'Obligors_Net_Capital',
    'Advance Rates' : 'Investor_Type',
    'Concentration Limits' : 'Investors',
    'Principle Obligations' : 'Principal_Obligations'
}

export const updateAssetModalData = {
    defaultSelectedSheet:'PL BB Build',
}

export const fundOptionsArray = [
    { value:0 , label:'Select Fund'},
    { value:1 , label:'PCOF'},
    { value:2 , label: 'PFLT' },
]

export const sidebarItemsArray = [
    { imgSrc: HomeIcon,imgAlt: "Home Icon" },
    { imgSrc: ThreeBarIcon,imgAlt:"ThreeBar Icon"},
    { imgSrc: DoneCheckIcon,imgAlt:"DoneCheck Icon"},
    { imgSrc: projectDocumentsIcon,imgAlt:"projectDocuments Icon" },
    { imgSrc: suitcasePortfolioIcon,imgAlt:"suitcasePortfolio Icon" },
    { imgSrc: GroupUserIcon,imgAlt:"GroupUser Icon" },
    { imgSrc: dollarMoneyCurrencyIcon,imgAlt:"dollarMoneyCurrency Icon" },
  ];
