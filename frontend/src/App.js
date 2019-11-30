import React,{useEffect} from 'react';
import logo from './logo.svg';
import './App.css';
import { Switch } from 'react-router-dom';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import Search from './Search';
import Result from './Result';

function App() {
  useEffect(()=>{
    fetch("/").then(response =>
      response.json().then(data => {
        console.log(data)
      }))
  },[])
  return (
    <Router>
      <div className="App">
       

          <Switch>
            <Route path="/" exact component={Search} />
            <Route path="/results" exact component={Result} />
            <Route path="" exact component={Search} />
          </Switch>
      </div>

    </Router>
  );
}

export default App;
