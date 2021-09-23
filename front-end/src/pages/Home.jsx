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
import './css/Style.css'
import Button from '@material-ui/core/Button';
import TextFieldControlled from '../components/TextFieldControlled';
import { setOS } from "../components/Sidebar.jsx";
import { setJSONAttribute, getJSONAttribute } from '../components/jsonFileEditor.jsx';
import TextAreaControlled from '../components/TextAreaControlled.jsx';

var os = -1;
var osName = "None";

const { dialog } = window.require('electron').remote;

export var filepath = "";
export const fs = window.require('fs');

export default class Home extends Component {

    constructor(props) {
        super(props);

        this.state = {
            filepath: "None",
            osName: "None",
            score: 0,
            readme: ""
        }
    }

    UNSAFE_componentWillMount() {
        if (filepath !== "None") {
            console.log("Attempting to load file: " + filepath);
            this.load();
            this.setState({ filepath: filepath })
            this.setState({ osName: osName })
        }
        else if (filepath === "None")
            this.selectFile();
    }

    componentWillUnmount() {
        this.save();
    }

    selectFile = () => {
        var test = undefined;

        test = dialog.showSaveDialogSync({ title: "Create a new JSON file", filters: [{ name: "json", extensions: ['json'] }] });

        if (test !== undefined) {
            filepath = test;
            this.setState({ filepath: filepath })
            this.prepareFile();
        }
    }

    save = () => {
        console.log(this.state);
        setJSONAttribute("score", this.state.score);
        setJSONAttribute("readme", this.state.readme);
    }

    load = () => {
        var fileType = getJSONAttribute("format");
        console.log(`format: ${fileType}`);

        if (fileType !== "DarkBlue") {
            console.warn(`Selected file ${filepath} is not a supported JSON format file.`);
            alert(`Selected file ${filepath} is not a supported Dark Blue JSON file.`);
            return;
        }

        var OS = getJSONAttribute("OS");
        console.log(`OS: ${OS}`);

        if (OS !== "Linux" && OS !== "Windows") {
            console.warn("OS Name does not match supported value.");
            return;
        }
        if (OS === "Linux") {
            setOS(1);
        }
        else if (OS === "Windows") {
            setOS(2);
        }
        osName = OS;
        this.setState({ osName: OS });

        var score = getJSONAttribute("score");
        this.setState({ score: score });
        console.log(`points: ${score}`);

        var readme = getJSONAttribute("readme");
        this.setState({ readme: readme });
        console.log(`Readme: ${readme}`);

    }

    prepareFile = () => {
        console.log(`Preparing file ${filepath}.`);
        //var data = "{ \"users\": {}, \n \"services\": {}}";
        var data = "{}";
        fs.writeFileSync(filepath, data, (err) => {
            if (err)
                console.log(err);
        });
        setJSONAttribute("format", "DarkBlue");
        setJSONAttribute("OS", osName);
    }

    generateReadme = () => {
        console.log("Attempting to generate readme information.");

        var os = getJSONAttribute("OS");

        var currentReadmeContent = this.state.readme;
        var allowedUsers = "\nAllowed users:\n\n";
        var administrators = "\nAllowed administrators/sudoers:\n";

        var newContent = "";

        //Users, basically copied from the answer key generator.
        var user_data = getJSONAttribute('users');

        if (os === "Windows"){
            if (user_data.length > 0) {
                for (var user of user_data) {
                    var allowed = user['allowed'];
                    var admin = user['is_admin'];
                    var name = user['name'];
    
                    if (allowed)
                        allowedUsers += name + "\n";
    
                    if (admin && allowed)
                        administrators += name + "\n";
                }
            }

        } else if (os === "Linux"){
            if (user_data.length > 0) {
                for (user of user_data) {
                    allowed = user['allowed'];
                    admin = user['is_sudo'];
                    name = user['name'];
    
                    if (allowed)
                        allowedUsers += name + "\n";
    
                    if (admin && allowed)
                        administrators += name + "\n";
                }
            }
        }

        newContent += currentReadmeContent + "\n" + allowedUsers + "\n" + administrators + "\n";

        if (os === "Windows") {
            newContent += "\nCritical services:\n"
            //Services
            var service_data = getJSONAttribute("services");

            if (service_data.length > 0) {
                for (var service of service_data) {
                    name = service['common_name'];
                    var desiredState = service['desired_state'];

                    if (desiredState === "running")
                        newContent += name + "\n";
                }
            } else {
                newContent += "None\n";
            }

        } else if (os === "Linux") {
            newContent += "\nCritical processes:\n"
            //Processes
            var process_data = getJSONAttribute("processes");

            if (process_data.length > 0) {
                for (var process of process_data) {
                    name = process['name'];
                    desiredState = process['desired_state'];

                    if (desiredState)
                        newContent += name + "\n";
                }
            } else {
                newContent += "None\n";
            }
        }
        console.log(newContent);
        this.setState({ readme: newContent });
    }

    handleChange = (e) => {
        if (e.target.name === "score") {
            this.setState({ score: parseInt(e.target.value, 10) });
        } else if (e.target.name === "readme") {
            this.setState({ readme: e.target.value });
        }
    }

    render() {
        return (
            <div className="page-div" >
                <div className="page-header">
                    <h1>Home</h1>
                </div>
                <div className="page-info">
                    <p>
                        Points: Sets the number of points for the image. Can be determined by setting reasonable sounding point values for everything, then generating an answer key and checking what it thinks the maximum number of points scored will be.
                        <br></br>
                        Readme: The readme file will provide necessary information about the images and what to do to score points.
                        <br></br>
                        Generate readme will attempt to automatically populate the readme file with useful information that is recommended. Will append to whatever is currently in the readme field.
                        Note: Generating the readme currently does not display a change until navigating away from the page and back.
                    </p>
                </div>
                <div className="page-body">
                    <h2>Operating System: {this.state.osName}</h2>
                    <h2>Filepath: {this.state.filepath}</h2>
                    <br>
                    </br>
                    <h2>Points:</h2>
                    <TextFieldControlled name="score" id="score" value={this.state.score} onChange={this.handleChange} integer={true}></TextFieldControlled>
                    <br>
                    </br>
                    <br>
                    </br>
                    <h2>Readme:</h2>
                    {/* <textarea rows="4" cols="50"></textarea> */}
                    <TextAreaControlled value={this.state.readme} onChange={this.handleChange}></TextAreaControlled>
                    <br>
                    </br>
                    <Button variant="contained" onClick={this.generateReadme}>Generate Readme</Button>
                    <br>
                    </br>
                    <br>
                    </br>
                    {/* <Button variant="contained" onClick={this.selectFile}> Choose file path </Button> */}
                    {/* <Button variant="contained" onClick={this.prepareFile}> Reset JSON file </Button> */}
                    <Button variant="contained" onClick={this.save}> Save </Button>
                </div>
            </div >
        );
    }
}

export function setOperatingSystem(value) {
    if (value === 1) {
        os = 1;
        osName = "Linux";
        setOS(1);
    }
    else if (value === 2) {
        os = 2;
        osName = "Windows";
        setOS(2);
    }

    console.log(`OS: ${os}`);
}

export function getOS() {
    console.log("Home.jsx is receiving a request for OS value.");

    var os = getJSONAttribute("OS");

    if (os === "Linux")
        return 1;
    else if (os === "Windows")
        return 0


    return os;
}

export function setFilepath(path) {
    console.log(`Filepath: ${path}`);
    if (path !== undefined)
        filepath = path;
}