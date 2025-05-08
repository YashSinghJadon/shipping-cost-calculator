#!/usr/bin/env python3
"""
Shipping Cost Calculator
------------------------
A tool to calculate shipping costs based on package details.
"""

import sys

# Constants for shipping rate calculations
BASE_RATES = {
    "economy": 5.00,
    "standard": 8.00,
    "express": 12.00
}

WEIGHT_MULTIPLIERS = {
    "economy": 1.0,
    "standard": 1.5,
    "express": 2.0
}

ZONE_MULTIPLIERS = {
    1: 1.0,  # Local
    2: 1.5,  # Regional
    3: 2.0,  # National
    4: 3.0   # International
}

def calculate_shipping_cost(weight, dimensions, zone, shipping_method):
    """
    Calculate shipping cost based on weight, dimensions, zone, and shipping method.
    
    Args:
        weight (float): Package weight in kg
        dimensions (tuple): Package dimensions (length, width, height) in cm
        zone (int): Shipping zone (1-4)
        shipping_method (str): Shipping method ('economy', 'standard', 'express')
    
    Returns:
        float: Calculated shipping cost
    """
    # Validate inputs
    if weight <= 0:
        raise ValueError("Weight must be greater than zero")
    
    if any(dim <= 0 for dim in dimensions):
        raise ValueError("All dimensions must be greater than zero")
    
    if zone not in ZONE_MULTIPLIERS:
        raise ValueError(f"Invalid zone. Must be one of {list(ZONE_MULTIPLIERS.keys())}")
    
    if shipping_method.lower() not in BASE_RATES:
        raise ValueError(f"Invalid shipping method. Must be one of {list(BASE_RATES.keys())}")
    
    # Calculate volumetric weight (length × width × height / 5000)
    length, width, height = dimensions
    volumetric_weight = (length * width * height) / 5000
    
    # Use the greater of actual weight or volumetric weight
    chargeable_weight = max(weight, volumetric_weight)
    
    # Calculate base cost
    base_cost = BASE_RATES[shipping_method.lower()]
    
    # Apply multipliers
    weight_factor = WEIGHT_MULTIPLIERS[shipping_method.lower()]
    zone_factor = ZONE_MULTIPLIERS[zone]
    
    # Final cost calculation
    cost = base_cost + (chargeable_weight * weight_factor * zone_factor)
    
    return round(cost, 2)

def get_user_input():
    """
    Get shipping details from user input
    
    Returns:
        tuple: (weight, dimensions, zone, shipping_method)
    """
    try:
        print("Welcome to the Shipping Cost Calculator!")
        print("---------------------------------------")
        
        # Get weight
        weight = float(input("Enter package weight (kg): "))
        
        # Get dimensions
        dim_input = input("Enter package dimensions (LxWxH in cm, e.g. 30x20x15): ")
        dimensions = tuple(map(float, dim_input.split('x')))
        if len(dimensions) != 3:
            raise ValueError("Dimensions must be in the format LxWxH")
        
        # Get zone
        print("\nShipping Zones:")
        print("1 - Local")
        print("2 - Regional")
        print("3 - National")
        print("4 - International")
        zone = int(input("Select destination zone (1-4): "))
        
        # Get shipping method
        print("\nShipping Methods:")
        print("1 - Economy")
        print("2 - Standard")
        print("3 - Express")
        method_choice = int(input("Select shipping provider (1-Economy, 2-Standard, 3-Express): "))
        
        method_map = {1: "economy", 2: "standard", 3: "express"}
        shipping_method = method_map.get(method_choice)
        if not shipping_method:
            raise ValueError("Invalid shipping method selection")
        
        return weight, dimensions, zone, shipping_method
    
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    """Main function to run the shipping cost calculator"""
    try:
        weight, dimensions, zone, shipping_method = get_user_input()
        cost = calculate_shipping_cost(weight, dimensions, zone, shipping_method)
        
        print(f"\nEstimated Shipping Cost: ${cost:.2f}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
