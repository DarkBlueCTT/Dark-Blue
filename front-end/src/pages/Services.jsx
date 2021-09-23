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
import ServiceFields from '../components/ServiceFields.jsx'
import { setJSONAttribute, getJSONAttribute } from '../components/jsonFileEditor.jsx';

export default class Services extends Component {

    constructor(props) {
        console.log("Constructing services...");
        super(props);
        this.state = {
            services: []
        }
    }

    componentDidMount() {
        this.load();
        console.log("State after load: " + this.state.services);
    }

    componentWillUnmount() {
        this.save();
    }

    addService = (e) => {
        console.log("Adding new service.");
        this.setState((prevState) => ({
            services: [...prevState.services, { index: Math.random(), name: "", common_name: "", default_state: '', desired_state: '', positive_points: 0, negative_points: 0, startup_state: '', desired_startup_state: '', positive_message: "", negative_message: ""}]
        }));
    }
    removeService = (e) => {
        console.log("Removing service with index: " + e.index);
        this.setState({
            services: this.state.services.filter(s => s.index !== e.index)
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

        if (e.target.name === "name" || e.target.name === "common_name") {
            let services = [...this.state.services];
            services[idx][e.target.name] = e.target.value;
        }

        if (["positive_points", "negative_points"].includes(e.target.name)) {
            let services = [...this.state.services];
            services[idx][e.target.name] = parseInt(e.target.value, 10);
        }

        if (["default_state", "desired_state",  "startup_state", "desired_startup_state"].includes(name) && idx !== -1 && name !== '') {
            let services = [...this.state.services];

            // if (e.target.value === 1)
            //     services[idx][name] = 'Running';
            // else if (e.target.value === 2)
            //     services[idx][name] = 'Stopped';

            services[idx][name] = e.target.value;
        }
    }

    save = () => {
        console.log("Printing service values.");
        console.log(this.state.services);
        setJSONAttribute("services", this.state.services);
    }

    load = () => {
        console.log("Attempting to load services from JSON.");
        var isEmpty = false;
        var isNull = false;
        var data = getJSONAttribute('services');

        if (data === undefined)
            isNull = true;

        if (!isNull && Object.keys(data).length === 0)
            isEmpty = true;

        if (!isEmpty && !isNull) {
            this.setState({ services: data }, () => {
                console.log(this.state.services);
            });
        }
        else if (isEmpty || isNull) {
            this.setState({ services: [{ index: Math.random(), name: "", common_name: "", default_state: '', desired_state: '', positive_points: 0, negative_points: 0, startup_state: '', desired_startup_state: '', positive_message: "", negative_message: "" }] })
        }

        return;
    }

    render() {
        return (
            <div className="page-div">
                <div className="page-header" >
                    <h1>Services</h1>
                </div>
                <div className="page-info">
                    <p>
                        Service name: Name of the service to be matched. Uses the service name, not common name. ex: Remote Desktop Services is TermService.
                        <br></br>
                        Common name: Common name of the service to display for scoring.
                        <br></br>
                        Default state: Starting state of the service.
                        <br></br>
                        Desired state: State that is supposed to be set.
                        <br></br>
                        Startup state: Startup state that is set by default.
                        <br></br>
                        Desired startup state: Startup state that is supposed to be set.
                        <br></br>
                        Note: Startup states are not currently scored.
                    </p>
                </div>
                <div className="page-body" >
                    <table style={{ width: '100%' }}>
                        <tbody>
                            <tr>
                                <th>Service name</th>
                                <th>Common name</th>
                                <th>Default state</th>
                                <th>Desired state</th>
                                <th>Positive Points</th>
                                <th>Negative Points</th>
                                <th>Startup State</th>
                                <th>Desired Startup State</th>
                            </tr>
                            <ServiceFields delete={this.removeService} services={this.state.services} onChange={this.handleChange}></ServiceFields>
                        </tbody>
                    </table>
                    <Button variant="contained" onClick={this.addService} > Add Service </Button>
                    <Button variant="contained" onClick={this.save} style={{ marginLeft: '200px' }}> Save </Button>
                </div>
            </div >);
    }

}