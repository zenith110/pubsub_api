import React, {useEffect, useState} from 'react';
import "./CheckBox.css"

import {Form, Container, Row, Col} from 'react-bootstrap'


const CheckBox = (props) =>
{

    const [sub, setSub] = useState([])
    //const [checkedSubs, setCheckedSubs] = useState([])

    
    
    useEffect(()=>{
        fetch('http://localhost:5000/onsale/')
        .then ((response) => response.json())
        .then((data) => setSub(data))
        .catch((error) => console.log(error))

    }, [])




    const handleCheck = (e) =>
    {

        if(e.target.checked == true)
        {
                console.log(e.target.id + " has been checked")
                props.setCheckedSubs([...props.checkedSubs, e.target.id])

        }
        else if (e.target.checked == false)
        {
            props.setCheckedSubs(props.checkedSubs.filter(sub => sub != e.target.id))

        }




        //setCheckedSubs([...sub, {'checked' : false}])

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

                                       
                         <Row >
                            <Col sm={1} className="checks">
                                <Form.Check
                                id = {sub.name}
                                type='checkbox'
                                value = {sub.name}
                                onChange={handleCheck}
                                />
                              
                               
                            </Col>
                            <Col sm={11}>
                                <h5>
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