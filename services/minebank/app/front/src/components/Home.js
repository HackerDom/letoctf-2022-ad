import React, {Component} from 'react';
import Login from "./Login";
import Profile from "./Profile";
import Transaction from "./Transaction";

class Home extends Component {
    render() {
        let component;
        if (this.props.transaction) {
            component = <Transaction transaction={this.props.transaction} unsetTransaction={this.props.unsetTransaction} />
        } else if (this.props.user) {
            component = <Profile user={this.props.user} setTransactionInfo={this.props.setTransactionInfo}/>
        } else {
            component = <Login />
        }
        return (
            <div className='componentContainer'>
                {component}
            </div>
        );
    }
}

export default Home;