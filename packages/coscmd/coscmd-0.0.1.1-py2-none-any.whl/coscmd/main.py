# -*- coding: utf-8 -*-

from __future__ import absolute_import
from coscmd.client import CosConfig, CosS3Client
from argparse import ArgumentParser
from ConfigParser import SafeConfigParser
from os import path


def config(args):
    print "config: ", args

    conf_path = path.expanduser('~/.cos.conf')

    with open(conf_path, 'w+') as f:
        cp = SafeConfigParser()
        cp.add_section("common")
        cp.set('common', 'access_id', args.access_id)
        cp.set('common', 'secret_key', args.secret_key)
        cp.set('common', 'appid', args.appid)
        cp.set('common', 'bucket', args.bucket)
        cp.set('common', 'region', args.region)
        cp.write(f)
        print "Created configuration file in {path}".format(path=conf_path)


def load_conf():

    conf_path = path.expanduser('~/.cos.conf')
    if not path.exists(conf_path):
        print "{conf} couldn't be found, please config tool!".format(conf=conf_path)
	raise IOError
    else:
        print '{conf} is found.'.format(conf=conf_path)

    with open(conf_path, 'r') as f:
        cp = SafeConfigParser()
        cp.readfp(fp=f)
        conf = CosConfig(
            appid=cp.get('common', 'appid'),
            access_id=cp.get('common', 'access_id'),
            access_key=cp.get('common', 'secret_key'),
            region=cp.get('common', 'region'),
            bucket=cp.get('common', 'bucket')
        )
        return conf


def upload(args):
    conf = load_conf()
    print conf
    client = CosS3Client(conf)
    mp = client.multipart_upload_from_filename(args.local_file, args.object_name)
    mp.init_mp()
    mp.upload_parts()
    mp.complete_mp()
    
def _main():

    parser = ArgumentParser()
    sub_parser = parser.add_subparsers(help="config")
    parser_a = sub_parser.add_parser("config")
    parser_a.add_argument('-a', '--access_id', help='specify your access id', type=str, required=True)
    parser_a.add_argument('-s', '--secret_key', help='specify your secret key', type=str, required=True)
    parser_a.add_argument('-u', '--appid', help='specify your appid', type=str, required=True)
    parser_a.add_argument('-b', '--bucket', help='specify your bucket', type=str, required=True)
    parser_a.add_argument('-r', '--region', help='specify your bucket', type=str, required=True)
    parser_a.set_defaults(func=config)

    parser_b = sub_parser.add_parser("upload")
    parser_b.add_argument('local_file', help="local file path as /tmp/a.txt", type=str)
    parser_b.add_argument("object_name", help="object name as a/b.txt", type=str)
    parser_b.add_argument("-t", "--type", help="storage class type: standard/nearline/coldline", type=str, choices=["standard", "nearline", "coldline"], default="standard")
    parser_b.set_defaults(func=upload)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    _main()
