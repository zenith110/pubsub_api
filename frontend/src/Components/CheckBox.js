import React, {useEffect, useState} from 'react';
import "./CheckBox.css"

import {Form, Container, Row, Col} from 'react-bootstrap'


const CheckBox = () =>
{

    const [sub, setSub] = useState([])
    const [checkedSubs, setCheckedSubs] = useState([])

    
    
    useEffect(()=>{
        fetch('http://localhost:5000/onsale/')
        .then ((response) => response.json())
        .then((data) => setSub(data))
        .catch((error) => console.log(error))

    }, [])




    const handleCheck = (e) =>
    {
        console.log(e.target.checked)

        if(e.target.checked == true)
        {
                console.log(e.target.id + " has been checked")
                setCheckedSubs([...checkedSubs, e.target.id])

                console.log(checkedSubs)

        }
        else if (e.target.checked == false)
        {
            setCheckedSubs(checkedSubs.filter(sub => sub != e.target.id))
            console.log(checkedSubs)
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