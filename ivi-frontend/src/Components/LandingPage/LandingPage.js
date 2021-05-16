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
import ivirobo from './ivi-robo.gif';
import DropzoneComponent from '../DropZoneComponent/DropZoneComponent';
import '../../App.css';
import TextField from '@material-ui/core/TextField';
import toast from 'react-hot-toast';
import Link from '@material-ui/core/Link';


const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  paper: {
    padding: theme.spacing(2),
    textAlign: 'center',
    color: theme.palette.text.secondary,
    height: '100%',
    backgroundImage: 'https://wallpaper.dog/large/5518945.jpg'
  },
  mainGrid: {
    marginTop: theme.spacing(3),
  },icon: {
    marginRight: theme.spacing(2),
  },
  heroContent: {
    backgroundColor: theme.palette.background.paper,
    padding: theme.spacing(5, 0, 4),
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

  useEffect(() => {
    notifyWelcome();
  }, []);


  const notifyWelcome = () => {
    console.log("here")
    toast.success("IVI welcomes you !");
  };


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
            <Typography component="h1" variant="h4" align="center" color="textPrimary" gutterBottom>
                IVI - BaScheD
            </Typography>
          </Container>
        </div>
      </main>
      <br/><br/>

      <Grid container spacing={3}>
            <Grid item xs className="ivi-robo">
              <img src={ivirobo} alt="ivirobo"/>
            </Grid>
            <Grid item xs >
              <Paper>
                <DropzoneComponent />
              </Paper>     
                {/* <br/><br/>
              <Button variant="contained" style={{backgroundColor:"#ffe600"}}>
                Apply IVI Now
              </Button> */}
              <br/><br/> <br/><br/>
                <TextField
                  id="outlined-basic"
                  style ={{width: '95%'}} 
                  margin="dense" 
                  autoFocus 
                  label="SharePoint Folder Path to Document" 
                />
                <br/><br/>
                <Button variant="contained" style={{backgroundColor:"#ffe600"}}>
                  Apply IVI on SharePoint Location Now
                </Button>
                <br/><br/><br/><br/><br/><br/><br/><br/>
                <Link href="#/myspace" variant="body2">
                  <Button variant="contained" style={{backgroundColor:"#797878",color:'white'}}>
                    My Space
                  </Button>
                </Link>
            </Grid>

           
          </Grid>
    </React.Fragment> 
  );
}