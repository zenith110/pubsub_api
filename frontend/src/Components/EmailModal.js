import React, {Component} from "react";

import {Modal, Container, Row, Col, Button } from 'react-bootstrap';
import './EmailModal.css'

class EmailModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
      email: "",
      name: "",

    };
    
  }

  handleInputChange = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    });
  };

  handleSubmit = (e) => {
    e.preventDefault();

    const { email, name } = this.state;

    const info = {
      email,
      name,
    };

    fetch("http://127.0.0.1:5000/email/", {
      method: "POST",
      body: JSON.stringify(info),
      headers: { "Content-Type": "application/json" },
    })
      .then((res) => res.json())
      .then((json) => console.log(json));
  };


  render() {
    return (
      <Container className="newsletter-container">

        <Row>

          <Col className="newsletter-input">

            <h2 className="newsletter-input-title">
              Sign up for Email notifications today!
            </h2>
       
          <form className="form-group" onSubmit={this.handleSubmit}>
            <div className="form-input" >
              <input
                type="email"
                className="form-control"
                name="email"
                placeholder="Email"
                onChange={this.handleInputChange}
              />
            </div>
            <br />
            <div className="form-input" >
              <input
                type="text"
                className="form-control"
                name="name"
                placeholder="First Name"
                onChange={this.handleInputChange}
              />
            </div>
            <div className="sub-btn-container">
              <button className="sub-btn " type="submit">
                <h4>
                Subscribe
                </h4>
              </button>
            </div>
          </form>
          </Col>

        </Row>

      </Container>
 
     
    );
  }
}

export default EmailModal;

