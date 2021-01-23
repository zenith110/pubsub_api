import React, {useState} from "react";
import CheckBox from "./CheckBox"
import {Modal, Container, Row, Col, Button } from 'react-bootstrap';
import Button1 from "./Button1"
import './PhoneModal.css'

const PhoneModal = () =>{

 const [checkedSubs, setCheckedSubs] = useState([])
  const [phoneNumber, setPhoneNumber] = useState("")

  console.log(checkedSubs)

  const handleInputChange = (e) => {

    setPhoneNumber(e.target.value)
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const info = {
      phoneNumber,
      checkedSubs
    };
    
    fetch("http://127.0.0.1:5000/phone/", {
      method: "POST",
      body: JSON.stringify(info),
      headers: { "Content-Type": "application/json" },
    })
      .then((res) => res.json())
      .then((json) => console.log(json));
  };

    return (
        <form className="form-group" onSubmit={handleSubmit}>
          <Container className="phone-modal-container">
            <Row>
              <Col>
              <h3>Enter phone number</h3>

              </Col>
            </Row>
            <Row>
              <Col>
                <input className="form-control" name = "phoneNumber" placeholder="Phone Number" onChange={handleInputChange}/>
              </Col>
            </Row>
            <Row>
              <Col>
                <CheckBox checkedSubs={checkedSubs} setCheckedSubs={setCheckedSubs}/>
              </Col>
            </Row>

            <Row>
              <Col>
              <Button1 title="Subscribe" onClick={handleSubmit} type="submit" size="md" variant="primary"/>
                
              </Col>
            </Row>
          </Container>
        
      </form> 
    );
  
}

export default PhoneModal;

