import shortid from 'shortid';
import * as actions from './actions';
import { now } from '../modules/dates';
import { addToObject, alterInObject, alterInArr, removeFromArr, getFromArr, addToArr }
  from '../reduxUtils.js';

export function getInitialState(defaultDbId) {
  const defaultQueryEditor = {
    id: shortid.generate(),
    title: 'Untitled Query',
    sql: 'SELECT *\nFROM\nWHERE',
    selectedText: null,
    latestQueryId: null,
    autorun: false,
    dbId: defaultDbId,
  };

  return {
    alerts: [],
    networkOn: true,
    queries: {},
    databases: {},
    queryEditors: [defaultQueryEditor],
    tabHistory: [defaultQueryEditor.id],
    tables: [],
    queriesLastUpdate: 0,
    activeSouthPaneTab: 'Results',
  };
}

export const portalReducer = function (state, action) {
  const actionHandlers = {
    [actions.RESET_STATE]() {
      return Object.assign({}, getInitialState());
    },
  };
  if (action.type in actionHandlers) {
    return actionHandlers[action.type]();
  }
  return state;
};
