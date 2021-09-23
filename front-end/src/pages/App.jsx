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

import React, { Component } from 'react'
import './css/App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Button from 'react-bootstrap/Button';
import { Link } from 'react-router-dom';
import { setFilepath } from './Home';
import { setOS } from "../components/Sidebar.jsx";
import { getJSONAttribute } from '../components/jsonFileEditor.jsx';


class App extends Component {

  selectFile = () => {
    const { dialog } = window.require('electron').remote;
    var test = undefined;

    test = dialog.showOpenDialogSync({ title: "Load existing JSON file", filters: [{ name: "json", extensions: ['json'] }] });

    if (test !== undefined) {
      console.log(test[0]);
      setFilepath(test[0]);
      var os = getJSONAttribute("OS");

      console.log("App.jsx is attempting to set OS value in sidebar. OS: " + os)
      if (os === "Linux")
        setOS(1);
      else if (os === "Windows")
        setOS(2);
    }
  }

  newFile = () => {
    setFilepath("None");
  }

  // componentDidMount() {
  //   const { app, globalShortcut } = require('electron')
  //   app.whenReady().then(() => {
  //     globalShortcut.register('CommandOrControl+r', () => {
  //       console.log('Control+r pressed.');
  //     })
  //   })
  // }

  render() {
    // Doesn't allow window to be closed.
    // window.addEventListener('beforeunload', (ev) => {
    //   console.log("Attempting to block reload.")
    //   ev.returnValue = true;
    // })

    return (
      <div>
        <div className="App">
          <header className="App-header">
            <h1 style={{ color: "#01003d" }}>
              Dark Blue
        </h1>
            <h3>CyberPatriot Training Tool</h3>
            <Button as={Link} to="/OS" variant="dark" size="lg" block onClick={this.newFile}>New Configuration</Button>
            <Button as={Link} to="/Home" variant="dark" size="lg" block onClick={this.selectFile}>Load Configuration</Button>
          </header >
        </div >
      </div>
    )
  }
}

export default App
