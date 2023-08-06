*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py

Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${site_setup}  ${PLONE_URL}/@@overview-controlpanel
${blueline_configlet}  ${PLONE_URL}/@@blueline-settings
${diazo_configlet}  ${PLONE_URL}/@@theming-controlpanel
${show_authenticated_locator}  css=#form-widgets-show_authenticated-0
${header_locator}  css=#form-widgets-header
${script}  <script>document.write('Hello' + ' ' + 'World!')</script>
${message}  Hello World!

*** Keywords ***

Goto Blueline Configlet
    Go to  ${blueline_configlet}
    Page Should Contain  Blueline

Goto Diazo Configlet
    Go to  ${diazo_configlet}
    Page Should Contain  Theme settings

Populate Viewlet
    Goto Blueline Configlet
    Input Text  ${header_locator}  ${script}
    Click Button  Save

Enable Show to Authenticated
    Goto Blueline Configlet
    Select Checkbox  ${show_authenticated_locator}
    Click Button  Save

*** Test cases ***

Test Configlet
    Enable Autologin as  Manager
    Go to  ${site_setup}
    Page Should Contain  Blueline

Test Viewlets as Authenticated
    Enable Autologin as  Manager
    Populate Viewlet

    # viewlet code should not be visible to authenticated users by default
    Go to Homepage
    Page Should Not Contain  ${message}

    # make it visible
    Enable Show to Authenticated
    Go to Homepage
    Page Should Contain  ${message}

    # viewlets should not be visible in the context of some configlets
    Goto Blueline Configlet
    Page Should Not Contain  ${message}
    Goto Diazo Configlet
    Page Should Not Contain  ${message}

Test Viewlets as Anonymous
    Enable Autologin as  Manager
    Populate Viewlet
    Disable Autologin
    Go to Homepage
    Page Should Contain  ${message}
