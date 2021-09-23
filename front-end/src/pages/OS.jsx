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

import React from 'react';
import './css/App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Button from 'react-bootstrap/Button';
import { Link } from 'react-router-dom';
import { setOperatingSystem } from "./Home.jsx";

export default function OS() {
    return (
        <div className="App">
            <header className="App-header">
                <h1 style={{ color: "#01003d" }}>
                    Dark Blue
        </h1>
                <h3>CyberPatriot Training Tool</h3>
                <Button as={Link} to="/home" variant="dark" size="lg" block onClick={() => test(1)}>Linux</Button>
                <Button as={Link} to="/home" variant="dark" size="lg" block onClick={() => test(2)}>Windows</Button>
            </header >
        </div >
    );
}


function test(value) {
    if (value === 1)
        console.log("Selected operating system is Linux.")
    else
        console.log("Selected operating system is Windows.")
    setOperatingSystem(value)
}
