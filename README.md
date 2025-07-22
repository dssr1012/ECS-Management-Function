# ECS Management Function for Huawei Cloud

## Overview
This repository contains a Python function for Huawei Cloud FunctionGraph that allows you to start up or shut down ECS instances based on a trigger event.

## Prerequisites
- Huawei Cloud account with access to FunctionGraph and ECS services
- Proper IAM permissions to create functions and manage ECS instances

## Setup Instructions

### 1. Create an Agency with Required Permissions
Before creating the function, you need to set up an agency with the following permissions:
- ECS FullAccess (or at least permissions to start/stop instances)
- FunctionGraph Administrator

### 2. Create a FunctionGraph Function
1. Log in to the [Huawei Cloud Console](https://console.huaweicloud.com/)
2. Navigate to FunctionGraph service
3. Click "Create Function"
4. Select:
   - Runtime: Python 3.9
   - Template: Empty Function
5. Name your function (e.g., "ECS-Management")
6. Click "Create Function"

### 3. Configure Environment Variables
Add the following environment variables to your function:
- `project_id`: Your Huawei Cloud project ID (e.g., `1c42334636a74945353423adad7a2d6ea3`)
- `region`: The region where your ECS instances are located (e.g., `la-south-2`)

### 4. Upload the Function Code
Copy the provided Python code into the function editor or upload it as a .zip file.

### 5. Create a Trigger
To create a timer trigger:

1. Go to the "Triggers" tab in your function
2. Click "Create Trigger"
3. Select "Timer" as the trigger type
4. Configure the trigger:
   - Timer Name: `Timer-tst` (or your preferred name)
   - Rule: Select either fixed rate or cron expression
     - For example: Every 3 minutes
5. Enable the trigger
6. Click "OK"

## Usage
The function expects an event with the following format:
```json
{
  "user_event": "ecs_id1,ecs_id2,ecs_id3,action"
}
