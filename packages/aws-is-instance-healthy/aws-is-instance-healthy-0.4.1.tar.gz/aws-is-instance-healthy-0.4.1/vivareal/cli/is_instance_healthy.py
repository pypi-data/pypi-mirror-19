#!/usr/bin/env python
# -*- coding: utf-8 -*-

import boto3

MAX_PAGESIZE = 100


def __describe_all_elbs(elb_client):
    elb_response = elb_client.describe_load_balancers(PageSize=MAX_PAGESIZE)
    while True:
        next_marker = elb_response.get('NextMarker')
        for load_balancer in elb_response.get('LoadBalancerDescriptions', []):
            yield load_balancer
        if next_marker:
            elb_response = elb_client.describe_load_balancers(PageSize=MAX_PAGESIZE, Marker=next_marker)
        else:
            break


def is_instance_healthy(region_name, instance_id):
    elb_client = boto3.client('elb', region_name=region_name)
    for load_balancer in __describe_all_elbs(elb_client):
        for instance in load_balancer.get('Instances', []):
            if instance.get('InstanceId') != instance_id:
                continue
            health_response = elb_client.describe_instance_health(
                LoadBalancerName=load_balancer['LoadBalancerName'],
                Instances=[{'InstanceId': instance_id}]
            )
            if 'InstanceStates' not in health_response:
                continue
            instance_state = health_response['InstanceStates'][0]  # we only asked for one instance
            return instance_state['State'] == 'InService', instance_state['ReasonCode'], instance_state['Description']
    return False, 'N/A', 'Instance %s not found or not attached to an ELB' % instance_id


if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Simple CLI to ensure that an AWS instance is healthy')
    parser.add_argument('region_name', metavar='region-name', help='AWS Region Name')
    parser.add_argument('instance_id', metavar='instance-id', help='AWS EC2 Instance Id')

    args = parser.parse_args()
    status = is_instance_healthy(args.region_name, args.instance_id)
    if status[0]:
        sys.stdout.write('Instance %s is healthy\n' % args.instance_id)
        sys.exit(0)
    else:
        sys.stdout.write('Instance %s is unhealthy!\n' % args.instance_id)
        sys.stderr.write('Instance %s is unhealthy based on %s. Reason: %s\n' % (args.instance_id, status[1], status[2]))
        sys.exit(100)
