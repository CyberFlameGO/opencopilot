# Running Helper Scripts
Helper scripts for Copilot.

## Running `local_unity.py`
Local Unity script to work with the remote Unity Copilot.

### Step 1: Requirements
Only requirements are having a macOS operating system and Python installed locally.

### Step 2: Create or Select a Conversation
After downloading the script, visit the [Unity Copilot](https://unity.sidekik.ai/) website. Here, you'll either create a new conversation or select an existing one. 

### Step 3: Copy the Conversation ID
In the URL of your selected conversation, you'll find the conversation ID. If you can't see it, simply refresh the page and select the chat again from the left side panel. 

The ID would look something like this: `ff105cf7-x1f4-4707-b634-177f6c3622d1`.

### Step 4: Run the Script Locally
From terminal navigate to `backend/scripts/` and run the script on your machine by typing in the following command:
```
python local_unity.py <conversation_id>
```

NB! Replace `<conversation_id>` with yours.


