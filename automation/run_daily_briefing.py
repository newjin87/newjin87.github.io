import sys
import subprocess
from pathlib import Path

def main():
    """
    Launcher for the Daily Briefing Agent.
    Executes 'generators/daily_briefing/run.py' maintaining the correct working directory.
    """
    # Define paths
    automation_root = Path(__file__).resolve().parent
    agent_dir = automation_root / "generators" / "daily_briefing"
    target_script = agent_dir / "run.py"
    
    print(f"🚀 Launching Daily Briefing Agent...")
    print(f"   Target: {target_script.relative_to(automation_root)}")
    print("=" * 60)

    if not target_script.exists():
        print(f"❌ Error: Script not found at {target_script}")
        sys.exit(1)

    try:
        # Run the agent script in its own directory
        # This ensures imports and relative path handling (like ../../data) work as designed.
        result = subprocess.run(
            [sys.executable, str(target_script.name)], 
            cwd=str(agent_dir), 
            check=False  # Allow script to handle its own errors
        )
        sys.exit(result.returncode)
        
    except KeyboardInterrupt:
        print("\n🛑 Execution interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
