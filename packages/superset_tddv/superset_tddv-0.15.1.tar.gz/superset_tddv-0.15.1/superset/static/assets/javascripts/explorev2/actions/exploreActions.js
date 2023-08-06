/* eslint camelcase: 0 */
const $ = window.$ = require('jquery');
const FAVESTAR_BASE_URL = '/superset/favstar/slice';

export const SET_FIELD_OPTIONS = 'SET_FIELD_OPTIONS';
export function setFieldOptions(options) {
  return { type: SET_FIELD_OPTIONS, options };
}

export const SET_DATASOURCE_TYPE = 'SET_DATASOURCE_TYPE';
export function setDatasourceType(datasourceType) {
  return { type: SET_DATASOURCE_TYPE, datasourceType };
}

export const FETCH_STARTED = 'FETCH_STARTED';
export function fetchStarted() {
  return { type: FETCH_STARTED };
}

export const FETCH_SUCCEEDED = 'FETCH_SUCCEEDED';
export function fetchSucceeded() {
  return { type: FETCH_SUCCEEDED };
}

export const FETCH_FAILED = 'FETCH_FAILED';
export function fetchFailed(error) {
  return { type: FETCH_FAILED, error };
}

export function fetchFieldOptions(datasourceId, datasourceType) {
  return function (dispatch) {
    dispatch(fetchStarted());

    if (datasourceId) {
      const params = [`datasource_id=${datasourceId}`, `datasource_type=${datasourceType}`];
      const url = '/superset/fetch_datasource_metadata?' + params.join('&');
      $.ajax({
        type: 'GET',
        url,
        success: (data) => {
          dispatch(setFieldOptions(data.field_options));
          dispatch(fetchSucceeded());
        },
        error(error) {
          dispatch(fetchFailed(error.responseJSON.error));
        },
      });
    } else {
      dispatch(fetchFailed('Please select a datasource'));
    }
  };
}

export const TOGGLE_FAVE_STAR = 'TOGGLE_FAVE_STAR';
export function toggleFaveStar(isStarred) {
  return { type: TOGGLE_FAVE_STAR, isStarred };
}

export const FETCH_FAVE_STAR = 'FETCH_FAVE_STAR';
export function fetchFaveStar(sliceId) {
  return function (dispatch) {
    const url = `${FAVESTAR_BASE_URL}/${sliceId}/count`;
    $.get(url, (data) => {
      if (data.count > 0) {
        dispatch(toggleFaveStar(true));
      }
    });
  };
}

export const SAVE_FAVE_STAR = 'SAVE_FAVE_STAR';
export function saveFaveStar(sliceId, isStarred) {
  return function (dispatch) {
    const urlSuffix = isStarred ? 'unselect' : 'select';
    const url = `${FAVESTAR_BASE_URL}/${sliceId}/${urlSuffix}/`;
    $.get(url);
    dispatch(toggleFaveStar(!isStarred));
  };
}

export const ADD_FILTER = 'ADD_FILTER';
export function addFilter(filter) {
  return { type: ADD_FILTER, filter };
}

export const REMOVE_FILTER = 'REMOVE_FILTER';
export function removeFilter(filter) {
  return { type: REMOVE_FILTER, filter };
}

export const CHANGE_FILTER = 'CHANGE_FILTER';
export function changeFilter(filter, field, value) {
  return { type: CHANGE_FILTER, filter, field, value };
}

export const ADD_STYLE = 'ADD_STYLE';
export function addStyle(style) {
  return { type: ADD_STYLE, style };
}

export const REMOVE_STYLE = 'REMOVE_STYLE';
export function removeStyle(style) {
  return { type: REMOVE_STYLE, style };
}

export const CHANGE_STYLE = 'CHANGE_STYLE';
export function changeStyle(style, field, value) {
  return { type: CHANGE_STYLE, style, field, value };
}

export const CHANGE_BASE_STYLE = 'CHANGE_BASE_STYLE';
export function changeBaseStyle(baseStyle, field, value) {
  return { type: CHANGE_BASE_STYLE, baseStyle, field, value };
}

export const ADD_COL_STYLE = 'ADD_COL_STYLE';
export function addColStyle(colStyle) {
  return { type: ADD_COL_STYLE, colStyle };
}

export const REMOVE_COL_STYLE = 'REMOVE_COL_STYLE';
export function removeColStyle(colStyle) {
  return { type: REMOVE_COL_STYLE, colStyle };
}

export const CHANGE_COL_STYLE = 'CHANGE_COL_STYLE';
export function changeColStyle(colStyle, field, value) {
  return { type: CHANGE_COL_STYLE, colStyle, field, value };
}

export const ADD_COMPARE = 'ADD_COMPARE';
export function addCompare(compare) {
  return { type: ADD_COMPARE, compare };
}

export const REMOVE_COMPARE = 'REMOVE_COMPARE';
export function removeCompare(compare) {
  return { type: REMOVE_COMPARE, compare };
}

export const CHANGE_COMPARE = 'CHANGE_COMPARE';
export function changeCompare(compare, field, value) {
  return { type: CHANGE_COMPARE, compare, field, value };
}

export const ADD_NAVIGATE = 'ADD_NAVIGATE';
export function addNavigate(navigate) {
  return { type: ADD_NAVIGATE, navigate };
}

export const REMOVE_NAVIGATE = 'REMOVE_NAVIGATE';
export function removeNavigate(navigate) {
  return { type: REMOVE_NAVIGATE, navigate };
}

export const CHANGE_NAVIGATE = 'CHANGE_NAVIGATE';
export function changeNavigate(navigate, field, value) {
  return { type: CHANGE_NAVIGATE, navigate, field, value };
}

export const CHANGE_FLOAT_STYLE = 'CHANGE_FLOAT_STYLE';
export function changeFloatStyle(style, field, value) {
  return { type: CHANGE_FLOAT_STYLE, style, field, value };
}

export const ADD_PROMPT_COL_STYLE = 'ADD_PROMPT_COL_STYLE';
export function addPromptColStyle(promptColStyle) {
  return { type: ADD_PROMPT_COL_STYLE, promptColStyle };
}

export const REMOVE_PROMPT_COL_STYLE = 'REMOVE_PROMPT_COL_STYLE';
export function removePromptColStyle(promptColStyle) {
  return { type: REMOVE_PROMPT_COL_STYLE, promptColStyle };
}

export const CHANGE_PROMPT_COL_STYLE = 'CHANGE_PROMPT_COL_STYLE';
export function changePromptColStyle(promptColStyle, field, value) {
  return { type: CHANGE_PROMPT_COL_STYLE, promptColStyle, field, value };
}

export const SET_FIELD_VALUE = 'SET_FIELD_VALUE';
export function setFieldValue(datasource_type, key, value, label) {
  return { type: SET_FIELD_VALUE, datasource_type, key, value, label };
}

export const CHART_UPDATE_STARTED = 'CHART_UPDATE_STARTED';
export function chartUpdateStarted() {
  return { type: CHART_UPDATE_STARTED };
}

export const CHART_UPDATE_SUCCEEDED = 'CHART_UPDATE_SUCCEEDED';
export function chartUpdateSucceeded(query) {
  return { type: CHART_UPDATE_SUCCEEDED, query };
}

export const CHART_UPDATE_FAILED = 'CHART_UPDATE_FAILED';
export function chartUpdateFailed(error) {
  return { type: CHART_UPDATE_FAILED, error };
}

export const UPDATE_EXPLORE_ENDPOINTS = 'UPDATE_EXPLORE_ENDPOINTS';
export function updateExploreEndpoints(jsonUrl, csvUrl, standaloneUrl) {
  return { type: UPDATE_EXPLORE_ENDPOINTS, jsonUrl, csvUrl, standaloneUrl };
}

export const REMOVE_CONTROL_PANEL_ALERT = 'REMOVE_CONTROL_PANEL_ALERT';
export function removeControlPanelAlert() {
  return { type: REMOVE_CONTROL_PANEL_ALERT };
}

export const REMOVE_CHART_ALERT = 'REMOVE_CHART_ALERT';
export function removeChartAlert() {
  return { type: REMOVE_CHART_ALERT };
}

export const FETCH_DASHBOARDS_SUCCEEDED = 'FETCH_DASHBOARDS_SUCCEEDED';
export function fetchDashboardsSucceeded(choices) {
  return { type: FETCH_DASHBOARDS_SUCCEEDED, choices };
}

export const FETCH_DASHBOARDS_FAILED = 'FETCH_DASHBOARDS_FAILED';
export function fetchDashboardsFailed(userId) {
  return { type: FETCH_FAILED, userId };
}

export function fetchDashboards(userId) {
  return function (dispatch) {
    const url = '/dashboardmodelviewasync/api/read?_flt_0_owners=' + userId;
    $.get(url, function (data, status) {
      if (status === 'success') {
        const choices = [];
        for (let i = 0; i < data.pks.length; i++) {
          choices.push({ value: data.pks[i], label: data.result[i].dashboard_title });
        }
        dispatch(fetchDashboardsSucceeded(choices));
      } else {
        dispatch(fetchDashboardsFailed(userId));
      }
    });
  };
}

export const SAVE_SLICE_FAILED = 'SAVE_SLICE_FAILED';
export function saveSliceFailed() {
  return { type: SAVE_SLICE_FAILED };
}

export const REMOVE_SAVE_MODAL_ALERT = 'REMOVE_SAVE_MODAL_ALERT';
export function removeSaveModalAlert() {
  return { type: REMOVE_SAVE_MODAL_ALERT };
}

export function saveSlice(url) {
  return function (dispatch) {
    $.get(url, (data, status) => {
      if (status === 'success') {
        // Go to new slice url or dashboard url
        window.location = data;
      } else {
        dispatch(saveSliceFailed());
      }
    });
  };
}

export const UPDATE_CHART_STATUS = 'UPDATE_CHART_STATUS';
export function updateChartStatus(status) {
  return { type: UPDATE_CHART_STATUS, status };
}
