/* eslint camelcase: 0 */
import { defaultFormData } from '../stores/store';
import * as actions from '../actions/exploreActions';
import { addToArr, removeFromArr, alterInArr } from '../../../utils/reducerUtils';
import { now } from '../../modules/dates';
import { getExploreUrl } from '../exploreUtils';

export const exploreReducer = function (state, action) {
  const actionHandlers = {
    [actions.TOGGLE_FAVE_STAR]() {
      return Object.assign({}, state, { isStarred: action.isStarred });
    },

    [actions.FETCH_STARTED]() {
      return Object.assign({}, state, { isDatasourceMetaLoading: true });
    },

    [actions.FETCH_SUCCEEDED]() {
      return Object.assign({}, state, { isDatasourceMetaLoading: false });
    },

    [actions.FETCH_FAILED]() {
      // todo(alanna) handle failure/error state
      return Object.assign({}, state,
        {
          isDatasourceMetaLoading: false,
          controlPanelAlert: action.error,
        });
    },
    [actions.REMOVE_CONTROL_PANEL_ALERT]() {
      return Object.assign({}, state, { controlPanelAlert: null });
    },

    [actions.FETCH_DASHBOARDS_SUCCEEDED]() {
      return Object.assign({}, state, { dashboards: action.choices });
    },

    [actions.FETCH_DASHBOARDS_FAILED]() {
      return Object.assign({}, state,
        { saveModalAlert: `fetching dashboards failed for ${action.userId}` });
    },

    [actions.SET_FIELD_OPTIONS]() {
      const newState = Object.assign({}, state);
      const optionsByFieldName = action.options;
      const fieldNames = Object.keys(optionsByFieldName);

      fieldNames.forEach((fieldName) => {
        if (fieldName === 'filterable_cols') {
          newState.filterColumnOpts = optionsByFieldName[fieldName];
        } else {
          newState.fields[fieldName].choices = optionsByFieldName[fieldName];
        }
      });
      return Object.assign({}, state, newState);
    },

    [actions.SET_FILTER_COLUMN_OPTS]() {
      return Object.assign({}, state, { filterColumnOpts: action.filterColumnOpts });
    },
    [actions.ADD_FILTER]() {
      const newFormData = addToArr(state.viz.form_data, 'filters', action.filter);
      const newState = Object.assign(
        {},
        state,
        { viz: Object.assign({}, state.viz, { form_data: newFormData }) }
      );
      return newState;
    },
    [actions.REMOVE_FILTER]() {
      const newFormData = removeFromArr(state.viz.form_data, 'filters', action.filter);
      return Object.assign(
        {},
        state,
        { viz: Object.assign({}, state.viz, { form_data: newFormData }) }
      );
    },
    [actions.CHANGE_FILTER]() {
      const changes = {};
      changes[action.field] = action.value;
      const newFormData = alterInArr(
        state.viz.form_data, 'filters', action.filter, changes);
      return Object.assign(
        {},
        state,
        { viz: Object.assign({}, state.viz, { form_data: newFormData }) }
      );
    },
    [actions.ADD_STYLE]() {
      const newFormData = addToArr(state.viz.form_data, 'styles', action.style);
      const newState = Object.assign(
        {},
        state,
        { viz: Object.assign({}, state.viz, { form_data: newFormData }) }
      );
      return newState;
    },
    [actions.REMOVE_STYLE]() {
      const newFormData = removeFromArr(state.viz.form_data, 'styles', action.style);
      return Object.assign(
        {},
        state,
        { viz: Object.assign({}, state.viz, { form_data: newFormData }) }
      );
    },
    [actions.CHANGE_STYLE]() {
      const changes = {};
      changes[action.field] = action.value;
      const newFormData = alterInArr(
        state.viz.form_data, 'styles', action.style, changes);
      return Object.assign(
        {},
        state,
        { viz: Object.assign({}, state.viz, { form_data: newFormData }) }
      );
    },
    [actions.CHANGE_BASE_STYLE]() {
      const newObject = Object.assign({}, state.viz.form_data.baseStyle);
      newObject[action.field] = action.value;
      const newFormData = Object.assign({}, state.viz.form_data, { ['baseStyle']: newObject });
      return Object.assign(
        {},
        state,
        { viz: Object.assign({}, state.viz, { form_data: newFormData }) }
      );
    },
    [actions.ADD_COL_STYLE]() {
      const newFormData = addToArr(state.viz.form_data, 'colStyles', action.colStyle);
      const newState = Object.assign(
        {},
        state,
        { viz: Object.assign({}, state.viz, { form_data: newFormData }) }
      );
      return newState;
    },
    [actions.REMOVE_COL_STYLE]() {
      const newFormData = removeFromArr(state.viz.form_data, 'colStyles', action.colStyle);
      return Object.assign(
        {},
        state,
        { viz: Object.assign({}, state.viz, { form_data: newFormData }) }
      );
    },
    [actions.CHANGE_COL_STYLE]() {
      const changes = {};
      changes[action.field] = action.value;
      const newFormData = alterInArr(
        state.viz.form_data, 'colStyles', action.colStyle, changes);
      return Object.assign(
        {},
        state,
        { viz: Object.assign({}, state.viz, { form_data: newFormData }) }
      );
    },
    [actions.ADD_COMPARE]() {
      const newFormData = addToArr(state.viz.form_data, 'compares', action.compare);
      const newState = Object.assign(
        {},
        state,
        { viz: Object.assign({}, state.viz, { form_data: newFormData }) }
      );
      return newState;
    },
    [actions.REMOVE_COMPARE]() {
      const newFormData = removeFromArr(state.viz.form_data, 'compares', action.compare);
      return Object.assign(
        {},
        state,
        { viz: Object.assign({}, state.viz, { form_data: newFormData }) }
      );
    },
    [actions.CHANGE_COMPARE]() {
      const changes = {};
      changes[action.field] = action.value;
      const newFormData = alterInArr(
        state.viz.form_data, 'compares', action.compare, changes);
      return Object.assign(
        {},
        state,
        { viz: Object.assign({}, state.viz, { form_data: newFormData }) }
      );
    },
    [actions.ADD_NAVIGATE]() {
      const newFormData = addToArr(state.viz.form_data, 'navigates', action.navigate);
      const newState = Object.assign(
        {},
        state,
        { viz: Object.assign({}, state.viz, { form_data: newFormData }) }
      );
      return newState;
    },
    [actions.REMOVE_NAVIGATE]() {
      const newFormData = removeFromArr(state.viz.form_data, 'navigates', action.navigate);
      return Object.assign(
        {},
        state,
        { viz: Object.assign({}, state.viz, { form_data: newFormData }) }
      );
    },
    [actions.CHANGE_NAVIGATE]() {
      const changes = {};
      changes[action.field] = action.value;
      const newFormData = alterInArr(
        state.viz.form_data, 'navigates', action.navigate, changes);
      return Object.assign(
        {},
        state,
        { viz: Object.assign({}, state.viz, { form_data: newFormData }) }
      );
    },
    [actions.CHANGE_FLOAT_STYLE]() {
      const changes = {};
      changes[action.field] = action.value;
      const newFormData = alterInArr(
        state.viz.form_data, 'promptBaseStyles', action.style, changes);
      return Object.assign(
        {},
        state,
        { viz: Object.assign({}, state.viz, { form_data: newFormData }) }
      );
    },
    [actions.ADD_PROMPT_COL_STYLE]() {
      const newFormData = addToArr(state.viz.form_data, 'promptColStyles', action.promptColStyle);
      const newState = Object.assign(
        {},
        state,
        { viz: Object.assign({}, state.viz, { form_data: newFormData }) }
      );
      return newState;
    },
    [actions.REMOVE_PROMPT_COL_STYLE]() {
      const newFormData = removeFromArr(state.viz.form_data, 'promptColStyles', action.promptColStyle);
      return Object.assign(
        {},
        state,
        { viz: Object.assign({}, state.viz, { form_data: newFormData }) }
      );
    },
    [actions.CHANGE_PROMPT_COL_STYLE]() {
      const changes = {};
      changes[action.field] = action.value;
      const newFormData = alterInArr(
        state.viz.form_data, 'promptColStyles', action.promptColStyle, changes);
      return Object.assign(
        {},
        state,
        { viz: Object.assign({}, state.viz, { form_data: newFormData }) }
      );
    },
    [actions.SET_FIELD_VALUE]() {
      const newFormData = action.key === 'datasource' ?
        defaultFormData(state.viz.form_data.viz_type, action.datasource_type) :
        Object.assign({}, state.viz.form_data);
      if (action.key === 'datasource') {
        newFormData.datasource_name = action.label;
        newFormData.slice_id = state.viz.form_data.slice_id;
        newFormData.slice_name = state.viz.form_data.slice_name;
        newFormData.viz_type = state.viz.form_data.viz_type;
        newFormData.slices = state.viz.form_data.slices;
      }
      if (action.key === 'viz_type') {
        newFormData.previous_viz_type = state.viz.form_data.viz_type;
      }
      newFormData[action.key] = (action.value !== undefined)
        ? action.value : (!state.viz.form_data[action.key]);
      return Object.assign(
        {},
        state,
        { viz: Object.assign({}, state.viz, { form_data: newFormData }) }
      );
    },
    [actions.CHART_UPDATE_SUCCEEDED]() {
      const vizUpdates = {
        query: action.query,
      };
      return Object.assign(
        {},
        state,
        {
          chartStatus: 'success',
          viz: Object.assign({}, state.viz, vizUpdates),
        });
    },
    [actions.CHART_UPDATE_STARTED]() {
      const chartUpdateStartTime = now();
      const form_data = Object.assign({}, state.viz.form_data);
      const datasource_type = state.datasource_type;
      const vizUpdates = {
        json_endpoint: getExploreUrl(form_data, datasource_type, 'json'),
        csv_endpoint: getExploreUrl(form_data, datasource_type, 'csv'),
        standalone_endpoint:
          getExploreUrl(form_data, datasource_type, 'standalone'),
      };
      return Object.assign({}, state,
        {
          chartStatus: 'loading',
          chartUpdateEndTime: null,
          chartUpdateStartTime,
          viz: Object.assign({}, state.viz, vizUpdates),
        });
    },
    [actions.CHART_UPDATE_FAILED]() {
      const chartUpdateEndTime = now();
      return Object.assign({}, state,
        { chartStatus: 'failed', chartAlert: action.error, chartUpdateEndTime });
    },
    [actions.UPDATE_CHART_STATUS]() {
      const newState = Object.assign({}, state, { chartStatus: action.status });
      if (action.status === 'success' || action.status === 'failed') {
        newState.chartUpdateEndTime = now();
      }
      return newState;
    },
    [actions.REMOVE_CHART_ALERT]() {
      return Object.assign({}, state, { chartAlert: null });
    },
    [actions.SAVE_SLICE_FAILED]() {
      return Object.assign({}, state, { saveModalAlert: 'Failed to save slice' });
    },
    [actions.REMOVE_SAVE_MODAL_ALERT]() {
      return Object.assign({}, state, { saveModalAlert: null });
    },
  };
  if (action.type in actionHandlers) {
    return actionHandlers[action.type]();
  }
  return state;
};
