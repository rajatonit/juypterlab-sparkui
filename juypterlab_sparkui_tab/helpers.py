from bs4 import BeautifulSoup
import re



def replace(content, root_url):
    """Replace all the links with our prefixed handler links,
     e.g.:
    /proxy/application_1467283586194_0015/static/styles.css" or
    /static/styles.css
    with
    /spark/static/styles.css
    """
    try:
        import lxml
    except ImportError:
        BEAUTIFULSOUP_BUILDER = "html.parser"
    else:
        BEAUTIFULSOUP_BUILDER = "lxml"
    # a regular expression to match paths against the Spark on EMR proxy paths
    PROXY_PATH_RE = re.compile(r"\/proxy\/application_\d+_\d+\/(.*)")
    # a tuple of tuples with tag names and their attribute to automatically fix
    PROXY_ATTRIBUTES = (
        (("a", "link"), "href"),
        (("img", "script"), "src"),
    )
    soup = BeautifulSoup(content, BEAUTIFULSOUP_BUILDER)
    for tags, attribute in PROXY_ATTRIBUTES:
        for tag in soup.find_all(tags, **{attribute: True}):
            value = tag[attribute]
            match = PROXY_PATH_RE.match(value)
            if match is not None:
                value = match.groups()[0]
            tag[attribute] = url_path_join(root_url, value)
    return str(soup)


def url_path_join(*pieces):
    """Join components of url into a relative url
    Use to prevent double slash when joining subpath. This will leave the
    initial and final / in place
    """
    initial = pieces[0].startswith("/")
    final = pieces[-1].endswith("/")
    stripped = [s.strip("/") for s in pieces]
    result = "/".join(s for s in stripped if s)
    if initial:
        result = "/" + result
    if final:
        result = result + "/"
    if result == "//":
        result = "/"
    return result