import os
import re
import logging
import click
import threading
import queue
import signal

from time import sleep
from boto import s3, connect_s3
from configstruct import ConfigStruct

from .worker import Worker
from .progress import S3KeyProgress
from .jobs import S3ListJob

SHARDS = ([chr(i) for i in range(ord('a'), ord('z') + 1)] +
          [chr(i) for i in range(ord('0'), ord('9') + 1)])

DEFAULTS = {
    'log_level': 'info',
    'log_file': 'STDERR',
    'concurrency': len(SHARDS),
}

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-c', '--config-file', type=click.Path(dir_okay=False, writable=True),
              default=os.path.join(os.path.expanduser('~'), '.s3tailrc'),
              help='Configuration file', show_default=True)
@click.option('-r', '--region', type=click.Choice(r.name for r in s3.regions()),
              help='AWS region to use when connecting')
@click.option('-l', '--log-level',
              type=click.Choice(['debug', 'info', 'warning', 'error', 'critical']),
              help='set logging level')
@click.option('--log-file', metavar='FILENAME', help='write logs to FILENAME')
@click.option('--concurrency', type=int, default=len(SHARDS))
@click.option('--select', 'selection_string')
@click.option('--accumulator', 'accumulation_string', default='0')
@click.option('--reduce', 'reduction_string')
@click.argument('command', type=click.Choice(['list', 'delete']))
@click.argument('s3_uri')
def main(config_file, region, log_level, log_file, concurrency,
         selection_string, accumulation_string, reduction_string,
         command, s3_uri):
    '''Perform simple listing, collating, or deleting of many S3 objects at the same time.'''

    config = ConfigStruct(config_file, options=DEFAULTS)
    opts = config.options

    # let command line options have temporary precedence if provided values
    opts.might_prefer(region=region, log_level=log_level, log_file=log_file,
                      concurrency=concurrency)

    s3_uri = re.sub(r'^(s3:)?/+', '', s3_uri)
    bucket, prefix = s3_uri.split('/', 1)

    log_kwargs = {
        'level': getattr(logging, opts.log_level.upper()),
        'format': '[%(asctime)s #%(process)d] %(levelname)-8s %(name)-12s %(message)s',
        'datefmt': '%Y-%m-%dT%H:%M:%S%z',
    }
    if opts.log_file != 'STDERR':
        log_kwargs['filename'] = opts.log_file
    logging.basicConfig(**log_kwargs)
    logger = logging.getLogger(__name__)

    progress = S3KeyProgress()

    accumulator = None
    if reduction_string:
        accumulator = eval(accumulation_string)
        accumulator_lock = threading.Lock()
        reducer_code = compile('def reducer(accumulator, name, size, last_modified): ' +
                               reduction_string +
                               '; return accumulator', 's3workers.cli', 'exec')
        exec(reducer_code, {}, {})

        def key_dumper(key):
            global accumulator
            with accumulator_lock:
                accumulator = reducer(accumulator, key.name, key.size,  # noqa: F821
                                      key.last_modified)
                progress.write('%s %10d %s %s => %s',
                               key.last_modified, key.size, key.md5, key.name, accumulator)
    else:
        def key_dumper(key):
            progress.write('%s %10d %s %s', key.last_modified, key.size, key.md5, key.name)

    def key_deleter(key):
        progress.write('DELETING: %s %10d %s %s', key.last_modified, key.size, key.md5, key.name)
        key.delete()

    work = queue.Queue(opts.concurrency * 3)
    workers = []

    for i in range(opts.concurrency):
        worker = Worker(work)
        worker.start()
        workers.append(worker)

    stopped = threading.Event()

    def stop_work(*args):
        stopped.set()
        logger.info('Stopping! work_item_count=%d', work.qsize())
        for worker in workers:
            if worker.is_alive():
                logger.debug(worker)
                worker.stop()

    signal.signal(signal.SIGINT, stop_work)
    signal.signal(signal.SIGTERM, stop_work)
    signal.signal(signal.SIGPIPE, stop_work)

    s3_uri = re.sub(r'^(s3:)?/+', '', s3_uri)
    bucket_name, prefix = s3_uri.split('/', 1)

    selector = compile(selection_string, '<select>', 'eval') if selection_string else None
    handler = key_deleter if command == 'delete' else key_dumper

    conn = s3.connect_to_region(opts.region) if opts.region else connect_s3()
    bucket = conn.get_bucket(bucket_name)

    logger.info('Preparing %d jobs for %d workers', len(SHARDS) * len(SHARDS), len(workers))

    # break up jobs into 2 char prefix elements
    for shard1 in SHARDS:
        if stopped.isSet():
            break
        for shard2 in SHARDS:
            if stopped.isSet():
                break
            prefix_shard = prefix + shard1 + shard2
            job = S3ListJob(bucket, prefix_shard, selector, handler, progress.report)
            logger.debug('Submitting %s', job)
            work.put(job)

    Worker.all_jobs_submitted()
    logger.debug('All jobs submitted. Waiting on %d to complete.', work.qsize())

    while threading.active_count() > 1:
        sleep(0.1)

    for worker in workers:
        worker.join(1)

    progress.finish()

    if accumulator:
        click.echo('accumulator: ' + str(accumulator))


if __name__ == '__main__':
    main()
