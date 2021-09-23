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
import Button from '@material-ui/core/Button';
import TextFieldControlled from './TextFieldControlled';
import CheckboxControlled from './CheckboxControlled';

const ProcessFields = (props) => {
    return (
        props.processes.map((val, idx) => {
            let name = `name-${idx}`, default_state = `default_state-${idx}`, desired_state = `desired_state-${idx}`, create_dummy = `create_dummy-${idx}`, positive_points = `positive_points-${idx}`, negative_points = `negative_points-${idx}`
            return (
                <tr key={val.index}>
                    <td>
                        <TextFieldControlled name="name" id={name} value={val.name} onChange={props.onChange}></TextFieldControlled>
                    </td>
                    <td>
                        <CheckboxControlled name="default_state" id={default_state} checked={val.default_state} onChange={props.onChange}></CheckboxControlled>
                    </td>
                    <td>
                        <CheckboxControlled name="desired_state" id={desired_state} checked={val.desired_state} onChange={props.onChange}></CheckboxControlled>
                    </td>
                    <td>
                        <CheckboxControlled name="create_dummy" id={create_dummy} checked={val.create_dummy} onChange={props.onChange}></CheckboxControlled>
                    </td>
                    <td>
                        <TextFieldControlled name="positive_points" id={positive_points} value={val.positive_points} onChange={props.onChange} integer={true}></TextFieldControlled>
                    </td>
                    <td>
                        <TextFieldControlled name="negative_points" id={negative_points} value={val.negative_points} onChange={props.onChange} integer={true}></TextFieldControlled>
                    </td>
                    <td>
                        <Button variant="contained" onClick={(() => props.delete(val))}>Delete</Button>
                    </td>
                </tr >
            );
        })
    );
}

export default ProcessFields