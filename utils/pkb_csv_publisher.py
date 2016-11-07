import argparse
import csv
import fnmatch
import json
import os
import sys

def parse_labels(labels):
    labels_sans_bars = labels.strip('|')
    key_value_list = labels_sans_bars.split('|,|')
    d = {}
    for kv in key_value_list:
        key,value = kv.split(':',1)
        d[key] = value
    return d


def load_json_samples(file_path):
    samples = []
    with open(file_path,'r') as fp:
        for line in fp:
            d = json.loads(line)
            d['metadata'] = parse_labels(d['labels'])
            del d['labels']
            samples.append(d)
    return samples


def write_samples_csv(samples, csv_name):
    _DEFAULT_FIELDS = ('timestamp', 'test', 'metric', 'value', 'unit',
        'product_name', 'official', 'owner', 'run_uri',
        'sample_uri')
    meta_keys = sorted(
            set(key for sample in samples for key in sample['metadata']))
    with open(csv_name, 'w') as fp:
        writer = csv.DictWriter(fp, list(self._DEFAULT_FIELDS) + meta_keys)
        writer.writeheader()
        for sample in samples:
            d = {}
            d.update(sample)
            d.update(d.pop('metadata'))
            writer.writerow(d)


def get_results_files(directory, file_regex='perfkitbenchmarker_results.json'):
    list_of_files = []
    for dirpath, dirs, files in os.walk(directory):
        for filename in fnmatch.filter(files, file_regex):
            list_of_files.append(os.path.join(dirpath, filename)
    return list_of_files


def load_workload_samples(file_list):
    samples = []
    for f in file_list:
        file_samples = load_json_samples(f)
        samples.extend(file_samples)
    return samples


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory',default=os.getcwd())
    parser.add_argument('-f', '--file', help='name of the output file')

    args = parser.parse_args()
    filelist = get_results_files(args.directory)
    samples = load_workload_samples(filelist)
    write_samples_csv(samples, args.file)


if __name__ == '__main__':
    main()
