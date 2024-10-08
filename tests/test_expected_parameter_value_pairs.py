# pylint: disable=missing-docstring
import unittest
import copy
from typing import List, Dict
from collections import OrderedDict as OD
import io
import packaging.version as pkv
import random

from utils_test import (
    parse_param_val,
    parse_param_vals,
    parse_expected_val_pairs,
    create_diff_parameter_value_pairs,
)
from covertable import make
from bashi.types import (
    Parameter,
    ParameterValue,
    ParameterValueSingle,
    ParameterValuePair,
    ParameterValueMatrix,
    CombinationList,
)
from bashi.globals import *  # pylint: disable=wildcard-import,unused-wildcard-import
from bashi.utils import (
    get_expected_parameter_value_pairs,
    check_parameter_value_pair_in_combination_list,
    check_unexpected_parameter_value_pair_in_combination_list,
    remove_parameter_value_pairs,
    create_parameter_value_pair,
)


class TestCreateParameterValuePair(unittest.TestCase):
    def test_create_parameter_value_pair_type_str(self):
        param1 = "param1"
        param2 = "param2"
        name1 = "name1"
        name2 = "name2"
        ver1 = "1.0"
        ver2 = "2.0"

        created_param_val_pair = create_parameter_value_pair(
            param1, name1, ver1, param2, name2, ver2
        )

        expected_param_val_pair = ParameterValuePair(
            ParameterValueSingle(
                param1,
                ParameterValue(name1, pkv.parse(ver1)),
            ),
            ParameterValueSingle(
                param2,
                ParameterValue(name2, pkv.parse(ver2)),
            ),
        )

        self.assertEqual(type(created_param_val_pair), type(expected_param_val_pair))

        self.assertEqual(
            created_param_val_pair,
            expected_param_val_pair,
        )

    def test_create_parameter_value_pair_type_float(self):
        param1 = "param1"
        param2 = "param2"
        name1 = "name1"
        name2 = "name2"
        ver1 = 1.0
        ver2 = 2.0

        created_param_val_pair = create_parameter_value_pair(
            param1, name1, ver1, param2, name2, ver2
        )

        expected_param_val_pair = ParameterValuePair(
            ParameterValueSingle(
                param1,
                ParameterValue(name1, pkv.parse(str(ver1))),
            ),
            ParameterValueSingle(
                param2,
                ParameterValue(name2, pkv.parse(str(ver2))),
            ),
        )

        self.assertEqual(type(created_param_val_pair), type(expected_param_val_pair))

        self.assertEqual(
            created_param_val_pair,
            expected_param_val_pair,
        )

    def test_create_parameter_value_pair_type_int(self):
        param1 = "param1"
        param2 = "param2"
        name1 = "name1"
        name2 = "name2"
        ver1 = 1
        ver2 = 2

        created_param_val_pair = create_parameter_value_pair(
            param1, name1, ver1, param2, name2, ver2
        )

        expected_param_val_pair = ParameterValuePair(
            ParameterValueSingle(
                param1,
                ParameterValue(name1, pkv.parse(str(ver1))),
            ),
            ParameterValueSingle(
                param2,
                ParameterValue(name2, pkv.parse(str(ver2))),
            ),
        )

        self.assertEqual(type(created_param_val_pair), type(expected_param_val_pair))

        self.assertEqual(
            created_param_val_pair,
            expected_param_val_pair,
        )

    def test_create_parameter_value_pair_type_version(self):
        param1 = "param1"
        param2 = "param2"
        name1 = "name1"
        name2 = "name2"
        ver1 = pkv.parse("1.0")
        ver2 = pkv.parse("2.0")

        created_param_val_pair = create_parameter_value_pair(
            param1, name1, ver1, param2, name2, ver2
        )

        expected_param_val_pair = ParameterValuePair(
            ParameterValueSingle(
                param1,
                ParameterValue(name1, ver1),
            ),
            ParameterValueSingle(
                param2,
                ParameterValue(name2, ver2),
            ),
        )

        self.assertEqual(type(created_param_val_pair), type(expected_param_val_pair))

        self.assertEqual(
            created_param_val_pair,
            expected_param_val_pair,
        )

    def test_create_parameter_value_pair_type_mixed(self):
        param1 = "param1"
        param2 = "param2"
        name1 = "name1"
        name2 = "name2"
        ver1 = pkv.parse("1.0")
        ver2 = "2.0"

        created_param_val_pair = create_parameter_value_pair(
            param1, name1, ver1, param2, name2, ver2
        )

        expected_param_val_pair = ParameterValuePair(
            ParameterValueSingle(
                param1,
                ParameterValue(name1, ver1),
            ),
            ParameterValueSingle(
                param2,
                ParameterValue(name2, pkv.parse(ver2)),
            ),
        )

        self.assertEqual(type(created_param_val_pair), type(expected_param_val_pair))

        self.assertEqual(
            created_param_val_pair,
            expected_param_val_pair,
        )


class TestExpectedValuePairs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.param_matrix: ParameterValueMatrix = OD()

        cls.param_matrix[HOST_COMPILER] = parse_param_vals(
            [(GCC, 10), (GCC, 11), (GCC, 12), (CLANG, 16), (CLANG, 17)]
        )
        cls.param_matrix[DEVICE_COMPILER] = parse_param_vals(
            [(NVCC, 11.2), (NVCC, 12.0), (GCC, 10), (GCC, 11)]
        )
        cls.param_matrix[CMAKE] = parse_param_vals([(CMAKE, 3.22), (CMAKE, 3.23)])
        cls.param_matrix[BOOST] = parse_param_vals([(BOOST, 1.81), (BOOST, 1.82), (BOOST, 1.83)])

        cls.generated_parameter_value_pairs: List[ParameterValuePair] = (
            get_expected_parameter_value_pairs(cls.param_matrix)
        )

        cls.expected_param_val_pairs: List[ParameterValuePair] = parse_expected_val_pairs(
            [
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.2)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.0)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (GCC, 10)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (GCC, 11)}),
                OD({HOST_COMPILER: (GCC, 10), CMAKE: (CMAKE, 3.22)}),
                OD({HOST_COMPILER: (GCC, 10), CMAKE: (CMAKE, 3.23)}),
                OD({HOST_COMPILER: (GCC, 10), BOOST: (BOOST, 1.81)}),
                OD({HOST_COMPILER: (GCC, 10), BOOST: (BOOST, 1.82)}),
                OD({HOST_COMPILER: (GCC, 10), BOOST: (BOOST, 1.83)}),
                OD({HOST_COMPILER: (GCC, 11), DEVICE_COMPILER: (NVCC, 11.2)}),
                OD({HOST_COMPILER: (GCC, 11), DEVICE_COMPILER: (NVCC, 12.0)}),
                OD({HOST_COMPILER: (GCC, 11), DEVICE_COMPILER: (GCC, 10)}),
                OD({HOST_COMPILER: (GCC, 11), DEVICE_COMPILER: (GCC, 11)}),
                OD({HOST_COMPILER: (GCC, 11), CMAKE: (CMAKE, 3.22)}),
                OD({HOST_COMPILER: (GCC, 11), CMAKE: (CMAKE, 3.23)}),
                OD({HOST_COMPILER: (GCC, 11), BOOST: (BOOST, 1.81)}),
                OD({HOST_COMPILER: (GCC, 11), BOOST: (BOOST, 1.82)}),
                OD({HOST_COMPILER: (GCC, 11), BOOST: (BOOST, 1.83)}),
                OD({HOST_COMPILER: (GCC, 12), DEVICE_COMPILER: (NVCC, 11.2)}),
                OD({HOST_COMPILER: (GCC, 12), DEVICE_COMPILER: (NVCC, 12.0)}),
                OD({HOST_COMPILER: (GCC, 12), DEVICE_COMPILER: (GCC, 10)}),
                OD({HOST_COMPILER: (GCC, 12), DEVICE_COMPILER: (GCC, 11)}),
                OD({HOST_COMPILER: (GCC, 12), CMAKE: (CMAKE, 3.22)}),
                OD({HOST_COMPILER: (GCC, 12), CMAKE: (CMAKE, 3.23)}),
                OD({HOST_COMPILER: (GCC, 12), BOOST: (BOOST, 1.81)}),
                OD({HOST_COMPILER: (GCC, 12), BOOST: (BOOST, 1.82)}),
                OD({HOST_COMPILER: (GCC, 12), BOOST: (BOOST, 1.83)}),
                OD({HOST_COMPILER: (CLANG, 16), DEVICE_COMPILER: (NVCC, 11.2)}),
                OD({HOST_COMPILER: (CLANG, 16), DEVICE_COMPILER: (NVCC, 12.0)}),
                OD({HOST_COMPILER: (CLANG, 16), DEVICE_COMPILER: (GCC, 10)}),
                OD({HOST_COMPILER: (CLANG, 16), DEVICE_COMPILER: (GCC, 11)}),
                OD({HOST_COMPILER: (CLANG, 16), CMAKE: (CMAKE, 3.22)}),
                OD({HOST_COMPILER: (CLANG, 16), CMAKE: (CMAKE, 3.23)}),
                OD({HOST_COMPILER: (CLANG, 16), BOOST: (BOOST, 1.81)}),
                OD({HOST_COMPILER: (CLANG, 16), BOOST: (BOOST, 1.82)}),
                OD({HOST_COMPILER: (CLANG, 16), BOOST: (BOOST, 1.83)}),
                OD({HOST_COMPILER: (CLANG, 17), DEVICE_COMPILER: (NVCC, 11.2)}),
                OD({HOST_COMPILER: (CLANG, 17), DEVICE_COMPILER: (NVCC, 12.0)}),
                OD({HOST_COMPILER: (CLANG, 17), DEVICE_COMPILER: (GCC, 10)}),
                OD({HOST_COMPILER: (CLANG, 17), DEVICE_COMPILER: (GCC, 11)}),
                OD({HOST_COMPILER: (CLANG, 17), CMAKE: (CMAKE, 3.22)}),
                OD({HOST_COMPILER: (CLANG, 17), CMAKE: (CMAKE, 3.23)}),
                OD({HOST_COMPILER: (CLANG, 17), BOOST: (BOOST, 1.81)}),
                OD({HOST_COMPILER: (CLANG, 17), BOOST: (BOOST, 1.82)}),
                OD({HOST_COMPILER: (CLANG, 17), BOOST: (BOOST, 1.83)}),
                OD({DEVICE_COMPILER: (NVCC, 11.2), CMAKE: (CMAKE, 3.22)}),
                OD({DEVICE_COMPILER: (NVCC, 11.2), CMAKE: (CMAKE, 3.23)}),
                OD({DEVICE_COMPILER: (NVCC, 11.2), BOOST: (BOOST, 1.81)}),
                OD({DEVICE_COMPILER: (NVCC, 11.2), BOOST: (BOOST, 1.82)}),
                OD({DEVICE_COMPILER: (NVCC, 11.2), BOOST: (BOOST, 1.83)}),
                OD({DEVICE_COMPILER: (NVCC, 12.0), CMAKE: (CMAKE, 3.22)}),
                OD({DEVICE_COMPILER: (NVCC, 12.0), CMAKE: (CMAKE, 3.23)}),
                OD({DEVICE_COMPILER: (NVCC, 12.0), BOOST: (BOOST, 1.81)}),
                OD({DEVICE_COMPILER: (NVCC, 12.0), BOOST: (BOOST, 1.82)}),
                OD({DEVICE_COMPILER: (NVCC, 12.0), BOOST: (BOOST, 1.83)}),
                OD({DEVICE_COMPILER: (GCC, 10), CMAKE: (CMAKE, 3.22)}),
                OD({DEVICE_COMPILER: (GCC, 10), CMAKE: (CMAKE, 3.23)}),
                OD({DEVICE_COMPILER: (GCC, 10), BOOST: (BOOST, 1.81)}),
                OD({DEVICE_COMPILER: (GCC, 10), BOOST: (BOOST, 1.82)}),
                OD({DEVICE_COMPILER: (GCC, 10), BOOST: (BOOST, 1.83)}),
                OD({DEVICE_COMPILER: (GCC, 11), CMAKE: (CMAKE, 3.22)}),
                OD({DEVICE_COMPILER: (GCC, 11), CMAKE: (CMAKE, 3.23)}),
                OD({DEVICE_COMPILER: (GCC, 11), BOOST: (BOOST, 1.81)}),
                OD({DEVICE_COMPILER: (GCC, 11), BOOST: (BOOST, 1.82)}),
                OD({DEVICE_COMPILER: (GCC, 11), BOOST: (BOOST, 1.83)}),
                OD({CMAKE: (CMAKE, 3.22), BOOST: (BOOST, 1.81)}),
                OD({CMAKE: (CMAKE, 3.22), BOOST: (BOOST, 1.82)}),
                OD({CMAKE: (CMAKE, 3.22), BOOST: (BOOST, 1.83)}),
                OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.81)}),
                OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.82)}),
                OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.83)}),
            ]
        )

        ppv = parse_param_val
        cls.handwritten_comb_list: CombinationList = [
            OD(
                {
                    HOST_COMPILER: ppv((GCC, 10)),
                    DEVICE_COMPILER: ppv((NVCC, 11.2)),
                    CMAKE: ppv((CMAKE, 3.22)),
                    BOOST: ppv((BOOST, 1.81)),
                }
            ),
            OD(
                {
                    HOST_COMPILER: ppv((GCC, 10)),
                    DEVICE_COMPILER: ppv((NVCC, 12.0)),
                    CMAKE: ppv((CMAKE, 3.22)),
                    BOOST: ppv((BOOST, 1.82)),
                }
            ),
            OD(
                {
                    HOST_COMPILER: ppv((CLANG, 16)),
                    DEVICE_COMPILER: ppv((CLANG, 16)),
                    CMAKE: ppv((CMAKE, 3.23)),
                    BOOST: ppv((BOOST, 1.83)),
                }
            ),
        ]

        cls.handwritten_all_existing_pairs: List[ParameterValuePair] = parse_expected_val_pairs(
            [
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.2)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.0)}),
                OD({HOST_COMPILER: (CLANG, 16), DEVICE_COMPILER: (CLANG, 16)}),
                OD({HOST_COMPILER: (GCC, 10), CMAKE: (CMAKE, 3.22)}),
                OD({HOST_COMPILER: (CLANG, 16), CMAKE: (CMAKE, 3.23)}),
                OD({HOST_COMPILER: (GCC, 10), BOOST: (BOOST, 1.81)}),
                OD({HOST_COMPILER: (GCC, 10), BOOST: (BOOST, 1.82)}),
                OD({HOST_COMPILER: (CLANG, 16), BOOST: (BOOST, 1.83)}),
                OD({DEVICE_COMPILER: (NVCC, 11.2), CMAKE: (CMAKE, 3.22)}),
                OD({DEVICE_COMPILER: (NVCC, 12.0), CMAKE: (CMAKE, 3.22)}),
                OD({DEVICE_COMPILER: (CLANG, 16), CMAKE: (CMAKE, 3.23)}),
                OD({DEVICE_COMPILER: (NVCC, 11.2), BOOST: (BOOST, 1.81)}),
                OD({DEVICE_COMPILER: (NVCC, 12.0), BOOST: (BOOST, 1.82)}),
                OD({DEVICE_COMPILER: (CLANG, 16), BOOST: (BOOST, 1.83)}),
                OD({CMAKE: (CMAKE, 3.22), BOOST: (BOOST, 1.81)}),
                OD({CMAKE: (CMAKE, 3.22), BOOST: (BOOST, 1.82)}),
                OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.83)}),
            ]
        )

    def test_expected_value_pairs(self):
        self.assertTrue(
            len(self.expected_param_val_pairs) == len(self.generated_parameter_value_pairs),
            f"\nlen(expected_param_val_pairs): {len(self.expected_param_val_pairs)}\n"
            f"len(generated_parameter_value_pairs): {len(self.generated_parameter_value_pairs)}",
        )

        missing_expected_param = False
        for ex_param_val_pair in self.expected_param_val_pairs:
            try:
                self.assertTrue(ex_param_val_pair in self.generated_parameter_value_pairs)
            except AssertionError:
                missing_expected_param = True
                print(
                    f"{ex_param_val_pair} was not found in the generated parameter-value-pair list"
                )

        self.assertFalse(missing_expected_param)

        missing_generated_param = False
        for gen_param_val_pair in self.generated_parameter_value_pairs:
            try:
                self.assertTrue(gen_param_val_pair in self.expected_param_val_pairs)
            except AssertionError:
                missing_generated_param = True
                print(
                    f"{gen_param_val_pair} was not found in the expected parameter-value-pair list"
                )

        self.assertFalse(missing_generated_param)

    def test_check_parameter_value_pair_in_combination_list_empty_input(self):
        self.assertTrue(
            check_parameter_value_pair_in_combination_list(self.handwritten_comb_list, [])
        )

    def test_check_parameter_value_pair_in_combination_list_less_valid_input(self):
        # all pairs exists in the combination list, but not all pairs are tested
        self.assertTrue(
            check_parameter_value_pair_in_combination_list(
                self.handwritten_comb_list,
                parse_expected_val_pairs(
                    [
                        OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.2)}),
                        OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.0)}),
                        OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.83)}),
                    ]
                ),
            )
        )

    def test_check_parameter_value_pair_in_combination_list_complete_valid_input(self):
        # test all existing pairs
        self.assertTrue(
            check_parameter_value_pair_in_combination_list(
                self.handwritten_comb_list, self.handwritten_all_existing_pairs
            )
        )

    def test_check_parameter_value_pair_in_combination_list_single_wrong_input(self):
        single_wrong_pair = parse_expected_val_pairs(
            [
                OD({HOST_COMPILER: (GCC, 11), DEVICE_COMPILER: (NVCC, 11.2)}),
            ]
        )

        output_wrong_single_pair = io.StringIO()
        self.assertFalse(
            check_parameter_value_pair_in_combination_list(
                self.handwritten_comb_list,
                single_wrong_pair,
                output_wrong_single_pair,
            )
        )
        output_wrong_single_pair_expected_str = (
            str(single_wrong_pair[0]) + " is missing in combination list"
        )
        self.assertTrue(
            output_wrong_single_pair.getvalue().rstrip() == output_wrong_single_pair_expected_str,
            (
                f"\nGet:      {output_wrong_single_pair.getvalue().rstrip()}\n"
                f"Expected: {output_wrong_single_pair_expected_str}"
            ),
        )

    def test_check_parameter_value_pair_in_combination_list_many_wrong_input(self):
        many_wrong_pairs = parse_expected_val_pairs(
            [
                OD({HOST_COMPILER: (GCC, 11), DEVICE_COMPILER: (NVCC, 11.2)}),
                OD({CMAKE: (CMAKE, 2.23), DEVICE_COMPILER: (BOOST, 1.83)}),
                OD({DEVICE_COMPILER: (NVCC, 12.0), BOOST: (BOOST, 1.84)}),
            ]
        )

        expected_output_many_wrong_pairs_list: List[str] = []
        for pair in many_wrong_pairs:
            expected_output_many_wrong_pairs_list.append(
                str(pair) + " is missing in combination list"
            )

        expected_output_many_wrong_pairs_list.sort()

        output_wrong_many_pairs = io.StringIO()
        self.assertFalse(
            check_parameter_value_pair_in_combination_list(
                self.handwritten_comb_list,
                many_wrong_pairs,
                output_wrong_many_pairs,
            )
        )

        output_wrong_many_pairs_list: List[str] = (
            output_wrong_many_pairs.getvalue().rstrip().split("\n")
        )
        output_wrong_many_pairs_list.sort()

        self.assertEqual(len(output_wrong_many_pairs_list), 3)

        self.assertEqual(output_wrong_many_pairs_list, expected_output_many_wrong_pairs_list)

    def test_check_parameter_value_pair_in_combination_list_complete_list_plus_wrong_input(self):
        many_wrong_pairs = parse_expected_val_pairs(
            [
                OD({HOST_COMPILER: (GCC, 11), DEVICE_COMPILER: (NVCC, 11.2)}),
                OD({CMAKE: (CMAKE, 2.23), DEVICE_COMPILER: (BOOST, 1.83)}),
                OD({DEVICE_COMPILER: (NVCC, 12.0), BOOST: (BOOST, 1.84)}),
            ]
        )

        all_pairs_plus_wrong_input = self.handwritten_all_existing_pairs + many_wrong_pairs

        expected_output_many_wrong_pairs_list: List[str] = []
        for pair in many_wrong_pairs:
            expected_output_many_wrong_pairs_list.append(
                str(pair) + " is missing in combination list"
            )

        expected_output_many_wrong_pairs_list.sort()

        output_wrong_many_pairs = io.StringIO()
        self.assertFalse(
            check_parameter_value_pair_in_combination_list(
                self.handwritten_comb_list,
                all_pairs_plus_wrong_input,
                output_wrong_many_pairs,
            )
        )

        output_wrong_many_pairs_list: List[str] = (
            output_wrong_many_pairs.getvalue().rstrip().split("\n")
        )
        output_wrong_many_pairs_list.sort()

        self.assertEqual(len(output_wrong_many_pairs_list), 3)

        self.assertEqual(output_wrong_many_pairs_list, expected_output_many_wrong_pairs_list)

    def test_check_unexpected_parameter_value_pair_in_combination_list_all_empty(self):
        self.assertTrue(
            check_unexpected_parameter_value_pair_in_combination_list(
                [],
                [],
            )
        )

    def test_check_unexpected_parameter_value_pair_in_combination_list_empty_input(self):
        self.assertTrue(
            check_unexpected_parameter_value_pair_in_combination_list(
                [],
                parse_expected_val_pairs(
                    [
                        OD({HOST_COMPILER: (GCC, 10), BOOST: (BOOST, 1.82)}),
                        OD({DEVICE_COMPILER: (CLANG, 16), CMAKE: (CMAKE, 3.23)}),
                        OD({DEVICE_COMPILER: (CLANG, 16), BOOST: (BOOST, 1.83)}),
                        OD({HOST_COMPILER: (GCC, 10), CMAKE: (CMAKE, 3.22)}),
                    ]
                ),
            )
        )

    def test_check_unexpected_parameter_value_pair_in_combination_list_empty_search_list(self):
        self.assertTrue(
            check_unexpected_parameter_value_pair_in_combination_list(
                self.handwritten_comb_list, []
            ),
        )

    def test_check_unexpected_parameter_value_pair_in_combination_list_non_existing_entries(self):
        # non of the pairs are in the combination list
        self.assertTrue(
            check_unexpected_parameter_value_pair_in_combination_list(
                self.handwritten_comb_list,
                parse_expected_val_pairs(
                    [
                        OD({HOST_COMPILER: (NVCC, 10), DEVICE_COMPILER: (NVCC, 11.2)}),
                        OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (CLANG, 7)}),
                        OD({HOST_COMPILER: (NVCC, 12.2), DEVICE_COMPILER: (CMAKE, 3.30)}),
                    ]
                ),
            )
        )

    def test_check_unexpected_parameter_value_pair_in_combination_list_existing_entries(self):
        # all of the pairs are in the combination list
        existing_parameter_value_pairs = parse_expected_val_pairs(
            [
                OD({HOST_COMPILER: (GCC, 10), BOOST: (BOOST, 1.82)}),
                OD({DEVICE_COMPILER: (CLANG, 16), CMAKE: (CMAKE, 3.23)}),
                OD({DEVICE_COMPILER: (CLANG, 16), BOOST: (BOOST, 1.83)}),
                OD({HOST_COMPILER: (GCC, 10), CMAKE: (CMAKE, 3.22)}),
            ]
        )

        error_output = io.StringIO()
        self.assertFalse(
            check_unexpected_parameter_value_pair_in_combination_list(
                self.handwritten_comb_list,
                existing_parameter_value_pairs,
                error_output,
            )
        )

        error_list = error_output.getvalue().rstrip().split("\n")
        self.assertEqual(len(error_list), 4)

        for unexpected_param_val_pair in existing_parameter_value_pairs:
            self.assertIn(
                f"found unexpected parameter-value-pair {unexpected_param_val_pair} in combination list",
                error_list,
            )

    def test_check_unexpected_parameter_value_pair_in_combination_list_mixed_entries(self):
        # some of the pairs are in the combination list
        error_output = io.StringIO()

        existing_parameter_value_pairs: List[ParameterValuePair] = parse_expected_val_pairs(
            [
                OD({HOST_COMPILER: (GCC, 10), BOOST: (BOOST, 1.82)}),
                OD({HOST_COMPILER: (GCC, 10), CMAKE: (CMAKE, 3.22)}),
            ]
        )

        not_parameter_value_pairs: List[ParameterValuePair] = parse_expected_val_pairs(
            [
                OD({DEVICE_COMPILER: (CLANG_CUDA, 16), CMAKE: (CMAKE, 3.23)}),
                OD({DEVICE_COMPILER: (CLANG, 16), BOOST: (UBUNTU, 22.04)}),
                OD({DEVICE_COMPILER: (GCC, 7), BOOST: (UBUNTU, 22.04)}),
            ]
        )

        parameter_value_pairs: List[ParameterValuePair] = (
            existing_parameter_value_pairs + not_parameter_value_pairs
        )
        random.shuffle(parameter_value_pairs)

        self.assertFalse(
            check_unexpected_parameter_value_pair_in_combination_list(
                self.handwritten_comb_list,
                parameter_value_pairs,
                error_output,
            )
        )

        error_list = error_output.getvalue().rstrip().split("\n")
        self.assertEqual(len(error_list), 2)

        for unexpected_param_val_pair in existing_parameter_value_pairs:
            self.assertIn(
                f"found unexpected parameter-value-pair {unexpected_param_val_pair} in combination list",
                error_list,
            )

    def test_unrestricted_covertable_generator(self):
        comb_list: CombinationList = []
        # pylance shows a warning, because it cannot determine the concrete type of a namedtuple,
        # which is returned by AllPairs
        all_pairs: List[Dict[Parameter, ParameterValue]] = make(
            factors=self.param_matrix
        )  # type: ignore

        for all_pair in all_pairs:
            comb_list.append(OD(all_pair))

        self.assertTrue(
            check_parameter_value_pair_in_combination_list(comb_list, self.expected_param_val_pairs)
        )


class TestRemoveExpectedParameterValuePairs(unittest.TestCase):
    def test_remove_parameter_value_pair(self):
        test_param_value_pairs: List[ParameterValuePair] = parse_expected_val_pairs(
            [
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.2)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.0)}),
                OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 12.0)}),
                OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.83)}),
            ]
        )
        original_length = len(test_param_value_pairs)

        t1_no_remove = copy.deepcopy(test_param_value_pairs)
        t1_expected = sorted(
            parse_expected_val_pairs(
                [
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.2)}),
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.0)}),
                    OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 12.0)}),
                    OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.83)}),
                ]
            )
        )
        t1_unexpected: List[ParameterValuePair] = sorted(list(set(t1_no_remove) - set(t1_expected)))

        t1_unexpected_test_param_value_pairs: List[ParameterValuePair] = []
        self.assertFalse(
            remove_parameter_value_pairs(
                t1_no_remove,
                t1_unexpected_test_param_value_pairs,
                HOST_COMPILER,
                GCC,
                9,
                DEVICE_COMPILER,
                NVCC,
                11.2,
            )
        )

        t1_no_remove.sort()
        t1_unexpected_test_param_value_pairs.sort()

        self.assertEqual(
            t1_no_remove, t1_expected, create_diff_parameter_value_pairs(t1_no_remove, t1_expected)
        )
        self.assertEqual(len(t1_no_remove), original_length)
        self.assertEqual(
            t1_unexpected_test_param_value_pairs,
            t1_unexpected,
            create_diff_parameter_value_pairs(t1_unexpected_test_param_value_pairs, t1_unexpected),
        )

        t2_remove_single_entry = copy.deepcopy(t1_no_remove)
        t2_expected = sorted(
            parse_expected_val_pairs(
                [
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.2)}),
                    OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 12.0)}),
                    OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.83)}),
                ]
            )
        )
        t2_unexpected: List[ParameterValuePair] = sorted(
            list(set(t2_remove_single_entry) - set(t2_expected))
        )

        t2_unexpected_test_param_value_pairs: List[ParameterValuePair] = []
        self.assertTrue(
            remove_parameter_value_pairs(
                t2_remove_single_entry,
                t2_unexpected_test_param_value_pairs,
                HOST_COMPILER,
                GCC,
                10,
                DEVICE_COMPILER,
                NVCC,
                12.0,
            )
        )

        t2_remove_single_entry.sort()
        t2_unexpected_test_param_value_pairs.sort()

        self.assertEqual(
            t2_remove_single_entry,
            t2_expected,
            create_diff_parameter_value_pairs(t2_remove_single_entry, t2_expected),
        )
        self.assertEqual(len(t2_remove_single_entry), original_length - 1)
        self.assertEqual(
            t2_unexpected_test_param_value_pairs,
            t2_unexpected,
            create_diff_parameter_value_pairs(t2_unexpected_test_param_value_pairs, t2_unexpected),
        )

        t3_remove_another_entry = copy.deepcopy(t2_remove_single_entry)
        t3_expected = sorted(
            parse_expected_val_pairs(
                [
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.2)}),
                    OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 12.0)}),
                ]
            )
        )
        t3_unexpected: List[ParameterValuePair] = sorted(
            list(set(t3_remove_another_entry) - set(t3_expected))
        )

        t3_unexpected_test_param_value_pairs: List[ParameterValuePair] = []
        self.assertTrue(
            remove_parameter_value_pairs(
                t3_remove_another_entry,
                t3_unexpected_test_param_value_pairs,
                CMAKE,
                CMAKE,
                3.23,
                BOOST,
                BOOST,
                1.83,
            )
        )

        t3_remove_another_entry.sort()
        t3_unexpected_test_param_value_pairs.sort()

        self.assertEqual(
            t3_remove_another_entry,
            t3_expected,
            create_diff_parameter_value_pairs(t3_remove_another_entry, t3_expected),
        )
        self.assertEqual(len(t3_remove_another_entry), original_length - 2)
        self.assertEqual(
            t3_unexpected_test_param_value_pairs,
            t3_unexpected,
            create_diff_parameter_value_pairs(t3_unexpected_test_param_value_pairs, t3_unexpected),
        )

    def test_all_white_card(self):
        test_param_value_pairs: List[ParameterValuePair] = parse_expected_val_pairs(
            [
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.2)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.0)}),
                OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 12.0)}),
                OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.83)}),
            ]
        )
        len_before = len(test_param_value_pairs)

        unexpected_test_param_value_pairs: List[ParameterValuePair] = []
        self.assertTrue(
            remove_parameter_value_pairs(
                test_param_value_pairs,
                unexpected_test_param_value_pairs,
                parameter1=ANY_PARAM,
                value_name1=ANY_NAME,
                value_version1=ANY_VERSION,
                parameter2=ANY_PARAM,
                value_name2=ANY_NAME,
                value_version2=ANY_VERSION,
            )
        )

        self.assertEqual(len(test_param_value_pairs), 0)
        self.assertEqual(len(unexpected_test_param_value_pairs), len_before)

    def test_single_white_card(self):
        test_param_value_pairs: List[ParameterValuePair] = parse_expected_val_pairs(
            [
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.2)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.0)}),
                OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 12.0)}),
                OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (CLANG, 17)}),
                OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (GCC, 17)}),
                OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.83)}),
                OD({HOST_COMPILER: (CLANG, 10), BOOST: (BOOST, 1.83)}),
                OD({HOST_COMPILER: (CLANG, 10), DEVICE_COMPILER: (NVCC, 12.0)}),
            ]
        )
        test_original_len = len(test_param_value_pairs)

        t1_any_version1_param_value_pairs = copy.deepcopy(test_param_value_pairs)
        t1_expected = sorted(
            parse_expected_val_pairs(
                [
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.2)}),
                    OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (CLANG, 17)}),
                    OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (GCC, 17)}),
                    OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.83)}),
                    OD({HOST_COMPILER: (CLANG, 10), BOOST: (BOOST, 1.83)}),
                    OD({HOST_COMPILER: (CLANG, 10), DEVICE_COMPILER: (NVCC, 12.0)}),
                ]
            )
        )
        t1_unexpected: List[ParameterValuePair] = sorted(
            list(set(t1_any_version1_param_value_pairs) - set(t1_expected))
        )

        t1_unexpected_test_param_value_pairs: List[ParameterValuePair] = []
        self.assertTrue(
            remove_parameter_value_pairs(
                t1_any_version1_param_value_pairs,
                t1_unexpected_test_param_value_pairs,
                parameter1=HOST_COMPILER,
                value_name1=GCC,
                value_version1=ANY_VERSION,
                parameter2=DEVICE_COMPILER,
                value_name2=NVCC,
                value_version2=12.0,
            )
        )
        t1_any_version1_param_value_pairs.sort()
        t1_unexpected_test_param_value_pairs.sort()

        self.assertEqual(
            t1_any_version1_param_value_pairs,
            t1_expected,
            create_diff_parameter_value_pairs(t1_any_version1_param_value_pairs, t1_expected),
        )
        self.assertEqual(len(t1_any_version1_param_value_pairs), test_original_len - 2)
        self.assertEqual(
            t1_unexpected_test_param_value_pairs,
            t1_unexpected,
            create_diff_parameter_value_pairs(t1_unexpected_test_param_value_pairs, t1_unexpected),
        )

        t2_any_name1_param_value_pairs = copy.deepcopy(test_param_value_pairs)
        t2_expected = sorted(
            parse_expected_val_pairs(
                [
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.2)}),
                    OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 12.0)}),
                    OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (CLANG, 17)}),
                    OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (GCC, 17)}),
                    OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.83)}),
                    OD({HOST_COMPILER: (CLANG, 10), BOOST: (BOOST, 1.83)}),
                ]
            )
        )
        t2_unexpected: List[ParameterValuePair] = sorted(
            list(set(t2_any_name1_param_value_pairs) - set(t2_expected))
        )

        t2_unexpected_test_param_value_pairs: List[ParameterValuePair] = []
        self.assertTrue(
            remove_parameter_value_pairs(
                t2_any_name1_param_value_pairs,
                t2_unexpected_test_param_value_pairs,
                parameter1=HOST_COMPILER,
                value_name1=ANY_NAME,
                value_version1=10,
                parameter2=DEVICE_COMPILER,
                value_name2=NVCC,
                value_version2=12.0,
            )
        )

        t2_any_name1_param_value_pairs.sort()
        t2_unexpected_test_param_value_pairs.sort()

        self.assertEqual(
            t2_any_name1_param_value_pairs,
            t2_expected,
            create_diff_parameter_value_pairs(t2_any_name1_param_value_pairs, t2_expected),
        )
        self.assertEqual(len(t2_any_name1_param_value_pairs), test_original_len - 2)
        self.assertEqual(
            t2_unexpected_test_param_value_pairs,
            t2_unexpected,
            create_diff_parameter_value_pairs(t2_unexpected_test_param_value_pairs, t2_unexpected),
        )

    def test_white_card_multi_parameter(self):
        t1_any_parameter_param_value_pairs: List[ParameterValuePair] = parse_expected_val_pairs(
            [
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.2)}),
                OD({BOOST: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.2)}),
                OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (CLANG, 17)}),
                OD({HOST_COMPILER: (CLANG, 17), DEVICE_COMPILER: (CLANG, 16)}),
                OD({CMAKE: (GCC, 10), UBUNTU: (NVCC, 11.2)}),
            ]
        )
        test_original_len = len(t1_any_parameter_param_value_pairs)

        t1_expected = sorted(
            parse_expected_val_pairs(
                [
                    OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (CLANG, 17)}),
                    OD({HOST_COMPILER: (CLANG, 17), DEVICE_COMPILER: (CLANG, 16)}),
                ]
            )
        )
        t1_unexpected: List[ParameterValuePair] = sorted(
            list(set(t1_any_parameter_param_value_pairs) - set(t1_expected))
        )

        t1_unexpected_test_param_value_pairs: List[ParameterValuePair] = []
        self.assertTrue(
            remove_parameter_value_pairs(
                t1_any_parameter_param_value_pairs,
                t1_unexpected_test_param_value_pairs,
                parameter1=ANY_PARAM,
                value_name1=GCC,
                value_version1=10,
                parameter2=ANY_PARAM,
                value_name2=NVCC,
                value_version2=11.2,
            )
        )

        t1_any_parameter_param_value_pairs.sort()
        t1_unexpected_test_param_value_pairs.sort()

        self.assertEqual(
            t1_any_parameter_param_value_pairs,
            t1_expected,
            create_diff_parameter_value_pairs(t1_any_parameter_param_value_pairs, t1_expected),
        )
        self.assertEqual(len(t1_any_parameter_param_value_pairs), test_original_len - 3)
        self.assertEqual(
            t1_unexpected_test_param_value_pairs,
            t1_unexpected,
            create_diff_parameter_value_pairs(t1_unexpected_test_param_value_pairs, t1_unexpected),
        )

    def test_remove_all_gcc_host(self):
        test_param_value_pairs: List[ParameterValuePair] = parse_expected_val_pairs(
            [
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.2)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.0)}),
                OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 12.0)}),
                OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (CLANG, 17)}),
                OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (GCC, 17)}),
                OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.83)}),
                OD({HOST_COMPILER: (CLANG, 10), BOOST: (BOOST, 1.83)}),
                OD({HOST_COMPILER: (CLANG, 10), DEVICE_COMPILER: (NVCC, 12.0)}),
            ]
        )
        test_original_len = len(test_param_value_pairs)
        t_expected = sorted(
            parse_expected_val_pairs(
                [
                    OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.83)}),
                    OD({HOST_COMPILER: (CLANG, 10), BOOST: (BOOST, 1.83)}),
                    OD({HOST_COMPILER: (CLANG, 10), DEVICE_COMPILER: (NVCC, 12.0)}),
                ]
            )
        )
        t1_unexpected: List[ParameterValuePair] = sorted(
            list(set(test_param_value_pairs) - set(t_expected))
        )

        unexpected_test_param_value_pairs: List[ParameterValuePair] = []
        self.assertTrue(
            remove_parameter_value_pairs(
                test_param_value_pairs,
                unexpected_test_param_value_pairs,
                parameter1=HOST_COMPILER,
                value_name1=GCC,
                value_version1=ANY_VERSION,
            )
        )

        test_param_value_pairs.sort()
        unexpected_test_param_value_pairs.sort()

        self.assertEqual(
            test_param_value_pairs,
            t_expected,
            create_diff_parameter_value_pairs(test_param_value_pairs, t_expected),
        )
        self.assertEqual(len(test_param_value_pairs), test_original_len - 5)
        self.assertEqual(
            unexpected_test_param_value_pairs,
            t1_unexpected,
            create_diff_parameter_value_pairs(unexpected_test_param_value_pairs, t1_unexpected),
        )

    def test_symmetric(self):
        test_param_value_pairs: List[ParameterValuePair] = parse_expected_val_pairs(
            [
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.2)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.0)}),
                OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.83)}),
                OD({DEVICE_COMPILER: (NVCC, 11.2), HOST_COMPILER: (GCC, 10)}),
                OD({DEVICE_COMPILER: (NVCC, 12.0), HOST_COMPILER: (GCC, 10)}),
                OD({BOOST: (BOOST, 1.83), CMAKE: (CMAKE, 3.23)}),
            ]
        )
        test_original_len = len(test_param_value_pairs)
        t1_expected = sorted(
            parse_expected_val_pairs(
                [
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.2)}),
                    OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.83)}),
                    OD({DEVICE_COMPILER: (NVCC, 11.2), HOST_COMPILER: (GCC, 10)}),
                    OD({BOOST: (BOOST, 1.83), CMAKE: (CMAKE, 3.23)}),
                ]
            )
        )
        t1_single_hit_symmetric_param_value_pairs = copy.deepcopy(test_param_value_pairs)
        t1_unexpected: List[ParameterValuePair] = sorted(
            list(set(t1_single_hit_symmetric_param_value_pairs) - set(t1_expected))
        )

        t1_unexpected_test_param_value_pairs: List[ParameterValuePair] = []
        self.assertTrue(
            remove_parameter_value_pairs(
                t1_single_hit_symmetric_param_value_pairs,
                t1_unexpected_test_param_value_pairs,
                parameter1=HOST_COMPILER,
                value_name1=GCC,
                value_version1=10,
                parameter2=DEVICE_COMPILER,
                value_name2=NVCC,
                value_version2=12.0,
            )
        )

        t1_single_hit_symmetric_param_value_pairs.sort()
        t1_unexpected_test_param_value_pairs.sort()

        self.assertEqual(
            t1_single_hit_symmetric_param_value_pairs,
            t1_expected,
            create_diff_parameter_value_pairs(
                t1_single_hit_symmetric_param_value_pairs, t1_expected
            ),
        )
        self.assertEqual(len(t1_single_hit_symmetric_param_value_pairs), test_original_len - 2)
        self.assertEqual(
            t1_unexpected_test_param_value_pairs,
            t1_unexpected,
            create_diff_parameter_value_pairs(t1_unexpected_test_param_value_pairs, t1_unexpected),
        )

        t2_single_hit_no_symmetric_param_value_pairs = copy.deepcopy(test_param_value_pairs)
        t2_expected = sorted(
            parse_expected_val_pairs(
                [
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.2)}),
                    OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.83)}),
                    OD({DEVICE_COMPILER: (NVCC, 11.2), HOST_COMPILER: (GCC, 10)}),
                    OD({DEVICE_COMPILER: (NVCC, 12.0), HOST_COMPILER: (GCC, 10)}),
                    OD({BOOST: (BOOST, 1.83), CMAKE: (CMAKE, 3.23)}),
                ]
            )
        )
        t2_unexpected: List[ParameterValuePair] = sorted(
            list(set(t2_single_hit_no_symmetric_param_value_pairs) - set(t2_expected))
        )

        t2_unexpected_test_param_value_pairs: List[ParameterValuePair] = []
        self.assertTrue(
            remove_parameter_value_pairs(
                t2_single_hit_no_symmetric_param_value_pairs,
                t2_unexpected_test_param_value_pairs,
                parameter1=HOST_COMPILER,
                value_name1=GCC,
                value_version1=10,
                parameter2=DEVICE_COMPILER,
                value_name2=NVCC,
                value_version2=12.0,
                symmetric=False,
            )
        )

        t2_single_hit_no_symmetric_param_value_pairs.sort()
        t2_unexpected_test_param_value_pairs.sort()

        self.assertEqual(
            t2_single_hit_no_symmetric_param_value_pairs,
            t2_expected,
            create_diff_parameter_value_pairs(
                t2_single_hit_no_symmetric_param_value_pairs, t2_expected
            ),
        )
        self.assertEqual(len(t2_single_hit_no_symmetric_param_value_pairs), test_original_len - 1)
        self.assertEqual(
            t2_unexpected_test_param_value_pairs,
            t2_unexpected,
            create_diff_parameter_value_pairs(t2_unexpected_test_param_value_pairs, t2_unexpected),
        )

        t3_single_hit_no_symmetric_param_value_pairs = copy.deepcopy(test_param_value_pairs)
        t3_expected = sorted(
            parse_expected_val_pairs(
                [
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.2)}),
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.0)}),
                    OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.83)}),
                    OD({DEVICE_COMPILER: (NVCC, 11.2), HOST_COMPILER: (GCC, 10)}),
                    OD({BOOST: (BOOST, 1.83), CMAKE: (CMAKE, 3.23)}),
                ]
            )
        )
        t3_unexpected: List[ParameterValuePair] = sorted(
            list(set(t3_single_hit_no_symmetric_param_value_pairs) - set(t3_expected))
        )

        t3_unexpected_test_param_value_pairs: List[ParameterValuePair] = []
        self.assertTrue(
            remove_parameter_value_pairs(
                t3_single_hit_no_symmetric_param_value_pairs,
                t3_unexpected_test_param_value_pairs,
                parameter1=DEVICE_COMPILER,
                value_name1=NVCC,
                value_version1=12.0,
                parameter2=HOST_COMPILER,
                value_name2=GCC,
                value_version2=10,
                symmetric=False,
            )
        )

        t3_single_hit_no_symmetric_param_value_pairs.sort()
        t3_unexpected_test_param_value_pairs.sort()

        self.assertEqual(
            t3_single_hit_no_symmetric_param_value_pairs,
            t3_expected,
            create_diff_parameter_value_pairs(
                t3_single_hit_no_symmetric_param_value_pairs, t3_expected
            ),
        )
        self.assertEqual(len(t3_single_hit_no_symmetric_param_value_pairs), test_original_len - 1)
        self.assertEqual(
            t3_unexpected_test_param_value_pairs,
            t3_unexpected,
            create_diff_parameter_value_pairs(t3_unexpected_test_param_value_pairs, t3_unexpected),
        )

        t4_multi_hit_symmetric_param_value_pairs = copy.deepcopy(test_param_value_pairs)
        t4_expected = sorted(
            parse_expected_val_pairs(
                [
                    OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.83)}),
                    OD({BOOST: (BOOST, 1.83), CMAKE: (CMAKE, 3.23)}),
                ]
            )
        )
        t4_unexpected: List[ParameterValuePair] = sorted(
            list(set(t4_multi_hit_symmetric_param_value_pairs) - set(t4_expected))
        )

        t4_unexpected_test_param_value_pairs: List[ParameterValuePair] = []
        self.assertTrue(
            remove_parameter_value_pairs(
                t4_multi_hit_symmetric_param_value_pairs,
                t4_unexpected_test_param_value_pairs,
                parameter1=HOST_COMPILER,
                value_name1=GCC,
                value_version1=ANY_VERSION,
            )
        )

        t4_multi_hit_symmetric_param_value_pairs.sort()
        t4_unexpected_test_param_value_pairs.sort()

        self.assertEqual(
            t4_multi_hit_symmetric_param_value_pairs,
            t4_expected,
            create_diff_parameter_value_pairs(
                t4_multi_hit_symmetric_param_value_pairs, t4_expected
            ),
        )
        self.assertEqual(len(t4_multi_hit_symmetric_param_value_pairs), test_original_len - 4)
        self.assertEqual(
            t4_unexpected_test_param_value_pairs,
            t4_unexpected,
            create_diff_parameter_value_pairs(t4_unexpected_test_param_value_pairs, t4_unexpected),
        )

        t5_multi_hit_no_symmetric_param_value_pairs = copy.deepcopy(test_param_value_pairs)
        t5_expected = sorted(
            parse_expected_val_pairs(
                [
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.2)}),
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.0)}),
                    OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.83)}),
                    OD({BOOST: (BOOST, 1.83), CMAKE: (CMAKE, 3.23)}),
                ]
            )
        )
        t5_unexpected: List[ParameterValuePair] = sorted(
            list(set(t5_multi_hit_no_symmetric_param_value_pairs) - set(t5_expected))
        )

        t5_unexpected_test_param_value_pairs: List[ParameterValuePair] = []

        self.assertTrue(
            remove_parameter_value_pairs(
                t5_multi_hit_no_symmetric_param_value_pairs,
                t5_unexpected_test_param_value_pairs,
                parameter2=HOST_COMPILER,
                value_name2=GCC,
                value_version2=ANY_VERSION,
                symmetric=False,
            )
        )

        t5_multi_hit_no_symmetric_param_value_pairs.sort()
        t5_unexpected_test_param_value_pairs.sort()

        self.assertEqual(
            t5_multi_hit_no_symmetric_param_value_pairs,
            t5_expected,
            create_diff_parameter_value_pairs(
                t5_multi_hit_no_symmetric_param_value_pairs, t5_expected
            ),
        )
        self.assertEqual(len(t5_multi_hit_no_symmetric_param_value_pairs), test_original_len - 2)
        self.assertEqual(
            t5_unexpected_test_param_value_pairs,
            t5_unexpected,
            create_diff_parameter_value_pairs(t5_unexpected_test_param_value_pairs, t5_unexpected),
        )

    def test_single_specifier_set(self):
        test_param_value_pairs: List[ParameterValuePair] = parse_expected_val_pairs(
            [
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.0)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.1)}),
                OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 11.2)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.3)}),
                OD({HOST_COMPILER: (GCC, 7), DEVICE_COMPILER: (NVCC, 11.4)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.5)}),
                OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 11.6)}),
                OD({HOST_COMPILER: (GCC, 8), DEVICE_COMPILER: (NVCC, 11.7)}),
                OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 11.8)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.0)}),
                OD({HOST_COMPILER: (GCC, 11), DEVICE_COMPILER: (NVCC, 12.1)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.2)}),
                OD({HOST_COMPILER: (GCC, 7), DEVICE_COMPILER: (NVCC, 12.3)}),
                OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.83)}),
            ]
        )
        test_original_len = len(test_param_value_pairs)

        t1_remove_cuda11 = copy.deepcopy(test_param_value_pairs)
        t1_expected = sorted(
            parse_expected_val_pairs(
                [
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.0)}),
                    OD({HOST_COMPILER: (GCC, 11), DEVICE_COMPILER: (NVCC, 12.1)}),
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.2)}),
                    OD({HOST_COMPILER: (GCC, 7), DEVICE_COMPILER: (NVCC, 12.3)}),
                    OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.83)}),
                ]
            )
        )
        t1_unexpected: List[ParameterValuePair] = sorted(
            list(set(t1_remove_cuda11) - set(t1_expected))
        )

        t1_unexpected_test_param_value_pairs: List[ParameterValuePair] = []
        self.assertTrue(
            remove_parameter_value_pairs(
                t1_remove_cuda11,
                t1_unexpected_test_param_value_pairs,
                parameter2=DEVICE_COMPILER,
                value_name2=NVCC,
                value_version2=">=12",
            )
        )
        t1_remove_cuda11.sort()
        t1_unexpected_test_param_value_pairs.sort()

        self.assertEqual(
            t1_remove_cuda11,
            t1_expected,
            create_diff_parameter_value_pairs(t1_remove_cuda11, t1_expected),
        )
        self.assertEqual(len(t1_remove_cuda11), test_original_len - 9)
        self.assertEqual(
            t1_unexpected_test_param_value_pairs,
            t1_unexpected,
            create_diff_parameter_value_pairs(t1_unexpected_test_param_value_pairs, t1_unexpected),
        )

        t2_cuda113_to_cuda122_ignore_cuda116 = copy.deepcopy(test_param_value_pairs)
        t2_expected = sorted(
            parse_expected_val_pairs(
                [
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.3)}),
                    OD({HOST_COMPILER: (GCC, 7), DEVICE_COMPILER: (NVCC, 11.4)}),
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.5)}),
                    OD({HOST_COMPILER: (GCC, 8), DEVICE_COMPILER: (NVCC, 11.7)}),
                    OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 11.8)}),
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.0)}),
                    OD({HOST_COMPILER: (GCC, 11), DEVICE_COMPILER: (NVCC, 12.1)}),
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.2)}),
                    OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.83)}),
                ]
            )
        )
        t2_unexpected: List[ParameterValuePair] = sorted(
            list(set(t2_cuda113_to_cuda122_ignore_cuda116) - set(t2_expected))
        )

        t2_unexpected_test_param_value_pairs: List[ParameterValuePair] = []
        self.assertTrue(
            remove_parameter_value_pairs(
                t2_cuda113_to_cuda122_ignore_cuda116,
                t2_unexpected_test_param_value_pairs,
                parameter2=DEVICE_COMPILER,
                value_name2=NVCC,
                value_version2=">=11.3,<12.3,!=11.6",
            )
        )

        t2_cuda113_to_cuda122_ignore_cuda116.sort()
        t2_unexpected_test_param_value_pairs.sort()

        self.assertEqual(
            t2_cuda113_to_cuda122_ignore_cuda116,
            t2_expected,
            create_diff_parameter_value_pairs(t2_cuda113_to_cuda122_ignore_cuda116, t2_expected),
        )
        self.assertEqual(len(t2_cuda113_to_cuda122_ignore_cuda116), test_original_len - 5)
        self.assertEqual(
            t2_unexpected_test_param_value_pairs,
            t2_unexpected,
            create_diff_parameter_value_pairs(t2_unexpected_test_param_value_pairs, t2_unexpected),
        )

        t3_gcc_8_and_9 = copy.deepcopy(test_param_value_pairs)
        t3_expected = sorted(
            parse_expected_val_pairs(
                [
                    OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 11.2)}),
                    OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 11.6)}),
                    OD({HOST_COMPILER: (GCC, 8), DEVICE_COMPILER: (NVCC, 11.7)}),
                    OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 11.8)}),
                    OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.83)}),
                ]
            )
        )
        t3_unexpected: List[ParameterValuePair] = sorted(
            list(set(t3_gcc_8_and_9) - set(t3_expected))
        )

        t3_unexpected_test_param_value_pairs: List[ParameterValuePair] = []
        self.assertTrue(
            remove_parameter_value_pairs(
                t3_gcc_8_and_9,
                t3_unexpected_test_param_value_pairs,
                parameter1=HOST_COMPILER,
                value_name1=GCC,
                value_version1=">=8,<=9",
            )
        )

        t3_gcc_8_and_9.sort()
        t3_unexpected_test_param_value_pairs.sort()

        self.assertEqual(
            t3_gcc_8_and_9,
            t3_expected,
            create_diff_parameter_value_pairs(t3_gcc_8_and_9, t3_expected),
        )
        self.assertEqual(len(t3_gcc_8_and_9), test_original_len - 9)
        self.assertEqual(
            t3_unexpected_test_param_value_pairs,
            t3_unexpected,
            create_diff_parameter_value_pairs(t3_unexpected_test_param_value_pairs, t3_unexpected),
        )

    def test_multi_specifier_set(self):
        t1_remove_specific_gcc_and_cuda: List[ParameterValuePair] = parse_expected_val_pairs(
            [
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.0)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.1)}),
                OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 11.2)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.3)}),
                OD({HOST_COMPILER: (GCC, 7), DEVICE_COMPILER: (NVCC, 11.4)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.5)}),
                OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 11.6)}),
                OD({HOST_COMPILER: (GCC, 8), DEVICE_COMPILER: (NVCC, 11.7)}),
                OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 11.8)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.0)}),
                OD({HOST_COMPILER: (GCC, 11), DEVICE_COMPILER: (NVCC, 12.1)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.2)}),
                OD({HOST_COMPILER: (GCC, 7), DEVICE_COMPILER: (NVCC, 12.3)}),
                OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.83)}),
            ]
        )
        test_original_len = len(t1_remove_specific_gcc_and_cuda)

        t1_expected = sorted(
            parse_expected_val_pairs(
                [
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.3)}),
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.5)}),
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.0)}),
                    OD({HOST_COMPILER: (GCC, 11), DEVICE_COMPILER: (NVCC, 12.1)}),
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.2)}),
                    OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.83)}),
                ]
            )
        )
        t1_unexpected: List[ParameterValuePair] = sorted(
            list(set(t1_remove_specific_gcc_and_cuda) - set(t1_expected))
        )

        t1_unexpected_test_param_value_pairs: List[ParameterValuePair] = []

        self.assertTrue(
            remove_parameter_value_pairs(
                t1_remove_specific_gcc_and_cuda,
                t1_unexpected_test_param_value_pairs,
                parameter1=HOST_COMPILER,
                value_name1=GCC,
                value_version1=">=10",
                parameter2=DEVICE_COMPILER,
                value_name2=NVCC,
                value_version2=">=11.3,<=12.2,!=11.6",
            )
        )
        t1_remove_specific_gcc_and_cuda.sort()
        t1_unexpected_test_param_value_pairs.sort()

        self.assertEqual(
            t1_remove_specific_gcc_and_cuda,
            t1_expected,
            create_diff_parameter_value_pairs(t1_remove_specific_gcc_and_cuda, t1_expected),
        )
        self.assertEqual(len(t1_remove_specific_gcc_and_cuda), test_original_len - 8)
        self.assertEqual(
            t1_unexpected_test_param_value_pairs,
            t1_unexpected,
            create_diff_parameter_value_pairs(t1_unexpected_test_param_value_pairs, t1_unexpected),
        )

    def test_version_and_specifier_set(self):
        test_param_value_pairs: List[ParameterValuePair] = parse_expected_val_pairs(
            [
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.0)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.1)}),
                OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 11.2)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.3)}),
                OD({HOST_COMPILER: (GCC, 7), DEVICE_COMPILER: (NVCC, 11.4)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.5)}),
                OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 11.6)}),
                OD({HOST_COMPILER: (GCC, 8), DEVICE_COMPILER: (NVCC, 11.7)}),
                OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 11.8)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.0)}),
                OD({HOST_COMPILER: (GCC, 11), DEVICE_COMPILER: (NVCC, 12.1)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.2)}),
                OD({HOST_COMPILER: (GCC, 7), DEVICE_COMPILER: (NVCC, 12.3)}),
                OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.83)}),
            ]
        )
        test_original_len = len(test_param_value_pairs)

        t1_remove_specific_gcc_and_cuda = copy.deepcopy(test_param_value_pairs)
        t1_expected = sorted(
            parse_expected_val_pairs(
                [
                    OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 11.2)}),
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.3)}),
                    OD({HOST_COMPILER: (GCC, 7), DEVICE_COMPILER: (NVCC, 11.4)}),
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.5)}),
                    OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 11.6)}),
                    OD({HOST_COMPILER: (GCC, 8), DEVICE_COMPILER: (NVCC, 11.7)}),
                    OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 11.8)}),
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.0)}),
                    OD({HOST_COMPILER: (GCC, 11), DEVICE_COMPILER: (NVCC, 12.1)}),
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.2)}),
                    OD({HOST_COMPILER: (GCC, 7), DEVICE_COMPILER: (NVCC, 12.3)}),
                    OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.83)}),
                ]
            )
        )
        t1_unexpected: List[ParameterValuePair] = sorted(
            list(set(t1_remove_specific_gcc_and_cuda) - set(t1_expected))
        )

        t1_unexpected_test_param_value_pairs: List[ParameterValuePair] = []
        self.assertTrue(
            remove_parameter_value_pairs(
                t1_remove_specific_gcc_and_cuda,
                t1_unexpected_test_param_value_pairs,
                parameter1=HOST_COMPILER,
                value_name1=GCC,
                value_version1="10",
                parameter2=DEVICE_COMPILER,
                value_name2=NVCC,
                value_version2=">=11.3,<=12.2,!=11.6",
            )
        )
        t1_remove_specific_gcc_and_cuda.sort()
        t1_unexpected_test_param_value_pairs.sort()

        self.assertEqual(
            t1_remove_specific_gcc_and_cuda,
            t1_expected,
            create_diff_parameter_value_pairs(t1_remove_specific_gcc_and_cuda, t1_expected),
        )
        self.assertEqual(len(t1_remove_specific_gcc_and_cuda), test_original_len - 2)
        self.assertEqual(
            t1_unexpected_test_param_value_pairs,
            t1_unexpected,
            create_diff_parameter_value_pairs(t1_unexpected_test_param_value_pairs, t1_unexpected),
        )

    def test_specifier_set_and_version(self):
        t1_remove_specific_gcc_and_cuda: List[ParameterValuePair] = parse_expected_val_pairs(
            [
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.0)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.1)}),
                OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 11.2)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.3)}),
                OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 11.3)}),
                OD({HOST_COMPILER: (GCC, 11), DEVICE_COMPILER: (NVCC, 11.3)}),
                OD({HOST_COMPILER: (GCC, 7), DEVICE_COMPILER: (NVCC, 11.3)}),
                OD({HOST_COMPILER: (GCC, 7), DEVICE_COMPILER: (NVCC, 11.4)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.5)}),
                OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 11.6)}),
                OD({HOST_COMPILER: (GCC, 8), DEVICE_COMPILER: (NVCC, 11.7)}),
                OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 11.8)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.0)}),
                OD({HOST_COMPILER: (GCC, 11), DEVICE_COMPILER: (NVCC, 12.1)}),
                OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.2)}),
                OD({HOST_COMPILER: (GCC, 7), DEVICE_COMPILER: (NVCC, 12.3)}),
                OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.83)}),
            ]
        )
        test_original_len = len(t1_remove_specific_gcc_and_cuda)
        t1_expected = sorted(
            parse_expected_val_pairs(
                [
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.0)}),
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.1)}),
                    OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 11.2)}),
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.3)}),
                    OD({HOST_COMPILER: (GCC, 11), DEVICE_COMPILER: (NVCC, 11.3)}),
                    OD({HOST_COMPILER: (GCC, 7), DEVICE_COMPILER: (NVCC, 11.4)}),
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 11.5)}),
                    OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 11.6)}),
                    OD({HOST_COMPILER: (GCC, 8), DEVICE_COMPILER: (NVCC, 11.7)}),
                    OD({HOST_COMPILER: (GCC, 9), DEVICE_COMPILER: (NVCC, 11.8)}),
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.0)}),
                    OD({HOST_COMPILER: (GCC, 11), DEVICE_COMPILER: (NVCC, 12.1)}),
                    OD({HOST_COMPILER: (GCC, 10), DEVICE_COMPILER: (NVCC, 12.2)}),
                    OD({HOST_COMPILER: (GCC, 7), DEVICE_COMPILER: (NVCC, 12.3)}),
                    OD({CMAKE: (CMAKE, 3.23), BOOST: (BOOST, 1.83)}),
                ]
            )
        )
        t1_unexpected: List[ParameterValuePair] = sorted(
            list(set(t1_remove_specific_gcc_and_cuda) - set(t1_expected))
        )

        t1_unexpected_test_param_value_pairs: List[ParameterValuePair] = []

        self.assertTrue(
            remove_parameter_value_pairs(
                t1_remove_specific_gcc_and_cuda,
                t1_unexpected_test_param_value_pairs,
                parameter1=HOST_COMPILER,
                value_name1=GCC,
                value_version1=">=10",
                parameter2=DEVICE_COMPILER,
                value_name2=NVCC,
                value_version2="11.3",
            )
        )
        t1_remove_specific_gcc_and_cuda.sort()
        t1_unexpected_test_param_value_pairs.sort()

        self.assertEqual(
            t1_remove_specific_gcc_and_cuda,
            t1_expected,
            create_diff_parameter_value_pairs(t1_remove_specific_gcc_and_cuda, t1_expected),
        )
        self.assertEqual(len(t1_remove_specific_gcc_and_cuda), test_original_len - 2)
        self.assertEqual(
            t1_unexpected_test_param_value_pairs,
            t1_unexpected,
            create_diff_parameter_value_pairs(t1_unexpected_test_param_value_pairs, t1_unexpected),
        )
