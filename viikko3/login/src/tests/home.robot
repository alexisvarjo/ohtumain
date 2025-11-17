*** Settings ***
Resource          resource.robot
Suite Setup       Open And Configure Browser
Suite Teardown    Close Browser
Test Setup        Reset Application And Go To Starting Page

*** Test Cases ***
Click Login Link
    Click Link  Login
    Login Page Should Be Open

Click Register Link
    Click Link  Register new user
    Register Page Should Be Open

*** Keywords ***
Reset Application And Go To Starting Page
    Reset Application
    Wait Until Keyword Succeeds  5s  0.2s  Home Page Should Be Open
    Go To Starting Page

Home Page Should Be Open
    Go To  ${HOME_URL}
    Title Should Be  Ohtu Application

Register Page Should Be Open
    Go To  ${REGISTER_URL}
    Title Should Be  Register
