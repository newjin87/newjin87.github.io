import argparse
import sys
import subprocess
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent
GENERATORS_DIR = BASE_DIR / "generators"

def list_agents():
    """Lists all available agents in the generators directory."""
    print("\n🤖 Available AI Agents:")
    if not GENERATORS_DIR.exists():
        print("   (No generators directory found)")
        return
    
    agents = []
    for item in GENERATORS_DIR.iterdir():
        if item.is_dir() and (item / "run.py").exists():
            agents.append(item.name)
    
    if agents:
        for name in sorted(agents):
            print(f"   🔹 {name}")
    else:
        print("   (No agents found. Create one with 'new <name>')")
    print()

def run_agent(name):
    """Runs the run.py script of the specified agent."""
    agent_dir = GENERATORS_DIR / name
    run_script = agent_dir / "run.py"
    
    if not run_script.exists():
        print(f"\n❌ Error: Agent '{name}' not found.")
        print(f"   Checked path: {run_script}")
        list_agents()
        return

    print(f"\n🚀 Launching Agent: {name}...")
    print(f"   📂 Working Directory: {agent_dir}")
    print("=" * 60)
    
    try:
        # Execute the script in its own directory to maintain relative path links
        subprocess.run([sys.executable, "run.py"], cwd=agent_dir, check=True)
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 60)
        print(f"❌ Agent '{name}' failed with exit code {e.returncode}.")
    except KeyboardInterrupt:
        print("\n🛑 Agent execution interrupted by user.")
    print("=" * 60 + "\n")

def create_agent(name):
    """Creates a new agent folder with boilerplate code."""
    agent_dir = GENERATORS_DIR / name
    
    if agent_dir.exists():
        print(f"\n⚠️  Error: Agent '{name}' already exists at {agent_dir}")
        return

    # Create directory
    agent_dir.mkdir(parents=True)

    # 1. Create _path_setup.py (Path helper)
    path_setup_content = """
import sys
from pathlib import Path

# Add automation root to sys.path to allow imports from libs & config
# Structure: automation/generators/<agent_name>/_path_setup.py
current_dir = Path(__file__).resolve().parent
automation_root = current_dir.parent.parent

if str(automation_root) not in sys.path:
    sys.path.append(str(automation_root))
"""
    (agent_dir / "_path_setup.py").write_text(path_setup_content.strip() + "\n", encoding="utf-8")

    # 2. Create run.py (Main entry point)
    run_content = f"""import _path_setup
import sys
from datetime import datetime
import config.settings as config
# from libs.utils import StateManager
# from libs.scraper import NewsScraper

def main():
    print("--- 🤖 {name.replace('_', ' ').title()} Started ---")
    print(f"   ⏰ Time: {{datetime.now()}}")
    
    # Example: Accessing config
    # print(f"   Config Loaded: {{config.BASE_DIR}}")
    
    # TODO: Implement your agent logic here
    print("   ✨ Hello! This is a new AI agent.")

if __name__ == "__main__":
    main()
"""
    (agent_dir / "run.py").write_text(run_content, encoding="utf-8")

    print(f"\n✅ Successfully created new agent: '{name}'")
    print(f"   📂 Location: {agent_dir}")
    print(f"   📝 Files created: run.py, _path_setup.py")
    print(f"   🚀 Try running it: python automation/agents.py run {name}\n")

def main():
    parser = argparse.ArgumentParser(description="Manage and Run AI Agents")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: list
    subparsers.add_parser("list", help="List all agents")

    # Command: run <name>
    run_parser = subparsers.add_parser("run", help="Run a specific agent")
    run_parser.add_argument("name", help="Name of the agent folder")

    # Command: new <name>
    new_parser = subparsers.add_parser("new", help="Create a new agent boilerplate")
    new_parser.add_argument("name", help="Name of the new agent (e.g., youtube_summary)")

    args = parser.parse_args()

    if args.command == "list":
        list_agents()
    elif args.command == "run":
        run_agent(args.name)
    elif args.command == "new":
        create_agent(args.name)
    else:
        # Default behavior if no args: Show help
        parser.print_help()

if __name__ == "__main__":
    main()
