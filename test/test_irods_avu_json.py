import unittest
import jsonavu
import json
import os

TEST_DATA_JSON_BASIC_FILE = os.path.join(os.path.dirname(__file__), '..', 'inputs', 'basic.json')
TEST_DATA_JSON_EMPTY_ARRAYS_FILE = os.path.join(os.path.dirname(__file__), '..', 'inputs', 'empty-arrays.json')
TEST_DATA_JSON_TYPES_FILE = os.path.join(os.path.dirname(__file__), '..', 'inputs', 'types.json')


class TestIrodsAvuJson(unittest.TestCase):

    def setUp(self):
        self.test_file_basic_json = open(TEST_DATA_JSON_BASIC_FILE)
        self.test_data_basic_json = self.test_file_basic_json.read()
        self.test_file_types_json = open(TEST_DATA_JSON_TYPES_FILE)
        self.test_data_types_json = self.test_file_types_json.read()
        self.test_file_empty_arrays_json = open(TEST_DATA_JSON_EMPTY_ARRAYS_FILE)
        self.test_data_empty_arrays_json = self.test_file_empty_arrays_json.read()

    def tearDown(self):
        self.test_file_basic_json.close()
        self.test_file_types_json.close()
        self.test_file_empty_arrays_json.close()

    def test_simple_json_to_avu_string(self):
        """
        Test if simple json is correctly transformed to avu's using string as type
        """
        data = json.loads('{"k1": "v1"}')
        avu = jsonavu.json2avu(data, "root")
        self.assertEqual([{'a': 'k1', 'u': 'root_0_s', 'v': 'v1'}], avu)

    def test_simple_avu_to_json_string(self):
        """
        Test if simple avu is correctly transformed to json using string as type
        """
        data = [{'a': 'k1', 'u': 'root_0_s', 'v': 'v1'}]
        json_output = jsonavu.avu2json(data, "root")
        self.assertEqual('{"k1": "v1"}', json.dumps(json_output))

    def test_simple_json_to_avu_integer(self):
        """
        Test if simple json is correctly transformed to avu's using integer as type
        """
        data = json.loads('{"k1": 5 }')
        avu = jsonavu.json2avu(data, "root")
        self.assertEqual([{'a': 'k1', 'u': 'root_0_n', 'v': '5'}], avu)

    def test_simple_avu_to_json_integer(self):
        """
        Test if simple avu is correctly transformed to json using integer as type
        """
        data = [{'a': 'k1', 'u': 'root_0_n', 'v': '5'}]
        json_output = jsonavu.avu2json(data, "root")
        self.assertEqual('{"k1": 5}', json.dumps(json_output))

    def test_simple_json_to_avu_float(self):
        """
        Test if simple json is correctly transformed to avu's using float as type
        """
        data = json.loads('{"k1": 5.0 }')
        avu = jsonavu.json2avu(data, "root")
        self.assertEqual([{'a': 'k1', 'u': 'root_0_n', 'v': '5.0'}], avu)

    def test_simple_avu_to_json_float(self):
        """
        Test if simple avu is correctly transformed to json using integer as type
        """
        data = [{'a': 'k1', 'u': 'root_0_n', 'v': '5.0'}]
        json_output = jsonavu.avu2json(data, "root")
        self.assertEqual('{"k1": 5.0}', json.dumps(json_output))

    def test_simple_json_to_avu_boolean(self):
        """
        Test if simple json is correctly transformed to avu's using boolean as type
        """
        data = json.loads('{"k1": true , "k2": false }')
        avu = jsonavu.json2avu(data, "root")
        self.assertCountEqual([{'a': u'k2', 'u': 'root_0_b', 'v': 'False'}, {'a': u'k1', 'u': 'root_0_b', 'v': 'True'}],
                              avu)

    def test_simple_avu_to_json_boolean(self):
        """
        Test if simple avu is correctly transformed to json using boolean as type
        """
        data = [{'a': u'k2', 'u': 'root_0_b', 'v': 'False'}, {'a': u'k1', 'u': 'root_0_b', 'v': 'True'}]
        json_output = jsonavu.avu2json(data, "root")
        self.assertEqual('{"k1": true, "k2": false}', json.dumps(json_output, sort_keys=True))

    def test_simple_json_to_avu_null(self):
        """
        Test if simple json is correctly transformed to avu's using null as type
        """
        data = json.loads('{"k1": null }')
        avu = jsonavu.json2avu(data, "root")
        self.assertEqual([{'a': 'k1', 'u': 'root_0_z', 'v': '.'}], avu)

    def test_simple_avu_to_json_null(self):
        """
        Test if simple avu is correctly transformed to json using null as type
        """
        data = [{'a': 'k1', 'u': 'root_0_z', 'v': '.'}]
        json_output = jsonavu.avu2json(data, "root")
        self.assertEqual('{"k1": null}', json.dumps(json_output))

    def test_simple_json_to_avu_empty_string(self):
        """
        Test if simple json is correctly transformed to avu's using empty_string as type
        """
        data = json.loads('{"k1": "" }')
        avu = jsonavu.json2avu(data, "root")
        self.assertEqual([{'a': 'k1', 'u': 'root_0_e', 'v': '.'}], avu)

    def test_simple_avu_to_json_empty_string(self):
        """
        Test if simple avu is correctly transformed to json using empty_string as type
        """
        data = [{'a': 'k1', 'u': 'root_0_e', 'v': '.'}]
        json_output = jsonavu.avu2json(data, "root")
        self.assertEqual('{"k1": ""}', json.dumps(json_output))

    def test_simple_json_to_avu_object(self):
        """
        Test if simple json is correctly transformed to avu's using object as type
        """
        data = json.loads('{"k2": {"k3" : null,"k4" : "v3" }}')
        avu = jsonavu.json2avu(data, "root")
        expected_avu = [{'a': u'k2', 'u': 'root_0_o1', 'v': 'o1'},
                        {'a': u'k3', 'u': 'root_1_z', 'v': '.'},
                        {'a': u'k4', 'u': 'root_1_s', 'v': u'v3'}]
        self.assertEqual(expected_avu, avu)

    def test_simple_avu_to_json_object(self):
        """
        Test if simple avu is correctly transformed to json using object as type
        """
        data = [{'a': u'k2', 'u': 'root_0_o1', 'v': 'o1'},
                {'a': u'k3', 'u': 'root_1_z', 'v': '.'},
                {'a': u'k4', 'u': 'root_1_s', 'v': u'v3'}]
        json_output = jsonavu.avu2json(data, "root")
        self.assertEqual('{"k2": {"k3": null, "k4": "v3"}}', json.dumps(json_output))

    def test_simple_json_to_avu_nested_array(self):
        """
        Test if simple json is correctly transformed to avu's using object as type
        """
        data = json.loads('{"k1": "v1","k2":[["v4", "v5"],["v6", "v7"]]}')
        avu = jsonavu.json2avu(data, "root")
        expected_avu = [{'a': u'k2', 'u': 'root_0_s#0#0', 'v': u'v4'},
                        {'a': u'k2', 'u': 'root_0_s#0#1', 'v': u'v5'},
                        {'a': u'k2', 'u': 'root_0_s#1#0', 'v': u'v6'},
                        {'a': u'k2', 'u': 'root_0_s#1#1', 'v': u'v7'},
                        {'a': u'k1', 'u': 'root_0_s', 'v': u'v1'}]
        self.assertCountEqual(expected_avu, avu)

    def test_simple_avu_to_json_nested_array(self):
        """
        Test if simple avu is correctly transformed to json using object as type
        """
        data = [{'a': u'k2', 'u': 'root_0_s#0#0', 'v': u'v4'},
                {'a': u'k2', 'u': 'root_0_s#0#1', 'v': u'v5'},
                {'a': u'k2', 'u': 'root_0_s#1#0', 'v': u'v6'},
                {'a': u'k2', 'u': 'root_0_s#1#1', 'v': u'v7'},
                {'a': u'k1', 'u': 'root_0_s', 'v': u'v1'}]
        json_output = jsonavu.avu2json(data, "root")
        self.assertEqual('{"k1": "v1", "k2": [["v4", "v5"], ["v6", "v7"]]}', json.dumps(json_output, sort_keys=True))

    def test_simple_json_to_avu_empty_array(self):
        """
        Test if simple json is correctly transformed to avu using empty array
        """
        data = json.loads('{"k1": "v1","emptyArr": []}')
        avu = jsonavu.json2avu(data, "root")
        expected_avu = [{'a': u'k1', 'u': 'root_0_s', 'v': u'v1'},
                        {'a': u'emptyArr', 'u': 'root_0_a', 'v': u'.'}]
        self.assertCountEqual(expected_avu, avu)

    def test_simple_avu_to_json_empty_array(self):
        """
        Test if simple avu is correctly transformed to json using empty array
        """
        data = [{'a': u'k1', 'u': 'root_0_s', 'v': u'v1'},
                {'a': u'emptyArr', 'u': 'root_0_a', 'v': u'.'}]
        json_output = jsonavu.avu2json(data, "root")
        self.assertEqual('{"emptyArr": [], "k1": "v1"}', json.dumps(json_output, sort_keys=True))

    def test_simple_json_to_avu_empty_object(self):
        """
        Test if simple json is correctly transformed to avu using empty object
        """
        data = json.loads('{"k1": "v1","emptyObj": {}}')
        avu = jsonavu.json2avu(data, "root")
        expected_avu = [{'a': u'k1', 'u': 'root_0_s', 'v': u'v1'},
                        {'a': u'emptyObj', 'u': 'root_0_o1', 'v': u'o1'}]
        self.assertCountEqual(expected_avu, avu)


    def test_simple_avu_to_json_empty_object(self):
        """
        Test if simple avu is correctly transformed to json using empty object
        """
        data = [{'a': u'k1', 'u': 'root_0_s', 'v': u'v1'},
                {'a': u'emptyObj', 'u': 'root_0_o1', 'v': u'o1'}]
        json_output = jsonavu.avu2json(data, "root")
        self.assertEqual('{"emptyObj": {}, "k1": "v1"}', json.dumps(json_output, sort_keys=True))

    def test_simple_bidirectional(self):
        """
        Test if simple json is correctly transformed to avu and back to json
        """
        data = json.loads('{"k1": "v1"}')
        avu = jsonavu.json2avu(data, "root")
        json_output = jsonavu.avu2json(avu, "root")
        self.assertEqual('{"k1": "v1"}', json.dumps(json_output))

    def test_unicode_bidirectional(self):
        """
        Test if unicode json is correctly transformed to avu and back to json
        """
        data = json.loads('{"k1": "µm"}')
        avu = jsonavu.json2avu(data, "root")
        json_output = jsonavu.avu2json(avu, "root")
        self.assertEqual('{"k1": "µm"}', json.dumps(json_output, ensure_ascii=False))

    def test_json_types_file_json_to_avu(self):
        """
        Test if types json file is correctly transformed to avu
        """
        data = json.loads(self.test_data_types_json)
        avu = jsonavu.json2avu(data, "root")
        expected_avu = [{'a': 'k2', 'u': 'root_0_o1', 'v': 'o1'},
                        {'a': 'k3', 'u': 'root_1_z', 'v': '.'},
                        {'a': 'k4', 'u': 'root_1_s', 'v': 'v3'},
                        {'a': 'k1', 'u': 'root_0_e', 'v': '.'},
                        {'a': 'k6', 'u': 'root_0_o2#0', 'v': 'o2'},
                        {'a': 'k8', 'u': 'root_2_b', 'v': 'False'},
                        {'a': 'k7', 'u': 'root_2_b', 'v': 'True'},
                        {'a': 'k5', 'u': 'root_0_n#0', 'v': '42'},
                        {'a': 'k5', 'u': 'root_0_n#1', 'v': '42.42'}]
        self.assertCountEqual(expected_avu, avu)

    def test_json_basic_file_bidirectional(self):
        """
        Test if basic json file is correctly transformed to avu and back to json
        """
        data = json.loads(self.test_data_basic_json)
        avu = jsonavu.json2avu(data, "root")
        json_output = jsonavu.avu2json(avu, "root")
        self.assertCountEqual(json.dumps(data, sort_keys=True), json.dumps(json_output, sort_keys=True))

    def test_json_empty_arrays_file_bidirectional(self):
        """
        Test if empty array and empty object json file is correctly transformed to avu and back to json
        """
        data = json.loads(self.test_data_empty_arrays_json)
        avu = jsonavu.json2avu(data, "root")
        json_output = jsonavu.avu2json(avu, "root")
        self.assertCountEqual(json.dumps(data, sort_keys=True), json.dumps(json_output, sort_keys=True))

    def test_avu_to_json_invalid_boolean_exception(self):
        """
        Test if basic json file is correctly transformed to avu and back to json
        """
        data = [{'a': 'k2', 'u': 'root_0_b', 'v': 'Boolean'}]

        with self.assertRaises(Exception):
            jsonavu.avu2json(data, "root")

    def test_avu_to_json_illegal_type(self):
        """
        Test if avu with an element with illegal type is ignored
        """
        data = [{'a': 'k1', 'u': 'root_0_s', 'v': 'v1'}, {'a': 'k2', 'u': 'root_0_q', 'v': 'Boolean'}]
        json_output = jsonavu.avu2json(data, "root")
        self.assertEqual('{"k1": "v1"}', json.dumps(json_output))

    def test_avu_to_json_incorrect_unit_pattern(self):
        """
        Test if avu with an element with incorrect pattern is ignored
        """
        data = [{'a': 'k1', 'u': 'root_0_s', 'v': 'v1'}, {'a': 'k2', 'u': 'this_is_a_test', 'v': 'Boolean'}]
        json_output = jsonavu.avu2json(data, "root")
        self.assertEqual('{"k1": "v1"}', json.dumps(json_output))

    def test_json_to_avu_only_string_input(self):
        """
        Test if json with only a string is correctly parsed
        """
        avu = jsonavu.json2avu('test', "root")
        self.assertEqual([{'a': 'root', 'u': 'root_0_s', 'v': 'test'}], avu)

    def test_json_to_avu_only_list_input(self):
        """
        Test if json with only a list is correctly parsed
        """
        avu = jsonavu.json2avu(['test', 'test2'], "root")
        self.assertEqual(
            [{'a': 'root', 'u': 'root_0_s#0', 'v': 'test'}, {'a': 'root', 'u': 'root_0_s#1', 'v': 'test2'}], avu)


if __name__ == '__main__':
    unittest.main()
