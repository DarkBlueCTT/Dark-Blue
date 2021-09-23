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
import ConfigFileField from '../components/ConfigFileFields.jsx'
import { setJSONAttribute, getJSONAttribute } from '../components/jsonFileEditor.jsx';

export default class ConfigFile extends Component {

    constructor(props) {
        super(props);

        this.state = {
            configfiles: []
        }
    }

    componentDidMount() {
        this.load();
    }

    componentWillUnmount() {
        this.save();
    }


    addFile = (e) => {
        console.log("Adding new configfile entry.");
        this.setState((prevState) => ({
            configfiles: [...prevState.configfiles, { index: Math.random(), filepath: "", default_value: "", positive_value: "", negative_value: "", positive_points: 0, negative_points: 0, create: false, positive_message: "", negative_message: "" }]
        }));
    }

    removeFile = (e) => {
        console.log("Removing configfile with index: " + e.index);
        this.setState({
            configfiles: this.state.configfiles.filter(r => r.index !== e.index)
        })
    }

    handleChange = (e) => {
        let idx = -1;

        try {
            idx = e.target.id.split('-')[1];
        } catch (error) {
            console.log("No id field is present.");
        }

        if (["filepath", "default_value", "positive_value", "negative_value", "positive_message", "negative_message"].includes(e.target.name)) {
            let configfiles = [...this.state.configfiles];
            configfiles[idx][e.target.name] = e.target.value;
        } else if (e.target.name === "create") {
            let configfiles = [...this.state.configfiles];
            configfiles[idx][e.target.name] = !configfiles[idx][e.target.name];
        }

        if (["positive_points", "negative_points"].includes(e.target.name)) {
            let configfiles = [...this.state.configfiles];
            configfiles[idx][e.target.name] = parseInt(e.target.value, 10);
        }
    }

    save = () => {
        console.log("Printing configfiles values.");
        console.log(this.state.configfiles);
        setJSONAttribute("config_files", this.state.configfiles);
    }

    load = () => {
        console.log("Attempting to load configfiles from JSON.");
        var isEmpty = false;
        var isNull = false;
        var data = getJSONAttribute('config_files');

        if (data === undefined)
            isNull = true;

        if (!isNull && Object.keys(data).length === 0)
            isEmpty = true;

        if (!isEmpty && !isNull) {
            this.setState({ configfiles: data }, () => {
            });
        }
        else if (isEmpty || isNull) {
            this.setState({ configfiles: [{ index: Math.random(), filepath: "", default_value: "", positive_value: "", negative_value: "", positive_points: 0, negative_points: 0, create: false, positive_message: "", negative_message: "" }] })
        }
    }

    render() {
        return (

            <div className="page-div">
                <div className="page-header" >
                    <h1>Configuration Files</h1>
                </div>
                <div className="page-info">
                    <p>
                        File path: Path to the file that will be created or scored.
                        <br></br>
                        Default value: Value that will be added to the file when it is created or the expected default value.
                        <br></br>
                        Positive value: Value that will award points when file is set to this value.
                        <br></br>
                        Negative value: Value that will subtract points when the file is set to this value.
                        <br></br>
                        Create: If the value will be created automatically at the given file path.  
                    </p>
                </div>
                <div className="page-body">
                    <table style={{ width: '100%' }}>
                        <tbody>
                            <tr>
                                <th>File path</th>
                                <th>Default value</th>
                                <th>Positive value</th>
                                <th>Negative value</th>
                                <th>Positive points</th>
                                <th>Negative points</th>
                                <th>Create</th>
                                <th>Positive message</th>
                                <th>Negative message</th>
                            </tr>
                            <ConfigFileField delete={this.removeFile} configfiles={this.state.configfiles} onChange={this.handleChange}></ConfigFileField>
                        </tbody>
                    </table>
                    <Button variant="contained" onClick={this.addFile}> Add Configuration File </Button>
                    <Button variant="contained" onClick={this.save} style={{ marginLeft: '200px' }}> Save </Button>
                </div>
            </div>
        );
    }
}