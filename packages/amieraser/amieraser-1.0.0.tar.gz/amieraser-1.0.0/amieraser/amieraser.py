import boto3
import botocore.exceptions

def cli():
    import sys
    from optparse import OptionParser

    # Parse command line arguments
    parser = OptionParser()
    parser.add_option('--id', dest="id", 
        help="One or more AMI Ids in a comma-seperated list. IDs take the form 'ami-xxxxxxxx'")
    parser.add_option('--region', dest="region", 
        help="The Amazon region the AMIs are located in. us-east-1 is used by default")
    parser.add_option('--profile', dest="profile",
        help="The name of the profile in your AWS credentials file. If not specified, the default profile is used")

    (options, args) = parser.parse_args()

    if (options.region == None):
        aws_region = 'us-east-1'
    else:
        aws_region = options.region

    if (options.profile == None):
        aws_profile = 'default'
    else:
        aws_profile = options.profile

    if options.id == None:
        print("Error: Image ID not provided!")
        sys.exit(1)

    session = boto3.Session(profile_name=aws_profile)
    client = session.client('ec2', region_name=aws_region)

    image_ids = options.id.split(',')

    for image_id in image_ids:
        delete_result = delete_ami(image_id)
        if delete_result == False:
            sys.exit(1)

def delete_ami(image_id):
    """
    Deletes a single AMI and any snapshots associated with that AMI
    Returns True if the delete succeeded, or False if an error occured
    """
    try:
        response = client.describe_images(ImageIds=[image_id])
        devices = response['Images'][0]['BlockDeviceMappings']
        snap_ids = [ device['Ebs']['SnapshotId'] for device in devices ]
        
        # Delete the image itself
        client.deregister_image(ImageId=image_id)
        print("Deregistered %s" % image_id)

        # Delete any associated snapshots
        for snap_id in snap_ids:
            client.delete_snapshot(SnapshotId=snap_id)
            print("  - Deleted snapshot %s" % snap_id)
        
        return True
    except botocore.exceptions.ClientError as e:
        print("An error occured deleting the image %s:" % image_id)
        print("\t" + str(e))
        return False
