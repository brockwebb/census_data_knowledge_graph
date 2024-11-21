def create_robust_session(total_retries=5, backoff_factor=1):
    """
    Create a requests.Session with retry capabilities for resilient HTTP requests.

    Parameters:
    -----------
    total_retries : int
        Maximum number of retries for failed requests (default: 5).
    backoff_factor : float
        Delay multiplier between retries (default: 1).

    Returns:
    --------
    requests.Session
        Session with retry logic applied.
    """
    session = requests.Session()
    retries = Retry(
        total=total_retries,
        backoff_factor=backoff_factor,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def fetch_url(url, session):
    """
    Fetch content from a URL using a robust session.

    Parameters:
    -----------
    url : str
        Target URL to fetch.
    session : requests.Session
        Session configured with retry logic.

    Returns:
    --------
    str or None
        Response content if successful, otherwise None.
    """
    try:
        response = session.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
        return None

