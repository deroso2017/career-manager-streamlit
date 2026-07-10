import json
import streamlit as st
import boto3


def get_b2_client():

    return boto3.client(
        "s3",
        endpoint_url=st.secrets["B2_ENDPOINT"],
        aws_access_key_id=st.secrets["B2_KEY_ID"],
        aws_secret_access_key=st.secrets["B2_APPLICATION_KEY"],
        region_name="eu-central-003",
    )


def upload_file(file_data, filename):
    s3 = get_b2_client()
    s3.put_object(Bucket=st.secrets["B2_BUCKET"], Key=filename, Body=file_data)


def download_file(filename):
    s3 = get_b2_client()
    response = s3.get_object(Bucket=st.secrets["B2_BUCKET"], Key=filename)
    return response["Body"].read()


def file_exists(filename):
    s3 = get_b2_client()

    try:
        s3.head_object(Bucket=st.secrets["B2_BUCKET"], Key=filename)
        return True
    except:
        return False


def load_json(filename):
    if not file_exists(filename):
        return []

    with st.spinner("Lade Daten..."):
        try:
            return json.loads(download_file(filename).decode("utf-8"))
        except (json.JSONDecodeError, Exception):
            return []


def save_json(filename, data):
    with st.spinner("📂 Speicheren..."):
        upload_file(
            json.dumps(data, ensure_ascii=False, indent=4).encode("utf-8"), filename
        )
