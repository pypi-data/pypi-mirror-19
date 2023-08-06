import os
import sys
import time


# TODO: convert to use LoggedPopen utility...
from subprocess import call, CalledProcessError, check_output

from Client import Client
from Command import Command
from ClientSocket import ClientSocket
from daemonize import Daemonize
from PackageInfo import PackageInfo
from ClientLogger import ClientLogger
from ClientOption import ClientOption
from ClientOptionParser import ClientOptionParser


# noinspection PyClassHasNoInit


class ClientDaemon:

    @staticmethod
    def start(**kwargs):
        logger = ClientLogger.setup()
        (opts, args) = ClientOptionParser().parse_args()

        if not ClientDaemon.__status(opts, args):
            try:
                client = Client()
                pid_file = opts.get(ClientOption.PID_FILE)
                foreground = opts.get(ClientOption.DEBUG)
                daemon = Daemonize(
                    app=PackageInfo.pip_package_name,
                    pid=pid_file,
                    action=client.run,
                    foreground=foreground,
                    verbose=True,
                    logger=logger,
                    auto_close_fds=False
                )
                daemon.start()
            except Exception as e:
                logger.debug('%s start failed.', PackageInfo.pip_package_name)
                logger.exception(e)
                raise e
        else:
            sys.stdout.write('{0} is already running...\n'.format(PackageInfo.pip_package_name))
            sys.stdout.flush()
            sys.exit(1)

    @staticmethod
    def stop(**kwargs):
        logger = ClientLogger.setup()
        (opts, args) = ClientOptionParser().parse_args()

        # Attempt to gracefully shutdown...
        if ClientDaemon.__status(opts, args):
            ClientDaemon.__stop(opts, args)

        # if any processes still exists at this point... we will become more persuasive...
        try:
            for pid in check_output(['pgrep', '-f', '{0} start'.format(
                    PackageInfo.pip_package_name)]).splitlines():
                try:
                    call(['kill', '-9', pid])
                except Exception as e:
                    logger.exception(e)
        except CalledProcessError:
            pass

        # if the pid file still exist at this point... nuke it from orbit!
        pid_file = opts.get(ClientOption.PID_FILE)
        if os.path.isfile(pid_file):
            try:
                os.remove(pid_file)
            except Exception as e:
                logger.exception(e)
                raise e

    @staticmethod
    def restart():
        #TODO: not fully implemented
        raise NotImplementedError

        # TODO: restart should wait until the client is idle.. not in use...

        logger = ClientLogger.setup()
        try:
            ClientDaemon.stop()
            ClientDaemon.start()

        except Exception as e:
            logger.debug('%s restart failed.', PackageInfo.pip_package_name)
            logger.exception(e)
            raise e

    # noinspection PyUnusedLocal
    @staticmethod
    def status(**kwargs):
        logger = ClientLogger.setup()
        (opts, args) = ClientOptionParser().parse_args()
        status = ClientDaemon.__status(opts, args)
        if status:
            sys.stdout.write('Status: {0}\n'.format(status))
            sys.stdout.flush()
            sys.exit(0)

        sys.stdout.write('the {0} is unavailable...\n'
                         'It may need to be restarted, try: \'sudo {0} restart\'\n'
                         .format(PackageInfo.pip_package_name))
        sys.stdout.flush()
        sys.exit(1)

    @staticmethod
    def __status(opts, args):
        # noinspection PyBroadException
        try:
            with ClientSocket() as socket:
                return socket.send(opts, args)

        except Exception:
            pass

        return None

    @staticmethod
    def __stop(opts, args):
        logout_coast_time = opts.get(ClientOption.LOGOUT_COAST_TIME)

        # noinspection PyBroadException
        try:
            with ClientSocket(logout_coast_time + 5) as socket:
                socket.send(opts, args)

                # TODO: look for ways to exit early here...
                #time.sleep(logout_coast_time)

        except Exception:
            pass

        return None

