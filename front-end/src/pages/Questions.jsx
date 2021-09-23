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
import './css/Style.css';
import Button from '@material-ui/core/Button';
import QuestionField from '../components/QuestionFields.jsx';
import { setJSONAttribute, getJSONAttribute } from '../components/jsonFileEditor.jsx';

export default class Questions extends Component {

    constructor(props) {
        super(props);

        this.state = {
            questions: []
        }
    }

    componentDidMount() {
        this.load();
    }

    componentWillUnmount() {
        this.save();
    }

    addQuestion = (e) => {
        console.log("Adding a new question.");
        this.setState((prevState) => ({
            questions: [...prevState.questions, { index: Math.random(), name: "", question_content: "", answer: "", points: 0}],
        }));
    }

    removeQuestion = (e) => {
        console.log("Removing question with index: " + e.index);
        this.setState({
            questions: this.state.questions.filter(q => q.index !== e.index)
        })
    }

    handleChange = (e) => {
        let idx = e.target.id.split('-')[1];
        if (["name", "answer", "question_content"].includes(e.target.name)) {
            let questions = [...this.state.questions]
            questions[idx][e.target.name] = e.target.value;
        }
            if (e.target.name === "points") {
            let questions = [...this.state.questions]
            questions[idx][e.target.name] = parseInt(e.target.value, 10);
        }
    }


    save = () => {
        console.log("Printing user values.");
        console.log(this.state.questions);
        setJSONAttribute("challenge_questions", this.state.questions);
    }

    load = () => {
        console.log("Attempting to load questions from JSON.");
        var isEmpty = false;
        var isNull = false;
        var data = getJSONAttribute('challenge_questions');

        if (data === undefined)
            isNull = true;

        if (!isNull && Object.keys(data).length === 0)
            isEmpty = true;

        if (!isEmpty && !isNull) {
            this.setState({ questions: data }, () => {
            });
        }
        else if (isEmpty || isNull) {
            this.setState({ questions: [{ index: Math.random(), name: "", question_content: "", answer: "", points: 0}] })
        }
        return;
    }

    render() {
        return (
            <div className="page-div">
                <div className="page-header" >
                    <h1>Challenge Questions</h1>
                </div>
                <div className="page-info">
                    <p>
                        Question name: Name that is displayed in the scoring report.
                        <br></br>
                        Question text: Text that will be put in the question file.
                        <br></br>
                        Answer: Answer to the question. Matched exactly, case insensitive.
                        <br></br>
                        Value: Points awarded for a correct answer.
                    </p>
                </div>
                <div className="page-body" >
                    <table style={{ width: '100%' }}>
                        <tbody>
                            <tr>
                                <th>Question Name</th>
                                <th>Question text</th>
                                <th>Answer</th>
                                <th>Value</th>
                            </tr>
                            <QuestionField delete={this.removeQuestion} questions={this.state.questions} onChange={this.handleChange}></QuestionField>
                        </tbody>
                    </table>
                    <Button variant="contained" onClick={this.addQuestion} onChange={this.handleChange} > Add Question </Button>
                    <Button variant="contained" onClick={this.save} style={{ marginLeft: '200px' }}> Save </Button>
                </div>
            </div >);
    }
}
