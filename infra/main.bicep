targetScope = 'resourceGroup'

param environmentName string
param location string = resourceGroup().location
param tenantId string
param sqlAdminObjectId string
param sqlAdminLogin string
@allowed([
  'User'
  'Group'
  'Application'
])
param sqlAdminPrincipalType string = 'User'
param containerImage string

var normalized = toLower(replace(environmentName, '-', ''))
var suffix = uniqueString(resourceGroup().id, environmentName)
var appName = 'ca-trudy-${environmentName}'
var jobName = 'caj-trudy-graph-${environmentName}'
var envName = 'cae-trudy-${environmentName}'
var logName = 'log-trudy-${environmentName}'
var acrName = take('acrtrudy${normalized}${suffix}', 50)
var keyVaultName = take('kv-trudy-${normalized}-${suffix}', 24)
var sqlServerName = take('sql-trudy-${normalized}-${suffix}', 63)
var sqlDatabaseName = 'sqldb-trudy'
var vnetName = 'vnet-trudy-${environmentName}'
var appSubnetName = 'snet-containerapps'
var privateEndpointSubnetName = 'snet-private-endpoints'
var webIdentityName = 'id-trudy-web-${environmentName}'
var graphIdentityName = 'id-trudy-graph-${environmentName}'

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: logName
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

resource vnet 'Microsoft.Network/virtualNetworks@2023-11-01' = {
  name: vnetName
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.42.0.0/16'
      ]
    }
    subnets: [
      {
        name: appSubnetName
        properties: {
          addressPrefix: '10.42.0.0/23'
          delegations: [
            {
              name: 'containerapps'
              properties: {
                serviceName: 'Microsoft.App/environments'
              }
            }
          ]
        }
      }
      {
        name: privateEndpointSubnetName
        properties: {
          addressPrefix: '10.42.2.0/24'
          privateEndpointNetworkPolicies: 'Disabled'
        }
      }
    ]
  }
}

resource appSubnet 'Microsoft.Network/virtualNetworks/subnets@2023-11-01' existing = {
  parent: vnet
  name: appSubnetName
}

resource privateEndpointSubnet 'Microsoft.Network/virtualNetworks/subnets@2023-11-01' existing = {
  parent: vnet
  name: privateEndpointSubnetName
}

resource acr 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: acrName
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: false
    publicNetworkAccess: 'Enabled'
  }
}

resource webIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: webIdentityName
  location: location
}

resource graphIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: graphIdentityName
  location: location
}

resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: keyVaultName
  location: location
  properties: {
    tenantId: tenantId
    sku: {
      family: 'A'
      name: 'standard'
    }
    enableRbacAuthorization: true
    enabledForDeployment: false
    enabledForDiskEncryption: false
    enabledForTemplateDeployment: false
  }
}

resource sqlServer 'Microsoft.Sql/servers@2023-08-01-preview' = {
  name: sqlServerName
  location: location
  properties: {
    publicNetworkAccess: 'Disabled'
    minimalTlsVersion: '1.2'
    administrators: {
      administratorType: 'ActiveDirectory'
      principalType: sqlAdminPrincipalType
      login: sqlAdminLogin
      sid: sqlAdminObjectId
      tenantId: tenantId
      azureADOnlyAuthentication: true
    }
  }
}

resource sqlDatabase 'Microsoft.Sql/servers/databases@2023-08-01-preview' = {
  parent: sqlServer
  name: sqlDatabaseName
  location: location
  sku: {
    name: 'Basic'
    tier: 'Basic'
  }
  properties: {
    collation: 'SQL_Latin1_General_CP1_CI_AS'
    maxSizeBytes: 2147483648
  }
}

resource sqlPrivateDns 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: 'privatelink.database.windows.net'
  location: 'global'
}

resource sqlPrivateDnsLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = {
  parent: sqlPrivateDns
  name: 'link-${vnet.name}'
  location: 'global'
  properties: {
    registrationEnabled: false
    virtualNetwork: {
      id: vnet.id
    }
  }
}

resource sqlPrivateEndpoint 'Microsoft.Network/privateEndpoints@2023-11-01' = {
  name: 'pe-${sqlServer.name}'
  location: location
  properties: {
    subnet: {
      id: privateEndpointSubnet.id
    }
    privateLinkServiceConnections: [
      {
        name: 'sql'
        properties: {
          privateLinkServiceId: sqlServer.id
          groupIds: [
            'sqlServer'
          ]
        }
      }
    ]
  }
}

resource sqlPrivateDnsZoneGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2023-11-01' = {
  parent: sqlPrivateEndpoint
  name: 'default'
  properties: {
    privateDnsZoneConfigs: [
      {
        name: 'sql'
        properties: {
          privateDnsZoneId: sqlPrivateDns.id
        }
      }
    ]
  }
}

resource containerEnv 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: envName
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.listKeys().primarySharedKey
      }
    }
    vnetConfiguration: {
      infrastructureSubnetId: appSubnet.id
      internal: true
    }
    workloadProfiles: [
      {
        name: 'Consumption'
        workloadProfileType: 'Consumption'
      }
    ]
  }
}

resource webAcrPull 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(acr.id, webIdentity.id, 'AcrPull')
  scope: acr
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')
    principalId: webIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource graphAcrPull 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(acr.id, graphIdentity.id, 'AcrPull')
  scope: acr
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')
    principalId: graphIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource webApp 'Microsoft.App/containerApps@2024-03-01' = {
  name: appName
  location: location
  tags: {
    'azd-service-name': 'web'
  }
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${webIdentity.id}': {}
    }
  }
  properties: {
    managedEnvironmentId: containerEnv.id
    configuration: {
      activeRevisionsMode: 'Single'
      ingress: {
        external: false
        targetPort: 8501
        transport: 'http'
        allowInsecure: false
      }
      registries: [
        {
          server: acr.properties.loginServer
          identity: webIdentity.id
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'web'
          image: containerImage
          env: [
            {
              name: 'TRUDY_DB_PROVIDER'
              value: 'azure_sql'
            }
            {
              name: 'TRUDY_SQL_SERVER'
              value: '${sqlServer.name}.database.windows.net'
            }
            {
              name: 'TRUDY_SQL_DATABASE'
              value: sqlDatabase.name
            }
            {
              name: 'AZURE_CLIENT_ID'
              value: webIdentity.properties.clientId
            }
          ]
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 3
      }
    }
  }
  dependsOn: [
    webAcrPull
    sqlPrivateDnsZoneGroup
  ]
}

resource graphJob 'Microsoft.App/jobs@2024-03-01' = {
  name: jobName
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${graphIdentity.id}': {}
    }
  }
  properties: {
    environmentId: containerEnv.id
    configuration: {
      triggerType: 'Schedule'
      replicaTimeout: 1800
      replicaRetryLimit: 1
      scheduleTriggerConfig: {
        cronExpression: '0 2 * * *'
        parallelism: 1
        replicaCompletionCount: 1
      }
      registries: [
        {
          server: acr.properties.loginServer
          identity: graphIdentity.id
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'graph-ingest'
          image: containerImage
          command: [
            'python'
            '-m'
            'src.graph.ingest'
          ]
          env: [
            {
              name: 'TRUDY_DB_PROVIDER'
              value: 'azure_sql'
            }
            {
              name: 'TRUDY_SQL_SERVER'
              value: '${sqlServer.name}.database.windows.net'
            }
            {
              name: 'TRUDY_SQL_DATABASE'
              value: sqlDatabase.name
            }
            {
              name: 'AZURE_CLIENT_ID'
              value: graphIdentity.properties.clientId
            }
          ]
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
        }
      ]
    }
  }
  dependsOn: [
    graphAcrPull
    sqlPrivateDnsZoneGroup
  ]
}

output AZURE_CONTAINER_REGISTRY_ENDPOINT string = acr.properties.loginServer
output TRUDY_WEB_APP_NAME string = webApp.name
output TRUDY_GRAPH_JOB_NAME string = graphJob.name
output TRUDY_CONTAINER_ENV_NAME string = containerEnv.name
output TRUDY_SQL_SERVER string = '${sqlServer.name}.database.windows.net'
output TRUDY_SQL_DATABASE string = sqlDatabase.name
output TRUDY_WEB_IDENTITY_CLIENT_ID string = webIdentity.properties.clientId
output TRUDY_WEB_IDENTITY_PRINCIPAL_ID string = webIdentity.properties.principalId
output TRUDY_GRAPH_IDENTITY_CLIENT_ID string = graphIdentity.properties.clientId
output TRUDY_GRAPH_IDENTITY_PRINCIPAL_ID string = graphIdentity.properties.principalId
