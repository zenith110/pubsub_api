import React, {useEffect, useState} from 'react';
import "./CheckBox.css"

import {Form, Container, Row, Col} from 'react-bootstrap'


const CheckBox = (props) =>
{

    const [sub, setSub] = useState([])
    //const [checkedSubs, setCheckedSubs] = useState([])

    const url = "https://api.pubsub-api.dev"
    
    useEffect(()=>{
        fetch(url + '/onsale/')
        .then ((response) => response.json())
        .then((data) => setSub(data))
        .catch((error) => console.log(error))

    }, [])




    const handleCheck = (e) =>
    {

        if(e.target.checked == true)
        {
                props.setCheckedSubs([...props.checkedSubs, e.target.id])
                //return( {'color': 'green'})

        }
        else if (e.target.checked == false)
        {
            props.setCheckedSubs(props.checkedSubs.filter(sub => sub != e.target.id))

        }

        


    }


    return(<div>
        <Container className="checkbox-container">
            <h4 className="checkbox-title">
                Choose! We tell you when your sub is on sale
            </h4>

            {
                sub.map(sub =>
                    {
                        return (

                                       
                         <Row className="check-row">
                            <Col xs={1}  className="checks">
                                <Form.Check
                                id = {sub.name}
                                type='checkbox'
                                value = {sub.name}
                                onChange={handleCheck}
                                
                                />
                              
                               
                            </Col>
                            <Col  name = {sub.name}>
                                <h5 className="check-title">
                                    {sub.name}
                                </h5>
                            </Col>

                        </Row>
                        )
                    })
            }

        </Container>

    </div>)
}

export default CheckBox;