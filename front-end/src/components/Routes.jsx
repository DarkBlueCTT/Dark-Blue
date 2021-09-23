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

import React, { Fragment } from 'react';
import { Route, Switch } from 'react-router-dom';
import App from '../pages/App.jsx';
import Home from '../pages/Home.jsx';
import Sidebar from './Sidebar.jsx';
import Users from '../pages/Users.jsx';
import Services from '../pages/Services.jsx';
import Registry from '../pages/Registry.jsx';
import Programs from '../pages/Programs.jsx';
import Questions from '../pages/Questions.jsx';
import Firewall from '../pages/Firewall.jsx';
import Filepaths from '../pages/Filepaths.jsx';
import OS from '../pages/OS.jsx';
import LinuxUsers from '../pages/LinuxUsers.jsx';
import Processes from '../pages/Processes.jsx';
import ConfigFile from '../pages/ConfigFiles.jsx'
import Packages from '../pages/Packages.jsx';
import AnswerKey from '../pages/AnswerKey.jsx';

const routes = (
    <Switch>
        <Route exact path="/" component={App} />
        <Route exact path="/OS" component={OS} />
        <Route exact path="/home" render={props =>
            <Fragment>
                <Home />
                < Sidebar />
            </Fragment>} />
        <Route exact path="/users" render={props =>
            <Fragment>
                <Users />
                < Sidebar />
            </Fragment>} />
        <Route exact path="/linuxusers" render={props =>
            <Fragment>
                <LinuxUsers />
                < Sidebar />
            </Fragment>} />
        <Route exact path="/services" render={props =>
            <Fragment>
                <Services />
                < Sidebar />
            </Fragment>} />
        <Route exact path="/processes" render={props =>
            <Fragment>
                <Processes />
                < Sidebar />
            </Fragment>} />
        <Route exact path="/registry" render={props =>
            <Fragment>
                <Registry />
                < Sidebar />
            </Fragment>} />
        <Route exact path="/configfile" render={props =>
            <Fragment>
                <ConfigFile />
                < Sidebar />
            </Fragment>} />
        <Route exact path="/programs" render={props =>
            <Fragment>
                <Programs />
                < Sidebar />
            </Fragment>} />
        <Route exact path="/packages" render={props =>
            <Fragment>
                <Packages />
                < Sidebar />
            </Fragment>} />
        <Route exact path="/questions" render={props =>
            <Fragment>
                <Questions />
                < Sidebar />
            </Fragment>} />
        <Route exact path="/firewall" render={props =>
            <Fragment>
                <Firewall />
                < Sidebar />
            </Fragment>} />
        <Route exact path="/filepaths" render={props =>
            <Fragment>
                <Filepaths />
                < Sidebar />
            </Fragment>} />
        <Route exact path="/answerkey" render={props =>
            <Fragment>
                <AnswerKey />
                < Sidebar />
            </Fragment>} />
    </Switch>
);

export default routes;