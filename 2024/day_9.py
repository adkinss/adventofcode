#!/usr/bin/python3

from utils import read_stream


def transformer(line):
    [disk, files, empty] = [[], [], []]
    [pos, block, toggle] = [0, 0, True]
    for l in list(line.rstrip()):
        if toggle:
            disk += [block] * int(l)
            files.append([pos, int(l)])
            block += 1
        elif int(l) > 0:
            disk += [-1] * int(l)
            empty.append([pos, int(l)])
        pos += int(l)
        toggle = not toggle
    return disk, files, empty


def is_defragged(disk):
    for free in range(len(disk)):
        if disk[free] == -1: break
    for used in range(len(disk) - 1, -1, -1):
        if disk[used] != -1: break
    return [free >= used, free, used]


def defrag_disk_by_block(disk):
    [done, free, used] = is_defragged(disk)
    while not done:
        disk[free] = disk[used]
        disk[used] = -1
        [done, free, used] = is_defragged(disk)

    checksum = 0
    for pos in range(len(disk)):
        if disk[pos] == -1: continue
        checksum += pos * disk[pos]
    return checksum


def defrag_disk_by_file(disk, files, empty):
    max_id = 0
    for block in disk:
        if disk[block] > max_id: max_id = disk[block]

    for file_id in range(len(files) - 1, -1, -1):
        [fp, fl] = files[file_id]
        for empty_id in range(len(empty)):
            [ep, el] = empty[empty_id]
            if el <= 0: continue
            if ep >= fp: break
            if fl > el: continue
            for i in range(fp, fp + fl):
                rel = i - fp
                disk[ep + rel] = disk[fp + rel]
                disk[fp + rel] = -1
            empty[empty_id] = [ep + fl, el - fl]
            files[file_id] = [fp, 0]
            break

    checksum = 0
    for pos in range(len(disk)):
        if disk[pos] == -1: continue
        checksum += pos * disk[pos]
    return checksum


[disk, files, empty] = read_stream('9', transformer, example=True)
total = defrag_disk_by_block(disk)
print(f'Part 1 Example:\t{total}\t\tIs Correct? {total == 1928}')

[disk, files, empty] = read_stream('9', transformer, example=False)
total = defrag_disk_by_block(disk)
print(f'Part 1 Actual:\t{total}\tIs Correct? {total == 6310675819476}')

[disk, files, empty] = read_stream('9', transformer, example=True)
total = defrag_disk_by_file(disk, files, empty)
print(f'Part 2 Example:\t{total}\t\tIs Correct? {total == 2858}')

[disk, files, empty] = read_stream('9', transformer, example=False)
total = defrag_disk_by_file(disk, files, empty)
print(f'Part 2 Actual:\t{total}\tIs Correct? {total == 6335972980679}')
