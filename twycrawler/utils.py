from json import load
import csv

queue_file = 'tmp/queue.tmp'
visited_file = 'tmp/visited.tmp'

def read_credentials(filename):
    json_file = open(filename)
    data = load(json_file)
    json_file.close()
    return data

# cache data
def save_queue(queue, visited):
    qwriter = csv.writer(open(queue_file, 'wb'))
    for id in queue:
        qwriter.writerow([id])
    vwriter = csv.writer(open(visited_file, 'wb'))
    for id in visited:
        vwriter.writerow([id])

def load_queue():
    try:
        qreader = csv.reader(open(queue_file, 'rb'))
        vreader = csv.reader(open(visited_file, 'rb'))
        queue = [int(row[0]) for row in qreader]
        visited = set([int(row[0]) for row in vreader])
    except IOError:
        queue = []
        visited = []
    return queue, visited
