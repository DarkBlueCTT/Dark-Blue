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

import { filepath } from '../pages/Home.jsx';

const fs = window.require('fs');

export function setJSONAttribute(attribute, data) {
    console.log("Attempting to modify attribute: " + attribute);
    var rawFile = fs.readFileSync(filepath);
    var parsedExistingJSON = JSON.parse(rawFile);
    parsedExistingJSON[attribute] = data;
    var dataNew = JSON.stringify(parsedExistingJSON);
    fs.writeFileSync(filepath, dataNew, (err) => {
        if (err)
            console.log(err);
    });
}

export function getJSONAttribute(attribute) {
    console.log("Attempting to retrieve attribute: " + attribute);

    var rawFile = fs.readFileSync(filepath);
    var parsedExistingJSON = JSON.parse(rawFile);
    return parsedExistingJSON[attribute];
}