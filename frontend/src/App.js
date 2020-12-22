import './App.css';
import SubCard from "./Components/SubCard.js"
import Carousel from 'react-elastic-carousel';
import React, { Component } from 'react';
import EmailModal from "./Components/EmailModal.js";
import EmailModalButton from "./Components/EmailModalButton.js";
import NotifcationsBox from "./Components/NotificationsBox.js"

import Navbar from "./Components/Navbar.js"
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return (
    <div className="App">
    <Navbar></Navbar>
    <p>Current Subs</p>
    <Carousel>
    <SubCard position={0}></SubCard>
    <SubCard position={1}></SubCard>
    <SubCard position={2}></SubCard>
    <SubCard position={3}></SubCard>
    <SubCard position={4}></SubCard>
    <SubCard position={5}></SubCard>
    </Carousel>

    <NotifcationsBox/>

    
    </div>
  );
}

export default App;
