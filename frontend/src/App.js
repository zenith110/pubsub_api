import './App.css';
import SubCard from "./Components/SubCard.js"
import Grid from "./Components/Grid.js"
import Carousel from 'react-elastic-carousel';
import React, { Component, useState, useEffect} from 'react';
import EmailModal from "./Components/EmailModal.js";
import EmailModalButton from "./Components/EmailModalButton.js";
import NotifcationsBox from "./Components/NotificationsBox.js"
import FilterButtons from "./Components/FilterButtons.js"

import Navbar from "./Components/Navbar.js"
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Row, Col, CardDeck, Card, Button, ToggleButton} from 'react-bootstrap';

function App() {
  // Assigns state to count so we can add new subs
  const[filter, setFilter] = useState("")



  return (
    <div className="App">
      <Navbar></Navbar>
      <Container fluid>
        <Row>
          <Col className="header">
          <h2 style={{'fontFamily': 'Poppins', 'font-size': '40px'}}>
            Current Subs
          </h2>
          <br/>
          </Col>

        </Row>
        <Row>
            <Col className="header">
              <FilterButtons setFilter={setFilter}/>

            </Col>
          </Row>

        <Row >

       
          <Col className="grid">    <Grid filter={filter}/></Col>
        </Row>
        <Row  className="newsletter-margin">
          <Col>
            <NotifcationsBox/>

          </Col>

        </Row>
    

      </Container>
      

    </div>
  );
}

export default App;
