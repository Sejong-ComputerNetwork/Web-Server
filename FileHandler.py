import os


def getFileAsString(pathToFile):
    result = ''
    try:
        with open(pathToFile, 'r', encoding='utf-8') as file:
            html_content = file.read()
        result += html_content
    except FileNotFoundError:
        print(f"Error: The file '{pathToFile}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return result

def load_html(filename):
    filepath = os.path.join("templates", filename)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>404 File Not Found</h1>"

def load_css(filename):
    try:
        css_path = os.path.join("./templates", filename)
        with open(css_path, "r", encoding="utf-8") as f:
            return f.read(), "200 OK", "text/css"
    except:
        return "", "404 Not Found", "text/css"