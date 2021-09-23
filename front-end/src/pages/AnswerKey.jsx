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

import React, { Component } from "react";
import './css/Style.css'
import Button from '@material-ui/core/Button';
import { getJSONAttribute } from '../components/jsonFileEditor.jsx';

const fs = window.require('fs');
const { dialog } = window.require('electron').remote;

export default class AnswerKey extends Component {

    constructor(props) {
        super(props);

        this.state = {
            filepath: null,
            score: 0,
            messages: []
        }
    }

    selectFile = () => {
        var test = null;

        test = dialog.showSaveDialogSync({ title: "Save answer key", defaultPath: "answerkey.txt", filters: [{ name: "txt", extensions: ['txt'] }] });

        console.log(test);

        if (test !== null) {
            this.setState({ filepath: test }, () => {
                console.log(this.state.filepath);
                this.generateKey();
            });
        }

    }

    generateKey = () => {
        console.log("Attempting to generate answer key to path: " + this.state.filepath);

        if (this.state.filepath === null) {
            console.error("No filepath was given to generate answer key.");
            dialog.showMessageBoxSync({ type: "error", title: "Dark Blue Answer Key Generator", message: "Could not generate answer key to the given filepath. Please try again." });
            return;
        }

        let messages = [];
        let score = 0;

        //Question files
        var question_data = getJSONAttribute('questions');
        var lengthQuestions = question_data.length;

        if (lengthQuestions <= 0) {
            console.error("No questions were loaded from configuration file.");
        } else {
            var question;

            for (question of question_data) {
                var answer = question['answer'];
                var points = question['points'];
                var name = question['name'];

                if (answer !== null && points !== null) {
                    messages.push(`[+${points}] Question ${name} was answered correctly. Answer: ${answer}`);
                    score += points;
                }
            }
        }

        //File paths
        var filepath_data = getJSONAttribute('files');
        var lengthFiles = filepath_data.length;

        if (lengthFiles <= 0) {
            console.error("No filepaths were loaded from configuration file.");
        } else {
            var file;

            for (file of filepath_data) {
                var exist = file['exist'];
                var path = file['filepath'];
                points = file['positive_points'];


                if (!exist) {
                    messages.push(`[+${points}] File ${path} was deleted.`);
                    score += points;
                }
            }
        }

        var os = getJSONAttribute('OS');

        if (os === "Linux") {

            //Users
            var user_data = getJSONAttribute('users');

            var lengthUsers = user_data.length;

            if (lengthUsers <= 0) {
                console.error("No users were loaded from configuration files.")
            } else {
                var user;
                for (user of user_data) {

                    var allowed = user['allowed'];
                    var admin = user['is_sudo'];
                    var startAdmin = user['sudo_initial_state'];
                    points = user['positive_points'];

                    //Disallowed users.
                    if (!allowed) {
                        messages.push(`[+${points}] User ${user['name']} has been removed.`);
                        score += points;
                    }

                    //User needs to become admin.
                    if (allowed && admin && !startAdmin) {
                        messages.push(`[+${points}] User ${user['name']} is now in the sudo group.`);
                        score += points ;
                    }

                    //User needs admin removed.
                    if (allowed && !admin && startAdmin) {
                        messages.push(`[+${points}] User ${user['name']} is not in the sudo group.`);
                        score += points;
                    }
                }
            }

            //Config files
            var configfile_data = getJSONAttribute('configfiles');
            var lengthConfigFiles = configfile_data.length;

            if (lengthConfigFiles <= 0) {
                console.error("No configuration files were loaded from file.");
            } else {
                for (var configFile of configfile_data) {
                    var defaultValue = configFile['default_value'];
                    var positiveValue = configFile['positive_value']
                    var positiveMessage = configFile['positive_message'];
                    var filepath = configFile['filepath'];
                    points = configFile['positive_points'];

                    if (defaultValue !== positiveValue) {

                        if (positiveMessage !== "") {
                            messages.push(`[+${points}] ${positiveMessage}`);
                            score += points;
                        } else {
                            messages.push(`[+${points}] Config File ${filepath} was set to positive value ${positiveValue}.`);
                            score += points;
                        }
                    }
                }
            }

            //Packages
            var package_data = getJSONAttribute('packages');
            var lengthPackage = package_data.length;

            if (lengthPackage <= 0) {
                console.error("No packages were loaded from configuration file");
            } else {
                //Apparently package is a reserved word, so it's called pack now.
                for (var pack of package_data) {
                    var installed = pack['installed'];
                    var desired = pack['desired'];
                    name = pack['name'];
                    points = pack['positive_points'];

                    if (!installed && desired) {
                        messages.push(`[+${points}] Package ${name} was installed.`);
                        score += points;
                    }
                    if (!desired) {
                        messages.push(`[+${points}] Package ${name} was uninstalled.`);
                        score += points;
                    }
                }
            }
            //Processes
            var process_data = getJSONAttribute("processes");
            var lengthProcess = process_data.length;

            if (lengthProcess <= 0) {
                console.error("No processes were loaded from configuration file.");
            } else {
                for (var process of process_data) {
                    var defaultState = process['default_state'];
                    var desiredState = process['desired_state'];
                    name = process['name'];
                    points = process['positive_points'];

                    if (defaultState && !desiredState) {
                        messages.push(`[+${points}] Process ${name} was stopped.`);
                        score += points;
                    }
                    if (!defaultState && desiredState) {
                        messages.push(`[+${points}] Process ${name} was started.`);
                        score += points;
                    }
                }
            }
        } else if (os === "Windows") {

             //Users
            user_data = getJSONAttribute('users');

            lengthUsers = user_data.length;

            if (lengthUsers <= 0) {
                console.error("No users were loaded from configuration files.")
            } else {
                for (user of user_data) {

                    name = user['name']
                    allowed = user['allowed'];
                    admin = user['is_admin'];
                    startAdmin = user['admin_initial_state'];
                    var positivePoints = user['positive_points'];

                    //Disallowed users.
                    if (!allowed) {
                        messages.push(`[+${positivePoints}] User ${user['name']} has been removed.`);
                        score += positivePoints;
                    }

                    //User needs to become admin.
                    if (allowed && admin && !startAdmin) {
                        messages.push(`[+${positivePoints}] User ${user['name']} is now an administrator.`);
                        score += positivePoints;
                    }

                    //User needs admin removed.
                    if (allowed && !admin && startAdmin) {
                        messages.push(`[+${positivePoints}] User ${user['name']} is not an administrator.`);
                        score += positivePoints;
                    }
                }
            }
            //Services
            var service_data = getJSONAttribute('services');
            var lengthService = service_data.length;

            if (lengthService <= 0) {
                console.error("No users were loaded from configuration file.");
            } else {
                for (var service of service_data) {
                    name = service['common_name'];
                    defaultState = service['default_state'];
                    desiredState = service['desired_state'];
                    points = service['positive_points'];

                    if (defaultState === "Stopped" && desiredState === "Running") {
                        messages.push(`[+${points}] Service ${name} was started.`);
                        score += points;
                    }

                    if (defaultState === "Running" && desiredState === "Stopped") {
                        messages.push(`[+${points}] Service ${name} was stopped.`);
                        score += points;
                    }
                }
            }

            //Firewall
            var firewall_data = getJSONAttribute('firewall');
            var lengthFirewall = firewall_data.length;

            if (lengthFirewall <= 0){
                console.error("No firewall profiles were loaded from the configuration file.");
            } else {
                for (var firewall of firewall_data){
                    name = firewall['name']
                    var startingState = firewall['starting_state']
                    desiredState = firewall['desired_state']
                    points = firewall['positive_points']

                    if (!startingState && desiredState){
                        messages.push(`[+${points}] ${name} firewall profile enabled.`)
                        score += points;
                    }

                    if (startingState && !desiredState){
                        messages.push(`[+${points}] ${name} firewall profile disabled.`)
                        score += points;
                    }
                }
            }

            //Registry
            var registry_data = getJSONAttribute('registry');
            var lengthRegistry = registry_data.length;

            if (lengthRegistry <= 0) {
                console.error("No registry entries were loaded from configuration file.");
            } else {
                for (var registry of registry_data) {
                    defaultValue = registry['default_value'];
                    positiveValue = registry['positive_value']
                    positiveMessage = registry['positive_message'];
                    name = registry['entry_name'];
                    points = registry['positive_points'];

                    if (defaultValue !== positiveValue) {
                        if (positiveMessage !== "") {
                            messages.push(`[+${points}] ${positiveMessage}`);
                            score += points;
                        } else {
                            messages.push(`[+${points}] Registry Entry ${name} was set to positive value ${positiveValue}.`);
                            score += points;
                        }
                    }
                }
            }

            //Programs

            var program_data = getJSONAttribute("programs");
            var programLength = program_data.length;

            if (programLength <= 0) {
                console.error("No programs were loaded from configuration file.");
            } else {
                for (var program of program_data) {
                    name = program['name'];
                    installed = program['installed'];
                    desired = program['desired'];
                    points = program['positive_points'];

                    if (installed && !desired) {
                        messages.push(`[+${points}] Program ${name} was uninstalled.`);
                        score += points;
                    }
                    else if (!installed && desired) {
                        messages.push(`[+${points}] Program ${name} was installed.`);
                        score += points;
                    }
                }
            }
        } else {
            console.fatal("Invalid operating system value.");
        }

        this.setState({ messages: messages, score: score }, () => {
            console.log("State mutation complete, writing answer key to file.");
            this.writeAnswerKey();
        });

    }

    writeAnswerKey = () => {

        var output = "";
        var msg;

        var score = getJSONAttribute('score');

        output += `Score: ${this.state.score}/${score}\n`;

        for (msg of this.state.messages) {
            output += msg + "\n";
        }
        console.log(this.state.filepath);
        fs.writeFileSync(this.state.filepath, output, { flag: 'w' }, (err) => {
            if (err)
                console.log(err);
        });
        console.log("Done writing.");
    }

    render() {
        return (
            <div className="page-div">
                <div className="page-header">
                    <h1>Answer Key Generation</h1>
                </div>
                <div className="page-info">Attempts to automatically generate an answer key for the given configuration file. May not be perfectly accurate.</div>
                <div className="page-body">
                    <Button variant="contained" onClick={this.selectFile}>Generate Answer Key</Button>
                </div>
            </div>);
    }

}