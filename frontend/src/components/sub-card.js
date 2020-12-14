import React, { useState } from "react";
import { Link } from "react-router-dom";

function SubCard() {
  const handleClick = async (event) => {
    // Call backend to get all the data from the API
    const response = await fetch("https://pubsub-api.dev/onsale/", {
        method: "POST",
      });
    const subData = await response.json();
    console.log(subData)
  };
}

export default SubCard;
