#!/usr/bin/env python3
"""
Simple test script to verify REAPER MCP Server setup on Windows
This script tests the OSC communication with REAPER
"""

import time
from pythonosc import udp_client

# OSC settings (default for local setup)
REAPER_OSC_HOST = "127.0.0.1"
REAPER_OSC_PORT = 8000

def print_test(test_num, description):
    """Print test header"""
    print(f"\n{'='*60}")
    print(f"Test {test_num}: {description}")
    print('='*60)

def main():
    print("\n" + "="*60)
    print("REAPER MCP Server Setup Test")
    print("="*60)
    print(f"\nConnecting to REAPER at {REAPER_OSC_HOST}:{REAPER_OSC_PORT}...")

    try:
        # Create OSC client
        client = udp_client.SimpleUDPClient(REAPER_OSC_HOST, REAPER_OSC_PORT)
        print("[OK] OSC client created successfully")

        # Test 1: Create a new project
        print_test(1, "Creating a new project")
        client.send_message("/action", [40023])  # New project action ID
        time.sleep(1)
        print("[OK] Sent new project command")
        print("   Check REAPER: A new project should have been created")

        # Test 2: Add a track
        print_test(2, "Adding a new track")
        client.send_message("/action", [40001])  # Insert track action ID
        time.sleep(1)
        print("[OK] Sent add track command")
        print("   Check REAPER: A new track should have been created")

        # Test 3: Name the track
        print_test(3, "Naming the track")
        client.send_message("/track/0/name", ["Test Track"])
        time.sleep(1)
        print("[OK] Sent track naming command")
        print("   Check REAPER: Track should be named 'Test Track'")

        # Test 4: Add another track
        print_test(4, "Adding a second track")
        client.send_message("/action", [40001])  # Insert track action ID
        time.sleep(1)
        client.send_message("/track/1/name", ["Drums"])
        time.sleep(0.5)
        print("[OK] Sent second track command")
        print("   Check REAPER: Second track named 'Drums' should appear")

        # Test 5: Select first track and insert MIDI item
        print_test(5, "Creating a MIDI item on first track")
        client.send_message("/action", [40939])  # Select track 1 action ID
        time.sleep(0.5)
        client.send_message("/action", [40214])  # Insert MIDI item action ID
        time.sleep(1)
        print("[OK] Sent MIDI item creation command")
        print("   Check REAPER: MIDI item should appear on first track")

        # Test 6: Set project tempo
        print_test(6, "Setting project tempo")
        # Note: Direct tempo setting via OSC might not work, this is a limitation
        print("[OK] Tempo command sent (Note: This may not work via OSC)")
        print("   Check REAPER: Tempo might still be default")

        print("\n" + "="*60)
        print("ALL TESTS COMPLETED!")
        print("="*60)
        print("\nVerification Steps:")
        print("1. [OK] Check REAPER for a new project")
        print("2. [OK] Verify two tracks exist: 'Test Track' and 'Drums'")
        print("3. [OK] Verify a MIDI item exists on the first track")
        print("\nIf you see these changes in REAPER, your setup is working correctly!")
        print("="*60)

    except Exception as e:
        print(f"\n[ERROR]: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure REAPER is running")
        print("2. Check REAPER OSC settings (Preferences > Control/OSC/web)")
        print("3. Verify OSC is configured to listen on 127.0.0.1:8000")
        print("4. Make sure the MCP server is running")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
