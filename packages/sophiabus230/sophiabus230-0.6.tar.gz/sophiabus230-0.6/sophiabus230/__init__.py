#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module fetches the timetable of the bus 230 in Sophia Antipolis
"""
import re
import logging
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse
from dateutil.tz import gettz
from bs4 import BeautifulSoup
from future.moves.urllib import request


def _get_html_from_cg06(stop_id):
    """
    Requests the timetable from the cg06 website

    :param stop_id: the stop to fetch the timetable for
    :return: The result of the request as a html content
    :rtype: str
    """
    cg06_url = "http://cg06.tsi.cityway.fr/qrcode/?id={0}"
    req = request.urlopen(cg06_url.format(stop_id))
    content = req.read()
    return content


def _sanitize_entry(entry, debug=False):
    """
    Sanitize the entry by removing the extra spaces and empty lines

    :param entry: the entry to sanitize
    :return: the entry without unnecessary spaces
    :rtype: str
    """
    if debug:
        logging.basicConfig(level=logging.INFO)
        logging.info("To sanitize: |%s|", entry)
    sane_line = re.sub(r"^\s+$", '\n', entry)
    sane_line = re.sub(r"\s+$", '', sane_line)
    sane_line = re.sub(r"^\s+", '', sane_line)
    sane_line.replace(u"é", "e")
    if len(sane_line) > 1:
        return sane_line
    logging.info('empty entry !')
    return None


def _parse_entry(entry, debug=False):
    """
    Convert a entry into a dict containing the following attributes:

    - bus_time
    - dest
    - is_real_time

    :param entry: the string representation of one bus passage
    :return: a dict representing the relevant information of the string
    :rtype: dict
    """
    if debug:
        logging.basicConfig(level=logging.INFO)
        logging.info("parsing the following entry: %s", entry)

    split_entry = entry.split(' ')
    if debug:
        logging.info("split entry: %s", split_entry)
    idx_end_direction = len(split_entry)
    is_real_time = True
    tz_paris = gettz('Europe/Paris')
    if split_entry[-1] == '*':
        is_real_time = False
        idx_end_direction = len(split_entry) - 1
    if split_entry[0] == 'dans':
        # case for immediate upcoming bus
        date_now = datetime.now(tz=tz_paris)
        delta_minutes = int(split_entry[1])
        bus_time = date_now + timedelta(minutes=delta_minutes)
        idx_start_direction = 4
    else:
        if 'approche' in split_entry[1]:
            bus_time = datetime.now(tz=tz_paris)
        else:
            # case for later upcoming bus
            tzinfos = {'FR': tz_paris}
            bus_time = parse(split_entry[1], tzinfos=tzinfos)
            bus_time.replace(tzinfo=tz_paris)
        idx_start_direction = 3
    dest = ' '.join(split_entry[idx_start_direction:idx_end_direction])
    parsed_entry = {'bus_time': bus_time, 'dest': dest, 'is_real_time': is_real_time}
    if debug:
        logging.info("parsed entry: %s", parsed_entry)
    return parsed_entry


def get_next_buses(stop_id=1939, bus_id=230, debug=False):
    """
    Fetches the list of upcoming buses at the INRIA bus stop for the bus 230 towards Nice

    :return: upcoming buses
    :rtype: list
    """
    if debug:
        logging.basicConfig(level=logging.INFO)
    tt = []
    content = _get_html_from_cg06(stop_id)
    soup = BeautifulSoup(content, "html.parser")
    data = [e for e in soup.find_all("div", attrs={"class": "data"}) if str(bus_id) in e.get_text()]
    if len(data) != 0:
        assert len(data) <= 1
        data_230 = data[0].div.get_text()
        data_230 = data_230.replace(u"à ", u"DELIMITERà ")
        data_230 = data_230.replace("dans ", "DELIMITERdans ")
        for e in data_230.split('DELIMITER'):
            sane_entry = _sanitize_entry(e, debug)
            if sane_entry is not None:
                if debug:
                    logging.info('found: %s', sane_entry.encode('utf-8'))
                tt.append(_parse_entry(sane_entry, debug))
    return tt
