import sys
import getopt
import configparser

from bucketlist import speedyio, logger
from bucketlist.commands import AddCommand
from bucketlist.commands import ViewCommand
from bucketlist.commands import MarkCommand
from bucketlist.commands import InitCommand
from bucketlist.commands import ConfigCommand
from bucketlist.errors import BucketlistError

commands = {
    AddCommand.__command_name__: AddCommand(),
    ViewCommand.__command_name__: ViewCommand(),
    MarkCommand.__command_name__: MarkCommand(),
    InitCommand.__command_name__: InitCommand(),
    ConfigCommand.__command_name__: ConfigCommand()
}

def execute(argv=None, settings=None):
    if argv is None:
        argv = sys.argv[1:]

    command = commands[argv.pop(0)]

    try:
        command.execute(argv)
    except BucketlistError as e:
        speedyio.error("{}".format(e.description))
    except getopt.GetoptError as e:
        speedyio.error(str(e))
    except configparser.NoOptionError as e:
        speedyio.error("Config '{}' under '{}' not set \u2639.\nRun `bucket-list config --set {} <value>`.".format(e.option, e.section, e.option))
    except KeyboardInterrupt:
        speedyio.error("\nThe process was killed \u2639")
    except Exception as e:
        logger.error(e)
        speedyio.error("\nSomething went really bad. Check the logs for more details \u2639")
