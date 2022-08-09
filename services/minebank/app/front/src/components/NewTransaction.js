import React, {Component} from 'react';

class NewTransaction extends Component {
    constructor(props) {
        super(props);
        this.state = {
            msg: "",
            formData: {
                recipient_accountID: "",
                diamondsCount: 0,
                description: ""
            }
        }
        this.onChangeForm = this.onChangeForm.bind(this)
        this.onSubmitForm = this.onSubmitForm.bind(this)
    }

    onChangeForm(event) {
        this.setState(prevState => ({
            formData: {
                ...prevState.formData,
                [event.target.name]: event.target.value
            },
            msg: ""
        }))
    }

    async onSubmitForm(event) {
        event.preventDefault()
        const formData = this.state.formData
        try {
            const res = await fetch("/transaction", {
                method: 'POST',
                body: JSON.stringify({...formData}),
                headers: {'Content-Type': 'application/json'},
            })
            if (res.status === 200) {
                window.location.replace("/")
            }
            if (res.status === 400 || res.status === 404) {
                let resJson = await res.json()
                this.setState({msg: resJson.msg})
            }
        } catch (e) {
            console.log(e)
        }
    }

    render() {
        return (
            <div className='new-transaction'>
                <h2>New transaction</h2>
                <div className='errmsg'> {this.state.msg} </div>
                <form className='transaction-form' onSubmit={this.onSubmitForm}>
                    <div className="input-container">
                        <label>Recipient AccountID</label>
                        <input type="text" name="recipient_accountID" className='text-input' value={this.state.formData.recipient_accountID} onChange={this.onChangeForm} required />
                    </div>
                    <div className="input-container">
                        <label>Diamonds</label>
                        <input type="number" name="diamondsCount" className='text-input' value={this.state.formData.diamondsCount} onChange={this.onChangeForm} required />
                    </div>
                    <div className="input-container">
                        <label>Description</label>
                        <input type="text" name="description" className='text-input' value={this.state.formData.description} onChange={this.onChangeForm} required />
                    </div>
                    <div className="button-container">
                        <input type="submit" value="Create transaction" className="btn" />
                    </div>
                </form>
            </div>
        );
    }
}

export default NewTransaction;