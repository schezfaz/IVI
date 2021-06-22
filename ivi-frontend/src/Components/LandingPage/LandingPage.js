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
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import InputColor from 'react-input-color';

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
    width: 1000,
  },
  button: {
    display: 'block',
    marginTop: theme.spacing(2),
    textAlign: 'center'
  },
  formControl: {
    margin: theme.spacing(1),
    minWidth: 520,
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

  const [brandGuideline, setBrandGuideline] = React.useState('');
  const [open, setOpen] = React.useState(false);
  const [viewOP, setViewOP] = React.useState(false);
  const [headingColor, setHeadingColor] = React.useState({});
  const [headingFontSize, setHeadingFontSize] = React.useState('24');
  const [bulletFontSize,setBulletFontSize] = React.useState('16');
  const [headingFontStyle,setHeadingFontStyle]  = React.useState('Arial');
  const [headingCasing, setHeadingCasing] = React.useState('Sentence Casing');
  const [bulletFontColour, setBulletFontColour]  = React.useState({});
  const [bulletBGColour, setBulletBGColour] = React.useState({});
  const [paraFontColour, setParaFontColour]  = React.useState({});
  const [paraBGColour, setParaBGColour] = React.useState({});
  const [paraFontSize, setParaFontSize] = React.useState({});
  

  const handleChange = (event) => {
    setBrandGuideline(event.target.value);
    localStorage.setItem("brandGuideline", event.target.value);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleOpen = () => {
    setOpen(true);
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
      {/* <main>
       
        <div className={classes.heroContent}>
          <Container maxWidth="lg">
            <Typography component="h1" variant="h4" align="center" color="textPrimary" gutterBottom>
                IVI - BaScheD
            </Typography>
          </Container>
        </div>
      </main> */}
      <br/><br/>

      <Grid container spacing={3}>
            <Grid item xs={2}>
            </Grid>
            <Grid item xs={8}>


              <Paper  style={{width:"20%;"}}> 
                <DropzoneComponent />
              </Paper>     
              <br/><br/> 

              <Paper>
                <h4>Heading Configuration</h4>
                <Grid container spacing={1}>
                  <Grid item xs={3}>
                    <TextField id="outlined-basic" placeholder="24" label="Font Size" variant="outlined" onChange={(e) => setHeadingFontSize(e.target.value)}/>
                  </Grid>

                  <Grid item xs={3}>
                      <h3>Font Colour</h3>
                      <InputColor
                        initialValue="#2e2e2e"
                        onChange={setHeadingColor}
                        placement="right"
                      />
                  </Grid>

                  <Grid item xs={3}>
                    <InputLabel id="headingFontStyleLabel">Font Style</InputLabel>
                    <Select
                      labelId="headingFontStyleLabel"
                      id="headingFontStyle"
                      value={headingFontStyle}
                      onChange={(e)=>setHeadingFontStyle(e.target.value)}
                    >
                      <MenuItem value={10}>Arial</MenuItem>
                      <MenuItem value={20}>Times New Roman</MenuItem>
                      <MenuItem value={30}>Comic Sans</MenuItem>
                    </Select>
                  </Grid>

                  <Grid item xs={3}>
                    <InputLabel id="headingCasingLabel">Casing</InputLabel>
                      <Select
                        labelId="headingCasingLabel"
                        id="headingCasing"
                        value={headingCasing}
                        onChange={(e)=>setHeadingCasing(e.target.value)}
                      >
                        <MenuItem value={10}>Sentence Case</MenuItem>
                        <MenuItem value={20}>Camel Case</MenuItem>
                      </Select>
                  </Grid>

                </Grid>
              </Paper>
              <br/>

              <Paper>
                <h4>Bullet Point - Configuration</h4>
                <Grid container spacing={2}>
                  <Grid item xs={4}>
                    <TextField id="outlined-basic" placeholder="16" label="Font Size" variant="outlined" onChange={(e) => setBulletFontSize(e.target.value)}/>
                  </Grid>

                  <Grid item xs={4}>
                      <h3>Font Colour</h3>
                        <InputColor
                          initialValue="#2e2e2e"
                          onChange={setBulletFontColour}
                          placement="right"
                        />
                  </Grid>

                  <Grid item xs={4}>
                    <h3>Background Colour</h3>
                        <InputColor
                          initialValue="#ffffff"
                          onChange={setBulletBGColour}
                          placement="right"
                        />
                  </Grid>
                </Grid>            
              </Paper>
              <br/>

              
              <Paper>
                <h4>Paragraph - Configuration</h4>
                <Grid container spacing={2}>
                  <Grid item xs={4}>
                    <TextField id="outlined-basic" placeholder="16" label="Font Size" variant="outlined" onChange={(e) => setParaFontSize(e.target.value)} />
                  </Grid>

                  <Grid item xs={4}>
                      <h3>Font Colour</h3>
                        <InputColor
                          initialValue="#2e2e2e"
                          onChange={setParaFontColour}
                          placement="right"
                        />
                  </Grid>

                  <Grid item xs={4}>
                    <h3>Background Colour</h3>
                        <InputColor
                          initialValue="#ffffff"
                          onChange={setParaBGColour}
                          placement="right"
                        />
                  </Grid>
                </Grid>
              </Paper>
              <br/>

              <Paper>
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
              </Paper>
              <br/><br/> 
              <Paper>
              <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Link href="#/myspace" variant="body2">
                      <Button variant="contained" style={{backgroundColor:"#797878",color:'white'}}>
                        My Space
                      </Button>
                    </Link>
                  </Grid>
                  <Grid item xs={6}>
                    <Link href="#/dashboardurl" variant="body2">
                      <Button variant="contained" style={{backgroundColor:"#797878",color:'white'}}>
                        View Analytics Dashboard
                      </Button>
                    </Link>
                  </Grid>
                </Grid>
              </Paper>
                <br/><br/><br/>
            </Grid>

           
          </Grid>
    </React.Fragment> 
  );
}