import React from 'react';
// import { Tab, Row, Col, Nav, NavItem } from 'react-bootstrap';
import Select from 'react-select';
import { Button } from 'react-bootstrap';

const propTypes = {
  actions: React.PropTypes.object.isRequired,
  form_data: React.PropTypes.object.isRequired,
  promptColStyle: React.PropTypes.object.isRequired,
};

export default class PromptColStyle extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      fieldChoices: this.props.form_data.groupby,
      multiChoices: [
        { key: 'false', value: 'false' },
        { key: 'true', value: 'true' },
      ],
    };
  }
  changeField(promptColStyle, col) {
    const val = (col) ? col.value : null;
    this.props.actions.changePromptColStyle(promptColStyle, 'field', val);
  }
  changeWidth(promptColStyle, event) {
    this.props.actions.changePromptColStyle(promptColStyle, 'width', event.target.value);
  }
  changeMulti(promptColStyle, col) {
    const val = (col) ? col.value : null;
    this.props.actions.changePromptColStyle(promptColStyle, 'multi', val);
  }
  removeColStyle(promptColStyle) {
    this.props.actions.removePromptColStyle(promptColStyle);
  }
  render() {
    return (
      <div>
        <div className="row space-1">
          <Select
            className="col-lg-6"
            multi={false}
            name="select-column"
            placeholder="字段"
            options={this.state.fieldChoices.map((o) => ({ value: o, label: o }))}
            value={this.props.promptColStyle.field}
            autosize={false}
            onChange={this.changeField.bind(this, this.props.promptColStyle)}
          />
          <div className="col-lg-6">
            <input
              type="text"
              onChange={this.changeWidth.bind(this, this.props.promptColStyle)}
              value={this.props.promptColStyle.width}
              className="form-control input-sm"
              placeholder="长度"
            />
          </div>
        </div>
        <div className="row space-1" style={{ marginTop: '5px' }}>
          <Select
            className="col-lg-6"
            multi={false}
            name="select-column"
            placeholder="单选/多选"
            options={this.state.multiChoices.map((o) => ({ value: o.value, label: o.key }))}
            value={this.props.promptColStyle.multi}
            autosize={false}
            onChange={this.changeMulti.bind(this, this.props.promptColStyle)}
          />
          <div className="col-lg-1">
            <Button
              id="remove-button"
              bsSize="small"
              onClick={this.removeColStyle.bind(this, this.props.promptColStyle)}
            >
              <i className="fa fa-minus" />
            </Button>
          </div>
        </div>
      </div>
    );
  }
}

PromptColStyle.propTypes = propTypes;
