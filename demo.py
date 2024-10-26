import requests
import uuid
from rich.console import Console
from rich.panel import Panel
from rich.pretty import Pretty
from rich.prompt import Prompt
from typing import Optional
import os

console = Console()

def send_chat_request(sender_id: str, receiver_id: str, content: str, session_id: str, message_id: str, base_url: str = "http://localhost:8000"):
    """Send a chat request to the API and return the response"""
    url = f"{base_url}/chat"

    # message_id = str(uuid.uuid4())
    
    request_data = {
        "chat_request": {
            "session_id": session_id,
            "message_id": message_id,
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "content": content
        },
        "llm": {
            "provider": "ollama", # openai / ollama are the two options
            "credentials": {
                "api_key": "N/A", # For OpenAI suggest this: os.environ.get("OPENAI_API_KEY") / for ollama and llama3 then just N/A
                "model": "llama3:latest" # gpt-4o-mini for OpenAI / llama3:latest for ollama
            }
        }

    }
    
    try:
        response = requests.post(url, json=request_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error sending request:[/red] {str(e)}")
        return None
    
def get_chat_history(session_id: str, base_url: str= "http://localhost:8000"):
    """Get chat history from the API"""
    url = f"{base_url}/history"

    request_data = {
        "session_id": session_id,
        "message_id": str(uuid.uuid4()),
        "sender_id": "User",
        "receiver_id": "System",
        "content": "Request for chat history"
    }

    try:
        response = requests.post(url, json=request_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error retrieving history:[/red] {str(e)}")
        return None
    
def get_raw_json(session_id: str, base_url: str= "http://localhost:8000"):
    """Get raw JSON from the API"""
    url = f"{base_url}/raw_json"

    request_data = {
        "session_id": session_id,
        "message_id": str(uuid.uuid4()),
        "sender_id": "User",
        "receiver_id": "System",
        "content": "Request for raw JSON data"
    }
    
    try:
        response = requests.post(url, json=request_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error retrieving raw JSON:[/red] {str(e)}")
        return None

def display_message(message: dict, direction: str, session_id: Optional[str] = None):
    """Display a message in a formatted panel"""
    if direction == "sent":
        title = f"[blue]Sent Message (Session: {session_id if session_id else 'None'})[/blue]"
        border_style = "blue"
    else:
        response_session = message['message']['metadata']['session_id']
        title = f"[green]Received Message (Session: {response_session})[/green]"
        border_style = "green"
    
    console.print(Panel(
        Pretty(message),
        title=title,
        border_style=border_style,
        padding=(1, 2)
    ))

def handle_command(command: str, session_id: str) -> bool:
    """Handle special commands. Returns True if should exit the program"""
    if command == "/quit":
        return True
    elif command == "/history":
        if not session_id:
            console.print("[red]No active session to show history for[/red]")
            return False
        
        console.print("\n[yellow]Retrieving chat history...[/yellow]")
        history_response = get_chat_history(session_id)
        if history_response:
            # Access the metadata and convert it to a dictionary
            metadata = history_response['message']['metadata']

            console.print(Panel(
                Pretty(metadata),
                title="[yellow]Metadata[/yellow]",
                border_style="yellow",
                padding=(1, 2)
            ))
            console.print(Panel(
                history_response['message']['content'],
                title="[yellow]Chat History[/yellow]",
                border_style="yellow",
                padding=(1, 2)
            ))
        return False
    elif command == "/raw":
        if not session_id:
            console.print("[red]No active session to show raw JSON for[/red]")
            return False
        console.print("\n[yellow]Retrieving raw JSON-LD...[/yellow]")
        raw_json = get_raw_json(session_id)
        if raw_json:
            # Return all of the raw JSON messages
            console.print(Panel(
                Pretty(raw_json),
                title="[yellow]Raw JSON Messages[/yellow]",
                border_style="yellow",
                padding=(1, 2)
            ))
        return False            
    return False

def run_demo():
    """Run an interactive demonstration of the LLM-to-LLM communication API"""
    console.print("\n[yellow]Starting Interactive LLM-to-LLM Communication Demo[/yellow]\n")
    console.print("[cyan]Available commands:[/cyan]")
    console.print("  [cyan]/quit[/cyan] - Exit the program")
    console.print("  [cyan]/history[/cyan] - Show conversation history\n")

    # Initialise session
    session_id = str(uuid.uuid4())
    console.print(f"[yellow]Initialising with session ID: {session_id}[/yellow]\n")

    sender_id = "Human"
    receiver_id = "LLM"

    while True:
        content = Prompt.ask("\n[blue]Enter your message[/blue]")

        # Handle commands
        if content.startswith('/'):
            if handle_command(content.lower(), session_id):
                break
            continue

        message_id = str(uuid.uuid4())

        # Construct and send the request
        request_data = {
            "metadata": {
                "sender_id": sender_id,
                "receiver_id": receiver_id,
                "message_id": message_id
            },
            "content": content
        }

        display_message(request_data, "sent", session_id)

        # Send the request and get the response
        response = send_chat_request(
            sender_id,
            receiver_id,
            content,
            session_id=session_id,
            message_id=message_id
        )

        if response:
            # Display the response and its session ID
            display_message(response, "received")

            # Check if session IDs match
            response_session = response['message']['metadata']['session_id']
            if response_session != session_id:
                console.print(f"\n[red]Warning: Session ID mismatch![/red]")
                console.print(f"Sent with session: {session_id}")
                console.print(f"Received response with session: {response_session}")
                
            # # Get or update session_id from the response
            # if not session_id:
            #     session_id = response['message']['metadata']['session_id']
            #     console.print(f"\n[yellow]Session initialised with ID: {session_id}[/yellow]\n")
                
            # # Display the response
            # display_message(response, "received")

        console.print("\n" + "-" * 80 + "\n")

if __name__ == "__main__":
    run_demo()