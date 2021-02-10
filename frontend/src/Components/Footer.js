import React, { useState, useEffect } from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import {Container, Row, Col} from 'react-bootstrap';
import Button1 from "./Button1.js"
import "./Footer.css"

const Footer = () =>{

    return (
      <div className="footer">
        <Container fluid className="footer-container">
            <Row>
              <Col>
                  <Row>
                    <h1>
                      Made By
                    </h1>

                  </Row>
                  <Row>
                      <Button1 title="Abrahan" variant="secondary" className="name-btn"/>
                  </Row>
                  <Row>
                    <h1>& </h1>
                      <Button1 title="Sebastian" variant = "secondary" className="name-btn"/>
                  </Row>
              </Col>
              <Col>
                  <Row>

                  </Row>
              </Col>
            </Row>
        
      </Container>
      </div>
      );

}

export default Footer
// import React, { useState, useEffect } from "react";
// import Modal from "react-modal";
// import 'bootstrap/dist/css/bootstrap.min.css';
// import Button from 'react-bootstrap/Button';
// function Footer(){
//   return ();
// }
  

// export default Footer;
