import {Card, Button} from 'react-bootstrap';
import React from 'react';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faQuestionCircle} from '@fortawesome/free-solid-svg-icons';

import {getObjectFromRegistryByRef} from './JsonSchemaHelpers';
import WarningIcon from './WarningIcon';

const WarningType = {
  NONE: 0,
  SINGLE: 1,
  MULTIPLE: 2
}

function getDefaultPaneParams(refString, registry, isUnsafeOptionSelected) {
  let configSection = getObjectFromRegistryByRef(refString, registry);
  return (
    {
      title: configSection.title,
      content: configSection.description,
      warningType: isUnsafeOptionSelected ? WarningType.Multiple : WarningType.NONE
    });
}

function InfoPane(props) {
  return (
    <Card className={'info-pane'}>
      {getTitle(props)}
      {getSubtitle(props)}
      {getBody(props)}
    </Card>);
}

function getTitle(props) {
  if (typeof (props.title) == 'string') {
    return (
      <Card.Title className={'pane-title'}>
        {props.title}
        {getLinkButton(props)}
      </Card.Title>)
  }
}

function getLinkButton(props) {
  if (typeof (props.link) == 'string') {
    return (
      <Button variant={'link'} className={'pane-link'} href={props.link} target={'_blank'}>
        <FontAwesomeIcon icon={faQuestionCircle}/>
      </Button>)
  }
}

function getSubtitle(props) {
  if (typeof (props.subtitle) == 'string') {
    return (
      <Card.Subtitle className={'pane-subtitle'}>
        {props.subtitle}
      </Card.Subtitle>)
  }
}

function getBody(props) {
  return (
    <Card.Body className={'pane-body'}>
      <span key={'body'}>{props.body}</span>
      {props.warningType !== WarningType.NONE && getWarning(props.warningType)}
    </Card.Body>
  )
}

function getWarning(warningType) {
  return (
    <div className={'info-pane-warning'} key={'warning'}>
      <WarningIcon/>{warningType === WarningType.SINGLE ? getSingleOptionWarning() : getMultipleOptionsWarning()}
    </div>
  );
}

function getSingleOptionWarning() {
  return (
    <span>This option may cause a system to become unstable or
    may change a system's state in undesirable ways. Therefore, this option
    is not recommended for use in production or other sensitive
    environments.</span>
  );
}

function getMultipleOptionsWarning() {
  return (
    <span>Some options have been selected that may cause a system
    to become unstable or may change a system's state in undesirable ways.
    Running Infection Monkey in a production or other sensitive environment
    with this configuration is not recommended.</span>
  );
}

export {getDefaultPaneParams, InfoPane, WarningType}
