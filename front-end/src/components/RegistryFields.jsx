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

import React from 'react';
import Button from '@material-ui/core/Button';
import TextFieldControlled from './TextFieldControlled';
import SelectControlled from './SelectControlled';
import CheckboxControlled from './CheckboxControlled';


const RegistryField = (props) => {
    return (
        props.registry.map((val, idx) => {
            let key = `key-${idx}`, key_path = `key_path-${idx}`, entry_name = `entry_name-${idx}`, default_value = `default_value-${idx}`, positive_value = `positive_value-${idx}`, negative_value = `negative_value-${idx}`, positive_points = `positive_points-${idx}`, negative_points = `negative_points-${idx}`, positive_message = `positive_message-${idx}`, negative_message = `negative_message-${idx}`, create = `create-${idx}`
            return (
                <tr key={val.index}>
                    <td>
                        <SelectControlled name={key} labels={['', 'HKEY_LOCAL_MACHINE', 'HKEY_CURRENT_USER']} id={key} value={val.key} onChange={props.onChange}>
                        </SelectControlled>
                    </td>
                    <td>
                        <TextFieldControlled name="key_path" id={key_path} value={val.key_path} onChange={props.onChange}></TextFieldControlled>
                    </td>
                    <td>
                        <TextFieldControlled name="entry_name" id={entry_name} value={val.entry_name} onChange={props.onChange}></TextFieldControlled>
                    </td>
                    <td>
                        <TextFieldControlled name="default_value" id={default_value} value={val.default_value} onChange={props.onChange}></TextFieldControlled>
                    </td>
                    <td>
                        <TextFieldControlled name="positive_value" id={positive_value} value={val.positive_value} onChange={props.onChange}></TextFieldControlled>
                    </td>
                    <td>
                        <TextFieldControlled name="negative_value" id={negative_value} value={val.negative_value} onChange={props.onChange}></TextFieldControlled>
                    </td>
                    <td>
                        <TextFieldControlled name="positive_points" id={positive_points} value={val.positive_points} onChange={props.onChange} integer={true}></TextFieldControlled>
                    </td>
                    <td>
                        <TextFieldControlled name="negative_points" id={negative_points} value={val.negative_points} onChange={props.onChange} integer={true}></TextFieldControlled>
                    </td>
                    <td>
                        <CheckboxControlled name="create" id={create} checked={val.create} onChange={props.onChange}></CheckboxControlled>
                    </td>
                    <td>
                        <TextFieldControlled name="positive_message" id={positive_message} value={val.positive_message} onChange={props.onChange}></TextFieldControlled>
                    </td>
                    <td>
                        <TextFieldControlled name="negative_message" id={negative_message} value={val.negative_message} onChange={props.onChange}></TextFieldControlled>
                    </td>
                    <td>
                        <Button variant="contained" onClick={(() => props.delete(val))}>Delete</Button>
                    </td>
                </tr >
            );
        })
    )
}

export default RegistryField;