import os
import sys
import json
import logging
import threading
from copy import copy
from datetime import date, timedelta

import boto3
import requests
from six.moves.queue import Queue
from six import iteritems, iterkeys
from sentinel_s3.crawler import get_products_metadata_path, get_product_metadata_path
from sentinel_s3.converter import metadata_to_dict, tile_metadata

# Python 2 comptability
try:
    JSONDecodeError = json.JSONDecodeError
except AttributeError:
    JSONDecodeError = ValueError


logger = logging.getLogger('sentinel.meta.s3')

bucket_name = os.getenv('BUCKETNAME', 'sentinel-metadata')
s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name)


def mkdirp(path):

    if not os.path.exists(path):
        os.makedirs(path)


def file_writer(product_dir, metadata):
    mkdirp(product_dir)

    f = open(os.path.join(product_dir, metadata['tile_name'] + '.json'), 'w')
    f.write(json.dumps(metadata))
    f.close()


def s3_writer(product_dir, metadata):
    # make sure product_dir doesn't start with slash (/) or dot (.)
    if product_dir.startswith('.'):
        product_dir = product_dir[1:]

    if product_dir.startswith('/'):
        product_dir = product_dir[1:]

    key = os.path.join(product_dir, metadata['tile_name'] + '.json')
    s3.Object(bucket_name, key).put(json.dumps(metadata))
    object_acl = s3.ObjectAcl(bucket_name, key)
    object_acl.put(ACL='public-read')


def product_metadata(product, dst_folder, counter=None, writers=[file_writer], geometry_check=None):
    """ Extract metadata for a specific product """

    if not counter:
        counter = {
            'products': 0,
            'saved_tiles': 0,
            'skipped_tiles': 0,
            'skipped_tiles_paths': []
        }

    s3_url = 'http://sentinel-s2-l1c.s3.amazonaws.com'

    product_meta_link = '{0}/{1}'.format(s3_url, product['metadata'])
    product_info = requests.get(product_meta_link, stream=True)
    product_metadata = metadata_to_dict(product_info.raw)
    product_metadata['product_meta_link'] = product_meta_link

    counter['products'] += 1

    for tile in product['tiles']:
        tile_info = requests.get('{0}/{1}'.format(s3_url, tile))
        try:
            metadata = tile_metadata(tile_info.json(), copy(product_metadata), geometry_check)

            for w in writers:
                w(dst_folder, metadata)

            logger.info('Saving to disk: %s' % metadata['tile_name'])
            counter['saved_tiles'] += 1
        except JSONDecodeError:
            logger.warning('Tile: %s was not found and skipped' % tile)
            counter['skipped_tiles'] += 1
            counter['skipped_tiles_paths'].append(tile)

    return counter


def single_metadata(product_name, dst_folder, writers=[file_writer], geometry_check=None):

    product_list = get_product_metadata_path(product_name)
    return product_metadata(product_list[product_name], dst_folder, writers=writers, geometry_check=geometry_check)


def daily_metadata(year, month, day, dst_folder, writers=[file_writer], geometry_check=None,
                   num_worker_threads=1):
    """ Extra metadata for all products in a specific date """

    threaded = False

    counter = {
        'products': 0,
        'saved_tiles': 0,
        'skipped_tiles': 0,
        'skipped_tiles_paths': []
    }

    if num_worker_threads > 1:
        threaded = True
        queue = Queue()

    # create folders
    year_dir = os.path.join(dst_folder, str(year))
    month_dir = os.path.join(year_dir, str(month))
    day_dir = os.path.join(month_dir, str(day))

    product_list = get_products_metadata_path(year, month, day)

    logger.info('There are %s products in %s-%s-%s' % (len(list(iterkeys(product_list))),
                                                       year, month, day))

    for name, product in iteritems(product_list):
        product_dir = os.path.join(day_dir, name)

        if threaded:
            queue.put([product, product_dir, counter, writers, geometry_check])
        else:
            counter = product_metadata(product, product_dir, counter, writers, geometry_check)

    if threaded:
        def worker():
            while not queue.empty():
                args = queue.get()
                try:
                    product_metadata(*args)
                except Exception:
                    exc = sys.exc_info()
                    logger.error('%s tile skipped due to error: %s' % (threading.current_thread().name,
                                                                       exc[1].__str__()))
                    args[2]['skipped_tiles'] += 1
                queue.task_done()

        threads = []
        for i in range(num_worker_threads):
            t = threading.Thread(target=worker)
            t.start()
            threads.append(t)

        queue.join()

    return counter


def range_metadata(start, end, dst_folder, num_worker_threads=0, writers=[file_writer], geometry_check=None):
    """ Extra metadata for all products in a date range """

    assert isinstance(start, date)
    assert isinstance(end, date)

    delta = end - start

    dates = []

    for i in range(delta.days + 1):
        dates.append(start + timedelta(days=i))

    days = len(dates)

    total_counter = {
        'days': days,
        'products': 0,
        'saved_tiles': 0,
        'skipped_tiles': 0,
        'skipped_tiles_paths': []
    }

    def update_counter(counter):
        for key in iterkeys(total_counter):
            if key in counter:
                total_counter[key] += counter[key]

    for d in dates:
        logger.info('Getting metadata of {0}-{1}-{2}'.format(d.year, d.month, d.day))
        update_counter(daily_metadata(d.year, d.month, d.day, dst_folder, writers, geometry_check,
                                      num_worker_threads))

    return total_counter
