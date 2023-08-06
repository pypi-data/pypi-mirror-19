
"""
________________________________________________________________________________

  /$$$$$$  /$$   /$$  /$$$$$$  /$$$$$$$$ /$$$$$$$$
 /$$__  $$| $$  | $$ /$$__  $$| $$_____/|__  $$__/
| $$  \__/| $$  | $$| $$  \ $$| $$         | $$
|  $$$$$$ | $$$$$$$$| $$$$$$$$| $$$$$      | $$
 \____  $$| $$__  $$| $$__  $$| $$__/      | $$
 /$$  \ $$| $$  | $$| $$  | $$| $$         | $$
|  $$$$$$/| $$  | $$| $$  | $$| $$         | $$
 \______/ |__/  |__/|__/  |__/|__/         |__/

https://github.com/mardix/shaft

________________________________________________________________________________
"""

from shaft.cli import CLI
from . import serve


class MyCli(CLI):
    def __init__(self, command, click):
        """
        Initiate the command line
        Place all your command functions in this method
        And they can be called with

            > shaft $fn_name

        ie:

            @command
            def hello():
                click.echo("Hello World!")

        In your terminal:
            > shaft hello


        :param command: copy of the cli.command
        :param click: click
        """

        @command()
        def setup():
            """
            The setup
            """
            click.echo("This is a setup!")
