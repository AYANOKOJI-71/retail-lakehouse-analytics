"""S3-compatible publishing for MinIO, AWS S3, and other object stores."""

from __future__ import annotations

from pathlib import Path

import boto3


def publish_file(endpoint_url: str, access_key: str, secret_key: str, bucket: str, local_file: Path, key: str) -> str:
    """Upload a local lakehouse artifact to an explicitly configured S3-compatible bucket."""

    client = boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    client.upload_file(str(local_file), bucket, key)
    return f"s3://{bucket}/{key}"
