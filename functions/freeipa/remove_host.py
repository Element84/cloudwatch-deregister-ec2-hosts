import json
import boto3
import os
import logging
import ipahttp



def get_private_dns_from_instance(event):
    '''
    Triggered by a CloudWatch event.
    Uses AWS SDK to get the Private DNS

    Hosts in FreeIPA are registered by Fully Qualified Domain Name (FQDN),
    which is the AWS Private DNS name

    Returns: the Private DNS of an instance that is being terminated
    Example: ip-10-64-3-216.ec2.internal
    '''

    instance_id = json.dumps(event['detail']['instance-id']).strip('"')
    logging.info('Event received for EC2 instance: {}'.format(instance_id))

    client = boto3.client('ec2')
    response = client.describe_instances(InstanceIds=[instance_id])
    private_dns = response['Reservations'][0]['Instances'][0]['PrivateDnsName']
    logging.info('Got Private DNS record: {}'.format(private_dns))
    return private_dns

def remove_host_from_freeipa(private_dns, ipa_server, ipa_user, ipa_pass):
    '''
    We use instance Private DNS for 'Host name' in FreeIPA
    Use the FreeIPA API to remove the host that was just terminated.

    Uses the `python-freeipa-json` library https://github.com/nordnet/python-freeipa-json

    Returns: Success if found and removed; Warning if not found; Error if error
    '''
    logging.info('Attempting to authenticate to IPA server: {}'.format(ipa_server))
    ipa = ipahttp.ipa(ipa_server)

    # Error handling for login request is in the ipahttp library
    ipa.login(ipa_user, ipa_pass)

    logging.info('Successful authentication to IPA server, searching for host: {}'.format(private_dns))
    reply = ipa.host_find(private_dns)
    logging.info('Host lookup response: {}'.format(reply))

    if private_dns is None or reply['result']['count'] == 0:
        logging.warning('Could not find host, doing nothing')
    else:
        host_to_delete = reply['result']['result'][0]['fqdn'][0]
        logging.info('Found host: {}, will delete.'.format(host_to_delete))

        del_reply = ipa.host_del(private_dns)
        logging.info('Delete response: {}'.format(del_reply))

        if del_reply['error'] is not None:
            logging.error('Error deleting host, please check FreeIPA server ({})'.format(ipa_server))
        else:
            logging.info('Successfully deleted host: {}'.format(host_to_delete))


def lambda_handler(event, context):
    logging.getLogger().setLevel(logging.INFO)

    ipa_server = os.environ['ipa_server']
    ipa_user = os.environ['ipa_user']
    ipa_pass = os.environ['ipa_pass']

    private_dns = get_private_dns_from_instance(event)
    remove_host_from_freeipa(private_dns, ipa_server, ipa_user, ipa_pass)