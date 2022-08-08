import React, {Component} from 'react';
import { TbDiamond } from "react-icons/tb";

class Transaction extends Component {
    constructor(props) {
        super(props);
        this.statusCodes = [
            "Processing",
            "Successful",
            "Incorrect AccID",
            "Not Enough Diamonds",
        ]
    }

    render() {
        return (
            <div className='profile'>
                <h2> Transaction Info </h2>
                <div className='account'>
                    <div className='infoLine'>
                        <span className='label'>Transaction ID:</span>
                        <span className='data'>{this.props.transaction.id}</span>
                    </div>
                    <div className='infoLine'>
                        <span className='label'>From:</span>
                        <span className='data'>{this.props.transaction.sender_accountID}</span>
                    </div>
                    <div className='infoLine'>
                        <span className='label'>To:</span>
                        <span className='data'>{this.props.transaction.recipient_accountID}</span>
                    </div>
                    <div className='infoLine'>
                        <span className='label'>Diamonds count:</span>
                        <span className='data'>{this.props.transaction.diamondsCount} <TbDiamond className='logo-icon' /></span>
                    </div>
                    <div className='infoLine'>
                        <span className='label'>Description</span>
                        <span className='data'>{this.props.transaction.description}</span>
                    </div>
                    <div className='infoLine'>
                        <span className='label'>Status:</span>
                        <span className='data'>{this.statusCodes[this.props.transaction.status]}</span>
                    </div>
                    <div className='infoLine'>
                        <span className='label'>Date:</span>
                        <span className='data'>{this.props.transaction.createdAt}</span>
                    </div>
                </div>
                <div className="btn" style={{ margin: 0 }} onClick={this.props.unsetTransaction}>Back</div>
            </div>
        );
    }
}

export default Transaction;