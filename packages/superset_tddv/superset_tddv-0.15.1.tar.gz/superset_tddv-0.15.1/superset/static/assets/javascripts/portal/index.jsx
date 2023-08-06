const $ = window.$ = require('jquery');
const jQuery = window.jQuery = $; // eslint-disable-line
require('bootstrap');

import React from 'react';
import { render } from 'react-dom';
import { getInitialState, portalReducer } from './reducers';
import { enhancer } from '../reduxUtils';
import { createStore, compose, applyMiddleware } from 'redux';
import { Provider } from 'react-redux';
import thunkMiddleware from 'redux-thunk';

import App from './components/App';


require('./main.css');

const appContainer = document.getElementById('app');
const bootstrapData = JSON.parse(appContainer.getAttribute('data-bootstrap'));
const state = Object.assign({}, getInitialState(bootstrapData.portalId), bootstrapData);

console.log(111111)
console.log(bootstrapData)

let store = createStore(
  portalReducer, state, compose(applyMiddleware(thunkMiddleware), enhancer()));

// jquery hack to highlight the navbar menu
$('a:contains("portal")').parent().addClass('active');

render(
  <Provider store={store}>
    <App />
  </Provider>,
  appContainer
);
