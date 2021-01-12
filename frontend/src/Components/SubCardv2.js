import React, { useState, useEffect } from "react";
import Modal from "react-modal";
import 'bootstrap/dist/css/bootstrap.min.css';
import {Button, Card, Badge, Container, Row, Col, CardDeck} from 'react-bootstrap';
import './SubCardv2.css'


Modal.setAppElement("#root")
const SubCardv2 = ( {option},props) => {

    let [subData, setSub] = useState([])
    const [modalIsOpen, setModalIsOpen] = useState(false)
    
    let subsLength = subData.length

    console.log(subsLength)

    console.log(subData)

    useEffect(()=>{
        fetch('http://localhost:5000/onsale/')
        .then ((response) => response.json())
        .then((data) => setSub(data))
        .catch((error) => console.log(error))
      }, [])


    
  return (
          <div>

              <CardDeck className="grid-deck" >

              {
                subData.filter(data => 
                    {
                        if (option == 'All')
                        {
                            return data
                        }
                            
                        else if (option == 'Sale')
                        {
                            return data.on_sale === 'True'
                        }
                        else if (option == "NotSale")
                        {
                            return data.on_sale === 'False'
                        }

                    }

                
                
                    
                    
                    ).map(pubsub => {

                    return(

                    <div>
                         <Card className="sub-card" key = {pubsub}>
                        <Card.Img className="sub-card-img" variant="top" src = {pubsub.image} />
                          
                          <Card.Body>
                            <Card.Title className="sub-card-title">{pubsub.name}</Card.Title>
                            
                            <Card.Text>
                              <Container fluid>
                                <Row className="card-details">
                                  <Col sm={4} >
                                      <Badge className="badge" pill variant = {pubsub.on_sale === 'False'? 'danger' : 'success'} >
                                         <h4>
                                          {pubsub.on_sale === 'True'? "On Sale" : "Not On Sale"}
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
                          <img src={pubsub.image}></img>
                          <p>Sub name: {pubsub.name}</p>
                       
                          <p>Price during sale: {pubsub.price}</p>
                          <p>Status: {pubsub.on_sale === 'True' ? 'On Sale': 'Not On Sale'}</p>
                         
                          <button onClick={() => setModalIsOpen(false)}>Close</button>
                        </center>
                        </Modal>


                        </div>
                       


                    );


                }
                )

              }

              </CardDeck>
              




           
          </div>
  );
}

export default SubCardv2;
