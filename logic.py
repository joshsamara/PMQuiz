from yaml import load
from collections import OrderedDict

# Load tools from yaml
with open("tools.yaml", 'r') as stream:
    tmp_tools = load(stream)
    stream.close()

# Sort our sections
# We want Other Software to be last
ALL_TOOLS = OrderedDict()
for key in reversed(sorted(tmp_tools)):
    ALL_TOOLS[key] = tmp_tools[key]


def filter_tools(selection):
    """Filter all tools based on a list of uids."""
    selected_tools = OrderedDict()
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


def choose_tools(form_data):
    """The logic behind choosing tools."""
    def check(key, options):
        """Check if the key in data == or is one of the given options."""
        v = form_data.get(key)
        if isinstance(options, list):
            return v in options
        else:
            return v == options

    selection = set()
    notes = []

    low_budget = check('budget', ['none', 'small'])
    small_team = check('size', ['personal', 'small'])

    # Other Storage logic
    if check('other-storage', 'on'):
        if low_budget:
            # Google drive
            selection.add('gr')
            notes.append('<span>Google Drive</span> is useful for file storage '
                         'and file sharing')
        else:
            # s3
            selection.add('s3')
            notes.append('<span>S3</span> is good for both file storage of any '
                         'type AND external file serving')

    # Text Editor
    if check('text-editor', 'on'):
        if low_budget:
            # Vim
            selection.add('vi')
            notes.append('<span>Vim</span> is a free customiziable, '
                         'multiplatform text editor')
        else:
            # Sublime
            selection.add('st')
            notes.append('<span>Sublime Text</span> is an affordable and '
                         'customizable text editor')

    # Markdown
    if check('markdown', 'on'):
        selection.add('md')

    # Regex
    if check('regex', 'on'):
        selection.add('re')

    # Source Control
    if check('source', 'public'):
        selection.add('gh')
        # Github
    elif check('source', 'private'):
        if low_budget:
            # BitBucket
            selection.add('bb')
            if small_team:
                notes.append('<span>BitBucket</span> provided a few free '
                             'private repositories. we recommend Github if '
                             'the budget can be expanded')
            else:
                notes.append('<span>BitBucket</span> provided a few free '
                             'private repositories. This may not be enough '
                             'for a larger team')
        else:
            selection.add('gh')
            notes.append('For your uses, <span>GitHub</span> is more expensive '
                         'but a better product than BitBucket')
    elif check('source', 'personal'):
        notes.append('You will need to create your own source control hosting option')

    # Project Tracking
    if check('multiple', 'no') and (selection & {'bb', 'gh'}):
        notes.append('Because you chose to not use multiple PM applications, '
                     'your source control manager should '
                     'be sufficient for task tracking')
    elif not low_budget:
        selection.add('jr')
    elif check('open', 'yes'):
        selection.add('jr')
        notes.append('<span>Jira</span> offers free licences for '
                     'non-profit projects')
    elif check('task-board', 'on') or (small_team and check('duration', 'short')):
        selection.add('tl')
        notes.append('<span>Trello</span> is good for smaller projects '
                     'or kanban projects')
    else:
        selection.add('pv')
        notes.append('<span>Producteev</span> is a functional project tracker. '
                     'The free version is very full-featured. ')

    # Documentation
    if not check('documentation', 'none'):
        if check('multiple', 'no') and (selection & {'bb', 'gh'}):
            notes.append('Because you chose to not use multiple applications, '
                         'your source control manager should'
                         'should be sufficient for documentation')
        elif check('multiple', 'no') and (selection & {'jr', 'tl', 'pv'}):
            notes.append('Because you chose to not use multiple applications, '
                         'Your issue tracker should be sufficient for '
                         'documentation')
        elif check('documentation', 'small'):
            if (selection & {'bb', 'gh'}):
                notes.append('Because you don\'t require much documentation, '
                             'your other tools should be sufficient for '
                             'documentation')
            elif small_team or check('duration', 'short'):
                selection.add('gd')
                notes.append('Because the small scope of your project, <span>'
                             'Google Docs</span> should be sufficient for '
                             'documentation')
            elif low_budget:
                selection.add('gd')
                notes.append('Because the small budget of your project, and lack '
                             'of other documentation options, <span>'
                             'Google Docs</span> should be sufficient for '
                             'documentation')
        elif check('documentation', 'large'):
            if low_budget:
                selection.add('gd')
                notes.append('Because the small budget of your project, <span>'
                             'Google Docs</span> may be the only option for '
                             'documentation')
            else:
                selection.add('cf')

    # Documentation
    need_pm_software = (check('wbs', 'on') or
                        check('gantt', 'on') or
                        check('anls', 'on') or
                        check('pm', 'on'))

    if not need_pm_software:
        notes.append('We\'ve determined specific PM software may not be '
                     'necessary for your project')
    elif (low_budget and small_team and check('duration', 'short')):
        selection.add('gs')
        notes.append('A spreadsheet tool like <span>Google Sheets</span> '
                     'may be sufficient for your low PM requirements')
    else:
        if check('budget', 'large'):
            selection.add('lp')
            notes.append('Because of your high budget, we think <span>'
                         'Liquid Planner</span> may be suitable')
            if (selection & {'jr', 'tl', 'pv'}):
                notes.append('<span>Liquid Planner</span> may have features that'
                             'overlap with your project tracking software.')
        elif check('web-based', 'yes'):
            if check('budget', 'none'):
                selection.add('gs')
                notes.append('Because of your low budget and web-based preference'
                             'a spreadsheet tool like <span>Google Sheets</span> '
                             'may be sufficient.')
            else:
                selection.add('tp')
                notes.append('Because you perfer web based software, we recommend '
                             '<span>Tom\'s planner</span>')
        elif check('budget', 'none'):
            selection.add('pl')
            notes.append('Because of your low budget, we recommend'
                         '<span>Project Libre</span>')
        else:
            selection.add('mp')

    # CI
    if check('ci', 'travis'):
        if low_budget:
            if check('source', 'public'):
                selection.add('travis')
                notes.append('<span>Travis CI</span> is free for public repositories')
            else:
                selection.add('jenkins')
                notes.append('<span>Travis</span>may be better suited for your project, but '
                             'because of your budget, we recommend <span>Jenkins</span>')
        else:
            selection.add('travis')
    elif check('ci', 'jenkins'):
        selection.add('jenkins')

    tools = filter_tools(selection)
    return tools, notes
