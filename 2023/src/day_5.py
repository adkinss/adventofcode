#!/usr/bin/python3

from utils import read_multisection_input


def print_almanac(almanac):
    seeds, soil_map, fertilizer_map, water_map, light_map, \
        temperature_map, humidity_map, location_map = almanac

    print("Almanac:")
    print(f"seeds: {seeds}")
    print(f"soil: {soil_map}")
    print(f"fertilzer: {fertilizer_map}")
    print(f"water: {water_map}")
    print(f"light: {light_map}")
    print(f"temperature: {temperature_map}")
    print(f"humidity: {humidity_map}")
    print(f"location: {location_map}")
    print()


def print_map(map, title):
    print(f"{title} Map:")
    print(map)
    print()


def transformer(line):
    """
    Read each multiline section and return a list of lists.
    For the first section, return a single list containing the seeds to be
    examined. For the remaining sections, return one list for each line in the
    map which contains the destination, source and length values for the map.
    """
    values = []
    for s in line.split('\n'):
        if s[:6] == "seeds:":
            values = [int(seed) for seed in s[7:].split()]
            # We don't want to sort seeds (at the moment), so return now.
            return values
        if s[-4:] == "map:":
            # Skip the title line, we don't care what it says.
            # Fortunately, the map ordering in the input file never changes.
            continue
        if s != "":
            map = [int(m) for m in s.split(' ')]
            values.append(map)

    # Use bubble sort to sort the map by the source field (second field).
    # This is simply a convenience to make it easier when working with ranges.
    n = len(values)
    for i in range(n):
        for j in range(n - 1):
            if values[j][1] > values[j + 1][1]:
                values[j], values[j + 1] = values[j + 1], values[j]

    return values


def find_destination(map, resource):
    """
    For a given resource (seed, soil, fertilizer, etc), find the location for
    that resource in the map provided. If the resource isn't found in the map,
    then return the resource as the result. The provided map must match the
    resource type that needs found.
    """
    for m in map:
        destination, source, length = m
        while length > 0:
            if source == resource:
                return destination
            # If length is a ridiculously long number, it would take too long
            # to increment source and destination by 1 and decrement length by 1.
            # Be smart. We know the resource location. Jump straight to it.
            # We only want to do this is the resource is greater than the source.
            if resource < source: break
            jump = resource - source
            destination += jump
            source += jump
            length -= jump

    # Return the resource itself if it was not found in a map
    return resource


def find_location_from_seeds(almanac, my_seeds):
    """
    For each seed, do a series of lookups in each map to determine the location
    of that seed. Allow seeds to be overridden on input. Return the smallest
    location for all the seeds examined.
    """
    seeds, soil_map, fertilizer_map, water_map, light_map, \
        temperature_map, humidity_map, location_map = almanac

    if my_seeds:
        seeds = my_seeds

    minimum_location = 0
    for seed in seeds:
        soil = find_destination(soil_map, seed)
        fertilizer = find_destination(fertilizer_map, soil)
        water = find_destination(water_map, fertilizer)
        light = find_destination(light_map, water)
        temperature = find_destination(temperature_map, light)
        humidity = find_destination(humidity_map, temperature)
        location = find_destination(location_map, humidity)
        if not minimum_location or location < minimum_location:
            minimum_location = location

    return minimum_location


def find_location_from_seed_pairs(almanac, my_seeds):
    """
    For each seed, do a series of lookups in each map to determine the location
    of that seed. Allow seeds to be overridden on input. Return the smallest
    location for all the seeds examined.
    """
    seeds, soil_map, fertilizer_map, water_map, light_map, \
        temperature_map, humidity_map, location_map = almanac

    if my_seeds:
        seeds = my_seeds

    unknown_ranges = []
    new_seeds = []

    print(f"STARTING: {seeds}")
    for starting_seed, seed_range in zip(seeds[::2], seeds[1::2]):
        ending_seed = starting_seed + seed_range - 1

        for l in soil_map:
            destination, source, length = l
            ending_source = source + length - 1

            if starting_seed < source:
                if ending_seed < source:
                    unknown_ranges.append([starting_seed, ending_seed])
                    starting_seed = ending_seed = -1
                    break
                unknown_ranges.append([starting_seed, source - 1])
                starting_seed = source

            if starting_seed >= source and starting_seed <= ending_source:
                new_seeds.append(starting_seed)
                if ending_seed <= ending_source:
                    starting_seed = ending_seed = -1
                    break
                starting_seed = ending_source + 1

        if starting_seed != -1:
            unknown_ranges.append([starting_seed, ending_seed])

    print(f"Soil:\nUnknown Ranges: {unknown_ranges}")
    print(f"New Seeds: {new_seeds}\n")

    if not unknown_ranges:
        return new_seeds

    print("NEXT ROUND\n")

    seeds = unknown_ranges[0]
    unknown_ranges = []
    print(f"STARTING: {seeds}")
    for starting_seed, ending_seed in zip(seeds[::2], seeds[1::2]):
        print(f"Starting Seed: {starting_seed} Ending Seed: {ending_seed}")
        for l in fertilizer_map:
            destination, source, length = l
            ending_source = source + length - 1

            if starting_seed < source:
                if ending_seed < source:
                    unknown_ranges.append([starting_seed, ending_seed])
                    starting_seed = ending_seed = -1
                    break
                unknown_ranges.append([starting_seed, source - 1])
                starting_seed = source

            if starting_seed >= source and starting_seed <= ending_source:
                new_seeds.append(starting_seed)
                if ending_seed <= ending_source:
                    starting_seed = ending_seed = -1
                    break
                starting_seed = ending_source + 1

        if starting_seed != -1:
            unknown_ranges.append([starting_seed, ending_seed])

    print(f"Fertilzer:\nUnknown Ranges: {unknown_ranges}")
    print(f"New Seeds: {new_seeds}\n")

    if not unknown_ranges:
        return new_seeds

    print("NEXT ROUND\n")

    seeds = unknown_ranges[0]
    unknown_ranges = []
    print(f"STARTING: {seeds}")
    for starting_seed, ending_seed in zip(seeds[::2], seeds[1::2]):
        print(f"Starting Seed: {starting_seed} Ending Seed: {ending_seed}")
        for l in water_map:
            destination, source, length = l
            ending_source = source + length - 1

            if starting_seed < source:
                if ending_seed < source:
                    unknown_ranges.append([starting_seed, ending_seed])
                    starting_seed = ending_seed = -1
                    break
                unknown_ranges.append([starting_seed, source - 1])
                starting_seed = source

            if starting_seed >= source and starting_seed <= ending_source:
                new_seeds.append(starting_seed)
                if ending_seed <= ending_source:
                    starting_seed = ending_seed = -1
                    break
                starting_seed = ending_source + 1

        if starting_seed != -1:
            unknown_ranges.append([starting_seed, ending_seed])

    print(f"Water:\nUnknown Ranges: {unknown_ranges}")
    print(f"New Seeds: {new_seeds}\n")

    if not unknown_ranges:
        return new_seeds

    print("NEXT ROUND\n")

    seeds = unknown_ranges[0]
    unknown_ranges = []
    print(f"STARTING: {seeds}")
    for starting_seed, ending_seed in zip(seeds[::2], seeds[1::2]):
        print(f"Starting Seed: {starting_seed} Ending Seed: {ending_seed}")
        for l in light_map:
            destination, source, length = l
            ending_source = source + length - 1

            if starting_seed < source:
                if ending_seed < source:
                    unknown_ranges.append([starting_seed, ending_seed])
                    starting_seed = ending_seed = -1
                    break
                unknown_ranges.append([starting_seed, source - 1])
                starting_seed = source

            if starting_seed >= source and starting_seed <= ending_source:
                new_seeds.append(starting_seed)
                if ending_seed <= ending_source:
                    starting_seed = ending_seed = -1
                    break
                starting_seed = ending_source + 1

        if starting_seed != -1:
            unknown_ranges.append([starting_seed, ending_seed])

    print(f"Light:\nUnknown Ranges: {unknown_ranges}")
    print(f"New Seeds: {new_seeds}\n")

    if not unknown_ranges:
        return new_seeds

    print("NEXT ROUND\n")

    seeds = unknown_ranges[0]
    unknown_ranges = []
    print(f"STARTING: {seeds}")
    for starting_seed, ending_seed in zip(seeds[::2], seeds[1::2]):
        print(f"Starting Seed: {starting_seed} Ending Seed: {ending_seed}")
        for l in temperature_map:
            destination, source, length = l
            ending_source = source + length - 1

            if starting_seed < source:
                if ending_seed < source:
                    unknown_ranges.append([starting_seed, ending_seed])
                    starting_seed = ending_seed = -1
                    break
                unknown_ranges.append([starting_seed, source - 1])
                starting_seed = source

            if starting_seed >= source and starting_seed <= ending_source:
                new_seeds.append(starting_seed)
                if ending_seed <= ending_source:
                    starting_seed = ending_seed = -1
                    break
                starting_seed = ending_source + 1

        if starting_seed != -1:
            unknown_ranges.append([starting_seed, ending_seed])

    print(f"Temperature:\nUnknown Ranges: {unknown_ranges}")
    print(f"New Seeds: {new_seeds}\n")

    if not unknown_ranges:
        return new_seeds

    print("NEXT ROUND\n")

    seeds = unknown_ranges[0]
    unknown_ranges = []
    print(f"STARTING: {seeds}")
    for starting_seed, ending_seed in zip(seeds[::2], seeds[1::2]):
        print(f"Starting Seed: {starting_seed} Ending Seed: {ending_seed}")
        for l in humidity_map:
            destination, source, length = l
            ending_source = source + length - 1

            if starting_seed < source:
                if ending_seed < source:
                    unknown_ranges.append([starting_seed, ending_seed])
                    starting_seed = ending_seed = -1
                    break
                unknown_ranges.append([starting_seed, source - 1])
                starting_seed = source

            if starting_seed >= source and starting_seed <= ending_source:
                new_seeds.append(starting_seed)
                if ending_seed <= ending_source:
                    starting_seed = ending_seed = -1
                    break
                starting_seed = ending_source + 1

        if starting_seed != -1:
            unknown_ranges.append([starting_seed, ending_seed])

    print(f"Humidity:\nUnknown Ranges: {unknown_ranges}")
    print(f"New Seeds: {new_seeds}\n")

    if not unknown_ranges:
        return new_seeds

    print("NEXT ROUND\n")

    seeds = unknown_ranges[0]
    unknown_ranges = []
    print(f"STARTING: {seeds}")
    for starting_seed, ending_seed in zip(seeds[::2], seeds[1::2]):
        print(f"Starting Seed: {starting_seed} Ending Seed: {ending_seed}")
        for l in location_map:
            destination, source, length = l
            ending_source = source + length - 1

            if starting_seed < source:
                if ending_seed < source:
                    unknown_ranges.append([starting_seed, ending_seed])
                    starting_seed = ending_seed = -1
                    break
                unknown_ranges.append([starting_seed, source - 1])
                starting_seed = source

            if starting_seed >= source and starting_seed <= ending_source:
                new_seeds.append(starting_seed)
                if ending_seed <= ending_source:
                    starting_seed = ending_seed = -1
                    break
                starting_seed = ending_source + 1

        if starting_seed != -1:
            unknown_ranges.append([starting_seed, ending_seed])

    print(f"Location:\nUnknown Ranges: {unknown_ranges}")
    print(f"New Seeds: {new_seeds}\n")

    if not unknown_ranges:
        return new_seeds

    return new_seeds


almanac = read_multisection_input("5", transformer, example=True)
distance = find_location_from_seeds(almanac, [])
print(f'Part 1 Example: {distance}\tExpecting: 35')

# seeds = find_location_from_seed_pairs(almanac, [4149283325, 4269624551])
seeds = find_location_from_seed_pairs(almanac, [])
distance = find_location_from_seeds(almanac, seeds)
print(f'Part 2 Example: {distance}\tExpecting: 46')
print()
exit(0)

almanac = read_multisection_input("5", transformer, example=False)
distance = find_location_from_seeds(almanac, [])
print(f'Part 1: {distance}\tExpecting: 403695602')
seeds = find_location_from_seed_pairs(almanac, [])
distance = find_location_from_seeds(almanac, seeds)
print(f'Part 2: {distance}\tExpecting: Unknown')
