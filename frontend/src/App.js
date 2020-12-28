import './App.css';
import SubCard from "./Components/SubCard.js"
import Grid from "./Components/Grid.js"
import Carousel from 'react-elastic-carousel';
import React, { Component, useState, useEffect} from 'react';
import EmailModal from "./Components/EmailModal.js";
import EmailModalButton from "./Components/EmailModalButton.js";
import NotifcationsBox from "./Components/NotificationsBox.js"

import Navbar from "./Components/Navbar.js"
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Row, Col, CardDeck, Card, Button} from 'react-bootstrap';

function App() {
  // Assigns state to count so we can add new subs
  let[subCount, setSubCount] = useState([])

  let SubCardArr = [];
  var i;
  // Creates an array of subcard components
  for(i = 0; i < subCount; i++){
    SubCardArr.push(<SubCard position={i}></SubCard>)
  }
  // Sends a post request for our number of subs
  useEffect(()=>{
    fetch('http://localhost:5000/totalcount/')
    .then ((response) => response.json())
    .then((data) => setSubCount(data))
    .catch((error) => console.log(error))
  }, [])

  return (
    <div className="App">
      <Navbar></Navbar>
      <Container fluid>
        <Row>
          <Col>
          <h2>
            Current Subs
          </h2>
          <br/>
          </Col>

        </Row>
        <Row>
            <Col>
              <Button>All</Button>
              <Button>Sale</Button>
              <Button>Not On Sale</Button>
            </Col>
          </Row>

        <Row>

       
          <Col>    <Grid/></Col>
        </Row>
      
 


    <NotifcationsBox/>

    

      </Container>

    </div>
  );
}

export default App;
