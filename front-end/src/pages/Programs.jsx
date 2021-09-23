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
import ProgramField from '../components/ProgramFields.jsx';
import { setJSONAttribute, getJSONAttribute } from '../components/jsonFileEditor.jsx';


export default class Program extends Component {

    constructor(props) {
        super(props);

        this.state = {
            programs: []
        }
    }

    componentDidMount() {
        this.load();
    }

    componentWillUnmount() {
        this.save();
    }

    addProgram = (e) => {
        console.log("Adding a new program.");
        this.setState((prevState) => ({
            programs: [...prevState.programs, { index: Math.random(), name: "", installed: false, desired: false, positive_points: 0, negative_points: 0 }],
        }));
    }

    removeProgram = (e) => {
        console.log("Removing program with index: " + e.index);
        this.setState({
            programs: this.state.programs.filter(p => p.index !== e.index)
        })
    }

    handleChange = (e) => {
        let idx = e.target.id.split('-')[1];
        if (e.target.name === "name") {
            let programs = [...this.state.programs]
            programs[idx][e.target.name] = e.target.value;
        }

        if (["positive_points", "negative_points"].includes(e.target.name)) {
            let programs = [...this.state.programs]
            programs[idx][e.target.name] = parseInt(e.target.value, 10);
        }

        if (e.target.name === "installed" || e.target.name === "desired") {
            let programs = [...this.state.programs]
            programs[idx][e.target.name] = !programs[idx][e.target.name];
        }
    }


    save = () => {
        console.log("Printing program values.");
        console.log(this.state.programs);
        setJSONAttribute("programs", this.state.programs);
    }

    load = () => {
        console.log("Attempting to load programs from JSON.");
        var isEmpty = false;
        var isNull = false;
        var data = getJSONAttribute('programs');

        if (data === undefined)
            isNull = true;

        if (!isNull && Object.keys(data).length === 0)
            isEmpty = true;

        if (!isEmpty && !isNull) {
            this.setState({ programs: data }, () => {
            });
        }
        else if (isEmpty || isNull) {
            this.setState({ programs: [{ index: Math.random(), name: "", installed: false, desired: false, positive_points: 0, negative_points: 0 }] })
        }
        return;
    }

    render() {
        return (
            <div className="page-div">
                <div className="page-header" >
                    <h1>Installed Programs</h1>
                </div>
                <div className="page-info">
                    <p>
                        Program name: Matches the exact name that appears in the uninstall list.
                        <br></br>
                        Installed: If the program is installed when scoring engine starts.
                        <br></br>
                        Desired: If the program is supposed to be installed.
                        <br></br>
                        Note:  In order for a program to be scored, it <b>MUST</b> have an entry in HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall
                    </p>
                </div>
                <div className="page-body" >
                    <table style={{ width: '100%' }}>
                        <tbody>
                            <tr>
                                <th>Program Name</th>
                                <th>Installed</th>
                                <th>Desired</th>
                                <th>Positive Points</th>
                                <th>Negative Points</th>
                            </tr>
                            <ProgramField delete={this.removeProgram} programs={this.state.programs} onChange={this.handleChange}></ProgramField>
                        </tbody>
                    </table>
                    <Button variant="contained" onClick={this.addProgram} onChange={this.handleChange} > Add Program </Button>
                    <Button variant="contained" onClick={this.save} style={{ marginLeft: '200px' }}> Save </Button>
                </div>
            </div >);
    }
}
