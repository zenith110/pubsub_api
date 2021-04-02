import React, { useState, useEffect } from "react";
import Modal from "react-modal";
import 'bootstrap/dist/css/bootstrap.min.css';
import {Button, Card, Badge, Container, Row, Col} from 'react-bootstrap';
import './SubCard.css'

class Sub{
  constructor(){
    this.query_name = [];
    this.image = [];
    this.last_on_sale = [];
    this.price = [];
    this.on_sale = [];
    this.status = "";
    this.buttontype = "";
    this.original_name = [];
  }
}
Modal.setAppElement("#root")
const SubCard = ({position}, params) => {

    let SubArr = []
    let[subData, setSub] = useState([])
    const [modalIsOpen, setModalIsOpen] = useState(false)
    let sub = new Sub();
    const url = "https://api.pubsub-api.dev"
    useEffect(()=>{
        fetch(url + '/onsale/')
        .then ((response) => response.json())
        .then((data) => setSub(data))
        .catch((error) => console.log(error))
      }, [])


 
    sub.query_name =  subData.map(pubsub => pubsub.query_name)
    sub.original_name = subData.map(pubsub => pubsub.name)
    sub.image = subData.map(pubsub => pubsub.image)
    sub.on_sale = subData.map(pubsub => pubsub.on_sale)
    sub.price = subData.map(pubsub => pubsub.price)
    sub.last_on_sale = subData.map(pubsub => pubsub.last_on_sale)
    if(sub.on_sale[position] === "False"){
      sub.status = "Not On Sale"
      sub.buttontype = "danger"
      console.log(params)
      console.log(typeof(params));
   
    }else if(sub.on_sale[position] === "True"){
      sub.status = "On Sale"
      sub.buttontype = "success"
      
    }

    
  return (
          <div>


            <Card className="sub-card">
            <Card.Img className="sub-card-img" variant="top" src = {sub.image[position]} />
              
              <Card.Body>
                <Card.Title className="sub-card-title">{sub.original_name[position]}</Card.Title>
                
                <Card.Text>
                  <Container fluid>
                    <Row className="card-details">
                      <Col sm={4} >
                          <Badge className="badge" pill variant = {sub.buttontype} >
                             <h4>
                              {sub.status}
                             </h4>
                          </Badge>
                      </Col>
                      <Col sm={{ span: 4, offset: 4 }}>
                        <Button size = "lg" className="more-info-btn" onClick={() => setModalIsOpen(true)}>
                          Info
                        </Button>
                      </Col>
                    </Row>
                  </Container>
                
           
                </Card.Text>
              </Card.Body>
             
            </Card>
            
            
            
            <Modal isOpen={modalIsOpen} onRequestClose={() => setModalIsOpen(false)}
            style={
              {
                overlay: {
                  backgroundColor: "gray"
                }
              }
            }>
            <center>
              <img src={sub.image[position]}></img>
              <p>Sub name: {sub.original_name[position]}</p>
              <p>Last time on sale: {sub.last_on_sale[position]}</p>
              <p>Price during sale: {sub.price[position]}</p>
              <p>Status: {sub.status}</p>
              <p>How to access {sub.query_name[position]} json:</p>
              <p>https://pubsub-api.dev/subs/?name={sub.query_name[position]}</p>
              <button onClick={() => setModalIsOpen(false)}>Close</button>
            </center>
            </Modal>
          </div>
  );
}

export default SubCard;

/*
const SubGrid = ({SubCard}) =>
{
   if (subData.length < 0)
    {let subCount = subData.length;}

  let SubCardArr = [];
  var i;
     // Creates an array of subcard components
  for(i = 0; i < subCount; i++){
    SubCardArr.push(<SubCard className="sub-card" position={i}></SubCard>)
  }

  return (
    <CardDeck>{SubCardArr}</CardDeck>
  )
}
*/