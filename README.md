# Overview

A hyperlocalised and interconnected grievances addressal system contains a web app that uses AI and ML,inorder to list out the local problems faced by the residents through satellite imaging and detection. 
This is a community based app that points out major problems in a locality and reports it to the local authority based on the number votes the problem has gained from the localites. The reported problem is then 
processed by the authorities who takes further actions. SevaSethu also include features like traffic analysis,air quality monitoring etc., to check the quality of living at a particular place. It also includes a feature
which allows the users to rate the actions taken for the reported problems. The user can also send feedbacks and report problems manually by uploading images.

# Dependencies

The front end for the web app has been built using Flutterflow.Supabase is the relational database management system. In the backend, Azure functions have been used for api calls and https triggers. The satellite images have been obtained through mapbox api which is sent to gemini-pro-vision for detection. Traffic analysis is carried using Mapbox api and Air quality montioring has beeen carried out using WAQI api.
