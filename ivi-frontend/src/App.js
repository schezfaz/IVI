import './App.css';
import { Route, Switch, HashRouter } from 'react-router-dom';
import LandingPage from './Components/LandingPage/LandingPage';
import MySpace from './Components/MySpace/MySpace';
import AdminModule from './Components/Admin/AdminModule';
import { Toaster } from 'react-hot-toast';

function App() {
  return (
    <div className="App">
      {/* <header className="App-header"> */}
      <HashRouter>
          <Switch>
            <Route exact path="/" component={LandingPage}/>
            <Route exact path="/myspace" component={MySpace}/>
            <Route exact path="/admin" component={AdminModule}/>
          </Switch>
      </HashRouter>

      <Toaster
        position="top-center"
        toastOptions={{
          className: '',
          style: {
            border: '1px solid #713200',
            padding: '16px',
            color: '#713200',
          },
          success: {
            duration: 2000,
            theme: {
              primary: 'green',
              secondary: 'black',
            },
          }
        }}
      />
      {/* </header> */}
    </div>
  );
}

export default App;
