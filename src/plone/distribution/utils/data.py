from base64 import b64encode


def convert_data_uri_to_b64(raw_data: str) -> bytes:
    """Convert data-uri format to one suitable to be used with the plone.app.registry."""
    response = b""
    if "base64," in raw_data:
        headers, data = raw_data.split("base64,")
        filename = headers.split("name=")[1][:-1]
        filenameb64 = b64encode(filename.encode("utf-8")).decode("utf-8")
        response = f"filenameb64:{filenameb64};datab64:{data}".encode()
    return response
