# -*- coding: utf-8 -*-

import logging
from os.path import basename

from .utils import generate_href, href_safe

logger = logging.getLogger(__name__)


def repair_storage(storage, repair_unsafe_uid):
    seen_uids = set()
    all_hrefs = list(storage.list())
    for i, (href, _) in enumerate(all_hrefs):
        item, etag = storage.get(href)
        logger.info(u'[{}/{}] Processing {}'
                    .format(i, len(all_hrefs), href))

        new_item = item

        if item.parsed is None:
            logger.warning('Item {} can\'t be parsed, skipping.'
                           .format(href))
            continue

        if not item.uid:
            logger.warning('No UID, assigning random one.')
            new_item = item.with_uid(generate_href())
        elif item.uid in seen_uids:
            logger.warning('Duplicate UID, assigning random one.')
            new_item = item.with_uid(generate_href())
        elif not href_safe(item.uid) or not href_safe(basename(href)):
            if not repair_unsafe_uid:
                logger.warning('UID or href may cause problems, add '
                               '--repair-unsafe-hrefs to repair.')
            else:
                logger.warning('UID or href is unsafe, assigning random UID.')
                new_item = item.with_uid(generate_href(item.uid))

        if not new_item.uid:
            logger.error('Item {!r} is malformed beyond repair. '
                         'This is a serverside bug.'
                         .format(href))
            logger.error('Item content: {!r}'.format(item.raw))
            continue

        seen_uids.add(new_item.uid)
        if new_item.raw != item.raw:
            try:
                if new_item.uid != item.uid:
                    storage.upload(new_item)
                    storage.delete(href, etag)
                else:
                    storage.update(href, new_item, etag)
            except Exception:
                logger.exception('Server rejected new item.')
