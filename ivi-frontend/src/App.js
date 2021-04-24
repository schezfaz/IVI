import './App.css';
import { Route, Switch, HashRouter } from 'react-router-dom';
import LandingPage from './Components/LandingPage/LandingPage';

function App() {
  return (
    <div className="App">
      {/* <header className="App-header"> */}
      <HashRouter>
          <Switch>
            <Route exact path="/" component={LandingPage}/>
          </Switch>
      </HashRouter>
      {/* </header> */}
    </div>
  );
}

export default App;
