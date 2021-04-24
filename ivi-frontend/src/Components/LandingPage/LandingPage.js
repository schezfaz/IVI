import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import banner from './ey.png';
import ivirobo from './ivi-robo.gif';
import DropzoneComponent from '../DropZoneComponent/DropZoneComponent';


const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  paper: {
    padding: theme.spacing(2),
    textAlign: 'center',
    color: theme.palette.text.secondary,
    height: '100%'
  },
  mainGrid: {
    marginTop: theme.spacing(3),
  },icon: {
    marginRight: theme.spacing(2),
  },
  heroContent: {
    backgroundColor: theme.palette.background.paper,
    padding: theme.spacing(8, 0, 6),
  },
  heroButtons: {
    marginTop: theme.spacing(4),
  },
  cardGrid: {
    paddingTop: theme.spacing(8),
    paddingBottom: theme.spacing(8),
  },
  card: {
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
  },
  cardMedia: {
    paddingTop: '56.25%', // 16:9
  },
  cardContent: {
    flexGrow: 1,
  },
  footer: {
    backgroundColor: theme.palette.background.paper,
    padding: theme.spacing(6),
  },
  search: {
    margin: theme.spacing(1),
    width: 600,
  },
}));



export default function LandingPage() {
  const classes = useStyles();

  return (
    <React.Fragment>
      <CssBaseline />
      <AppBar color="default" position="relative">
        <Toolbar>
          <img src={banner} alt="Banner" width="40" height="50" />
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          <Typography variant="h6" color="inherit" noWrap>
          Intelligent Visual Identifier - (IVI)
          </Typography>
        </Toolbar>
      </AppBar>
      <main>
        {/* Hero unit */}
        <div className={classes.heroContent}>
          <Container maxWidth="lg">
            <Typography component="h1" variant="h2" align="center" color="textPrimary" gutterBottom>
                IVI
            </Typography>
            <Typography variant="h5" align="center" color="textSecondary" paragraph>
              <i>IVI all EY Documents</i>
            </Typography>
          </Container>
          <Grid container spacing={3}>
            <Grid item xs>
              <img src={ivirobo} alt="ivirobo"/>
            </Grid>
            <Grid item xs>
              <Paper className={classes.paper}>
                <DropzoneComponent/>
              </Paper>
            </Grid>
          </Grid>
          
        </div>
       

      </main>
    </React.Fragment> 
  );
}