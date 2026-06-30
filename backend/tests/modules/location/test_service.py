from app.modules.location.service import calculate_position

def test_calculate_position_with_three_aps():
    """
    Given 3 APs with known positions and RSSI, 
    return the asset's X/Y coordinate.
    """
    # Mock data: 3 APs forming a triangle
    # AP1 is at (0,0), AP2 at (10,0), AP3 at (5,10)
    # RSSI is strongest (-50) at AP1, so the asset should be closest to AP1
    aps = [
        {"id": "AP-1", "x": 0.0, "y": 0.0, "rssi": -50},
        {"id": "AP-2", "x": 10.0, "y": 0.0, "rssi": -80},
        {"id": "AP-3", "x": 5.0, "y": 10.0, "rssi": -70},
    ]
    
    x, y = calculate_position(aps)
    
    # We expect the result to be closer to (0,0) than (10,0) or (5,10)
    # A weighted centroid should put it roughly around x=2.5, y=1.5
    assert x is not None
    assert y is not None
    assert x < 5.0  # Closer to AP-1 (x=0) than AP-2 (x=10)
    assert y < 5.0  # Closer to AP-1 (y=0) than AP-3 (y=10)

def test_calculate_position_insufficient_data():
    """
    If we have fewer than 3 APs, we cannot trilaterate.
    The function should return None.
    """
    aps = [
        {"id": "AP-1", "x": 0.0, "y": 0.0, "rssi": -50},
        {"id": "AP-2", "x": 10.0, "y": 0.0, "rssi": -80},
    ]
    
    result = calculate_position(aps)
    assert result is None

def test_calculate_position_handles_zero_rssi():
    """
    If an AP reports 0 RSSI, we should ignore it or handle it safely,
    not crash with ZeroDivisionError.
    """
    aps = [
        {"id": "AP-1", "x": 0.0, "y": 0.0, "rssi": 0},  # Bad data
        {"id": "AP-2", "x": 10.0, "y": 0.0, "rssi": -70},
        {"id": "AP-3", "x": 5.0, "y": 10.0, "rssi": -60},
    ]
    
    # Should not crash
    result = calculate_position(aps)
    assert result is not None