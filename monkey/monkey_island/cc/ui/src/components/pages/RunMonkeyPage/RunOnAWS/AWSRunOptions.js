import React, {useEffect, useState} from 'react';
import {Button, Nav} from 'react-bootstrap';

import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faSync} from '@fortawesome/free-solid-svg-icons/faSync';
import {faInfoCircle} from '@fortawesome/free-solid-svg-icons/faInfoCircle';
import AwsRunTable from './AWSInstanceTable';
import AuthComponent from '../../../AuthComponent';
import InlineSelection from '../../../ui-components/inline-selection/InlineSelection';


const AWSRunOptions = (props) => {
  return InlineSelection(getContents, {
    ...props,
    onBackButtonClick: () => {props.setComponent()}
  })
}


const getContents = (props) => {

  const authComponent = new AuthComponent({});

  let [allIPs, setAllIPs] = useState([]);
  let [selectedIp, setSelectedIp] = useState(null);
  let [AWSClicked, setAWSClicked] = useState(false);
  let [runResults, setRunResults] = useState([]);
  let [selectedInstances, setSelectedInstances] = useState([]);

  useEffect(() => {
    getIps();
  }, []);

  function getIps() {
    authComponent.authFetch('/api')
      .then(res => res.json())
      .then(res => {
        setAllIPs(res['ip_addresses']);
        setSelectedIp(res['ip_addresses'][0]);
      });
  }

  function runOnAws() {
    setAWSClicked(true);
    let instances = selectedInstances.map(x => instanceIdToInstance(x));

    authComponent.authFetch('/api/remote-monkey',
      {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({type: 'aws', instances: instances, island_ip: selectedIp})
      }).then(res => res.json())
      .then(res => {
        let result = res['result'];

        // update existing state, not run-over
        let prevRes = result;
        for (let key in result) {
          if (Object.prototype.hasOwnProperty.call(result, key)) {
            prevRes[key] = result[key];
          }
        }
        setRunResults(prevRes);
        setSelectedInstances([]);
        setAWSClicked(false);
      });
  }

  function instanceIdToInstance(instance_id) {
    let instance = props.AWSInstances.find(
      function (inst) {
        return inst['instance_id'] === instance_id;
      });

    return {'instance_id': instance_id, 'os': instance['os']}
  }

  return (
    <div style={{'marginBottom': '2em'}}>
      <div style={{'marginTop': '1em', 'marginBottom': '1em'}}>
        <p className="alert alert-info">
          <FontAwesomeIcon icon={faInfoCircle} style={{'marginRight': '5px'}}/>
          Not sure what this is? Not seeing your AWS EC2 instances? <a
          href="https://www.guardicore.com/infectionmonkey/docs/usage/integrations/aws-run-on-ec2-machine/"
          rel="noopener noreferrer" target="_blank">Read the documentation</a>!
        </p>
      </div>
      {
        allIPs.length > 1 ?
          <Nav variant="pills" activeKey={selectedIp} onSelect={setSelectedIp}
               style={{'marginBottom': '2em'}}>
            {allIPs.map(ip => <Nav.Item key={ip}><Nav.Link eventKey={ip}>{ip}</Nav.Link></Nav.Item>)}
          </Nav>
          : <div style={{'marginBottom': '2em'}}/>
      }
      <AwsRunTable
        data={props.AWSInstances}
        results={runResults}
        selection={selectedInstances}
        setSelection={setSelectedInstances}
      />
      <div className={'aws-run-button-container'}>
        <Button
          size={'lg'}
          onClick={runOnAws}
          className={'btn btn-default btn-md center-block'}
          disabled={AWSClicked}>
          Run on selected machines
          {AWSClicked ?
            <FontAwesomeIcon icon={faSync} className={`text-success spinning-icon`} style={{'marginLeft': '5px'}}/> : null}
        </Button>
      </div>
    </div>
  );
}

export default AWSRunOptions;
