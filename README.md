# onboardingBot
Bot which aids in making onboarding a smoother process

This bot uses the concept of rule based learning, where pre defined input and repsonse types are fed to the bot. In best effort, the bot tries to answer based on the knowledge it is fed.

Requisites

1. slackclient
2. slack account where you are able to create and add apps
3. brew or any other package manager according to the distribution you are using


Concepts learned

1. API - Slack
2. NLP (as an extension to this project)


Note:

While running the script some issues were found and the fixes for those are also explained


1. While creating the slack app, ensure you use the classic way --> This is the version which allows RTM ie Real Time Messaging.

For instructions follow this link here: https://github.com/slackapi/python-slackclient/issues/609

2. While connecting to the slack bot created, it gives a SSL certificate error -- > Download the DigiCert Certificates and export it to environment variable where you will be running your master script.

wget https://www.tbs-certificats.com/issuerdata/DigiCertGlobalRootCA.crt

export WEBSOCKET_CLIENT_CA_BUNDLE=DigiCertGlobalRootCA.crt


