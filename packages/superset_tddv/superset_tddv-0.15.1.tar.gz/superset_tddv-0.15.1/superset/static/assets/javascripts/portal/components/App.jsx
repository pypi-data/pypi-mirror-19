const $ = window.$ = require('jquery');
import * as Actions from '../actions';
import React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import Alerts from './Alerts';

class App extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      hash: window.location.hash,
      contentHeight: this.getHeight(),
    };
  }

  getHeight() {
    const navHeight = 90;
    const headerHeight = $('.nav-tabs').outerHeight() ?
      $('.nav-tabs').outerHeight() : $('#search-header').outerHeight();
    const warningHeight = $('#navbar-warning').outerHeight();
    const alertHeight = $('#sqllab-alerts').outerHeight();
    return `${window.innerHeight - navHeight - headerHeight - warningHeight - alertHeight}px`;
  }
  handleResize() {
    this.setState({ contentHeight: this.getHeight() });
  }
  onHashChanged() {
    this.setState({ hash: window.location.hash });
  }
  render() {

    return (
      <div className="App SqlLab">
        <Alerts id="sqllab-alerts" alerts={this.props.alerts} actions={this.props.actions} />
        <div className="container-fluid" height={this.state.contentHeight}>
          hello world, this is my portal!
        </div>
      </div>
    );
  }
}

App.propTypes = {
  alerts: React.PropTypes.array,
  actions: React.PropTypes.object,
};

function mapStateToProps(state) {
  return {
    alerts: state.alerts,
  };
}
function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(Actions, dispatch),
  };
}

export { App };
export default connect(mapStateToProps, mapDispatchToProps)(App);
