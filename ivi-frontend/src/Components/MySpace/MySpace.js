import React, { useEffect } from 'react';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';
import { useSpeechSynthesis } from 'react-speech-kit';
import toast from 'react-hot-toast';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';

const useStyles = makeStyles((theme) => ({
  root: {
    height: '100vh',
  },
  image: {
    backgroundImage: 'url(https://bloopglobal.com/wp-content/uploads/2020/11/interactive-presentation-header-1.gif)',
    // backgroundImage : 'url(https://cdn.dribbble.com/users/42048/screenshots/8350927/robotintro_dribble.gif)',
    backgroundRepeat: 'no-repeat',
    backgroundColor:
      theme.palette.type === 'light' ? theme.palette.grey[50] : theme.palette.grey[900],
    backgroundSize: 'cover',
    backgroundPosition: 'center',
  },
  paper: {
    //margin: theme.spacing(8, 4),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.primary.main,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    //margin: theme.spacing(3, 0, 2),
  },
  card : {
    backgroundColor: '#e2e1fc'
  }
}));

const MySpace = () => {
  const classes = useStyles();
  const { transcript, resetTranscript } = useSpeechRecognition();
  const [notes, setNotes] = React.useState([]);

//   const [value, setValue] = useState('');
  const { speak } = useSpeechSynthesis();

  // Similar to componentDidMount and componentDidUpdate:
  useEffect(() => {
  });

  useEffect(() => {
    notifyWelcome();
  }, []);

  function stopCapture() {
    SpeechRecognition.stopListening();
    console.log(transcript);
    speak({ text: "Note has been made for " + transcript, rate: 0.9 })
    setNotes(prevArray => [...prevArray, transcript]);
    console.log(notes);
    notifyAddNote();
  }

  const notifyWelcome = () => {
    console.log("here")
    toast.success("IVI welcomes you !");
  };

  const notifyAddNote = () => {
    toast.success("Great! Your Note is submitted.", {
        icon: '🔥',
    });
};


  if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
    return null
  }

  return (
    <React.Fragment>
      <CssBaseline />
        <Container maxWidth="lg">
          <br />
          <Grid container component="main" className={classes.root}>
            <CssBaseline />
            <Grid item xs={false} sm={4} md={5} component={Paper} elevation={5} className={classes.image} />
            <Grid item xs={12} sm={4} md={7} component={Paper} elevation={5} >
              <div className={classes.paper}>
                <img alt="mind_note" width="60%" height="20%" src="https://www.pocketprep.com/wp-content/uploads/2021/03/Brain-dumps-and-other-test-day-hacks_post-image-full.jpg" />
                <div>
                  <Button
                    // type="submit"
                    // fullWidth
                    variant="outlined"
                    color="secondary"
                    className={classes.submit}
                    onClick={SpeechRecognition.startListening}
                  >
                    Capture
            </Button>
            &nbsp;
            <Button
                    // type="submit"
                    // fullWidth
                    variant="outlined"
                    color="secondary"
                    className={classes.submit}
                    onClick={stopCapture}
                  >
                    Stop
            </Button>
            &nbsp;
            <Button
                    // type="submit"
                    // fullWidth
                    variant="outlined"
                    color="secondary"
                    className={classes.submit}
                    onClick={resetTranscript}
                  >
                    Reset
            </Button>
                  {/* <button onClick={SpeechRecognition.startListening}>Capture</button>
            <button onClick={SpeechRecognition.stopListening}>Stop</button>
            <button onClick={resetTranscript}>Reset</button> */}
                  <h5>{transcript}</h5>
                  {/* {notes.map((item) => (
                    <p>{item}</p>
                  ))} */}

                </div>
                <Container maxWidth="lg">
                  <Grid container spacing={4}>
                    {notes.map((note) => (
                      <Grid item xs={12} sm={6} md={6}>
                        <Card className={classes.card}>

                          <CardContent className={classes.cardContent}>
                            <Typography gutterBottom variant="body1" component="h2">
                              {note}
                            </Typography>
                          </CardContent>
                          {/* <center> */}
                            <CardActions>
                              <Button
                                variant="outlined"
                                size="small"
                                color="primary"
                                fullWidth
                              // onClick={() => {window.open('/#/digital')}}
                              >
                                Edit/delete
                      </Button>

                            </CardActions>
                          {/* </center> */}
                        </Card>
                      </Grid>
                    ))}
                  </Grid>
                </Container>
              </div>
            </Grid>
          </Grid>
        </Container>
        <br />
    </React.Fragment>
  )
}
export default MySpace