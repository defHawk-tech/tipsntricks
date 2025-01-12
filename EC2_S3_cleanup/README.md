# AWS Instance Cleanup Script

This Python script automates the cleanup of AWS resources associated with a terminated instance. It securely handles the following tasks:

1. **Lists and Wipes Attached Volumes**: Ensures data on EBS volumes is securely erased.
2. **Deletes Volumes**: Removes any leftover EBS volumes.
3. **Deletes Associated Snapshots**: Removes any snapshots created for the instance.
4. **Cleans Up S3 Buckets (Optional)**: Deletes all objects in a specified S3 bucket.

---

## Prerequisites

1. **Python 3.x** installed on your system.
2. **boto3** library installed.
   ```bash
   pip install boto3
   ```
3. AWS credentials configured with sufficient permissions to:
   - List and manage EC2 instances, volumes, and snapshots.
   - Manage S3 buckets (if using the S3 cleanup functionality).

---

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/aws-cleanup-script.git
   cd aws-cleanup-script
   ```

2. Ensure your AWS credentials are configured via the AWS CLI or environment variables.
   ```bash
   aws configure
   ```

3. Edit the script if needed to customize cleanup behavior.

---

## Usage

1. Run the script:
   ```bash
   python aws_cleanup_script.py
   ```

2. Provide the **Instance ID** and optional **S3 bucket name** when prompted:
   ```
   Enter the instance ID to clean up: i-0abcdef1234567890
   Enter the S3 bucket name (if any) to clean up: my-bucket-name
   ```

3. The script will:
   - List and detach attached volumes.
   - Wipe and delete EBS volumes.
   - Remove associated snapshots.
   - Optionally clean up the specified S3 bucket.

---

## Notes

- **Security**: Ensure you have permissions only for the necessary resources to prevent accidental deletions.
- **Testing**: Test the script in a non-production environment before using it on live systems.
- **Manual Verification**: For secure wiping, verify volumes are properly detached and wiped manually if required.

---

## Contributions

Contributions and improvements are welcome! Please open an issue or submit a pull request.

---

## Contact

For any questions or issues, feel free to contact specter@defhawk.com.
