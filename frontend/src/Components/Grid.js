import './Grid.css';
import SubCard from "./SubCard.js"

import React, { Component, useState, useEffect} from 'react';

import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Row, Col, CardDeck, Card} from 'react-bootstrap';


function Grid() {
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
  
    // Will render grid 
    const renderGrid = () =>
    {
        return (<Col>
        <SubCard/>
        </Col>)
    }
    return (
      <div>
         <CardDeck>
             {SubCardArr}
             
         </CardDeck>

   
      </div>
    );
  }
  
  export default Grid;
  