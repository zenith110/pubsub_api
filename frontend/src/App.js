import './App.css';

import SubCardv2 from "./Components/SubCardv2.js"

import Grid from "./Components/Grid.js"
import Carousel from 'react-elastic-carousel';
import React, { Component, useState, useEffect} from 'react';
import EmailModal from "./Components/EmailModal.js";
import EmailModalButton from "./Components/EmailModalButton.js";
import NotifcationsBox from "./Components/NotificationsBox.js"
import FilterButtons from "./Components/FilterButtons.js"
import Footer from "./Components/Footer.js"

import Navbar from "./Components/Navbar.js"
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Row, Col, CardDeck, Card, Button, ToggleButton} from 'react-bootstrap';
// import Footer from "./Components/Footer.js"
function App() {
  // Assigns state to count so we can add new subs
  const[option, setOption] = useState("All")



  return (
    <div className="App">
      <Navbar></Navbar>
      <Container fluid sm className="content-container">
     

       
        <Row className="row-buffer-sm">
          <Col className="header">
          <h2 style={{'fontFamily': 'Poppins', 'font-size': '40px'}}>
            Current Subs
          </h2>
          <br/>
          </Col>

        </Row>
        <Row>
            <Col className="header grid ">
              <FilterButtons setOption={setOption}/>

            </Col>
        </Row>

        <Row className="grid-row row-buffer-sm" >
            <Col xs={12} className="grid ">    
              <SubCardv2 option={option}/>
            </Col>
        </Row>
        <Row  className="newsletter-margin">
          <Col>
            <NotifcationsBox/>

          </Col>

        </Row>

        <Row >
          <Col md={12} fluid>
            <Footer/>
          </Col>
        </Row>

      </Container>
      
    </div>
  );
}

export default App;
