def data():
    return {
        "hello": "cool",
        "my_name": "all",
        "my_list": [
            {"one": "one"},
            {"one": "two"}
        ],
    }


def index():
    return """
    <div style="background-color:aqua;">
        <h1>${hello}</h1>
        <h2>${my_name}<h2>
        <div>
            {for val in my_list}
                <h2>${my_name}</h2>
                <h3>{val.one}</h3>
            {end}
        </div>
    </div>
    """
