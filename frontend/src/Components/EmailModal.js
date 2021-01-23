import React, {Component, useState} from "react";

import {Modal, Container, Row, Col, Button } from 'react-bootstrap';
import CheckBox from "./CheckBox"
import Button1 from "./Button1"
import './EmailModal.css'

const EmailModal = () =>{
  const [email, setEmail] = useState("")
  const [name, setName] = useState("") 
  const [checkedSubs, setCheckedSubs] = useState([])

  const[error, setError] = useState("")

  console.log(checkedSubs)


  const handleInputChange = (e) => {
    
    if(e.target.name == 'email')
      setEmail(e.target.value)
    else if (e.target.name == 'name')
      setName(e.target.value)

    //handle errors
    if(e.target.name == 'name')
    {
      if(Number(e.target.name)== true)
        setError("Name must only be letters")

    }

        


  };


  const handleSubmit = (e) => {
    e.preventDefault();

    const info = {
      email,
      name,
      checkedSubs
    };

    console.log(info)

    fetch("http://127.0.0.1:5000/email/", {
      method: "POST",
      body: JSON.stringify(info),
      headers: { "Content-Type": "application/json" },
    })
      .then((res) => res.json())
      .then((json) => console.log(json));
  };

    


  
    return (
      <div>
      <form className="form-group" onSubmit={handleSubmit}>
        <Container className="newsletter-container">

          <Row>

            <Col className="newsletter-input ">

            <h2 className="newsletter-input-title">
              Sign up for Email notifications today!
            </h2>
       
          
            <div className="form-input" >
              <input
                type="email"
                className="form-control"
                name="email"
                placeholder="Email"
                onChange={handleInputChange}
              />

            </div>
            <br />
            <div className="form-input" >
              <input
                type="text"
                className="form-control"
                name="name"
                placeholder="First Name"
                onChange={handleInputChange}
              />
               <h1>{error}</h1>
            </div>

        
          </Col>

        </Row>

        <Row>
          <Col>
            <CheckBox setCheckedSubs={setCheckedSubs} checkedSubs={checkedSubs}/>
          </Col>
        </Row>

        <Row>
          <Col>
          <div className="sub-btn-container">

            <Button1 title="Subscribe" onClick={handleSubmit} type="submit" size="md" variant="primary"/>

            {/*}
              <button className="sub-btn " type="submit">
                <h4>
                Subscribe
                </h4>
              </button>
            {*/}
            </div>
          </Col>
        </Row>

        

          </Container>
          </form>
       </div>
 
     
    );
  
}

export default EmailModal;

