#!/usr/bin/python3

from commandhandler import CommandHandler
from clockcreator import ClockCreator
from userbot import UserBot
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('command',
                    nargs='?',
                    default=False,
                    const='')

clock_bot = UserBot()


async def main():
    await clock_bot.connect()

    command = parser.parse_args().command
    if command:
        CommandHandler().handle(command)
    else:
        await clock_bot.upload_clock('next.png')

    ClockCreator().create_next()


if __name__ == '__main__':
    clock_bot.run(main)
