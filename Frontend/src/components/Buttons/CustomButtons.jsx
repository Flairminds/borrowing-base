import React from 'react'
import ButtonStyle from './Buttons.module.css'
export const CustomButtons = ({isfilled , text , isOk }) => {
  return (
    <button 
    className={`mx-3 ${isfilled ? `${ButtonStyle.filledBtn}` : `${ButtonStyle.outlinedBtn}` } ${isOk ? `${ButtonStyle.okButton}` : '' }`}>
        {text}
    </button>
  )
}
