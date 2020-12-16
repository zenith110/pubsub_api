import './App.css';
import SubCard from "./Components/SubCard.js"
import Carousel from 'react-elastic-carousel';
import React, { Component } from 'react';
import Email from "./Components/Email.js";
function App() {
  return (
    <div className="App">
    <p>Current Subs</p>
    <Carousel>
    <SubCard position={0}></SubCard>
    <SubCard position={1}></SubCard>
    <SubCard position={2}></SubCard>
    <SubCard position={3}></SubCard>
    <SubCard position={4}></SubCard>
    <SubCard position={5}></SubCard>
    </Carousel>
    <Email></Email>
    
    </div>
  );
}

export default App;
