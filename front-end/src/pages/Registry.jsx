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
import RegistryField from '../components/RegistryFields';
import { setJSONAttribute, getJSONAttribute } from '../components/jsonFileEditor.jsx';

export default class Registry extends Component {

    constructor(props) {
        super(props);

        this.state = {
            registry: []
        }
    }

    componentDidMount() {
        this.load();
    }

    componentWillUnmount() {
        this.save();
    }

    addRegistry = (e) => {
        console.log("Adding new registry entry.");
        this.setState((prevState) => ({
            registry: [...prevState.registry, { index: Math.random(), key: "", key_path: "", entry_name: "", default_value: "", positive_value: "", negative_value: "", positive_points: 0, negative_points: 0, create: false, positive_message: "", negative_message: "" }]
        }));
    }

    removeRegistry = (e) => {
        console.log("Removing registry with index: " + e.index);
        this.setState({
            registry: this.state.registry.filter(r => r.index !== e.index)
        })
    }

    handleChange = (e) => {
        let idx = -1;
        let name = '';

        try {
            idx = e.target.id.split('-')[1];
        } catch (error) {
            console.log("No id field is present.");
        }

        if (idx === -1) {
            try {
                idx = e.target.name.split('-')[1];
                name = e.target.name.split('-')[0];
            } catch (error) {
                console.log("No ID or name field is present.");
            }
        }

        if (["entry_name", "default_value", "positive_value", "negative_value", "positive_message", "negative_message"].includes(e.target.name)) {
            let registry = [...this.state.registry];
            registry[idx][e.target.name] = e.target.value;
        } else if (e.target.name === "create") {
            let registry = [...this.state.registry];
            registry[idx][e.target.name] = !registry[idx][e.target.name];
        }

        if (e.target.name === "key_path") {
            let registry = [...this.state.registry];
            registry[idx][e.target.name] = e.target.value.replace("/", "\\");
        }

        if (["positive_points", "negative_points"].includes(e.target.name)) {
            let registry = [...this.state.registry];
            registry[idx][e.target.name] = parseInt(e.target.value, 10);
        }

        if (["key"].includes(name) && idx !== -1 && name !== '') {
            let registry = [...this.state.registry];
            registry[idx][name] = e.target.value;
        }

    }

    save = () => {
        console.log("Printing registry values.");
        console.log(this.state.registry);
        setJSONAttribute("registry", this.state.registry);
    }

    load = () => {
        console.log("Attempting to load registry from JSON.");
        var isEmpty = false;
        var isNull = false;
        var data = getJSONAttribute('registry');

        if (data === undefined)
            isNull = true;

        if (!isNull && Object.keys(data).length === 0)
            isEmpty = true;

        if (!isEmpty && !isNull) {
            this.setState({ registry: data }, () => {
            });
        }
        else if (isEmpty || isNull) {
            this.setState({ registry: [{ index: Math.random(), key: "", key_path: "", entry_name: "", default_value: "", positive_value: "", negative_value: "", positive_points: 0, negative_points: 0, create: false, positive_message: "", negative_message: "" }] })
        }
        return;
    }

    render() {
        return (

            <div className="page-div">
                <div className="page-header" >
                    <h1>Registry Entries</h1>
                </div>
                <div className="page-info">
                    <p>
                        Key: HKEY_LOCAL_MACHINE or HKEY_CURRENT_USER.
                        <br></br>
                        Key path: Path to the registry entry inside the selected key. Must use backslashes.
                        <br></br>
                        Entry name: Name of the value to check inside of the key at the given path.
                        <br></br>
                        Default value: Value the key will be set to when the engine starts.
                        <br></br>
                        Positive value: Value that will award points when set.
                        <br></br>
                        Negative value: Value that will subtract points when set.
                        <br></br>
                        Create: If the entry at the key path in the selected key will be created automatically. If the entry already exists, the value will be modified to match the default value.
                        <br></br>
                        Positive message: Message in the scoring report when points are awarded.
                        <br></br>
                        Negative message: Message in the scoring report when points are subtracted.
                    </p>
                </div>
                <div className="page-body">
                    <table style={{ width: '100%' }}>
                        <tbody>
                            <tr>
                                <th>Key</th>
                                <th>Key path</th>
                                <th>Entry name</th>
                                <th>Default value</th>
                                <th>Positive value</th>
                                <th>Negative value</th>
                                <th>Positive points</th>
                                <th>Negative points</th>
                                <th>Create</th>
                                <th>Positive message</th>
                                <th>Negative message</th>
                            </tr>
                            <RegistryField delete={this.removeRegistry} registry={this.state.registry} onChange={this.handleChange}></RegistryField>
                        </tbody>
                    </table>
                    <Button variant="contained" onClick={this.addRegistry}> Add Registry Entry </Button>
                    <Button variant="contained" onClick={this.save} style={{ marginLeft: '200px' }}> Save </Button>
                </div>
            </div>
        );
    }
}