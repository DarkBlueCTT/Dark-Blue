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
import ProcessFields from '../components/ProcessFields.jsx'
import { setJSONAttribute, getJSONAttribute } from '../components/jsonFileEditor.jsx';

export default class Processes extends Component {

    constructor(props) {
        console.log("Constructing processes...");
        super(props);
        this.state = {
            processes: []
        }
    }

    componentDidMount() {
        this.load();
        console.log("State after load: " + this.state.users);
    }

    componentWillUnmount() {
        this.save();
    }

    addProcess = (e) => {
        console.log("Adding new process.");
        this.setState((prevState) => ({
            processes: [...prevState.processes, { index: Math.random(), name: "", default_state: false, desired_state: false, positive_points: 0, negative_points: 0, create_dummy: false, positive_message: "", negative_message: ""}]
        }));
    }

    removeProcess = (e) => {
        console.log("Removing service with index: " + e.index);
        this.setState({
            processes: this.state.processes.filter(s => s.index !== e.index)
        })
    }

    handleChange = (e) => {

        let idx = e.target.id.split('-')[1];

        if (e.target.name === "name") {
            let services = [...this.state.processes];
            services[idx][e.target.name] = e.target.value;
        }

        if (["positive_points", "negative_points"].includes(e.target.name)) {
            let services = [...this.state.processes];
            services[idx][e.target.name] = parseInt(e.target.value, 10);
        }

        if (["default_state", "desired_state", "create_dummy"].includes(e.target.name)) {
            let processes = [...this.state.processes];
            processes[idx][e.target.name] = !processes[idx][e.target.name];
        }
    }

    save = () => {
        console.log("Printing process values.");
        console.log(this.state.processes);
        setJSONAttribute("processes", this.state.processes);
    }

    load = () => {
        console.log("Attempting to load processes from JSON.");
        var isEmpty = false;
        var isNull = false;
        var data = getJSONAttribute('processes');

        if (data === undefined)
            isNull = true;

        if (!isNull && Object.keys(data).length === 0)
            isEmpty = true;

        if (!isEmpty && !isNull) {
            this.setState({ processes: data }, () => {
                //console.log("Services in assignment during load: " + this.state.services);
            });
        }
        else if (isEmpty || isNull) {
            this.setState({ processes: [{ index: Math.random(), name: "", default_state: false, desired_state: false, positive_points: 0, negative_points: 0, create_dummy: false, positive_message: "", negative_message: ""}] })
        }
        return;
    }

    render() {
        return (
            <div className="page-div">
                <div className="page-header" >
                    <h1>Processes</h1>
                </div>
                <div className="page-info">
                    <p>
                        Process name: Name of the process that will be matched. Must match as the name appears in ps -ef.
                        <br></br>
                        Default state: State the process is in when the scoring engine starts.
                        <br></br>
                        Desired state: If the process is supposed to be running.
                        <br></br>
                        Create dummy: Generator will create a dummy process that will appear in process list. Will use the exact process name.
                    </p>
                </div>
                <div className="page-body" >
                    <table style={{ width: '100%' }}>
                        <tbody>
                            <tr>
                                <th>Process name</th>
                                <th>Default state</th>
                                <th>Desired state</th>
                                <th>Create dummy</th>
                                <th>Positive Points</th>
                                <th>Negative Points</th>
                            </tr>
                            <ProcessFields delete={this.removeProcess} processes={this.state.processes} onChange={this.handleChange}></ProcessFields>
                        </tbody>
                    </table>
                    <Button variant="contained" onClick={this.addProcess} > Add Process </Button>
                    <Button variant="contained" onClick={this.save} style={{ marginLeft: '200px' }}> Save </Button>
                </div>
            </div >);
    }

}