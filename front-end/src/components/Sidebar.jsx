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
import './Components.css';
import { Link } from 'react-router-dom'
import { makeStyles } from "@material-ui/core/styles";
import { Drawer, List, ListItem, ListItemIcon, ListItemText } from "@material-ui/core";
import { getOS } from '../pages/Home.jsx';

import HomeIcon from "@material-ui/icons/Home";
import PersonIcon from '@material-ui/icons/Person';
import SettingsIcon from '@material-ui/icons/Settings';
import VpnKeyIcon from '@material-ui/icons/VpnKey';
import SportsEsportsIcon from '@material-ui/icons/SportsEsports';
import HelpIcon from '@material-ui/icons/Help';
import KeyboardBackspaceIcon from '@material-ui/icons/KeyboardBackspace';
import FileCopyIcon from '@material-ui/icons/FileCopy';
import BlockIcon from '@material-ui/icons/Block';

const useStyles = makeStyles((theme) => ({
    drawerPaper: { width: 'inherit', backgroundColor: "#282c34" },
    link: { textDecoration: 'none', color: "white", "&:hover": { textDecoration: 'none', color: "white" } },
    icon: { color: "white" },
    big: {
        position: 'fixed', bottom: 0, width: '240px', color: "white", textDecoration: 'none', "&:hover": { textDecoration: 'none', color: "white" }
    }
}))

var os = 0;
var osName = "None";

export default function Sidebar() {
    const classes = useStyles();

    if (os === 0) {
        console.log("Sidebar: attempting to get OS value.");
        os = getOS();
        console.log("Sidebar retrieved OS: " + os);
    }


    if (os === 2) {
        console.log("Rendering sidebar.");
        return (
            <div style={{ display: 'flex' }}>
                <Drawer
                    style={{ width: '15rem' }}
                    variant="persistent"
                    anchor="left"
                    open={true}
                    classes={{ paper: classes.drawerPaper }}>

                    <List>
                        <Link to="/home" className={classes.link}>
                            <ListItem button>
                                <ListItemIcon className={classes.icon}>
                                    <HomeIcon />
                                </ListItemIcon>
                                <ListItemText primary={"Home"} />
                            </ListItem>
                        </Link>
                        < Link to="/users" className={classes.link}>
                            <ListItem button>
                                <ListItemIcon className={classes.icon}>
                                    <PersonIcon />
                                </ListItemIcon>
                                <ListItemText primary={"Users"} />
                            </ListItem>
                        </Link>
                        < Link to="/services" className={classes.link}>
                            <ListItem button>
                                <ListItemIcon className={classes.icon}>
                                    <SettingsIcon />
                                </ListItemIcon>
                                <ListItemText primary={"Services"} />
                            </ListItem>
                        </Link>
                        < Link to="/firewall" className={classes.link}>
                            <ListItem button>
                                <ListItemIcon className={classes.icon}>
                                    <BlockIcon />
                                </ListItemIcon>
                                <ListItemText primary={"Firewall"} />
                            </ListItem>
                        </Link>
                        < Link to="/filepaths" className={classes.link}>
                            <ListItem button>
                                <ListItemIcon className={classes.icon}>
                                    <FileCopyIcon />
                                </ListItemIcon>
                                <ListItemText primary={"Filepaths"} />
                            </ListItem>
                        </ Link>
                        < Link to="/registry" className={classes.link}>
                            <ListItem button>
                                <ListItemIcon className={classes.icon}>
                                    <VpnKeyIcon />
                                </ListItemIcon>
                                <ListItemText primary={"Registry Entries"} />
                            </ListItem>
                        </Link>
                        < Link to="/programs" className={classes.link}>
                            <ListItem button>
                                <ListItemIcon className={classes.icon}>
                                    <SportsEsportsIcon />
                                </ListItemIcon>
                                <ListItemText primary={"Installed Programs"} />
                            </ListItem>
                        </Link>
                        < Link to="/questions" className={classes.link} >
                            <ListItem button >
                                <ListItemIcon className={classes.icon}>
                                    <HelpIcon />
                                </ListItemIcon>
                                <ListItemText primary={"Challenge Questions"} />
                            </ListItem>
                        </Link>
                        < Link to="/answerkey" className={classes.link} >
                            <ListItem button >
                                <ListItemIcon className={classes.icon}>
                                    <VpnKeyIcon />
                                </ListItemIcon>
                                <ListItemText primary={"Answer Key"} />
                            </ListItem>
                        </Link>
                        < Link to="/" className={classes.big}>
                            <ListItem button>
                                <ListItemIcon className={classes.icon}>
                                    <KeyboardBackspaceIcon />
                                </ListItemIcon>
                                <ListItemText primary={"Back"} />
                            </ListItem>
                        </Link>
                    </List>
                </Drawer>
            </div >
        );
    }
    else if (os === 1) {
        console.log("Rendering sidebar.");

        return (
            <div style={{ display: 'flex' }}>
                <Drawer
                    style={{ width: '15rem' }}
                    variant="persistent"
                    anchor="left"
                    open={true}
                    classes={{ paper: classes.drawerPaper }}>

                    <List>
                        <Link to="/home" className={classes.link}>
                            <ListItem button>
                                <ListItemIcon className={classes.icon}>
                                    <HomeIcon />
                                </ListItemIcon>
                                <ListItemText primary={"Home"} />
                            </ListItem>
                        </Link>
                        < Link to="/linuxusers" className={classes.link}>
                            <ListItem button>
                                <ListItemIcon className={classes.icon}>
                                    <PersonIcon />
                                </ListItemIcon>
                                <ListItemText primary={"Users"} />
                            </ListItem>
                        </Link>
                        < Link to="/processes" className={classes.link}>
                            <ListItem button>
                                <ListItemIcon className={classes.icon}>
                                    <SettingsIcon />
                                </ListItemIcon>
                                <ListItemText primary={"Processes"} />
                            </ListItem>
                        </Link>
                        < Link to="/filepaths" className={classes.link}>
                            <ListItem button>
                                <ListItemIcon className={classes.icon}>
                                    <FileCopyIcon />
                                </ListItemIcon>
                                <ListItemText primary={"Filepaths"} />
                            </ListItem>
                        </ Link>
                        < Link to="/configfile" className={classes.link}>
                            <ListItem button>
                                <ListItemIcon className={classes.icon}>
                                    <VpnKeyIcon />
                                </ListItemIcon>
                                <ListItemText primary={"Configuration Files"} />
                            </ListItem>
                        </Link>
                        < Link to="/packages" className={classes.link}>
                            <ListItem button>
                                <ListItemIcon className={classes.icon}>
                                    <SportsEsportsIcon />
                                </ListItemIcon>
                                <ListItemText primary={"Installed Packages"} />
                            </ListItem>
                        </Link>
                        < Link to="/questions" className={classes.link} >
                            <ListItem button >
                                <ListItemIcon className={classes.icon}>
                                    <HelpIcon />
                                </ListItemIcon>
                                <ListItemText primary={"Challenge Questions"} />
                            </ListItem>
                        </Link>
                        < Link to="/answerkey" className={classes.link} >
                            <ListItem button >
                                <ListItemIcon className={classes.icon}>
                                    <VpnKeyIcon />
                                </ListItemIcon>
                                <ListItemText primary={"Answer Key"} />
                            </ListItem>
                        </Link>
                        < Link to="/" className={classes.big}>
                            <ListItem button>
                                <ListItemIcon className={classes.icon}>
                                    <KeyboardBackspaceIcon />
                                </ListItemIcon>
                                <ListItemText primary={"Back"} />
                            </ListItem>
                        </Link>
                    </List>
                </Drawer>
            </div >
        );
    }
    else {
        return (
            <div style={{ display: 'flex' }}>
                <Drawer
                    style={{ width: '15rem' }}
                    variant="persistent"
                    anchor="left"
                    open={true}
                    classes={{ paper: classes.drawerPaper }}>
                    <List>
                        < Link to="/" className={classes.big}>
                            <ListItem button>
                                <ListItemIcon className={classes.icon}>
                                    <KeyboardBackspaceIcon />
                                </ListItemIcon>
                                <ListItemText primary={"Back"} />
                            </ListItem>
                        </Link>
                    </List>
                </Drawer>
            </div >
        );
    }
}

export function setOS(value) {
    if (value === 1) {
        os = 1;
        osName = "Linux";
    }
    else if (value === 2) {
        os = 2;
        osName = "Windows";
    }

    console.log(`Sidebar OS: ${os}`);
    console.log(`Sidebar OS Name: ${osName}`);
}