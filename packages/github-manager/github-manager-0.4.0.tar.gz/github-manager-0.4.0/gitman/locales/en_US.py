DESCRIPTION = 'Gitman - Github repository manager'
LIST_HELP = 'List the repositories of the user.'
SETUP_HELP = 'Setup user credentials in the form of a Github OAuth token.'
CLONE_HELP = 'Clones the specified repository.\n\n\tREPO: the repository to \
clone in the format <username?>/<repo_name>. Username defaults to the \
authenticated user if no <user> specified.'
USER_HELP = 'Targets a user in Github. Default: user configured by setup'
FORK_HELP = 'Forks the given repository <username>/<repository> into your \
authenticated account'

LIST_USERNAME = 'Repositories for user: {}'
LIST_NOTFOUND = 'User "{}" not found or not authorized.'

SETUP_INSTRUCTIONS = 'Please provide your Github OAuth token with "repos" \
permission.'
SETUP_INPUT = 'Github OAuth token: '
SETUP_CANCEL = 'Aborting setup.'

CLONE_NOTFOUND = 'You must have Git installed and available in your $PATH to \
clone a repository'

FORK_SYNTAXERROR = 'Fork requests must be in the format \
<username>/<repository>'
FORK_NOTFOUND = 'The repository {} is private or does not exist.'
FORK_SELFERROR = 'You cannot fork your own repositories.'
FORK_SUCCESS = 'Repository {} has been successfully forked from {}.\nPlease \
wait a few minutes for the operation to complete.'

API_ERROR = 'ERROR: Invalid token.'
