import argparse
import os
import time
from pprint import pprint

from requests import get

from googleapiclient import discovery
import google.auth
from six.moves import input


credentials, project = google.auth.default()
service = discovery.build('compute', 'v1', credentials=credentials)

#
# Stub code - just lists all instances
#
def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None

#print("Your running instances are:")
#for instance in list_instances(service, project, 'us-west1-b'):
#    print(instance['name'])

#
# Stub code - creates an instances
#
#[START create_instance]
def create_instance(compute, project, zone, name, bucket, snapshot=None):
    # Configure the machine
    machine_type = "zones/%s/machineTypes/n1-standard-1" % zone
    startup_script = open(
        os.path.join(
            os.path.dirname(__file__), 'startup-script.sh'), 'r').read()
    image_url = "http://storage.googleapis.com/gce-demo-input/photo.jpg"
    image_caption = "Ready for dessert?"

    config = {
        'name': name,
        'machineType': machine_type,

        # Specify the boot disk and the image to use as a source.
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceSnapshot': "global/snapshots/"+snapshot,
                }
            }
        ],

        # Specify a network interface with NAT to access the public
        # internet.
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],

        # Allow the instance to access cloud storage and logging.
        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/devstorage.read_write',
                'https://www.googleapis.com/auth/logging.write'
            ]
        }],

        # Metadata is readable from the instance and allows you to
        # pass configuration from deployment scripts to instances.
        'metadata': {
            'items': [{
                # Startup script is automatically executed by the
                # instance upon startup.
                'key': 'startup-script',
                'value': startup_script
            }, {
                'key': 'url',
                'value': image_url
            }, {
                'key': 'text',
                'value': image_caption
            }, {
                'key': 'bucket',
                'value': bucket
            }]
        }
    }

    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()
# [END create_instance]

#
# Stub code - deletes an instances
#
# [START delete_instance]
def delete_instance(compute, project, zone, name):
    return compute.instances().delete(
        project=project,
        zone=zone,
        instance=name).execute()
# [END delete_instance]

#
# Stub code - waiting for operation
#
# [START wait_for_operation]
def wait_for_operation(compute, project, zone, operation):
    print('Waiting for operation to finish...')
    while True:
        result = compute.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation).execute()

        if result['status'] == 'DONE':
            print("done.")
            if 'error' in result:
                raise Exception(result['error'])
            return result

        time.sleep(1)
# [END wait_for_operation]

def get_ext_ip(project, zone, instance_name):
    ext_ip_request = service.instances().get(project=project, zone=zone, instance=instance_name)
    ext_ip_response = ext_ip_request.execute()
    ext_ip = ext_ip_response['networkInterfaces'][0]['accessConfigs'][0]['natIP']
    return ext_ip

def setting_tag(project, zone, instance_name):
    fingerprint_request = service.instances().get(project=project, zone=zone, instance=instance_name)
    fingerprint_response = fingerprint_request.execute()
    my_fingerprint = fingerprint_response['tags']['fingerprint']
    #Add firewall network tag to the vm instance
    tags_body = {
        "items": [
            "allow-5000"
        ],
        "fingerprint": my_fingerprint
    }

    network_tag_request = service.instances().setTags(project=project, zone=zone, instance=instance_name, body=tags_body)
    network_tag_response = network_tag_request.execute()
    #print("Add network tags response: {}".format(network_tag_response))
    settingTag = "Network tag allow-5000 added to {}".format(instance_name)
    return settingTag

#
# Stub code - main code that calls the creation/deletion of vm instances
#
# [START run]
def main(project, bucket, zone, instance_name, wait=True):
    #compute = googleapiclient.discovery.build('compute', 'v1')
    """
    #Add firewall network tag to the vm instance
    tags_body = {
            "allow-5000"
        ],
        "items": [
        "fingerprint": fingerprint_response['tags']['fingerprint']
    }

    network_tag_request = service.instances().setTags(project=project, zone=zone, instance=instance_name, body=tags_body)
    network_tag_response = network_tag_request.execute()
    #print("Add network tags response: {}".format(network_tag_response))
    print("Network tag allow-5000 added")

    #Get external IP
    print("Getting external IP")
    ext_ip_request = service.instances().get(project=project, zone=zone, instance=instance_name)
    ext_ip_response = ext_ip_request.execute()
    ext_ip = ext_ip_response['networkInterfaces'][0]['accessConfigs'][0]['natIP']
    print("External IP: {}".format(ext_ip))
    port = 5000
    url = "http://" + ext_ip + ":" + str(port)
    pprint("Please visit url: {}".format(url))
    """

    #Creating SnapShot from Disk
    print("Creating snapshot of instance: {}".format(instance_name))
    snapshot_name = "base-snapshot-blog"
    snapshot_body = {
        "name": snapshot_name,
        "sourceDisk": instance_name
    }

    snapshot_request = service.disks().createSnapshot(project=project, zone=zone, disk=instance_name, body=snapshot_body)
    operation = snapshot_request.execute()
    wait_for_operation(service, project, zone, operation['name'])
    print("Snapshot created: {}".format(snapshot_name))

    #create 3 instances from snapshot
    creation_time=[]
    for i in range(3):
        print('Creating instance {} from snapshot.'.format(i+1))
        name = "instance"+str(i+1)
        operation = create_instance(service, project, zone, name, bucket, snapshot_name)
        start_time = time.time()
        wait_for_operation(service, project, zone, operation['name'])
        CreationTime = time.time() - start_time        
        creation_time.append(CreationTime)
        print("Time taken to create {} is {}".format(name, CreationTime))
        networkTag = setting_tag(project, zone, name)
        getExtIp = get_ext_ip(project, zone, name)
        print("The external IP of {} is {}".format(name, getExtIp))
        print()
    
    """
    #write instance creation timing to TIMING.md
    f= open("TIMING.md","w+")
    for i in range(len(creation_time)):
        f.write("instance{} creation time: {} secs \n".format((i+1), creation_time[i]))
    f.close()
    print("TIMING.md created")
    """

    print("Press enter to delete the instances")

    #Waiting for user input to delete the created instance    
    if wait:
        input()

    print('Deleting instance {}.'.format(instance_name))

    operation = delete_instance(service, project, zone, instance_name)
    wait_for_operation(service, project, zone, operation['name'])

    for i in range(3):
        name = "instance"+str(i+1)
        print('Deleting instance {}.'.format(name))
        operation = delete_instance(service, project, zone, name)
        wait_for_operation(service, project, zone, operation['name'])

    print('Done.')

    print('Press enter to delete snapshot')

    if wait:
        input()

    print('Deleting snapshot {}.'.format(snapshot_name))

    del_req = service.snapshots().delete(project=project, snapshot=snapshot_name)
    operation = del_req.execute()

    print ('Done.')

#
# Stub code - main default function
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    #parser.add_argument('project_id', help='Your Google Cloud project ID.')
    parser.add_argument(
        'bucket_name', help='Your Google Cloud Storage bucket name.')
    parser.add_argument(
        '--zone',
        default='us-central1-f',
        help='Compute Engine zone to deploy to.')
    parser.add_argument(
        '--name', default='demo-instance', help='New instance name.')

    args = parser.parse_args()

    main(project, args.bucket_name, args.zone, args.name)
# [END run]