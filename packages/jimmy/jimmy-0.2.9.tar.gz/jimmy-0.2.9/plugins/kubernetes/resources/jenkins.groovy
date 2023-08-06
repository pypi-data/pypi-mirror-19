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
import net.sf.json.JSONObject
import org.csanchez.jenkins.plugins.kubernetes.ContainerEnvVar
import org.csanchez.jenkins.plugins.kubernetes.ContainerTemplate
import org.csanchez.jenkins.plugins.kubernetes.KubernetesCloud
import org.csanchez.jenkins.plugins.kubernetes.PodAnnotation
import org.csanchez.jenkins.plugins.kubernetes.PodEnvVar
import org.csanchez.jenkins.plugins.kubernetes.PodImagePullSecret
import org.csanchez.jenkins.plugins.kubernetes.PodTemplate
import org.csanchez.jenkins.plugins.kubernetes.volumes.ConfigMapVolume
import org.csanchez.jenkins.plugins.kubernetes.volumes.EmptyDirVolume
import org.csanchez.jenkins.plugins.kubernetes.volumes.HostPathVolume
import org.csanchez.jenkins.plugins.kubernetes.volumes.NfsVolume
import org.csanchez.jenkins.plugins.kubernetes.volumes.PersistentVolumeClaim
import org.csanchez.jenkins.plugins.kubernetes.volumes.PodVolume
import org.csanchez.jenkins.plugins.kubernetes.volumes.SecretVolume

class Actions {
  Actions(out) { this.out = out }
  def out

  static def kubeInput = '''
    ${cloud_config}
  '''

  public Map kubeParams = JSONObject.fromObject(kubeInput)

  private createContainerTemplate(Map containerParams) {
    // Container Env Variables
    ArrayList<ContainerEnvVar> envVars = new ArrayList<ContainerEnvVar>()
    for (Map vars : containerParams['env_vars'] ?: []) {
      ContainerEnvVar var = new ContainerEnvVar(vars['key'], vars['value'])
      envVars.add(var)
    }

    // Pod container template
    ContainerTemplate podContainer = new ContainerTemplate(
      containerParams['name'],
      containerParams['image'] ?: '',
      containerParams['command'] ?: '',
      containerParams['arguments'] ?: ''
    )

    podContainer.setTtyEnabled(containerParams['enable_tty'] ?: false)
    podContainer.setWorkingDir(containerParams['working_dir'] ?: '')
    podContainer.setPrivileged(containerParams['privileged'] ?: false)
    podContainer.setAlwaysPullImage(containerParams['always_pull_image'] ?: false)
    podContainer.setEnvVars(envVars)
    podContainer.setResourceRequestMemory(containerParams['request_memory'] ?: '')
    podContainer.setResourceLimitCpu(containerParams['limit_cpu'] ?: '')
    podContainer.setResourceLimitMemory(containerParams['limit_memory'] ?: '')
    podContainer.setResourceRequestCpu(containerParams['request_cpu'] ?: '')

    return podContainer
  }

  private createVolume(Map volumeParams, String type) {
    def volume
    switch (type) {
      case 'config_map':
        volume = new ConfigMapVolume(volumeParams['mount_path'], volumeParams['name'])
        break
      case 'empty_dir':
        volume = new EmptyDirVolume(volumeParams['mount_path'], volumeParams['in_memory'])
        break
      case 'host_path':
        volume = new HostPathVolume(volumeParams['host_path'], volumeParams['mount_path'])
        break
      case 'nfs':
        volume = new NfsVolume(
          volumeParams['server_adress'],
          volumeParams['server_path'],
          volumeParams['read_only'],
          volumeParams['mount_path']
        )
        break
      case 'persistent_claim':
        volume = new PersistentVolumeClaim(
          volumeParams['mount_path'],
          volumeParams['claim_name'],
          volumeParams['read_only']
        )
        break
      case 'secret':
        volume = new SecretVolume(volumeParams['mount_path'], volumeParams['secret_name'])
        break
    }

    return volume
  }


  private createPodTemplate(Map podParams) {
    // add Container templates
    ArrayList<ContainerTemplate> containers = new ArrayList<ContainerTemplate>()
    for (Map container : podParams['containers'] ?: []) {
      containers.add(createContainerTemplate(container))
    }

    // add ImagePullSecrets
    ArrayList<PodImagePullSecret> listImagePullSecrets = new ArrayList<PodImagePullSecret>()
    for (String imageName : podParams['image_pull_secrets'] ?: []) {
      PodImagePullSecret imagePullSecrets = new PodImagePullSecret(imageName)
      listImagePullSecrets.add(imagePullSecrets)
    }

    // add Annotations
    ArrayList<PodAnnotation> podAnnotations = new ArrayList<PodAnnotation>()
    for (Map podAnnotation : podParams['annotations'] ?: []) {
      PodAnnotation annotation = new PodAnnotation(podAnnotation['key'], podAnnotation['value'])
      podAnnotations.add(annotation)
    }

    // add Env Variables
    ArrayList<PodEnvVar> podEnvVars = new ArrayList<PodEnvVar>()
    for (Map vars : podParams['env_vars'] ?: []) {
      PodEnvVar var = new PodEnvVar(vars['key'], vars['value'])
      podEnvVars.add(var)
    }

    // add Volumes
    ArrayList<PodVolume> podVolumes = new ArrayList<PodVolume>()
    def volumeTypes = ['config_map', 'empty_dir', 'host_path', 'nfs', 'persistent_claim', 'secret']
    def volumes = podParams['volumes'] ?: []
    for (String volumeType : volumeTypes) {
      for (Map volume : volumes[volumeType] ?: []) {
        podVolumes.add(createVolume(volume, volumeType))
      }
    }

    // create PodTemplate object
    PodTemplate kubePod = new PodTemplate()

    kubePod.setName(podParams['name'])
    kubePod.setLabel(podParams['labels'] ?: '')
    kubePod.setInheritFrom(podParams['inherit_from'] ?: '')
    kubePod.setNodeSelector(podParams['node_selector'] ?: '')
    kubePod.setVolumes(podVolumes)
    kubePod.setEnvVars(podEnvVars)
    kubePod.setServiceAccount(podParams['service_account'] ?: '')
    kubePod.setInstanceCap(podParams['instance_cap'] ?: Integer.MAX_VALUE)
    kubePod.setIdleMinutes(podParams['idle_minutes'] ?: 0)
    kubePod.setContainers(containers)
    kubePod.setAnnotations(podAnnotations)
    kubePod.setImagePullSecrets(listImagePullSecrets)

    return kubePod
  }

  public setKubernetesConfig(Map kubeParams) {
    // process Pod Templates
    ArrayList<PodTemplate> podTemplates = new ArrayList<PodTemplate>()
    for (Map podTemplate : kubeParams['pod_templates'] ?: []) {
      podTemplates.add(createPodTemplate(podTemplate))
    }

    // create KubernetesCloud
    KubernetesCloud cloudConfig = new KubernetesCloud(
      kubeParams['id']
    )

    cloudConfig.setTemplates(podTemplates)
    cloudConfig.setServerUrl(kubeParams['server_url'])
    cloudConfig.setNamespace(kubeParams['namespace'] ?: '')
    cloudConfig.setJenkinsUrl(kubeParams['jenkins_url'] ?: '')
    cloudConfig.setContainerCapStr(String.valueOf(kubeParams['container_cap'] ?: Integer.MAX_VALUE))
    cloudConfig.setConnectTimeout(kubeParams['connection_timeout'] ?: 5)
    cloudConfig.setRetentionTimeout(kubeParams['container_cleanup_timeout'] ?: 5)
    cloudConfig.setReadTimeout(kubeParams['read_timeout'] ?: 15)
    cloudConfig.setServerCertificate(kubeParams['server_certificate'] ?: '')
    cloudConfig.setCredentialsId(kubeParams['credentials_id'] ?: '')
    cloudConfig.setJenkinsTunnel(kubeParams['jenkins_tunnel'] ?: '')
    cloudConfig.setSkipTlsVerify(kubeParams['disable_certificate_check'] ?: false)

    def instance = Jenkins.getInstance()
    def clouds = instance.clouds ?: []

    for (KubernetesCloud cloud : clouds) {
      if (cloud.getDisplayName() == kubeParams['id']) {
        clouds = clouds.minus(cloud)
      }
    }

    clouds = clouds.plus(cloudConfig)

    instance.clouds.replaceBy(clouds)
    instance.save()

  }
}

///////////////////////////////////////////////////////////////////////////////
// CLI Argument Processing
///////////////////////////////////////////////////////////////////////////////

actions = new Actions(out)
actions.setKubernetesConfig(actions.kubeParams)
