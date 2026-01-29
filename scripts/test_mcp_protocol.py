#!/usr/bin/env python3
"""
Test script for MCP Protocol Interface
This script tests the actual MCP tools as they would be called by Claude or AI agents
"""

import json
import time
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_mcp_tools():
    """Test MCP tools through the protocol interface"""

    print("="*70)
    print(" REAPER MCP Protocol Interface Test")
    print("="*70)
    print("\nThis test demonstrates how AI agents (like Claude) interact with")
    print("the REAPER MCP server through the MCP protocol.\n")

    # Server parameters - adjust path to your MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "reaper_mcp", "--mode=osc", "--host=127.0.0.1", "--send-port=8000", "--receive-port=9000"],
        env=None
    )

    try:
        print("[INFO] Starting MCP client connection...")

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                print("[OK] Connected to MCP server")

                # Initialize the connection
                await session.initialize()
                print("[OK] Session initialized")

                # List available tools
                print("\n" + "-"*70)
                print("Available MCP Tools:")
                print("-"*70)

                tools_response = await session.list_tools()
                for i, tool in enumerate(tools_response.tools, 1):
                    print(f"{i}. {tool.name}")
                    print(f"   Description: {tool.description}")
                    if hasattr(tool, 'inputSchema'):
                        params = tool.inputSchema.get('properties', {})
                        if params:
                            print(f"   Parameters: {', '.join(params.keys())}")
                    print()

                # Test 1: Get project info
                print("-"*70)
                print("[Test 1] Calling 'get_project_info' tool")
                print("-"*70)

                result = await session.call_tool("get_project_info", arguments={})
                print(f"Result: {json.dumps(result.content[0].text, indent=2)}")

                # Test 2: Create a new project
                print("\n" + "-"*70)
                print("[Test 2] Calling 'create_project' tool")
                print("-"*70)

                result = await session.call_tool("create_project", arguments={
                    "name": "MCP Protocol Test Project",
                    "template": None
                })
                print(f"Result: {result.content[0].text}")
                time.sleep(1)

                # Test 3: Create tracks
                print("\n" + "-"*70)
                print("[Test 3] Calling 'create_track' tool (multiple tracks)")
                print("-"*70)

                track_names = ["Piano", "Strings", "Brass", "Percussion"]
                created_tracks = []

                for track_name in track_names:
                    result = await session.call_tool("create_track", arguments={
                        "name": track_name
                    })
                    print(f"  Created: {track_name} - {result.content[0].text}")
                    created_tracks.append(track_name)
                    time.sleep(0.5)

                # Test 4: List tracks
                print("\n" + "-"*70)
                print("[Test 4] Calling 'list_tracks' tool")
                print("-"*70)

                result = await session.call_tool("list_tracks", arguments={})
                print(f"Result: {result.content[0].text}")

                # Test 5: Add MIDI notes to tracks
                print("\n" + "-"*70)
                print("[Test 5] Calling 'add_midi_note' tool")
                print("-"*70)

                for i, track_name in enumerate(created_tracks[:3]):  # Add to first 3 tracks
                    result = await session.call_tool("add_midi_note", arguments={
                        "track_index": i,
                        "note": str(60 + i*2),  # C4, D4, E4
                        "start_time": "0.0",
                        "duration": "1.0",
                        "velocity": "100"
                    })
                    print(f"  Track {i} ({track_name}): {result.content[0].text}")
                    time.sleep(0.5)

                # Test 6: Get final project info
                print("\n" + "-"*70)
                print("[Test 6] Calling 'get_project_info' again (final state)")
                print("-"*70)

                result = await session.call_tool("get_project_info", arguments={})
                print(f"Result: {json.dumps(result.content[0].text, indent=2)}")

                # Summary
                print("\n" + "="*70)
                print(" Test Summary")
                print("="*70)
                print("\n[SUCCESS] All MCP protocol tests completed!")
                print("\nMCP Tools Tested via Protocol:")
                print("  1. get_project_info - Retrieved project information")
                print("  2. create_project - Created new project")
                print("  3. create_track - Created multiple tracks")
                print("  4. list_tracks - Listed all tracks")
                print("  5. add_midi_note - Added MIDI items to tracks")
                print("\nVerification:")
                print("  Check REAPER for:")
                print("  - Project named 'MCP Protocol Test Project'")
                print(f"  - {len(created_tracks)} tracks: {', '.join(created_tracks)}")
                print("  - MIDI items on the first 3 tracks")
                print("\n[INFO] This is how Claude and other AI agents interact with REAPER!")
                print("="*70)

    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        print("\nNote: This test requires the MCP server to NOT be running already,")
        print("as it starts its own instance. If the MCP server is running,")
        print("please stop it first and run this test again.")
        print("\nAlternatively, use the test_mcp_tools.py script which works")
        print("with a running MCP server.")
        return 1

    return 0

def main():
    """Main entry point"""
    try:
        return asyncio.run(test_mcp_tools())
    except KeyboardInterrupt:
        print("\n[INFO] Test interrupted by user")
        return 1

if __name__ == "__main__":
    exit(main())
