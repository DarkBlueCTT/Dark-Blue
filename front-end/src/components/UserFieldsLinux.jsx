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

const UserField = (props) => {
    return (
        props.users.map((val, idx) => {
            let name = `name-${idx}`, allowed = `allowed-${idx}`, is_sudo = `is_sudo-${idx}`, sudo_initial_state = `sudo_initial_state-${idx}`, positive_points = `positive_points-${idx}`, negative_points = `negative_points-${idx}`
            return (
                <tr key={val.index} className="user-field">
                    <td>
                        <TextFieldControlled name="name" id={name} value={val.name} onChange={props.onChange}></TextFieldControlled>
                    </td>
                    <td>
                        <CheckboxControlled name="allowed" id={allowed} checked={val.allowed} onChange={props.onChange}></CheckboxControlled>
                    </td>
                    <td>
                        <CheckboxControlled name="is_sudo" id={is_sudo} checked={val.is_sudo} onChange={props.onChange}></CheckboxControlled>

                    </td>
                    <td>
                        <CheckboxControlled name="sudo_initial_state" id={sudo_initial_state} checked={val.sudo_initial_state} onChange={props.onChange}></CheckboxControlled>

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
                </tr>);
        })
    );
}

export default UserField