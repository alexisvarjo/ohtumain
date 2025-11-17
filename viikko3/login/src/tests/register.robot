*** Settings ***
Resource          resource.robot
Suite Setup       Open And Configure Browser
Suite Teardown    Close Browser
Test Setup        Reset Application Create User And Go To Register Page

*** Test Cases ***
Register With Valid Username And Password
    Input Text     username     pekka
    Input Text     password     salainen1
    Input Text     password_confirmation    salainen1
    Click Button   Register
    Title Should Be    Welcome to Ohtu Application!

Register With Too Short Username And Valid Password
    Input Text     username     ab
    Input Text     password     salasana1
    Input Text     password_confirmation    salasana1
    Click Button   Register
    Page Should Contain   Käyttäjätunnuksen tulee olla vähintään 3 merkkiä pitkä

Register With Valid Username And Too Short Password
    Input Text     username     mikko
    Input Text     password     abcd12
    Input Text     password_confirmation    abcd12
    Click Button   Register
    Page Should Contain   Salasanan tulee olla vähintään 8 merkkiä pitkä

Register With Valid Username And Invalid Password
    # password contains only letters
    Input Text     username     laura
    Input Text     password     pelkkiäkirjaimia
    Input Text     password_confirmation    pelkkiäkirjaimia
    Click Button   Register
    Page Should Contain   Salasana ei saa koostua pelkästään kirjaimista

Register With Nonmatching Password And Password Confirmation
    Input Text     username     niko
    Input Text     password     salasana1
    Input Text     password_confirmation    salasana2
    Click Button   Register
    Page Should Contain   Salasanat eivät täsmää

Register With Username That Is Already In Use
    # user "existing" is created in Test Setup by AppLibrary
    Input Text     username     existing
    Input Text     password     vahva123
    Input Text     password_confirmation    vahva123
    Click Button   Register
    Page Should Contain   Käyttäjätunnus on jo käytössä

*** Keywords ***
Reset Application Create User And Go To Register Page
    Reset Application
    Create User   existing   VeryStrong1
    Go To   ${REGISTER_URL}
