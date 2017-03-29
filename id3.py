#! /usr/bin/python
import fileinput
from copy import copy
from math import log


# dataset's entropy
def entropy(attributes, data):
    total = 0
    rowcount = len(data)
    for value in attributes[-1]['values']:
        count = 0
        for row in data:
            if row[-1] == value:
                count += 1
        if count != 0:
            total -= (float(count)/rowcount) * log(float(count)/rowcount, 2)
        # print float(count)/rowcount
    # print total
    return total


# information gain based on selected attribute
def gain(data, entr, attributes, attr_index):
    gain = entr
    rowcount = len(data)
    for value in attributes[attr_index]['values']:
        count = 0
        filtered_data = []
        for row in data:
            if row[attr_index] == value:
                count += 1
                filtered_data.append(row)

        gain -= (float(count)/rowcount) * entropy(attributes, filtered_data)

    # print gain
    return gain


# create new dataset filtered by an attribute's value
def filter_data(data, value, attr_index):
    filtered_data = []
    for row in data:
        if row[attr_index] == value:
            new_row = copy(row)
            new_row.pop(attr_index)
            filtered_data.append(new_row)
    return filtered_data


# build decision tree as a dict structure
def create_id3(attributes, data):
    decision_tree = {}

    # if there's only the result attribute left
    if len(attributes) == 1:
        decision_tree['ANSWER'] = data[0][-1]
        return decision_tree

    entr = entropy(attributes, data)
    maxgain = (-1, -1)  # attribute index, gain
    for i in range(len(attributes[:-1])):
        attr_gain = gain(data, entr, attributes, i)
        if attr_gain > maxgain[1]:
            maxgain = (i, attr_gain)

    # if there's no more gain, an answer has been reached
    if maxgain[1] == 0:
        for row in data:
            decision_tree['ANSWER'] = row[-1]
            return decision_tree

    attr_name = attributes[maxgain[0]]['name']
    new_attributes = copy(attributes)
    new_attributes.pop(maxgain[0])
    # print new_attributes

    for value in attributes[maxgain[0]]['values']:
        # print attr_name + ': ' + value
        new_data = filter_data(data, value, maxgain[0])
        new_node = attr_name + ': ' + value
        decision_tree[new_node] = create_id3(new_attributes, new_data)

    return decision_tree


# prints tree following the attribute's order
def print_tree(tree, attributes, identation=0):
    if len(tree) > 1:
        attr_name = tree.keys()[0].split(': ')[0]
        # find attribute used by tree node
        for attr in attributes:
            if attr['name'] == attr_name:
                # iterate attr values following input order
                for value in attr['values']:
                    # find tree node using current value
                    for node in tree.keys():
                        if value == node.split(': ')[1]:
                            for i in range(0, identation):
                                print '',
                            print node
                            print_tree(tree[node], attributes, identation+2)
                break

    # if it's a leaf, print as answer
    else:
        for i in range(0, identation):
            print '',

        print 'ANSWER: ' + tree.values()[0]


# reads input in ARFF format
if __name__ == "__main__":
    relation = None
    attributes = []
    data = None

    # parse input file
    for line in fileinput.input():
        line = line.replace('\n', '')
        line = line.replace('\r', '')

        if line.startswith('%') or not line.strip():
            # ignore comment
            continue
        elif line.startswith('@relation'):
            relation = line[len('@relation') + 1:]
        elif line.startswith('@attribute'):
            attr_name = line[len('@attribute') + 1:line.find('{')]
            attr_name = attr_name.replace('\t', '').replace(' ', '')
            attr_values = line[line.find('{') + 1: -1].split(', ')
            attributes.append({'name': attr_name, 'values': attr_values})
        elif line.startswith('@data'):
            data = []
        else:
            data.append(line.split(','))

    # print relation
    # print attributes
    # print data

    decision_tree = create_id3(attributes, data)
    print_tree(decision_tree, attributes)
