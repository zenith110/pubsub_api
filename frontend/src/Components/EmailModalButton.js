import React, {Component, useState} from "react";
import EmailModal from './EmailModal.js'
import {Modal, Container, Row, Col, Button, Tabs, Tab} from 'react-bootstrap';
import { MailIcon } from 'react-mail-icon'
import PhoneModal from "./PhoneModal.js"
import Button1 from "./Button1"
import './EmailModalButton.css'


const mailIconStyle = {
    display: 'flex',
    pointer: 'cursor'
  } 

export default function EmailModalButton()
{

    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
  
    return(

        <>
      <Button className="email-btn" variant="primary" onClick={handleShow}>
          <h3>
          Newsletter


          </h3>

        <MailIcon
      mailBackFoldColor="#2874A6"
      mailTopFoldColor="#2E86C1"
      mailLeftFoldColor="#3498DB"
      mailRightFoldColor="#5DADE2"
      letterBackgroundColor="#FFFFFF"
      letterBorderColor="#1ABC9C"
      letterTextColor="#1ABC9C"

      shouldAnimateOnHover
      style={{'pointer': 'cursor'}}/>
      </Button>

 
        
        <Modal show={show} onHide={handleClose} animation={true} centered className="email-modal">

        <Tabs defaultActiveKey="email" className="tabs">

          <Tab eventKey="email" title="Email">
               
            <Modal.Body>

                <EmailModal/>
            </Modal.Body>

          </Tab>

          <Tab eventKey="phone" title="Phone">
              <Modal.Body>
                <PhoneModal/>
              </Modal.Body>

          </Tab>



      </Tabs>
        <Modal.Footer>

          <Button1 onClick={handleClose} title="Close" size="sm" variant="secondary"/>
        </Modal.Footer>
      </Modal>
      </>
       

    );
}

