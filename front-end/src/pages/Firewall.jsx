/*
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
*/

import React, { Component } from 'react';
import './css/Style.css';
import Button from '@material-ui/core/Button';
import TextFieldControlled from '../components/TextFieldControlled';
import CheckboxControlled from '../components/CheckboxControlled';
import { setJSONAttribute, getJSONAttribute } from '../components/jsonFileEditor.jsx';

export default class Firewall extends Component {

    constructor(props) {
        console.log("Constructing firewall...");
        super(props);

        this.state = {
            firewall: {}
        }
    }

    // Apparently ComponentDidMount runs after render.
    // We need to make sure load runs before render or the value the controlled inputs receive is undefined.
    // I now have no clue why everything else works using componentDidMount.
    // And it turns out that will mount isn't supposed to be a thing anymore. Love it.
    // To properly fix this I guess I would have to create a firewall fields component.
    UNSAFE_componentWillMount() {
        console.log("ComponentWillMount");
        this.load();
    }

    componentWillUnmount() {
        this.save();
    }

    handleChange = (e) => {
        let split = e.target.name.split('-');

        // Public: 0 Private: 1 Domain: 2
        let profile = split[0];
        let attribute = split[1];

         if (["starting_state", "desired_state"].includes(attribute)) {
                let firewall = this.state.firewall;
                firewall[profile][attribute] = !this.state.firewall[profile][attribute];
            } else {
                let firewall = this.state.firewall;
                firewall[profile][attribute] = parseInt(e.target.value, 10);
        }
    }

    save = () => {
        console.log("Printing firewall values.");

        setJSONAttribute("firewall", this.state.firewall);
    }

    load = () => {
        console.log("Attempting to load firewall states from JSON.");
        var isEmpty = false;
        var isNull = false;
        var data = getJSONAttribute('firewall');

        if (data === undefined)
            isNull = true;

        if (!isNull && Object.keys(data).length === 0)
            isEmpty = true;

        if (!isEmpty && !isNull) {
            this.setState({ firewall: data }, () => {
            });
        } else if (isEmpty || isNull) {
            this.setState({ firewall: [{index: Math.random(), name: "public", starting_state: false, desired_state: false, positive_points: 0, negative_points: 0},{index: Math.random(), name: "private", starting_state: false, desired_state: false, positive_points: 0, negative_points: 0}, {index: Math.random(), name: "domain", starting_state: false, desired_state: false, positive_points: 0, negative_points: 0}] })
        }
    }

    render() {
        return (
            <div className="page-div">
                <div className="page-header" >
                    <h1>Firewall</h1>
                </div>
                <div className="page-info">
                    <p>
                        Starting state: If the firewall profile is enabled when the scoring engine starts.
                        <br></br>
                        Desired state: If the firewall is supposed to be enabled.
                    </p>
                </div>
                <div className="page-body" >

                    <h2>Public</h2>
                    <table style={{ width: '50%' }}>
                        <tbody>
                            <tr>
                                <th>
                                    Starting State
                                </th>
                                <th>
                                    Desired State
                                </th>
                                <th>
                                    Positive Points
                                 </th>
                                <th>
                                    Negative Points
                                </th>
                            </tr>
                            <tr>
                                <td>
                                    <CheckboxControlled name="0-starting_state" id={"0-starting_state"} checked={this.state.firewall[0]["starting_state"]} onChange={this.handleChange}></CheckboxControlled>
                                </td>
                                <td>
                                    <CheckboxControlled name="0-desired_state" id={"0-desired_state"} checked={this.state.firewall[0]["desired_state"]} onChange={this.handleChange}></CheckboxControlled>
                                </td>
                                <td>
                                    <TextFieldControlled name="0-positive_points" id={"0-positive_points"} value={this.state.firewall[0]['positive_points']} onChange={this.handleChange} integer={true}></TextFieldControlled>
                                </td>
                                <td>
                                    <TextFieldControlled name="0-negative_points" id={"0-negative_points"} value={this.state.firewall[0]['negative_points']} onChange={this.handleChange} integer={true}></TextFieldControlled>
                                </td>
                            </tr>
                        </tbody>
                    </table>

                    <h2>Private</h2>
                    <table style={{ width: '50%' }}>
                        <tbody>
                            <tr>
                                <th>
                                    Starting State
                                </th>
                                <th>
                                    Desired State
                                </th>
                                <th>
                                    Positive Points
                                 </th>
                                <th>
                                    Negative Points
                                </th>
                            </tr>
                            <tr>
                                <td>
                                    <CheckboxControlled name="1-starting_state" id={"1-starting_state"} checked={this.state.firewall[1]["starting_state"]} onChange={this.handleChange}></CheckboxControlled>
                                </td>
                                <td>
                                    <CheckboxControlled name="1-desired_state" id={"1-desired_state"} checked={this.state.firewall[1]["desired_state"]} onChange={this.handleChange}></CheckboxControlled>
                                </td>
                                <td>
                                    <TextFieldControlled name="1-positive_points" id={"1-positive_points"} value={this.state.firewall[1]['positive_points']} onChange={this.handleChange} integer={true}></TextFieldControlled>

                                </td>
                                <td>
                                    <TextFieldControlled name="1-negative_points" id={"1-negative_points"} value={this.state.firewall[1]['negative_points']} onChange={this.handleChange} integer={true}></TextFieldControlled>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <h2>Domain</h2>
                    <table style={{ width: '50%' }}>
                        <tbody>
                            <tr>
                                <th>
                                    Starting State
                                </th>
                                <th>
                                    Desired State
                                </th>
                                <th>
                                    Positive Points
                                 </th>
                                <th>
                                    Negative Points
                                </th>
                            </tr>
                            <tr>
                                <td>
                                    <CheckboxControlled name="2-starting_state" id={"2-starting_state"} checked={this.state.firewall[2]["starting_state"]} onChange={this.handleChange}></CheckboxControlled>
                                </td>
                                <td>
                                    <CheckboxControlled name="2-desired_state" id={"2-desired_state"} checked={this.state.firewall[2]["desired_state"]} onChange={this.handleChange}></CheckboxControlled>
                                </td>
                                <td>
                                    <TextFieldControlled name="2-positive_points" id={"2-positive_points"} value={this.state.firewall[2]['positive_points']} onChange={this.handleChange} integer={true}></TextFieldControlled>
                                </td>
                                <td>
                                    <TextFieldControlled name="2-negative_points" id={"2-negative_points"} value={this.state.firewall[2]['negative_points']} onChange={this.handleChange} integer={true}></TextFieldControlled>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <Button variant="contained" onClick={this.save} style={{ marginLeft: '200px' }}> Save </Button>
                </div>
            </div >);
    }
}
