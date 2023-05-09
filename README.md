# Inventory Management System

- **University**: University of North Dakota
- **Course**: CSCI 455: Database Management Systems
- **Semester**: Spring 2023
- **Project**: Inventory Management System
- **Group Members**: Daniel De Jesus, Alycia Sloan, Austin Garcia

## Static Code Analysis with [pre-commit](https://pre-commit.com/)

pre-commit is used to automate formatting, detection of errors and bugs, and to enforce general code quality standards. It is set up to run on the remote and can be configured to run locally. pre-commit on your branch must pass all checks before merging into `main`.

To see all hooks configured, see [.pre-commit-config.yaml](.pre-commit-config.yaml)

### Setup

- Install pre-commit: `pip install pre-commit`

Decide which stages you want pre-commit to run at:

- Manual (no stages): See [Usage](#usage)
- pre-commit: `pre-commit install`
- pre-push: `pre-commit install --hook-type pre-push`
- pre-merge-commit: `pre-commit install --hook-type pre-merge-commit`
- Stages specified in the config: `pre-commit install --all`
- For other stages, see [confining hooks to run at certain stages](https://pre-commit.com/#confining-hooks-to-run-at-certain-stages) (pre-commit.com)
- To disable hooks for all stages: `pre-commit uninstall`

It's up to you how you want to set this up locally. Some people want regular, frequent feedback from their tools, others just want to go full stream of consciousness and work on their feature without distraction. The best workflow is the one that makes you more productive. However, you will want to run pre-commit at some point before merging into `main`.

I would recommend at least enabling for pre-push, but enabling for the pre-commit stage as well will generally make it easier to resolve failures. Other stages (mentioned above) such as pre-merge-commit and post-rewrite might be helpful, but generally aren't going to be as necessary.

### Usage

Depending on which stage(s) you enabled hooks for, pre-commit will run automatically. However, if you chose not to have pre-commit run automatically, the following can be run at any time:

- Run pre-commit on staged changes: `pre-commit`
- Run a specific hook on staged changes: `pre-commit run <hook_id>`
  - Note: If you want to pass extra arguments to the tool, you'll have to install it separately. You shouldn't have to worry about conflicting with pre-commit in doing so as pre-commit runs in an isolated environment with its own binaries. The only thing I might suggest is that you ensure you're using the same version as specified in `.pre-commit-config.yaml` if you're getting unexpected results.
- Run pre-commit on all files, whether or not changes were made: `pre-commit run --all-files`

Handling failures: Any time a pre-commit run fails, the operation you attmpted will be cancelled. You must either resolve the failures or repeat the operation with `--no-verify` or `-n` to ignore them.
