'=================================================================================

Set Shell = WScript.CreateObject("WScript.Shell")

Set fwPolicy2 = CreateObject("HNetCfg.FwPolicy2")

'=================================================================================

ruleExists = False

' Check if rule already exists
For Each rule In fwPolicy2.Rules
    If rule.Name = "Plex Media Server" Then
        ruleExists = True
        Exit For
    End If
Next

'=================================================================================

If Not ruleExists Then

    ' Create new inbound rule
    Set newRule = CreateObject("HNetCfg.FwRule")

    newRule.Name = "Plex Media Server"
    newRule.Protocol = 6 'TCP
    newRule.LocalPorts = 32400
    newRule.Direction = 1 'Inbound
    newRule.Action = 1 'Allow
    newRule.Enabled = True

    fwPolicy2.Rules.Add newRule

End If

'=================================================================================

Shell.CurrentDirectory = "C:/Program Files/Plex/Plex Media Server/"

Shell.run """Plex Media Server.exe""", 0, 0

'=================================================================================