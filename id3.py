#!/usr/bin/python
import fileinput
from copy import copy
from math import log


#dataset's entropy
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
        
        gain -= (float(count)/rowcount)* entropy(attributes, filtered_data)
    
    # print gain
    return gain


def filter_data(data, value, attr_index):
    filtered_data = []
    #print str(attr_index) + ' = ' + value
    for row in data:
        if row[attr_index] == value:
            new_row = copy(row)
            #print 'row: ' + str(row)
            new_row.pop(attr_index)
            filtered_data.append(new_row)
    # print filtered_data
    return filtered_data


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
        #if not decision_tree[new_node]:
        #    decision_tree[new_node] = {}
        #    for row in data:
        #        decision_tree[new_node]['ANSWER'] = row[-1]

    return decision_tree


def print_tree(tree, attributes, identation = 0):
    print ' ' * identation
    if isinstance(tree, str):
        print tree
    else:
        for key, value in tree.iteritems():
            print key + ': ',
            print_tree(value, attributes, identation+2)


if __name__ == "__main__":
    relation = None
    attributes = []
    data = None
    
    for line in fileinput.input():
        line = line.replace('\n', '')
        line = line.replace('\r', '')
        
        if line.startswith('%') or not line.strip():
            # ignore comment
            continue
        elif line.startswith('@relation'):
            relation = line[len('@relation') + 1:]
        elif line.startswith('@attribute'):
            attr_name = line[len('@attribute') + 1:line.find('{')].replace('\t', '').replace(' ', '')
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
    print print_tree(decision_tree, attributes)