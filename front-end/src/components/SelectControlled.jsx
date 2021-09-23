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
import Select from '@material-ui/core/Select';
import { MenuItem } from '@material-ui/core';

class SelectControlled extends Component {
    constructor(props) {
        super(props)

        this.superHandleChange = this.props.onChange.bind(this);

        this.state = {
            value: props.value,
            name: props.name,
            id: props.id,
            labels: props.labels,
        }
    }

    superHandleChange = (e) => {
    }

    handleChange = (e) => {
        this.setState({ value: e.target.value });
        this.superHandleChange(e);
    }

    render() {
        return (
            <div>
                <Select name={this.state.name} id={this.state.id} value={this.state.value} onChange={this.handleChange} style={{ backgroundColor: "white" }}>
                    {this.state.labels.map((label) =>
                        <MenuItem key={label} value={label}>{label}</MenuItem>
                    )}
                </Select>
            </div>
        )
    }
}

export default SelectControlled
