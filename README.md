# Inventory Management System

- **University**: University of North Dakota
- **Course**: CSCI 455: Database Management Systems
- **Semester**: Spring 2023
- **Project**: Inventory management system
- **Group Members**: Daniel De Jesus, Alycia Sloan, Austin Garcia

## Static Code Analysis with pre-commit

### Running Locally

pre-commit can be run locally during development to automate formatting, detection of errors and bugs, and to enforce general code quality standards. If you decide to install the pre-commit hooks in your local repo, it will run every time you attempt to commit. If a check fails, you will have to resolve any warnings emitted or commit with `--no-verify` to ignore them.

pre-commit can also be run manually even if you haven't installed the hooks into your local repo.

Note: If we all decide that we want to do this early on, it shouldn't be too difficult at all to keep everything in the green at all times.

### Running Remotely

Remotely -- in the GitHub repo -- pre-commit will run the same local checks on the most recent commit of each push to see if any warnings have been emitted. If your checks passed locally and the remote still complains, it's likely due to someone else's code. However, if there is a problem with your code, you can just push a new commit with the corrections.

Note: All devs must handle their warnings before merging into `main` or the remote will always warn -- even for those who handled all of their warnings. If you don't want to use pre-commit, that's fine. Those who do wish to, however, will have to beware that they can only do so meaningfully locally, as pre-commit on the remote will check all files whether or not they've been changed. That is, you'll get others' accumulated warnings as opposed to only your own most recent changes.

### Hooks Configured

pre-commit has been configured with the following tools:
- sqlfluff: Formats and lints SQL code.
  - This tool works a little strangely, in that it will try to enforce consistency with the first use of a construct. For example, if the first identifier you name is lowercase, it will complain when you use a different convention for future identifiers in the same SQL file.
  - **NOTE!** An important quirk to note is that trailing commas will cause a parsing error. This is silly and easy to do, so beware of where you're putting your commas. If you see `[1 templating/parsing errors found]` and you know your SQL is valid, this may be the issue.
- pyupgrade: Upgrades syntax to a specified version.
  - As one example, for specified version >= 3.10, `def thing(): -> List[int]:` becomes `def thing() -> list[int]:`, allowing the builtin `list` to be used for annotations instead of importing `from typing import List`.
  - It is currently specified to python version 3.11.
- autoflake: Removes unused imports and variables.
- isort: Sorts imports alphabetically by import type.
- black: Formats code according to the PEP 8 standard. Will prevent the linters below from reporting nit-picky things, and save you from having to think about such nit-picky things.
- vulture: Checks for dead code.
- pylint: A proper static code analyzer.
- mypy: Static type checking. Example warning: "Returning None from function declared to return str".
- flake8: Also performs static code analysis (this time with pyflakes), checks compliance with the PEP 8 style guide (using pycodestyle), performs complexity analysis (with McCabe).
  - The `flake8-bugbear` plugin is also being used with flake8 for semantic analysis.
- The vanilla hooks for checking miscellaneous things like yaml, toml, and trailing whitespace.

Some of these tools are already configured in `pyproject.toml` and `.flake8`. If anything pops up that annoys you, we can re-configure it.

### Setup

- `pip install pre-commit`
- `pre-commit install` to install the hooks in your local repo (this makes `git commit` trigger pre-commit)
  - You can skip this if you like and use pre-commit exclusively manually if you like.
  - To uninstall, run `pre-commit uninstall` and pre-commit won't be triggered automatically when you attempt to commit.
- `pre-commit run --all-files` will install and run each tool's binary on all of the project files. This will take a minute, but is only a one-time thing.

### Usage

For smaller changes, just commit normally, resolving any warnings that come up. For larger changes, you may wish to manually run pre-commit every so often.

If the hooks were installed in your repo (`pre-commit install`), pre-commit will run automatically when you run `git commit`.

- If warnings are emitted, you will have to resolve them before you attempt to commit again.
- To bypass this (for example, if you want to save all changes and/or warnings for a dedicated commit before you push), you can add the `--no-verify` flag to your `git commit` command.

Whether or not you installed the hooks into your repo, you can still run pre-commit whenever you like using the following commands:
- `pre-commit` runs pre-commit only on **staged** changes.
- `pre-commit run <hook_id>` runs only the specified hook (eg, `black`, `mypy`, etc) on staged changes.
  - Note: If you want to pass extra arguments to the tool, you'll have to install it separately. You shouldn't have to worry about conflicting with pre-commit in doing so as pre-commit runs in an isolated environment with its own binaries. The only thing I might suggest is that you ensure you're using the same version as specified in `.pre-commit-config.yaml` if you're getting unexpected results.
- `pre-commit run --all-files` will run pre-commit on all of the files, whether or not changes were made.
