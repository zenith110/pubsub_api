import React, { useState, useEffect } from "react";
import {Nav, Container, Row, Col} from 'react-bootstrap';
import "./NotificationsBox.css"
import EmailModalButton from "./EmailModalButton.js"
export default function NotificationsBox() 
{
    return(

        <Container className="notifications-container">
            <Row>
                <Col>
                    <h1 style={{'text-align': 'center'}}>
                         Want to get notified?
                    </h1>
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