from services.replenishment_api.engine import create_recommendation, round_to_case_pack, select_execution_method


def test_round_to_case_pack() -> None:
    assert round_to_case_pack(13, 12) == 24
    assert round_to_case_pack(24, 12) == 24


def test_execution_method_for_heavy_case() -> None:
    assert select_execution_method({"handling_class": "heavy", "case_weight": 22}) == "forklift"


def test_create_recommendation() -> None:
    event = {
        "inspection_id": "insp-1",
        "facility_id": "cs-facility-001",
        "location_id": "A01-R01-B01-L01",
        "fill_state": "empty",
        "fill_percentage": 0,
        "confidence_score": 0.94,
    }
    plan = {"sku_id": "SKU-10001", "max_capacity": "24", "min_threshold": "8"}
    sku = {"sku_id": "SKU-10001", "case_pack": "12", "handling_class": "standard_case", "case_weight": "7.5"}
    inventory = [{"source_location_id": "RESERVE-A09-B01", "sku_id": "SKU-10001", "available_quantity": "120", "reserved_quantity": "0"}]
    recommendation = create_recommendation(event, plan, sku, inventory)
    assert recommendation["recommended_quantity"] == 24
    assert recommendation["recommendation_status"] == "pending_approval"

