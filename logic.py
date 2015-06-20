from yaml import load

# Load tools from yaml
with open("tools.yaml", 'r') as stream:
    ALL_TOOLS = load(stream)
    stream.close()


def choose_tools(form_data):
    selection = set()
    print form_data
    tools = filter_tools(selection)
    return tools, []


def filter_tools(selection):
    selected_tools = {}
    for group, tools in ALL_TOOLS.iteritems():
        group_selection = []
        for tool in tools:
            # Add any tools we have selected
            if tool['uid'] in selection:
                group_selection.append(tool)
        if group_selection:
            # If we have any tools in this group add them
            selected_tools[group] = group_selection
    return selected_tools
