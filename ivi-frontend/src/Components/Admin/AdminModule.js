import React, { useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import Paper from '@material-ui/core/Paper';
import banner from './ey.png';
import DropzoneComponentAdmin from '../DropComponentAdmin/DropComponentAdmin';
import '../../App.css';
import TextField from '@material-ui/core/TextField';
import Link from '@material-ui/core/Link';


function AdminModule() {
    return (
        <React.Fragment>
            <CssBaseline />
            <AppBar color="default" position="relative">
                <Toolbar>
                    <img src={banner} alt="Banner" width="40" height="50" />
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    <Typography variant="h6" color="inherit" noWrap>
                        IVI Admin
                    </Typography>
                </Toolbar>
            </AppBar> 

            <Paper>
                <DropzoneComponentAdmin />
            </Paper>     
    </React.Fragment> 
  )
}

export default AdminModule;