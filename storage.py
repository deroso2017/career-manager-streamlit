import json
import boto3
import streamlit as st


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

    # Clear the read cache after uploading a new file so the app gets fresh data immediately
    load_json_cached.clear()


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


# --- Helper to check file metadata ---
def get_file_version_token(filename):
    """Returns a unique token (ETag or LastModified) representing the file state."""
    s3 = get_b2_client()
    try:
        response = s3.head_object(Bucket=st.secrets["B2_BUCKET"], Key=filename)

        # Combine ETag and LastModified to create a robust version string
        return f"{response.get('ETag', '')}-{response.get('LastModified', '')}"
    except:
        return None


# --- Cached Data Fetcher ---
@st.cache_data(show_spinner="Lade Daten aus Cloud...")
def load_json_cached(filename, version_token):
    """
    This function actually downloads the file. Because it takes 'version_token'
    as an argument, Streamlit will hit the cache unless the version_token changes.
    """
    try:
        return json.loads(download_file(filename).decode("utf-8"))
    except (json.JSONDecodeError, Exception):
        return []


# --- Public Main Loader ---
def load_json(filename):
    if not file_exists(filename):
        return []

    # 1. Get the current token of the file from B2 (Fast HEAD request)
    version_token = get_file_version_token(filename)

    # 2. Call the cached function. If token matches old run, returns instantly from local cache.
    return load_json_cached(filename, version_token)


def save_json(filename, data):
    with st.spinner("📂 Speicheren..."):
        upload_file(
            json.dumps(data, ensure_ascii=False, indent=4).encode("utf-8"),
            filename,
        )
        # Force cache clear for this function just to be absolutely sure next load is fresh
        load_json_cached.clear()
