import numpy as np
import pandas as pd

from zentickr.server import convert_to_json_serializable, format_response


def test_dataframe_with_index_becomes_records():
    df = pd.DataFrame({"a": [1, 2]}, index=pd.Index(["x", "y"], name="sym"))
    assert convert_to_json_serializable(df) == [
        {"sym": "x", "a": 1},
        {"sym": "y", "a": 2},
    ]


def test_series_becomes_dict():
    s = pd.Series({"a": 1, "b": 2})
    assert convert_to_json_serializable(s) == {"a": 1, "b": 2}


def test_nested_dict_and_list_are_converted():
    data = {"outer": [pd.Series({"a": 1}), {"inner": float("nan")}]}
    assert convert_to_json_serializable(data) == {"outer": [{"a": 1}, {"inner": None}]}


def test_scalar_nan_and_nat_become_none():
    assert convert_to_json_serializable(float("nan")) is None
    assert convert_to_json_serializable(pd.NaT) is None


def test_array_like_does_not_raise():
    arr = np.array([1.0, float("nan")])
    # Old code raised ValueError (ambiguous truth value of pd.isna(array)).
    result = convert_to_json_serializable(arr)
    assert result is arr


def test_format_response_empty_data_says_no_data():
    assert format_response(None, "T") == "T: No data available"
    assert format_response([], "T") == "T: No data available"
    assert format_response({}, "T") == "T: No data available"


def test_format_response_pretty_prints_title_and_json():
    out = format_response({"a": 1}, "T")
    assert out.startswith("T:\n")
    assert '"a": 1' in out
