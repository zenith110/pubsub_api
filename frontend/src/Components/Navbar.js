import React, { useState, useEffect } from "react";
import {Nav, Container, Row, Col} from 'react-bootstrap';
import "./Navbar.css"
function Navbar() 
{
    return(
       <div>
       <Container fluid className="navbar">
           <Row>
               <Col className="title-container">
                    <h1>Publix-Sub Tracker</h1>

               </Col>
           </Row>

       </Container>
       </div>
    )

}

export default Navbar;