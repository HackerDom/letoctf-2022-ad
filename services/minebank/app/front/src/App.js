import React from "react";
import Home from "./components/Home";
import About from "./components/About";
import {BrowserRouter, NavLink, Routes, Route} from "react-router-dom";
import { RiBankCardLine } from "react-icons/ri";
import NewTransaction from "./components/NewTransaction";
import XMLParser from 'react-xml-parser';

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoggedIn: false,
            transaction: undefined,
            user: undefined,
        }
        this.setUser = this.setUser.bind(this)
        this.setTransactionInfo = this.setTransactionInfo.bind(this)
        this.unsetTransaction = this.unsetTransaction.bind(this)
        this.setProfile()
    }

    setUser(user) {
        this.setState({user: user})
    }

    async getTransactions() {
        let res = await fetch("/transaction")
        if (res.status === 200)
            return await res.json()
        return {}
    }

    setProfile() {
        fetch("/profile").then(res => {
                if (res.status === 200)
                    res.json().then(resProfile => {
                        this.getTransactions().then( resTransactions =>
                            this.setUser({...resProfile.data, transactions: resTransactions.data})
                        )
                    })
            }
        ).catch(res => console.log(res))
    }

    async setTransactionInfo(transaction_id) {
        let body = `<?xml version="1.0" encoding="UTF-8"?><xml><transaction_id>${transaction_id}</transaction_id></xml>`
        const res = await fetch("/transaction-info", {
            method: 'POST',
            body: body,
            headers: {'Content-Type': 'application/xml'},
        })
        if (res.status === 200) {
            let xml = new XMLParser().parseFromString(await res.text());
            this.setState({
                transaction:
                    Object.assign({}, ...xml.children.find(el => el.name === "data").children.map(el => ({[el.name]: el.value})))
            })
        }
        else
            this.setState({transaction: undefined})
    }

    unsetTransaction(){
        this.setState({transaction: undefined})
    }

    render() {
        return (
            <div className="wrapper">
                <BrowserRouter>
                    <header>
                        <NavLink to="/"><RiBankCardLine className='logo-icon' /> MineBank</NavLink>
                        <ul className='nav'>
                            {!this.state.user && (
                                <li>
                                    <NavLink to="/about" className='navlink'>About</NavLink>
                                </li>
                            )}
                            {this.state.user && (
                                <div>
                                    <li>
                                        <NavLink to="/new" className='navlink'>New Transaction</NavLink>
                                    </li>
                                    <li>
                                        <a className="navlink" href="/logout">Logout</a>
                                    </li>
                                </div>
                            )}
                        </ul>
                    </header>
                    <main>
                        <Routes>
                            <Route exact path="/" element={<Home
                                user={this.state.user}
                                transaction={this.state.transaction}
                                setTransactionInfo={this.setTransactionInfo}
                                unsetTransaction={this.unsetTransaction}
                            />} />
                            <Route exact path="/about" element={<About />} />
                            <Route exact path="/new" element={<NewTransaction />} />
                        </Routes>
                    </main>
                </BrowserRouter>
            </div>
        );
    }
}

export default App;
