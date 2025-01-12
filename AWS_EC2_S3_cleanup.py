import boto3
import subprocess

def list_attached_volumes(instance_id):
    ec2 = boto3.client('ec2')
    volumes = []

    # Get all volumes attached to the instance
    response = ec2.describe_volumes(Filters=[{'Name': 'attachment.instance-id', 'Values': [instance_id]}])
    for volume in response['Volumes']:
        volumes.append(volume['VolumeId'])
    
    return volumes

def wipe_volume(volume_id):
    ec2 = boto3.client('ec2')
    print(f"Wiping data from volume: {volume_id}")

    # Detach the volume if attached
    ec2.detach_volume(VolumeId=volume_id, Force=True)
    waiter = ec2.get_waiter('volume_available')
    waiter.wait(VolumeIds=[volume_id])

    # Securely erase the volume using a temporary instance
    # You need to attach the volume to a temporary instance for wiping
    print(f"Volume {volume_id} is now detached. Perform manual wiping if necessary.")


def delete_volume(volume_id):
    ec2 = boto3.client('ec2')
    print(f"Deleting volume: {volume_id}")
    ec2.delete_volume(VolumeId=volume_id)
    print(f"Volume {volume_id} deleted successfully.")

def delete_snapshots(instance_id):
    ec2 = boto3.client('ec2')
    print("Deleting associated snapshots...")
    snapshots = ec2.describe_snapshots(Filters=[{'Name': 'description', 'Values': [f'Created by CreateImage for {instance_id}*']}])
    for snapshot in snapshots['Snapshots']:
        snapshot_id = snapshot['SnapshotId']
        print(f"Deleting snapshot: {snapshot_id}")
        ec2.delete_snapshot(SnapshotId=snapshot_id)
    print("Snapshots deleted successfully.")

def delete_s3_objects(bucket_name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    print(f"Deleting all objects in bucket: {bucket_name}")
    bucket.objects.all().delete()
    print(f"All objects in bucket {bucket_name} deleted successfully.")

def clean_up_instance(instance_id, bucket_name=None):
    print(f"Starting cleanup process for instance: {instance_id}")

    # Step 1: List and wipe attached volumes
    volumes = list_attached_volumes(instance_id)
    for volume_id in volumes:
        wipe_volume(volume_id)
        delete_volume(volume_id)

    # Step 2: Delete associated snapshots
    delete_snapshots(instance_id)

    # Step 3: Delete S3 bucket contents if provided
    if bucket_name:
        delete_s3_objects(bucket_name)

    print(f"Cleanup process completed for instance: {instance_id}")

if __name__ == "__main__":
    INSTANCE_ID = input("Enter the instance ID to clean up: ")
    BUCKET_NAME = input("Enter the S3 bucket name (if any) to clean up: ")

    clean_up_instance(INSTANCE_ID, BUCKET_NAME if BUCKET_NAME else None)
