import React from 'react';
import CollapsibleWellComponent from '../CollapsibleWell';
import {generateInfoBadges} from './utils';

export function sharedPasswordsIssueOverview() {
   return (<li key={'shared_passwords'}>Multiple users have the same password</li>)
}

export function sharedAdminsDomainIssueOverview() {
   return (<li key={'admin_domains'}>Shared local administrator account - Different machines have the same account as a local
                      administrator.</li>)
}

export function sharedCredsDomainIssueReport(issue) {
    return (
      <>
        Some domain users are sharing passwords, this should be fixed by changing passwords.
        <CollapsibleWellComponent>
          These users are sharing access password:
          {generateInfoBadges(issue.shared_with)}.
        </CollapsibleWellComponent>
      </>
    );
  }

export function sharedCredsIssueReport(issue) {
    return (
      <>
        Some users are sharing passwords, this should be fixed by changing passwords.
        <CollapsibleWellComponent>
          These users are sharing access password:
          {generateInfoBadges(issue.shared_with)}.
        </CollapsibleWellComponent>
      </>
    );
  }

export function sharedLocalAdminsIssueReport(issue) {
    return (
      <>
        Make sure the right administrator accounts are managing the right machines, and that there isn’t an
        unintentional local
        admin sharing.
        <CollapsibleWellComponent>
          Here is a list of machines which the account <span
          className="badge badge-primary">{issue.username}</span> is defined as an administrator:
          {generateInfoBadges(issue.shared_machines)}
        </CollapsibleWellComponent>
      </>
    );
  }
