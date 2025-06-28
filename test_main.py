import pytest
from main import read_csv, apply_filter, apply_aggregation, parse_condition, evaluate_condition
import csv
import os
from typing import List, Dict


@pytest.fixture
def sample_csv(tmp_path):
    csv_data = [
        ["name", "brand", "price", "rating"],
        ["iphone 15 pro", "apple", "999", "4.9"],
        ["galaxy s23 ultra", "samsung", "1199", "4.8"],
        ["redmi note 12", "xiaomi", "199", "4.6"],
        ["poco x5 pro", "xiaomi", "299", "4.4"]
    ]
    
    file_path = tmp_path / "test.csv"
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)
    
    return str(file_path)


def test_read_csv(sample_csv):
    data = read_csv(sample_csv)
    assert len(data) == 4
    assert data[0]["name"] == "iphone 15 pro"
    assert data[1]["brand"] == "samsung"
    assert data[2]["price"] == "199"


def test_parse_condition():
    assert parse_condition("rating>4.5") == ("rating", ">", "4.5")
    assert parse_condition("brand=apple") == ("brand", "=", "apple")
    assert parse_condition("price<=1000") == ("price", "<=", "1000")


def test_evaluate_condition():
    assert evaluate_condition("4.9", ">", "4.5") is True
    assert evaluate_condition("apple", "=", "apple") is True
    assert evaluate_condition("199", "<", "200") is True
    assert evaluate_condition("samsung", "!=", "apple") is True


def test_apply_filter(sample_csv):
    data = read_csv(sample_csv)
    
    filtered = apply_filter(data, "rating>4.7")
    assert len(filtered) == 2
    assert filtered[0]["name"] == "iphone 15 pro"
    assert filtered[1]["name"] == "galaxy s23 ultra"
    
    filtered = apply_filter(data, "brand=xiaomi")
    assert len(filtered) == 2
    assert all(item["brand"] == "xiaomi" for item in filtered)


def test_apply_aggregation(sample_csv):
    data = read_csv(sample_csv)
    
    result = apply_aggregation(data, "rating=avg")
    assert pytest.approx(result["avg"], 0.01) == 4.675
    
    result = apply_aggregation(data, "price=min")
    assert result["min"] == 199.0
    
    result = apply_aggregation(data, "price=max")
    assert result["max"] == 1199.0
    
    # Ошибка при агрегации нечислового поля
    with pytest.raises(ValueError):
        apply_aggregation(data, "name=avg")


def test_integration(sample_csv, capsys):
    from main import main
    import sys
    
    sys.argv = ["main.py", "--file", sample_csv, "--where", "rating>4.7"]
    main()
    captured = capsys.readouterr()
    assert "iphone 15 pro" in captured.out
    assert "galaxy s23 ultra" in captured.out
    assert "redmi note 12" not in captured.out
    
    sys.argv = ["main.py", "--file", sample_csv, "--aggregate", "rating=avg"]
    main()
    captured = capsys.readouterr()
    assert "4.67" in captured.out