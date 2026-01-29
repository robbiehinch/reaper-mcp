# REAPER MCP Server Testing Guide

This guide explains the test scripts available for verifying your REAPER MCP server setup.

## Test Scripts Overview

### 1. `test_setup.py` - Basic OSC Communication Test

**Purpose**: Verifies that OSC communication between Python and REAPER is working correctly.

**What it tests**:
- OSC client creation
- Creating a new project
- Adding tracks
- Naming tracks
- Creating MIDI items

**When to use**: Run this first to verify basic OSC setup.

**How to run**:
```bash
# Make sure REAPER is running with OSC enabled
venv\Scripts\python test_setup.py
```

**Expected results**:
- New project created in REAPER
- Two tracks: "Test Track" and "Drums"
- MIDI item on the first track

---

### 2. `test_mcp_tools.py` - Comprehensive MCP Tools Test

**Purpose**: Tests all MCP tool functionality through OSC commands.

**What it tests** (16 tests total):
1. Get initial project info
2. Create new project
3-6. Create four tracks (Drums, Bass, Lead Synth, Vocals)
7. List all tracks
8-10. Add MIDI items to three tracks
11. Set track volume
12. Set track pan
13. Mute track
14. Solo track
15. Unsolo track
16. Get final project info

**When to use**: Run this after `test_setup.py` to thoroughly test all MCP tool operations.

**How to run**:
```bash
# Make sure REAPER is running with OSC enabled
venv\Scripts\python test_mcp_tools.py
```

**Expected results**:
- New project with four tracks:
  - Drums (with MIDI item, reduced volume)
  - Bass (with MIDI item, panned left)
  - Lead Synth (with MIDI item, soloed then unsoloed)
  - Vocals (muted)

---

### 3. `test_mcp_protocol.py` - MCP Protocol Interface Test

**Purpose**: Tests the MCP server as it would be used by Claude or other AI agents through the MCP protocol.

**What it tests**:
- MCP protocol connection
- Listing available tools
- Calling tools through the MCP interface:
  - `get_project_info`
  - `create_project`
  - `create_track`
  - `list_tracks`
  - `add_midi_note`

**When to use**: Run this to verify the full MCP protocol stack works correctly.

**IMPORTANT**: This test starts its own MCP server instance, so:
- Stop the running MCP server before running this test
- Or use `test_mcp_tools.py` instead if you want to keep the server running

**How to run**:
```bash
# Stop the MCP server first if it's running
venv\Scripts\python test_mcp_protocol.py
```

**Expected results**:
- List of all available MCP tools
- New project named "MCP Protocol Test Project"
- Four tracks: Piano, Strings, Brass, Percussion
- MIDI items on the first three tracks

---

## Prerequisites

Before running any tests, ensure:

1. **REAPER is running**
2. **OSC is enabled in REAPER**:
   - Go to Preferences > Control/OSC/web
   - Add OSC control surface
   - Configure:
     - Local listen port: `8000`
     - Local IP: `127.0.0.1`
3. **Python virtual environment is activated**:
   ```bash
   venv\Scripts\activate
   ```

---

## Troubleshooting

### Tests fail with connection errors

**Check**:
1. REAPER is running
2. OSC settings in REAPER match the test configuration
3. No firewall is blocking localhost communication on ports 8000-9001

### Tests pass but nothing happens in REAPER

**Check**:
1. OSC is properly configured in REAPER
2. The correct port (8000) is set in REAPER's OSC settings
3. Try restarting REAPER and re-running the tests

### Unicode errors on Windows

All test scripts use ASCII characters only to avoid Windows console encoding issues.

### MCP protocol test fails

**Check**:
1. Stop any running MCP server instances first
2. Ensure all dependencies are installed: `pip install -e .`
3. Use `test_mcp_tools.py` instead if you want to keep the server running

---

## Test Execution Order

For a complete verification of your setup:

1. **First time setup**:
   ```bash
   venv\Scripts\python test_setup.py
   ```

2. **Comprehensive testing**:
   ```bash
   venv\Scripts\python test_mcp_tools.py
   ```

3. **MCP protocol verification** (optional):
   ```bash
   # Stop MCP server first
   venv\Scripts\python test_mcp_protocol.py
   ```

---

## What Each Test Validates

| Test | OSC Comm | Track Ops | MIDI | Volume/Pan | Mute/Solo | MCP Protocol |
|------|----------|-----------|------|------------|-----------|--------------|
| test_setup.py | ✓ | ✓ | ✓ | | | |
| test_mcp_tools.py | ✓ | ✓ | ✓ | ✓ | ✓ | |
| test_mcp_protocol.py | ✓ | ✓ | ✓ | | | ✓ |

---

## Success Criteria

Your REAPER MCP server setup is working correctly if:

- ✓ All test scripts complete without errors
- ✓ You can see the expected changes in REAPER after each test
- ✓ The MCP server logs show successful command processing
- ✓ Claude (or other AI agents) can successfully call the MCP tools

---

## Next Steps

After successful testing:

1. **Configure Claude to use the MCP server**:
   - Add the server configuration to your Claude settings
   - Test basic commands through Claude

2. **Explore advanced features**:
   - Check the examples folder for more complex use cases
   - Try creating complete musical compositions

3. **Customize**:
   - Modify OSC settings for your network setup
   - Add custom tools as needed

---

## Support

If tests continue to fail:

1. Check the main README.md for detailed setup instructions
2. Verify REAPER version compatibility
3. Review the OSC configuration in REAPER
4. Check the MCP server logs for error messages
