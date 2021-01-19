import React, { useState, useEffect } from "react";
//import Modal from "react-modal";
import 'bootstrap/dist/css/bootstrap.min.css';
import {Button, Card, Badge, Container, Row, Col, CardDeck, Modal} from 'react-bootstrap';
import './SubCardv2.css'

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
      //console.log(subData)
      console.log("Cur Sub" + e.target.value)
    }
    const handleClose = () => setModalIsOpen(false)

    // fetching pubsub data
    useEffect(()=>{
        fetch('http://localhost:5000/onsale/')
        .then ((response) => response.json())
        .then((data) => setSub(data))
        .catch((error) => console.log(error))

      }, [])

    

      // Modal function returning data by using handleOpen()
      const CustomModal = () =>
      {
        
        return (

          <Modal show={modalIsOpen} onHide={handleClose} centered id={subIndex} animation={false} size="sm">

          
            <Modal.Header>
                          <Modal.Title>
                              {subData.filter(sub => {
                                if(sub.name == curSub)
                                {
                                  return sub
                                } 
                                
                                }
                              ).map(sub => {return sub.name})
                              }
                          </Modal.Title>

                        </Modal.Header>
                        <Modal.Body>
                             <img src={subData.filter(sub => {
                                if(sub.name == curSub)
                                {
                                  return sub
                                } 
                                
                                }
                              ).map(sub => {return sub.image})
                              }></img>

                          </Modal.Body>
                          <Modal.Footer>
                            <h3>
                              {"$" + subData[subIndex].price}
                            </h3>
                            <h2>
                              {subData[subIndex].on_sale}
                            </h2>
                            <Button onClick={handleClose}>Close</Button>
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

                    <div key = {pubsub.name}>
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
