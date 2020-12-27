import React, {Component} from "react";

import {Modal, Container, Row, Col, Button } from 'react-bootstrap';
import './EmailModal.css'

class PhoneModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
      phoneNumber: "",
    };
    
  }

  handleInputChange = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    });
  };

  handleSubmit = (e) => {
    e.preventDefault();
    const { phoneNumber } = this.state;

    const info = {
      phoneNumber
    };
    
    fetch("http://127.0.0.1:5000/phone/", {
      method: "POST",
      body: JSON.stringify(info),
      headers: { "Content-Type": "application/json" },
    })
      .then((res) => res.json())
      .then((json) => console.log(json));
  };

  render() {
    return (
        <form className="form-group" onSubmit={this.handleSubmit}>
        <div>
        <h3>Enter phone number</h3>
        <input name = "phoneNumber" onChange={this.handleInputChange}>
        </input>
        <button className="sub-btn">Subscribe</button>
      </div>
      </form> 
    );
  }
}

export default PhoneModal;

