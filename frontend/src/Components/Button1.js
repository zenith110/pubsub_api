import React from 'react'
import "./Button1.css"
import {motion} from "framer-motion"

const Button1 = ({title, onClick}) => {
    return (
        <motion.div onClick={onClick} className="btn1"
            whileHover={{scale:1.1
                        }}>
            <a className="btn1-title">{title}</a>
        </motion.div>
    )
}

export default Button1
