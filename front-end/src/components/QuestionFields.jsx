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

const QuestionField = (props) => {
    return (
        props.questions.map((val, idx) => {
            let name = `name-${idx}`, points = `points-${idx}`, answer = `answer-${idx}`, question_content = `question_content-${idx}`
            return (
                <tr key={val.index} className="user-field">
                    <td>
                        <TextFieldControlled name="name" id={name} value={val.name} onChange={props.onChange}></TextFieldControlled>
                    </td>
                    <td>
                        <TextFieldControlled name="question_content" id={question_content} value={val.question_content} onChange={props.onChange}></TextFieldControlled>
                    </td>
                    <td>
                        <TextFieldControlled name="answer" id={answer} value={val.answer} onChange={props.onChange}></TextFieldControlled>
                    </td>
                    <td>
                        <TextFieldControlled name="points" id={points} value={val.points} onChange={props.onChange} integer={true}></TextFieldControlled>
                    </td>
                    <td>
                        <Button variant="contained" onClick={(() => props.delete(val))}>Delete</Button>
                    </td>
                </tr>);
        })
    );
}

export default QuestionField