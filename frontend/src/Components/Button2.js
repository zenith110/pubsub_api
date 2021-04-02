import React from 'react'
import {motion} from "framer-motion"
import "./Button2.css"

const Button2 = ({title, onClick, type, size, variant, href}) => {
    return (

            <motion.div type={type} onClick={onClick} className={`btn2 ${size} ${variant}`}
                 whileHover={{scale:1.1
                        }}>
                <a className="btn2-title" href={href}>{title}</a>
            </motion.div>
 
    )
}

export default Button2
