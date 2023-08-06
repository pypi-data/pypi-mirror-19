/*
*  Copyright 2017 Mirantis, Inc.
*
*  Licensed under the Apache License, Version 2.0 (the "License"); you may
*  not use this file except in compliance with the License. You may obtain
*  a copy of the License at
*
*       http://www.apache.org/licenses/LICENSE-2.0
*
*  Unless required by applicable law or agreed to in writing, software
*  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
*  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
*  License for the specific language governing permissions and limitations
*  under the License.
*/

import jenkins.model.Jenkins
import com.cloudbees.plugins.credentials.CredentialsProvider
import com.cloudbees.plugins.credentials.CredentialsScope
import com.cloudbees.plugins.credentials.domains.Domain
import org.csanchez.jenkins.plugins.kubernetes.ServiceAccountCredential

class Actions {
  Actions(out) { this.out = out }
  def out

  void updateCredentials(String scope,
                         String id,
                         String description="") {

    def globalDomain = Domain.global()
    def credentialsStore =
      Jenkins.instance.getExtensionList(
        'com.cloudbees.plugins.credentials.SystemCredentialsProvider'
      )[0].getStore()

    def credsScope
    if (scope == "global") {
      credsScope = CredentialsScope.GLOBAL
    } else if (scope == "system") {
      credsScope = CredentialsScope.SYSTEM
    }

    // Create or update the credentials in the Jenkins instance
    def availableCredentials = CredentialsProvider.lookupCredentials(ServiceAccountCredential.class,
                                                                    Jenkins.getInstance())
    def existingCredentials

    ServiceAccountCredential credentials = new ServiceAccountCredential(credsScope, id, description)

    for (ServiceAccountCredential cred : availableCredentials) {
      if (cred.id == id) {
        existingCredentials = cred
      }
    }


    if(existingCredentials != null) {
      credentialsStore.updateCredentials(
        globalDomain,
        existingCredentials,
        credentials
      )
    } else {
      credentialsStore.addCredentials(globalDomain, credentials)
    }
  }
}

///////////////////////////////////////////////////////////////////////////////
// CLI Argument Processing
///////////////////////////////////////////////////////////////////////////////

actions = new Actions(out)
action = args[0]
if (args.length < 2) {
  actions."$action"()
} else {
  actions."$action"(*args[1..-1])
}
