import React, {Component} from "react";
import Modal from "react-modal";
class Email extends Component {
  constructor(props) {
    super(props);
    this.state = {
      email: "",
      name: "",
    };
  }

  handleInputChange = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    });
  };

  handleSubmit = (e) => {
    e.preventDefault();

    const { email, name } = this.state;

    const info = {
      email,
      name,
    };

    fetch("http://127.0.0.1:5000/email/", {
      method: "POST",
      body: JSON.stringify(info),
      headers: { "Content-Type": "application/json" },
    })
      .then((res) => res.json())
      .then((json) => console.log(json));
  };

  render() {
    return (
      <div className="newsletter-container">
        <br />
        <h1>
          Join our newsletter!
        </h1>
        <h4>
          Get notified whenever there's a pubsub sale!
        </h4>
          <center>
          <form className="form-group" onSubmit={this.handleSubmit}>
            <div style={{ width: "80%" }} >
              <input
                type="email"
                className="form-control"
                name="email"
                placeholder="Email"
                onChange={this.handleInputChange}
              />
            </div>
            <br />
            <div style={{ width: "80%" }} >
              <input
                type="text"
                className="form-control"
                name="name"
                placeholder="First Name"
                onChange={this.handleInputChange}
              />
            </div>
            <div className="sub-btn-container">
              <button className="sub-btn " type="submit">
                <h4>
                Subscribe
                </h4>
              </button>
            </div>
          </form>
       </center>
      </div>
    );
  }
}

export default Email;

