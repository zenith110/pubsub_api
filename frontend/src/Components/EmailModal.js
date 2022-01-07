import React, { Component, useState } from "react";

import { Modal, Container, Row, Col, Button } from "react-bootstrap";
import CheckBox from "./CheckBox";
import Button1 from "./Button1";
import "./EmailModal.css";

const EmailModal = ({ setShow }) => {
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [checkedSubs, setCheckedSubs] = useState([]);
  const [error, setError] = useState("");

  const handleInputChange = (e) => {
    if (e.target.name === "email") setEmail(e.target.value);
    else if (e.target.name === "name") setName(e.target.value);

    //handle errors
    if (e.target.name === "name") {
      if (Number(e.target.name) === true) setError("Name must only be letters");
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const info = {
      email,
      name,
      checkedSubs,
    };
    if (email === "" || name === "") {
      alert("Please provide a first name and email!");
    }

    const url = process.env.REACT_APP_PUBSUB_API_URL;
    fetch(url, {
      method: "POST",
      body: JSON.stringify(info),
      headers: { "Content-Type": "application/json" },
      mode: "cors",
    });
    setShow(false);
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

              <div className="form-input">
                <input
                  type="email"
                  className="form-control"
                  name="email"
                  placeholder="Email"
                  onChange={handleInputChange}
                />
              </div>
              <br />
              <div className="form-input">
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
              <CheckBox
                setCheckedSubs={setCheckedSubs}
                checkedSubs={checkedSubs}
              />
            </Col>
          </Row>

          <Row>
            <Col>
              <div className="sub-btn-container">
                <Button1
                  title="Subscribe"
                  onClick={handleSubmit}
                  type="submit"
                  size="md"
                  variant="primary"
                />
              </div>
            </Col>
          </Row>
        </Container>
      </form>
    </div>
  );
};

export default EmailModal;
