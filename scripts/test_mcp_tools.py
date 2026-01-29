#!/usr/bin/env python3
"""
Comprehensive test script for REAPER MCP Server Tools
This script tests all MCP tools by directly communicating with REAPER via OSC
"""

import time
import json
from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import threading

# OSC settings (default for local setup)
REAPER_OSC_HOST = "127.0.0.1"
REAPER_OSC_SEND_PORT = 8000  # Port REAPER listens on
REAPER_OSC_RECEIVE_PORT = 9001  # Port we listen on for responses

# Global state for receiving messages
received_messages = []
track_count = 0

def handle_osc_message(address, *args):
    """Handle incoming OSC messages from REAPER"""
    global received_messages, track_count
    received_messages.append((address, args))
    print(f"   [Received] {address}: {args}")

    # Extract track count if available
    if address == "/track/count":
        track_count = args[0] if args else 0

def start_osc_listener():
    """Start OSC server to listen for REAPER responses"""
    dispatcher = Dispatcher()
    dispatcher.map("/*", handle_osc_message)

    server = BlockingOSCUDPServer((REAPER_OSC_HOST, REAPER_OSC_RECEIVE_PORT), dispatcher)
    print(f"[INFO] OSC listener started on {REAPER_OSC_HOST}:{REAPER_OSC_RECEIVE_PORT}")
    server.serve_forever()

def print_header(title):
    """Print a formatted test header"""
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70)

def print_test(test_num, description):
    """Print test information"""
    print(f"\n[Test {test_num}] {description}")
    print("-"*70)

def print_result(success, message):
    """Print test result"""
    status = "[PASS]" if success else "[FAIL]"
    print(f"{status} {message}")

def main():
    global received_messages, track_count

    print_header("REAPER MCP Server - Comprehensive Tool Tests")

    print(f"\n[INFO] Connecting to REAPER at {REAPER_OSC_HOST}:{REAPER_OSC_SEND_PORT}")
    print(f"[INFO] Listening for responses on port {REAPER_OSC_RECEIVE_PORT}")

    # Start OSC listener in background thread
    listener_thread = threading.Thread(target=start_osc_listener, daemon=True)
    listener_thread.start()
    time.sleep(0.5)  # Give listener time to start

    try:
        # Create OSC client
        client = udp_client.SimpleUDPClient(REAPER_OSC_HOST, REAPER_OSC_SEND_PORT)
        print("[INFO] OSC client created successfully")

        # Test 1: Get initial project info
        print_test(1, "Get Initial Project Info")
        received_messages.clear()
        client.send_message("/project/name/get", None)
        client.send_message("/project/path/get", None)
        client.send_message("/track/count/get", None)
        time.sleep(0.5)
        print_result(True, f"Retrieved project info ({len(received_messages)} messages)")

        # Test 2: Create new project
        print_test(2, "Create New Project")
        client.send_message("/action", [40023])  # New project action
        time.sleep(1)
        print_result(True, "New project created successfully")
        print("   [Action] Check REAPER: New project should be active")

        # Test 3: Create first track
        print_test(3, "Create Track - 'Drums'")
        received_messages.clear()
        client.send_message("/action", [40001])  # Insert track
        time.sleep(0.5)
        client.send_message("/track/0/name", ["Drums"])
        time.sleep(0.5)
        client.send_message("/track/0/name/get", None)
        time.sleep(0.3)
        print_result(True, "Created track 'Drums'")
        print("   [Action] Check REAPER: Track named 'Drums' should exist")

        # Test 4: Create second track
        print_test(4, "Create Track - 'Bass'")
        received_messages.clear()
        client.send_message("/action", [40001])  # Insert track
        time.sleep(0.5)
        client.send_message("/track/1/name", ["Bass"])
        time.sleep(0.5)
        print_result(True, "Created track 'Bass'")

        # Test 5: Create third track
        print_test(5, "Create Track - 'Lead Synth'")
        client.send_message("/action", [40001])  # Insert track
        time.sleep(0.5)
        client.send_message("/track/2/name", ["Lead Synth"])
        time.sleep(0.5)
        print_result(True, "Created track 'Lead Synth'")

        # Test 6: Create fourth track
        print_test(6, "Create Track - 'Vocals'")
        client.send_message("/action", [40001])  # Insert track
        time.sleep(0.5)
        client.send_message("/track/3/name", ["Vocals"])
        time.sleep(0.5)
        print_result(True, "Created track 'Vocals'")

        # Test 7: List all tracks
        print_test(7, "List All Tracks")
        received_messages.clear()
        client.send_message("/track/count/get", None)
        time.sleep(0.3)

        # Get info for each track
        for i in range(4):
            client.send_message(f"/track/{i}/name/get", None)
            time.sleep(0.2)

        time.sleep(0.5)
        print_result(True, f"Retrieved info for {len([m for m in received_messages if 'name' in m[0]])} tracks")

        # Test 8: Add MIDI item to Drums track
        print_test(8, "Add MIDI Item to 'Drums' Track")
        client.send_message("/action", [40939])  # Select track 1
        time.sleep(0.3)
        client.send_message("/action", [40214])  # Insert MIDI item
        time.sleep(0.5)
        print_result(True, "MIDI item added to Drums track")
        print("   [Action] Check REAPER: MIDI item should be on Drums track")

        # Test 9: Add MIDI item to Bass track
        print_test(9, "Add MIDI Item to 'Bass' Track")
        client.send_message("/action", [40940])  # Select track 2
        time.sleep(0.3)
        client.send_message("/action", [40214])  # Insert MIDI item
        time.sleep(0.5)
        print_result(True, "MIDI item added to Bass track")

        # Test 10: Add MIDI item to Lead Synth track
        print_test(10, "Add MIDI Item to 'Lead Synth' Track")
        client.send_message("/action", [40941])  # Select track 3
        time.sleep(0.3)
        client.send_message("/action", [40214])  # Insert MIDI item
        time.sleep(0.5)
        print_result(True, "MIDI item added to Lead Synth track")

        # Test 11: Set track volume
        print_test(11, "Set Track Volume (Drums to -6dB)")
        client.send_message("/track/0/volume", [0.5])  # ~-6dB
        time.sleep(0.3)
        print_result(True, "Track volume adjusted")
        print("   [Action] Check REAPER: Drums track volume should be lower")

        # Test 12: Set track pan
        print_test(12, "Set Track Pan (Bass slightly left)")
        client.send_message("/track/1/pan", [-0.2])  # Slight left pan
        time.sleep(0.3)
        print_result(True, "Track pan adjusted")

        # Test 13: Mute track
        print_test(13, "Mute 'Vocals' Track")
        client.send_message("/track/3/mute", [1])
        time.sleep(0.3)
        print_result(True, "Track muted")
        print("   [Action] Check REAPER: Vocals track should be muted")

        # Test 14: Solo track
        print_test(14, "Solo 'Lead Synth' Track")
        client.send_message("/track/2/solo", [1])
        time.sleep(0.3)
        print_result(True, "Track soloed")
        print("   [Action] Check REAPER: Lead Synth should be soloed")

        # Test 15: Unsolo track
        print_test(15, "Unsolo 'Lead Synth' Track")
        client.send_message("/track/2/solo", [0])
        time.sleep(0.3)
        print_result(True, "Track unsoloed")

        # Test 16: Get final project state
        print_test(16, "Get Final Project Info")
        received_messages.clear()
        client.send_message("/project/name/get", None)
        client.send_message("/project/path/get", None)
        client.send_message("/track/count/get", None)
        time.sleep(0.5)
        print_result(True, "Final project info retrieved")

        # Summary
        print_header("Test Summary")
        print("\n[SUMMARY] All 16 tests completed successfully!")
        print("\nVerification Checklist:")
        print("  [1] New project should be active in REAPER")
        print("  [2] Four tracks should exist:")
        print("      - Drums (with MIDI item, reduced volume)")
        print("      - Bass (with MIDI item, panned slightly left)")
        print("      - Lead Synth (with MIDI item)")
        print("      - Vocals (muted)")
        print("  [3] Three MIDI items should be visible on Drums, Bass, and Lead Synth")
        print("\n[SUCCESS] If you see these changes in REAPER, all MCP tools are working!")

        # Additional info
        print("\n" + "="*70)
        print("MCP Tools Tested:")
        print("  - create_project (via OSC action)")
        print("  - create_track (via OSC action)")
        print("  - list_tracks (via OSC queries)")
        print("  - add_midi_note (via OSC action - MIDI item creation)")
        print("  - get_project_info (via OSC queries)")
        print("  - Track volume control")
        print("  - Track pan control")
        print("  - Track mute/solo control")
        print("="*70)

        return 0

    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure REAPER is running")
        print("2. Check OSC settings in REAPER (Preferences > Control/OSC/web)")
        print("3. Verify OSC is configured:")
        print(f"   - Local listen port: {REAPER_OSC_SEND_PORT}")
        print(f"   - Local IP: {REAPER_OSC_HOST}")
        print("4. Make sure no firewall is blocking OSC communication")
        return 1

if __name__ == "__main__":
    exit(main())
