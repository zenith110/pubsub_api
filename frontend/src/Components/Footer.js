import React, { useState, useEffect } from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import {Container, Row, Col} from 'react-bootstrap';
import Button1 from "./Button1.js"
import Button2 from "./Button2.js"
import {FaDiscord, FaRobot, FaGithub} from "react-icons/fa"
import "./Footer.css"

const Footer = () =>{

    return (
      <div className="footer">
        <Container className="footer-container">
            <Row>
              <Col className="footer-col-1">
                  
                    <h1>
                      Made By
                    </h1>
                    <Button2 href = "https://www.linkedin.com/in/abrahan-nevarez/" className="" title="Abrahan Nevarez" />
                    <h1>&</h1>
                    <Button2 href = "https://www.linkedin.com/in/sebastian-fabara-695b39171/" className="" title="Sebastian Fabara"/>


          
              
              </Col>

            </Row>

            <Row className="row-buffer">
              <Col >
                    <h4>Go to our Pub Sub API here</h4>
                    <Button1 href= "https://api.pubsub-api.dev/apidocs/" title="Pub Sub API" variant="secondary" className= "api-btn"/>

                
              </Col>
            </Row>

            <Row className="row-buffer-sm icons">
                <Col>
                <a className="icon" href="https://discord.gg/DeHK6C3Kc5">
                    <FaDiscord  size={50}/>
                </a>
                    
                </Col>
                <Col>
                <a className="icon" href="https://discord.com/api/oauth2/authorize?client_id=711747646179770390&permissions=8&scope=bot" >
                  <FaRobot  size={50}/>
                </a>
                    
                </Col>
                <Col>
                <a className="icon" href="https://github.com/zenith110/pubsub_api">
                     <FaGithub  size={50}/>
                </a>
                    
                </Col>
            </Row>

            <Row className="row-buffer">
              <Col>
                    <p>We are not associated with Publix® but we are fans of pub subs. </p>
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
