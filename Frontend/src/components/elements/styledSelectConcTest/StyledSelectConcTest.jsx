import React, { useState,useEffect } from 'react'
import {
    Select,
    Tooltip
  } from "antd";
import styles from './StyledSelectConcTest.module.css'


const optionRender = (option) => (
    <div className={styles.optionParent}>
       <div className={styles.testName}>
            {option.data.label.length > 65 ? `${option.data.label.slice(0, 55)}...` : option.data.label }
       </div>
       <Tooltip 
            title={option.data.description.length > 80 ? option.data.description : null } 
            placement="topLeft"
        >
        <div className={styles.description}>
                {option.data.description.length > 80 ? `${option.data.description.slice(0, 80)}...` : option.data.description }
        </div>
       </Tooltip>
    </div>
)




export const StyledSelectConcTest = ({optionsArray, onChange}) => {
    const [options, setOptions] = useState()

    // const filterOption =(searchValue) =>{
    //     setOptions([])
    //     const filteredArray =  options?.filter(item =>{
    //         let str = item.label
    //         return item.label.toLowerCase().includes(searchValue.toLowerCase())
    //     } );
    //     setOptions(filteredArray)
    // }

    const resetOptions = () => {
        if(optionsArray?.length > 0) {
            setOptions(optionsArray)
        }
    }

    useEffect(() => {
        
        if(optionsArray?.length > 0) {
            setOptions(optionsArray)
        }
    }, [optionsArray])
    
  return (
    <>
        <Select
            removeIcon={true}
            style={{
            // width: "100%",
            height: "30px",
            borderRadius: "8px 8px 8px 8px",
            width: "80%",
            margin:'0rem 1rem'
            }}
            showSearch
            placeholder="Select Test"
            onChange={(value) => onChange(value)}
            options={options}
            // onSearch={filterOption}
            // onBlur={resetOptions}
            onFocus={resetOptions}
            onDropdownVisibleChange={resetOptions}
            // dropdownRender={dropdownRender}
            optionRender={optionRender}
        />
        
    </>
  )
}
