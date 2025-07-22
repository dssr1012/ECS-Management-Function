ECS Management Function for Huawei Cloud
Overview
This repository contains a Python function for Huawei Cloud FunctionGraph that allows you to start up or shut down ECS instances based on a trigger event.

Prerequisites
Huawei Cloud account with access to FunctionGraph and ECS services

Proper IAM permissions to create functions and manage ECS instances

Setup Instructions
1. Create an Agency with Required Permissions
Before creating the function, you need to set up an agency with the following permissions:

ECS FullAccess (or at least permissions to start/stop instances)

FunctionGraph Administrator

2. Create a FunctionGraph Function
Log in to the Huawei Cloud Console

Navigate to FunctionGraph service

Click "Create Function"

Select:

Runtime: Python 3.9

Template: Empty Function

Name your function (e.g., "ECS-Management")

Click "Create Function"

3. Configure Environment Variables
Add the following environment variables to your function:

project_id: Your Huawei Cloud project ID (e.g., 1c42334636a749199423adad7a2d6ea3)

region: The region where your ECS instances are located (e.g., lasouth2)

ecs_id_list: Comma-separated list of ECS instance IDs to manage

4. Upload the Function Code
Copy the provided Python code into the function editor or upload it as a .zip file.

5. Create a Trigger
To create a timer trigger (as shown in the example image):

Go to the "Triggers" tab in your function

Click "Create Trigger"

Select "Timer" as the trigger type

Configure the trigger:

Timer Name: Timer-5m7j (or your preferred name)

Rule: Select either fixed rate or cron expression

For example: Every 3 minutes

Enable the trigger

Click "OK"
