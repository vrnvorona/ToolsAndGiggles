import webbrowser

URL = "https://jira.surfstudio.ru/browse/"


def chrome_parser(*argv):
    for arg in argv:
        if type(arg) == list:
            for item in arg:
                temp_url = URL + item
                webbrowser.get("chrome").open_new_tab(temp_url)
        else:
            temp_url = URL + arg
            webbrowser.get("chrome").open_new_tab(temp_url)


def default_browser_parser(*argv):
    for arg in argv:
        if type(arg) == list:
            for item in arg:
                temp_url = URL + item
                webbrowser.open_new_tab(temp_url)
        else:
            temp_url = URL + arg
            webbrowser.open_new_tab(temp_url)
