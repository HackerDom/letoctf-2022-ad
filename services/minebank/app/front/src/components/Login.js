import React, {Component} from 'react';

class Login extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoginForm: true,
            msg: "",
            formData : {
                login: "",
                password: "",
                idNumber: "",
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
        const url = this.state.isLoginForm ? "/signin" : "/signup"
        try {
            const res = await fetch(url, {
                method: 'POST',
                body: JSON.stringify({...formData}),
                headers: {'Content-Type': 'application/json'},
            })
            if (res.status === 200) {
                window.location.reload()
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
        let loginBtnStyle = {
            textDecoration: 'underline',
            textDecorationThickness: '3px'
        }
        let registerBtnStyle = {}

        let additionalFields

        if (!this.state.isLoginForm) {
            additionalFields = (
                <div className="input-container">
                    <label> ID number</label>
                    <input type="text" name="idNumber" className='text-input' value={this.state.formData.idNumber} onChange={this.onChangeForm} required />
                </div>
            )
            registerBtnStyle = loginBtnStyle
            loginBtnStyle = {}
        }

        return (
            <div className="loginForm">
                <h2>
                    <span className='navlink' style={loginBtnStyle} onClick={() => this.setState({isLoginForm: true}) }>
                        Sign In
                    </span> /
                    <span className='navlink' style={registerBtnStyle} onClick={() => this.setState({isLoginForm: false})}>
                        Sign Up
                    </span>
                </h2>
                <div className='errmsg'> {this.state.msg} </div>
                <form onSubmit={this.onSubmitForm}>
                    <div className="input-container">
                        <label>Login </label>
                        <input type="text" name="login" className='text-input' value={this.state.formData.username} onChange={this.onChangeForm} required />
                    </div>
                    <div className="input-container">
                        <label>Password </label>
                        <input type="password" name="password" className='text-input' value={this.state.formData.password} onChange={this.onChangeForm} required />
                    </div>
                    {additionalFields}
                    <div className="button-container">
                        <input type="submit" value={this.state.isLoginForm ? "Sign in" : "Sign up now!"} className="btn" />
                    </div>
                </form>
            </div>
        );
    }
}

export default Login;