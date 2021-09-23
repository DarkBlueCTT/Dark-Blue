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
import FilepathFields from '../components/FilepathFields.jsx';
import { setJSONAttribute, getJSONAttribute } from '../components/jsonFileEditor.jsx';


export default class Filepath extends Component {

    constructor(props) {
        super(props);

        this.state = {
            files: []
        }
    }

    componentDidMount() {
        this.load();
    }

    componentWillUnmount() {
        this.save();
    }


    addFile = (e) => {
        console.log("Adding a new file.");
        this.setState((prevState) => ({
            files: [...prevState.files, { index: Math.random(), filepath: "", exist: false, create: false, positive_points: 0, negative_points: 0 }],
        }));
    }

    removeFile = (e) => {
        console.log("Removing row with index: " + e.index);
        this.setState({
            files: this.state.files.filter(s => s.index !== e.index)
        })
    }

    handleChange = (e) => {
        let idx = e.target.id.split('-')[1];
        if (e.target.name === "filepath") {
            let files = [...this.state.files]
            files[idx][e.target.name] = e.target.value;
        }

        if (["positive_points", "negative_points"].includes(e.target.name)) {
            let files = [...this.state.files]
            files[idx][e.target.name] = parseInt(e.target.value, 10);
        }

        if (e.target.name === "exist" || e.target.name === "create") {
            let files = [...this.state.files]
            files[idx][e.target.name] = !files[idx][e.target.name];
        }
    }


    save = () => {
        console.log("Printing file values.");
        console.log(this.state.files);
        setJSONAttribute("files", this.state.files);
    }

    load = () => {
        console.log("Attempting to load files from JSON.");
        var isEmpty = false;
        var isNull = false;
        var data = getJSONAttribute('files');

        if (data === undefined)
            isNull = true;

        if (!isNull && Object.keys(data).length === 0)
            isEmpty = true;


        if (!isEmpty && !isNull) {
            this.setState({ files: data }, () => {
            });
        }
        else if (isEmpty || isNull) {
            this.setState({ files: [{ index: Math.random(), filepath: "", exist: false, create: false, positive_points: 0, negative_points: 0 }] })
        }
        return;
    }

    render() {
        return (
            <div className="page-div">
                <div className="page-header" >
                    <h1>Filepaths</h1>
                </div>
                <div className="page-info">
                    <p>
                        Filepath: Path to the file or directory that will be scored. $DESKTOP is available as a shortcut to the current user's desktop.
                        ex: $DESKTOP/file.txt will place the file on the desktop of the user that is logged in when the image is created.
                        <br></br>
                        Exist: If the filepath is supposed to exist.
                        <br></br>
                        Create: If the filepath is supposed to be automatically created.
                        <br></br>
                    </p>
                </div>
                <div className="page-body" >
                    <table style={{ width: '70%' }}>
                        <tbody>
                            <tr>
                                <th>Filepath</th>
                                <th>Exist</th>
                                <th>Create</th>
                                <th>Positive points</th>
                                <th>Negative points</th>
                            </tr>
                            <FilepathFields files={this.state.files} delete={this.removeFile.bind(this)} onChange={this.handleChange}></FilepathFields>
                        </tbody>
                    </table>
                    <Button variant="contained" onClick={this.addFile} > Add Filepath </Button>
                    <Button variant="contained" onClick={this.save} style={{ marginLeft: '200px' }}> Save </Button>
                </div>
            </div >);
    }
}
