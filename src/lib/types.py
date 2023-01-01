from typing import Optional

Headers = dict[str, str]

def get_content_type(headers: Headers) -> Optional[str]:
    lower_case_headers = {k.lower(): v for k, v in headers.items()}
    content_type = lower_case_headers.get('content-type')

    if content_type is None:
        return None
    elif 'json' in content_type:
        return 'JSON'
    elif 'xml' in content_type:
        return 'XML'
    elif 'html' in content_type:
        return 'HTML'
    elif 'javascript' in content_type:
        return 'Javascript'
    elif 'image' in content_type:
        return 'Image'
    else:
        return None
