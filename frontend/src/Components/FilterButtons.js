import './FilterButtons.css';
import SubCard from "./SubCard.js"

import React, { Component, useState, useEffect} from 'react';

import {Button} from 'react-bootstrap';


const FilterButtons = (props) => {

    useEffect(() =>
    {
      

    })

    const handleButtons = (e) =>
    {
      if (e.target.value === "All")
      {
         //Show all subs

        props.setOption("All")
        return true
      }
     
      else if (e.target.value === "Sale")
      {
          //Show sale sub(s)

        props.setOption("Sale")
        return true
      }
    
      else if (e.target.value == "NotSale")
      {
        //Show not sale items

        props.setOption("NotSale")
        return true
      }
      
    }

    return (
      <div>

              <Button value="All" className="filter-btn" onClick={handleButtons}>All</Button>
              <Button value="Sale" className="filter-btn" onClick={handleButtons}>On Sale</Button>
              <Button value="NotSale" className="filter-btn" onClick={handleButtons}>Not On Sale</Button>

   
      </div>
    );
  }
  
  export default FilterButtons;
  