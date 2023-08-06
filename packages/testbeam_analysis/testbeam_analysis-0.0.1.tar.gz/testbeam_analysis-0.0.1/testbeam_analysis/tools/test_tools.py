''' Helper functions for the unittests are defined here.
'''

import numpy as np
import tables as tb


def nan_to_num(array):
    ''' Like np.nan_to_num but also works on recarray
    '''
    if array.dtype.names is None:  # normal nd.array
        array = np.nan_to_num(array)
    else:
        for column_name in array.dtype.names:
            array[column_name] = np.nan_to_num(array[column_name])


def get_array_differences(first_array, second_array):
    '''Takes two numpy.ndarrays and compares them on a column basis.
    Different column data types, missing columns and columns with different values are returned in a string.

    Parameters
    ----------
    first_array : numpy.ndarray
    second_array : numpy.ndarray

    Returns
    -------
    string
    '''
    if first_array.dtype.names is None:  # normal nd.array
        return ': Sum first array: ' + str(np.sum(first_array)) + ', Sum second array: ' + str(np.sum(second_array))
    else:
        return_str = ''
        for column_name in first_array.dtype.names:
            first_column = first_array[column_name]
            nan_to_num(first_column)  # Otherwise check with nan fails
            try:
                second_column = second_array[column_name]
                nan_to_num(second_column)  # Otherwise check with nan fails
            except ValueError:
                return_str += 'No ' + column_name + ' column found. '
                continue
            if (first_column.dtype != second_column.dtype):
                return_str += 'Column ' + column_name + ' has different data type. '
            if (first_column.shape != second_column.shape):
                return_str += 'The array length is different: %s != %s' % (str(first_column.shape), str(second_column.shape))
                return ': ' + return_str
            if not np.all(first_column == second_column):  # Check if the data of the column is equal
                return_str += 'Column ' + column_name + ' not equal. '
        for column_name in second_array.dtype.names:
            try:
                first_array[column_name]
            except ValueError:
                return_str += 'Additional column ' + column_name + ' found. '
                continue
        return ': ' + return_str


def array_close(array_1, array_2, rtol=1.e-5, atol=1.e-8):
    '''Compares two numpy arrays elementwise for similarity with small differences.'''
    if not array_1.dtype.names:
        try:
            return np.allclose(array_1, array_2, rtol=1.e-5, atol=1.e-8)  # Only works on non recarrays
        except ValueError:  # Raised if shape is incompatible
            return False
    results = []
    for column in array_1.dtype.names:
        results.append(np.allclose(array_1[column], array_2[column], rtol=1.e-5, atol=1.e-8))
    return np.all(results)


def compare_h5_files(first_file, second_file, expected_nodes=None, detailed_comparison=True, exact=True, rtol=1.e-5, atol=1.e-8):
    '''Takes two hdf5 files and check for equality of all nodes.
    Returns true if the node data is equal and the number of nodes is the number of expected nodes.
    It also returns a error string containing the names of the nodes that are not equal.

    Parameters
    ----------
    first_file : string
        Path to the first file.
    second_file : string
        Path to the first file.
    expected_nodes : Int
        The number of nodes expected in the second_file. If not specified the number of nodes expected in the second_file equals
        the number of nodes in the first file.
    detailed_comparison : boolean
        Print reason why the comparison failed
    exact : boolean
        True if the results have to match exactly. E.g. False for fit results.
    rtol, atol: number
        From numpy.allclose:
        rtol : float
            The relative tolerance parameter (see Notes).
        atol : float
            The absolute tolerance parameter (see Notes).
    Returns
    -------
    bool, string
    '''
    checks_passed = True
    error_msg = ""
    with tb.open_file(first_file, 'r') as first_h5_file:
        with tb.open_file(second_file, 'r') as second_h5_file:
            n_expected_nodes = sum(1 for _ in enumerate(first_h5_file.root)) if expected_nodes is None else expected_nodes  # set the number of expected nodes
            n_nodes = sum(1 for _ in enumerate(second_h5_file.root))  # calculated the number of nodes
            if n_nodes != n_expected_nodes:
                checks_passed = False
                error_msg += 'The number of nodes in the file is wrong.\n'
            for node in second_h5_file.root:  # loop over all nodes and compare each node, do not abort if one node is wrong
                try:
                    expected_data = first_h5_file.get_node(first_h5_file.root, node.name)[:]
                    data = second_h5_file.get_node(second_h5_file.root, node.name)[:]
                    # Convert nan to number otherwise check fails
                    nan_to_num(data)
                    nan_to_num(expected_data)
                    if exact:
                        # Use close without error to allow equal nan
                        if not np.array_equal(expected_data, data):
                            checks_passed = False
                            error_msg += node.name
                            if detailed_comparison:
                                error_msg += get_array_differences(expected_data, data)
                            error_msg += '\n'
                    else:
                        if not array_close(expected_data, data, rtol, atol):
                            checks_passed = False
                            error_msg += node.name
                            if detailed_comparison:
                                error_msg += get_array_differences(expected_data, data)
                            error_msg += '\n'
                except tb.NoSuchNodeError:
                    checks_passed = False
                    error_msg += 'Unknown node ' + node.name + '\n'
    return checks_passed, error_msg
