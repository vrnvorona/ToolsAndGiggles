import webbrowser

url = "https://jira.surfstudio.ru/browse/"


def parser(*argv):
    for arg in argv:
        temp_url = url + arg
        webbrowser.get("safari").open_new_tab(temp_url)


# webbrowser.open_new_tab(url)
