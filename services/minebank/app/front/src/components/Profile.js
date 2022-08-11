import React, {Component} from 'react';
import { TbDiamond } from "react-icons/tb";

class Profile extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isTxCurrentTab: true
        }
        this.statusCodes = [
            "Processing",
            "Successful",
            "Incorrect AccID",
            "Not Enough Diamonds",
        ]
    }

    render() {
        const underlineStyle = {
            backgroundColor: "rgba(188, 188, 188, 80%)"
        }

        return (
            <div className='profile'>
                <h2> Hello, {this.props.user.login} </h2>
                <div className='account'>
                    <div className='infoLine'>
                        <span className='label'>Your account ID:</span>
                        <span className='data'>{this.props.user.accountID}</span>
                    </div>
                    <div className='infoLine'>
                        <span className='label'>Diamonds count:</span>
                        <span className='data'>{this.props.user.diamondsCount} <TbDiamond className='logo-icon' /></span>
                    </div>
                </div>

                <div className='transactions'>
                    <div className='transactionsTypes'>
                        <div className='transactionsType btn navlink' style={this.state.isTxCurrentTab ? underlineStyle : {}} onClick={() => this.setState({isTxCurrentTab: true}) }>Transmitted</div>
                        <div className='transactionsType btn navlink' style={!this.state.isTxCurrentTab ? underlineStyle : {}} onClick={() => this.setState({isTxCurrentTab: false}) }>Received</div>
                    </div>
                    {this.state.isTxCurrentTab && (
                        <div className='transmitted'>
                            <table>
                                <th>
                                    <td>To AccID</td>
                                    <td>Description</td>
                                    <td>Diamonds Count</td>
                                    <td>Status</td>
                                </th>
                                {this.props.user.transactions.transmitted.map(t => {
                                    return <tr onClick={(e) => this.props.setTransactionInfo(t.id)}>
                                        <td>{t.accountID}</td>
                                        <td>{t.description}</td>
                                        <td>{t.diamondsCount}</td>
                                        <td>{this.statusCodes[t.status]}</td>
                                    </tr>
                                })}
                            </table>
                        </div>
                    )}
                    {!this.state.isTxCurrentTab && (
                        <div className='received'>
                            <table>
                                <th>
                                    <td>From AccID</td>
                                    <td>Description</td>
                                    <td>Diamonds Count</td>
                                    <td>Status</td>
                                </th>
                                {this.props.user.transactions.received.map(t => {
                                    return <tr onClick={(e) => this.props.setTransactionInfo(t.id)}>
                                        <td>{t.accountID}</td>
                                        <td>{t.description}</td>
                                        <td>{t.diamondsCount}</td>
                                        <td>{this.statusCodes[t.status]}</td>
                                    </tr>
                                })}
                            </table>
                        </div>
                    )}
                </div>
            </div>
        );
    }
}

export default Profile;