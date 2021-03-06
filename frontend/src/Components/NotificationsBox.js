import React, { useState, useEffect } from "react";
import {Nav, Container, Row, Col} from 'react-bootstrap';
import "./NotificationsBox.css"
import EmailModalButton from "./EmailModalButton.js"

export default function NotificationsBox() 
{
    return(

        <Container fluid className="notifications-container">
            <Row>
                <Col>
                    <h1 className="notifications-title" style={{'text-align': 'center'}}>
                         Want to get notified?
                    </h1>
                    <h4 className="notifications-desc" style={{'text-align': 'center'}}>Sign up for email notifications for your favorite sub!</h4>
                </Col>

            </Row>
            <Row  className="justify-content-md-center">
                <Col md="auto">
                <EmailModalButton/>
                </Col>

            </Row>
            

           

        </Container>
    );
}