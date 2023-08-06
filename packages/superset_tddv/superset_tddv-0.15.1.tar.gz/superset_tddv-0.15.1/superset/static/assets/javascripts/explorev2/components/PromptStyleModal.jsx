/* eslint camel-case: 0 */
import React from 'react';
import { Modal } from 'react-bootstrap';
import { connect } from 'react-redux';
import PromptBaseStyle from './PromptBaseStyle';

const propTypes = {
  onHide: React.PropTypes.func.isRequired,
  actions: React.PropTypes.object.isRequired,
  form_data: React.PropTypes.object.isRequired,
  promptColStyles: React.PropTypes.array.isRequired,
};

const defaultProps = {
  promptColStyles: [],
};

class PromptStyleModal extends React.Component {
  render() {
    return (
      <Modal
        show
        onHide={this.props.onHide}
        bsStyle="large"
      >
        <Modal.Header closeButton>
          <Modal.Title>
            <div>
               基本设置
            </div>
          </Modal.Title>
        </Modal.Header>
        <Modal.Body style={{ minHeight: '300px' }}>
          <div>
            <PromptBaseStyle
              actions={this.props.actions}
              form_data={this.props.form_data}
              promptColStyles={this.props.promptColStyles}
            />
          </div>
        </Modal.Body>
        <Modal.Footer>
        </Modal.Footer>
      </Modal>
    );
  }
}

PromptStyleModal.propTypes = propTypes;
PromptStyleModal.defaultProps = defaultProps;

function mapStateToProps(state) {
  return {
    promptColStyles: state.viz.form_data.promptColStyles,
  };
}

export { PromptStyleModal };
export default connect(mapStateToProps, () => ({}))(PromptStyleModal);
