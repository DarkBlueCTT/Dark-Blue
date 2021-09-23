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

import React, { Component } from 'react';
import './css/Style.css';
import Button from '@material-ui/core/Button';
import UserField from '../components/UserFields.jsx';
import { setJSONAttribute, getJSONAttribute } from '../components/jsonFileEditor.jsx';


export default class Users extends Component {

    constructor(props) {
        console.log("Constructing users...");
        super(props);
        this.state = {
            users: []
        }
    }

    componentDidMount() {
        this.load();
    }

    componentWillUnmount() {
        this.save();
    }

    addUser = (e) => {
        console.log("Adding a new user.");
        this.setState((prevState) => ({
            users: [...prevState.users, { index: Math.random(), name: "", allowed: false, is_admin: false, admin_initial_state: false, positive_points: 0, negative_points: 0 }],
        }));
    }

    removeUser = (e) => {
        console.log("Removing user with index: " + e.index);
        this.setState({
            users: this.state.users.filter(u => u.index !== e.index)
        })
    }

    handleChange = (e) => {
        let idx = e.target.id.split('-')[1];
        console.log(idx)
        if ("name" === e.target.name) {
            let users = [...this.state.users]
            users[idx][e.target.name] = e.target.value;
        }

        if (["positive_points", "negative_points"].includes(e.target.name)) {
            let users = [...this.state.users]
            users[idx][e.target.name] = parseInt(e.target.value, 10);
        }

        if (["allowed", "is_admin", "admin_initial_state"].includes(e.target.name)) {
            let users = [...this.state.users]
            users[idx][e.target.name] = !users[idx][e.target.name];
        }
    }


    save = () => {
        console.log("Printing user values.");
        console.log(this.state.users);
        setJSONAttribute("users", this.state.users);
    }

    load = () => {
        console.log("Attempting to load users from JSON.");
        var isEmpty = false;
        var isNull = false;
        var data = getJSONAttribute('users');

        if (data === undefined)
            isNull = true;

        if (!isNull && Object.keys(data).length === 0)
            isEmpty = true;

        if (!isEmpty && !isNull) {
            this.setState({ users: data }, () => {
            });
        }
        else if (isEmpty || isNull) {
            this.setState({ users: [{ index: Math.random(), name: "", allowed: false, is_admin: false, admin_initial_state: false, positive_points: 0, negative_points: 0 }] })
        }
        return;
    }

    render() {
        return (
            <div className="page-div">
                <div className="page-header" >
                    <h1>Users</h1>
                </div>
                <div className="page-info">
                    <p>
                        Username: Name of the user that will be created and scored.
                        <br></br>
                        Allowed: If the user is supposed to be present on the system.
                        <br></br>
                        Administrator: If the user is supposed to have administrator status on the system.
                        <br></br>
                        Starting Admin Status: If the user is created with administrator status.
                    </p>
                </div>
                <div className="page-body" >
                    <table style={{ width: '100%' }}>
                        <tbody>
                            <tr>
                                <th>Username</th>
                                <th>Allowed</th>
                                <th>Administrator</th>
                                <th>Starting Admin Status</th>
                                <th>Positive Points</th>
                                <th>Negative Points</th>
                            </tr>
                            <UserField delete={this.removeUser} users={this.state.users} onChange={this.handleChange}></UserField>
                        </tbody>
                    </table>
                    <Button variant="contained" onClick={this.addUser}> Add User </Button>
                    <Button variant="contained" onClick={this.save} style={{ marginLeft: '200px' }}> Save </Button>
                </div>
            </div >);
    }
}
