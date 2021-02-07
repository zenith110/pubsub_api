import React, { useState, useEffect } from "react";
//import Modal from "react-modal";
import 'bootstrap/dist/css/bootstrap.min.css';
import {Button, Card, Badge, Container, Row, Col, CardDeck, Modal} from 'react-bootstrap';
import './SubCardv2.css'
import {motion} from "framer-motion"

import Button1 from "./Button1"

const SubCardv2 = ( {option}) => {

    let [subData, setSub] = useState([])
    const [modalIsOpen, setModalIsOpen] = useState(false)
    const [subIndex, setSubIndex] = useState(0);
    const [curSub, setCurSub] = useState("");

    // Get ID for indivdual card info button. Return subData position for modal
    const handleOpen = (e) => 
    {
      setModalIsOpen(true);
      setSubIndex(e.target.id);
      setCurSub(e.target.value)

    }
    const handleClose = () => setModalIsOpen(false)

    // fetching pubsub data
    useEffect(()=>{
        fetch('https://api.pubsub-api.dev/onsale/')
        .then ((response) => response.json())
        .then((data) => setSub(data))
        .catch((error) => console.log(error))
      }, [])

      console.log(subData)

    
      
      // Modal function returning data by using handleOpen()
      // Why does this look complicated?
      //
      // Answer:
      // I am mapping all the buttons on each sub card to the correct modal.
      // This was the only way to work around a react bug that does not allow for modals to be called
      // over and over again when rendering each individual sub card
      const CustomModal = () =>
      {
        
        return (

          <Modal className= "sub-modal" show={modalIsOpen} onHide={handleClose} centered id={subIndex} animation={false} size="md">

          
            <Modal.Header >
                          <Modal.Title >
                            <div className="modal-title">

                            <h2>
                            {subData.filter(sub => {
                                if(sub.name == curSub)
                                {
                                  return sub
                                } 
                                
                                }
                              ).map(sub => {return sub.name})
                              }

                            </h2>

                            
                              
                            </div>
                            
                            
                          </Modal.Title>

                        </Modal.Header>
                        <Modal.Body className="modal-image-container">
                             <img className="modal-image" src={subData.filter(sub => {
                                if(sub.name == curSub)
                                {
                                  return sub
                                } 
                                
                                }
                              ).map(sub => {return sub.image})
                              }></img>

                          </Modal.Body>
                          <Modal.Footer>
                            <Container className="modal-details-container">
                              <Row>
                                <Col>
                                <h3 style={{fontWeight: 600}}>
                              
                            {subData.filter(sub => {
                                if(sub.name == curSub)
                                {
                                  return sub
                                } 
                                
                                }
                              ).map(sub => {return sub.price })
                              }
                            </h3>
                                </Col>
                              </Row>
                              <Row>
                                <Col>
                                
                            {subData.filter(sub => {
                                if(sub.name == curSub)
                                {
                                  return sub
                                } 
                                
                                }
                              ).map(sub => {return sub.on_sale=== "True" ? <h2 style={{color: ' #34af6b'}}>On Sale</h2>: <h2 style={{color: 'red'}}>Not On Sale</h2>})
                              }
                            
                                </Col>
                              </Row>
                              <Row>
                                <Col>
                                <h2>
                              Last on Sale:
                              {subData.filter(sub => {
                                if(sub.name == curSub)
                                {
                                  return sub
                                } 
                                
                                }
                              ).map(sub => {return sub.last_on_sale})
                              }

                            </h2>
                                </Col>
                              </Row>

                              <Row>
                                <Col>
                                  <Button1 onClick={handleClose} title="Close" size="sm" variant="secondary"/>
                                </Col>
                              </Row>
                            </Container>
                            
                           
                            
                           
            </Modal.Footer>
        
          </Modal>
        )
      }

    
  return (
          <div>

              <CardDeck className="grid-deck" >

              {
                // filters pubsub cards bases on filterbuttons
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

                
      
                    //maps the filtered array to card component
                    ).map((pubsub, index) => {

                     

                    return(

                      <motion.div key = {pubsub.name}
                      
                      whileHover={{scale: 1.09, originX: .48, originY: .5}}
                      transition={{type: 'spring', stiffness: 200 }}>
                         <Card className="sub-card" >
                        <Card.Img className="sub-card-img" variant="top" src = {pubsub.image} />
                          
                          <Card.Body>
                            <Card.Title className="sub-card-title">{pubsub.name}  </Card.Title>
                            
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
                                    <Button id={index} size = "lg" className="more-info-btn" onClick={handleOpen} value={pubsub.name}>
                                      Info
                                    </Button>

                                    <CustomModal key={pubsub.name} pubsub={pubsub} pos={index} />

                                  </Col>
                                </Row>
                              </Container>
                            
                       
                            </Card.Text>
                          </Card.Body>
                         
                        </Card>
                        
                        
                        
                   
                         
                       


                        </motion.div>
                       


                    );


                }
                )

              }
              {
                subData.length === 0 ? <h1>Nothing here</h1> : ""
              }

              </CardDeck>
              

          </div>
  );
}

export default SubCardv2;
