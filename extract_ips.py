import re
import itertools


def get_range(line):
    match = re.search('\((\d+.\d+.\d+.\d+) - (\d+.\d+.\d+.\d+)\)', line)
    if match:
        return [match.group(1), match.group(2)]


def expand_range(ip_range_entry):
    print "Working with range: [%s] - [%s]" % (ip_range_entry[0], ip_range_entry[1])
    ip_a_parts = ip_range_entry[0].split('.')
    ip_b_parts = ip_range_entry[1].split('.')
    klass = -1
    prefix = ''

    for index in range(len(ip_a_parts)):
        if ip_a_parts[index] != ip_b_parts[index]:
            klass = index
            break

        prefix += ip_a_parts[index] + '.'

    prefix = prefix[0:-1]

    if klass == -1:
        return

    print "Class %s IP range detected." % ['A', 'B', 'C', 'D'][klass]
    klass_values = {}
    for index in range(klass, klass + len(ip_a_parts) - klass):
        klass_values[index] = map(str, range(int(ip_a_parts[index]),
                                             int(ip_b_parts[index]) + 1))

    running_permutations = klass_values[klass]
    if len(klass_values) > 1:
        for index in range(klass + 1, klass + len(klass_values)):
            running_permutations = itertools.product(running_permutations, klass_values[index])

    permutations = map(lambda x: prefix + accumulate_parts(x), running_permutations)
    print "Range expanded to %d IP addresses." % len(permutations)
    return permutations


def accumulate_parts(p):
    return {str: lambda x: '.' + x,
            tuple: lambda x: ''.join(map(accumulate_parts, x))}.get(type(p))(p)


print accumulate_parts("s")
print accumulate_parts(("s", "c"))

input_file_handle = open('amazon_eu_ireland_ips.txt', 'r')
lines = input_file_handle.readlines()
input_file_handle.close()
ranges = map(get_range, lines)

output_file_handle = open('expanded_ips.txt', 'w')
for r in ranges:
    output_file_handle.writelines(map(lambda x: x + '\n', expand_range(r)))
output_file_handle.close()
