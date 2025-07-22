# -*- coding:utf-8 -*-
import ssl
import os
import json
import time,sys
from httpclient import HTTPClient

def handler(event, context):
    print("event: %s" % event)
    project_id = context.getUserData('project_id')
    region = context.getUserData('region')
    aditionalData = event.get("user_event")
    print("Aditional Data:", aditionalData)
    
    if not project_id:
        print("project_id is invalid.")
        return "parameters invalid."

    if not region:
        print("region is invalid.")
        return "parameters invalid."

    ecs_ids = context.getUserData('ecs_id_list')
    if not ecs_ids:
        print("no ecs servers to operate.")
        return "nothing todo"

    parts = aditionalData.rsplit(',',1) 
    ecs_id = parts[0]
    print("servers: '%s'." % ecs_id)
    ecs_id_list = ecs_id.split(',') 
    logger = context.getLogger()
    if not project_id:
        print("operation failed for project_id or region or ak or sk empty.")
        sys.exit(1)
    operation =parts[1]
    logger.info("operation: %s.", operation)
    if operation == "startup":
        return _startup_ecs(logger, project_id, region, ecs_id_list, context)
    elif operation == "shutdown":
        return _shutdown_ecs(logger, project_id, region, ecs_id_list, context)
    else:
        logger.warn("no-op for ecs servers '%s'.", ecs_id_list)
        return "nothing to do"

def _shutdown_ecs(logger, project_id, region, ecs_id_list, context):
    client = HTTPClient("https://ecs." + region + ".myhuaweicloud.com")
    token = context.getToken()
    if not token:
        logger.error("get token failed")
        return "shutdown ecs failed for getting token failure."

    header = {"X-Auth-Token": token}
    reqbody = {"os-stop": {"type":"HARD", "servers": []}}
    for ecs_id in ecs_id_list:
        reqbody["os-stop"]["servers"].append({"id": ecs_id})
    status, headers, result = client.post("/v1/%s/cloudservers/action" % project_id, header, reqbody, logger)
    if status != 200 and status != 201 and status != 204:
        logger.error("shutdown request failed, status: %d, message: %s.", status, result)
        return "shutdown request failed"

    return "shutdown ecs servers '%s' complete." % (ecs_id_list)

def _startup_ecs(logger, project_id, region, ecs_id_list, context):
    client = HTTPClient("hhttps://ecs." + region + ".myhuaweicloud.com")
    token = context.getToken()
    if not token:
        logger.error("get token failed")
        return "startup ecs failed for getting token failure."

    header = {"X-Auth-Token": token}
    reqbody = {"os-start": {"servers": []}}
    for ecs_id in ecs_id_list:
        reqbody["os-start"]["servers"].append({"id": ecs_id})
    status, headers, result = client.post("/v1/%s/cloudservers/action" % project_id, header, reqbody, logger)
    if status != 200 and status != 201 and status != 204:
        logger.error("startup request failed, status: %d, message: %s.", status, result)
        return "startup request failed"

    return "startup ecs servers '%s' complete." % (ecs_id_list)
