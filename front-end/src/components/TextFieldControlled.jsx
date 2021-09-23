{/*
The Dark Blue CyberPatriot Training Tool
Copyright (C) 2021 Scott Semian <darkbluedev@gmail.com>

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <https://www.gnu.org/licenses/>.
*/}

import React, { Component } from 'react'
import TextField from '@material-ui/core/TextField';

class TextFieldControlled extends Component {
    constructor(props) {
        super(props)
        this.superHandleChange = this.props.onChange.bind(this);

        this.state = {
            value: props.value,
            name: props.name,
            id: props.id,
            integer: props.integer
        }
    }

    superHandleChange = (e) => {
    }

    handleChange = (e) => {

        if (!this.state.integer && !this.state.backslash) {
            this.setState({ value: e.target.value });
            this.superHandleChange(e);
        } else if (this.state.integer) {
            const re = /[0-9]/g;
            if (e.target.value !== '' && re.test(e.target.value)) {
                this.setState({ value: parseInt(e.target.value, 10) });
                this.superHandleChange(e);
            }

            if (e.target.value === '') {
                this.setState({ value: '' });
                this.superHandleChange(e);
            }
        }
    }

    render() {
        return (
            <div>
                <TextField name={this.state.name} id={this.state.id} value={this.state.value} onChange={this.handleChange} style={{ backgroundColor: "white" }}></TextField>
            </div>
        )
    }
}

export default TextFieldControlled
