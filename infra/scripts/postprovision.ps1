$ErrorActionPreference = "Stop"

function Require-Env($name) {
  $value = [Environment]::GetEnvironmentVariable($name)
  if ([string]::IsNullOrWhiteSpace($value)) {
    throw "Required environment variable '$name' was not provided by azd."
  }
  return $value
}

function Az-Json($args) {
  $out = az @args --only-show-errors -o json
  if ([string]::IsNullOrWhiteSpace($out)) {
    return $null
  }
  return $out | ConvertFrom-Json
}

function Ensure-GraphAppRole($principalId, $roleValue) {
  $graphAppId = "00000003-0000-0000-c000-000000000000"
  $graphSp = Az-Json @("ad", "sp", "list", "--filter", "appId eq '$graphAppId'")
  if (-not $graphSp -or $graphSp.Count -eq 0) {
    throw "Microsoft Graph service principal was not found in this tenant."
  }

  $resourceId = $graphSp[0].id
  $role = $graphSp[0].appRoles | Where-Object { $_.value -eq $roleValue -and $_.allowedMemberTypes -contains "Application" } | Select-Object -First 1
  if (-not $role) {
    throw "Microsoft Graph app role '$roleValue' was not found."
  }

  $existing = Az-Json @("rest", "--method", "GET", "--url", "https://graph.microsoft.com/v1.0/servicePrincipals/$principalId/appRoleAssignments")
  $alreadyAssigned = $false
  if ($existing -and $existing.value) {
    $alreadyAssigned = @($existing.value | Where-Object { $_.resourceId -eq $resourceId -and $_.appRoleId -eq $role.id }).Count -gt 0
  }

  if (-not $alreadyAssigned) {
    $body = @{
      principalId = $principalId
      resourceId = $resourceId
      appRoleId = $role.id
    } | ConvertTo-Json -Compress
    az rest --method POST --url "https://graph.microsoft.com/v1.0/servicePrincipals/$principalId/appRoleAssignments" --body $body --headers "Content-Type=application/json" --only-show-errors | Out-Null
    Write-Host "Assigned Microsoft Graph app role $roleValue to managed identity $principalId."
  }
}

$environmentName = Require-Env "AZURE_ENV_NAME"
$resourceGroup = Require-Env "AZURE_RESOURCE_GROUP"
$tenantId = Require-Env "AZURE_TENANT_ID"
$webAppName = Require-Env "TRUDY_WEB_APP_NAME"
$sqlServer = Require-Env "TRUDY_SQL_SERVER"
$sqlDatabase = Require-Env "TRUDY_SQL_DATABASE"
$webPrincipalId = Require-Env "TRUDY_WEB_IDENTITY_PRINCIPAL_ID"
$graphPrincipalId = Require-Env "TRUDY_GRAPH_IDENTITY_PRINCIPAL_ID"

$webIdentityName = "id-trudy-web-$environmentName"
$graphIdentityName = "id-trudy-graph-$environmentName"
$groupName = "trudy-web-users-$environmentName"
$authAppName = "trudy-web-auth-$environmentName"

$group = Az-Json @("ad", "group", "list", "--filter", "displayName eq '$groupName'")
if (-not $group -or $group.Count -eq 0) {
  $group = Az-Json @("ad", "group", "create", "--display-name", $groupName, "--mail-nickname", $groupName)
  Write-Host "Created Entra group $groupName. Add Trudy users to this group before opening the app."
} else {
  $group = $group[0]
}

$fqdn = az containerapp show --name $webAppName --resource-group $resourceGroup --query "properties.configuration.ingress.fqdn" -o tsv
if ([string]::IsNullOrWhiteSpace($fqdn)) {
  throw "Container App ingress FQDN was not available."
}
$redirectUri = "https://$fqdn/.auth/login/aad/callback"

$authApp = Az-Json @("ad", "app", "list", "--filter", "displayName eq '$authAppName'")
if (-not $authApp -or $authApp.Count -eq 0) {
  $authApp = Az-Json @("ad", "app", "create", "--display-name", $authAppName, "--sign-in-audience", "AzureADMyOrg", "--web-redirect-uris", $redirectUri, "--enable-id-token-issuance", "true")
  az ad sp create --id $authApp.appId --only-show-errors | Out-Null
} else {
  $authApp = $authApp[0]
  az ad app update --id $authApp.appId --web-redirect-uris $redirectUri --enable-id-token-issuance true --only-show-errors | Out-Null
}

$authSp = Az-Json @("ad", "sp", "list", "--filter", "appId eq '$($authApp.appId)'")
if (-not $authSp -or $authSp.Count -eq 0) {
  $authSp = Az-Json @("ad", "sp", "create", "--id", $authApp.appId)
} else {
  $authSp = $authSp[0]
}

az ad sp update --id $authSp.id --set appRoleAssignmentRequired=true --only-show-errors | Out-Null
$assignments = Az-Json @("rest", "--method", "GET", "--url", "https://graph.microsoft.com/v1.0/groups/$($group.id)/appRoleAssignments")
$hasGroupAssignment = $false
if ($assignments -and $assignments.value) {
  $hasGroupAssignment = @($assignments.value | Where-Object { $_.resourceId -eq $authSp.id }).Count -gt 0
}
if (-not $hasGroupAssignment) {
  $body = @{
    principalId = $group.id
    resourceId = $authSp.id
    appRoleId = "00000000-0000-0000-0000-000000000000"
  } | ConvertTo-Json -Compress
  az rest --method POST --url "https://graph.microsoft.com/v1.0/groups/$($group.id)/appRoleAssignments" --body $body --headers "Content-Type=application/json" --only-show-errors | Out-Null
}

$secret = az ad app credential reset --id $authApp.appId --display-name "container-app-auth" --query password -o tsv --only-show-errors
az containerapp auth microsoft update --name $webAppName --resource-group $resourceGroup --client-id $authApp.appId --client-secret $secret --tenant-id $tenantId --yes --only-show-errors | Out-Null
az containerapp auth update --name $webAppName --resource-group $resourceGroup --enabled true --unauthenticated-client-action RedirectToLoginPage --only-show-errors | Out-Null

foreach ($role in @("Application.Read.All", "Directory.Read.All", "AuditLog.Read.All", "Reports.Read.All", "Sites.Read.All", "Policy.Read.All")) {
  Ensure-GraphAppRole $graphPrincipalId $role
}

$env:TRUDY_DB_PROVIDER = "azure_sql"
$env:TRUDY_SQL_SERVER = $sqlServer
$env:TRUDY_SQL_DATABASE = $sqlDatabase
$env:TRUDY_WEB_IDENTITY_NAME = $webIdentityName
$env:TRUDY_GRAPH_IDENTITY_NAME = $graphIdentityName
python -m src.db.sql.bootstrap --web-identity-name $webIdentityName --graph-identity-name $graphIdentityName

Write-Host "Trudy post-provision configuration completed."
Write-Host "Private URL: https://$fqdn"
Write-Host "Web access group: $groupName"
