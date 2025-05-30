#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2024 Vasiliy Stelmachenok <ventureo@yandex.ru>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import argparse
import asyncio
import configparser
import logging

from jabagram.database.chats import ChatStorage
from jabagram.database.stickers import StickerCache
from jabagram.database.topics import TopicNameCache
from jabagram.dispatcher import MessageDispatcher
from jabagram.messages import Messages
from jabagram.service import ChatService
from jabagram.telegram.client import TelegramClient
from jabagram.xmpp.client import XmppClient
from os import path

CONFIG_FILE_NOT_FOUND = """
Configuration file not found.
Perhaps you forgot to rename config.ini.example?
Use the -c key to specify the full path to the config.
"""
def main():
    parser = argparse.ArgumentParser(
        prog='jabagram',
        description='Bridge beetween Telegram and XMPP',
    )
    parser.add_argument(
        '-c', '--config', default="config.ini",
        dest="config", help="path to configuration file"
    )
    parser.add_argument(
        '-d', '--data', default="jabagram.db",
        dest="data", help="path to bridge database"
    )
    parser.add_argument(
        '-v', '--verbose', dest="verbose",
        action='store_true', help="output debug information",
    )

    parser.add_argument(
        '--password', dest="xmpp_passwd"
    )
    parser.add_argument(
        '--jid',dest="xmpp_jid"
    )
    parser.add_argument(
        '--token',dest="tg_token"
    )

    parser.add_argument(
        '--topic_id',dest="topic_id"
    )
    
    global args
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(
            filename=None if path.exists("/.dockerenv") else "jabagram.log",
            filemode='a',
            format="[%(asctime)s] %(name)s - %(levelname)s: %(message)s",
            level=logging.DEBUG
        )
    else:
        logging.basicConfig(
            format="[%(asctime)s] %(name)s - %(levelname)s: %(message)s",
            level=logging.INFO
        )

    logger = logging.Logger("Runner")

    try:
        config = configparser.ConfigParser(interpolation=None)
        messages = Messages(config)
        if args.xmpp_jid and args.xmpp_passwd and args.tg_token:
            with open("config.example.ini", "r", encoding="utf-8") as f:
                config.read_file(f)
           
            config.set("xmpp","password",args.xmpp_passwd)
            config.set("xmpp","login",args.xmpp_jid)
            config.set("telegram","token",args.tg_token)

        
        else:
            with open(args.config, "r", encoding="utf-8") as f:

                config.read_file(f)
        
        

        messages.load()
        chat_storage = ChatStorage(path=args.data)
        sticker_cache = StickerCache(path=args.data)
        topic_name_cache = TopicNameCache(path=args.data)

        if not all([
            chat_storage.create(),
            sticker_cache.create(),
            topic_name_cache.create()
        ]):
            logger.error("Error when working with the database, interrupt...")
            return

        loop = asyncio.get_event_loop()

        service: ChatService = ChatService(
            storage=chat_storage,
            key=config.get("general", "key")
        )
        dispatcher: MessageDispatcher = MessageDispatcher(
            storage=chat_storage
        )
        telegram = TelegramClient(
            config.get("telegram", "token"),
            config.get("xmpp", "login"),
            service,
            dispatcher,
            topic_name_cache,
            messages,
            max_limit=int(config.get("privatebin","limited_length")) or 1000,
            privatebin_address=config.get("privatebin","api_address") or "https://0.0g.gg/",
            topic_id=args.topic_id

        )
        xmpp = XmppClient(
            config.get("xmpp", "login"),
            config.get("xmpp", "password"),
            service,
            dispatcher,
            sticker_cache,
            messages,
            max_limit=int(config.get("privatebin","limited_length")) or 1000,
            privatebin_address=config.get("privatebin","api_address") or "https://0.0g.gg/",
            topic_id=args.topic_id
        )
        
        loop.create_task(telegram.start())
        loop.create_task(xmpp.start())
        loop.create_task(dispatcher.start())
        loop.run_forever()
    except FileNotFoundError:
        logger.error(CONFIG_FILE_NOT_FOUND)
    except configparser.NoOptionError:
        logger.exception("Missing mandatory option")
    except configparser.Error:
        logger.exception("Config parsing error")


if __name__ == "__main__":
    main()
