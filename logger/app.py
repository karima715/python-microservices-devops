import time
import os

LOG_FILE = '/app/logs/backend.log'
OUTPUT_FILE = '/app/logs/processed.log'

def process_logs():
    # Create logs directory if it doesn't exist
    os.makedirs('/app/logs', exist_ok=True)
    
    # Create files if they don't exist
    open(LOG_FILE, 'a').close()
    open(OUTPUT_FILE, 'a').close()
    
    # Read existing content
    processed_lines = set()
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r') as f:
            processed_lines = set(f.readlines())
    
    # Continuously monitor the log file
    while True:
        with open(LOG_FILE, 'r') as f:
            lines = f.readlines()
        
        new_lines = [line for line in lines if line not in processed_lines]
        
        for line in new_lines:
            # Process the log entry (add timestamp and write to output)
            processed_line = f"{time.ctime()}: {line}"
            with open(OUTPUT_FILE, 'a') as f:
                f.write(processed_line)
            processed_lines.add(line)
            print(processed_line, end='')
        
        time.sleep(5)  # Check every 5 seconds

if __name__ == '__main__':
    process_logs()