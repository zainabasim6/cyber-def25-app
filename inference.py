import pandas as pd
import joblib
import os
import glob
from datetime import datetime

def load_model():
    try:
        model = joblib.load('model.pkl')
        print("✅ Model loaded successfully")
        return model
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None

def process_logs():
    input_dir = '/input/logs'
    output_file = '/output/alerts.csv'
    
    print(f"📁 Looking for logs in: {input_dir}")
    
    if not os.path.exists(input_dir):
        print(f"❌ Input directory {input_dir} not found")
        return
    
    log_files = glob.glob(os.path.join(input_dir, '*.log'))
    print(f"📄 Found {len(log_files)} log files")
    
    if not log_files:
        print("No log files found")
        return
    
    alerts = []
    for log_file in log_files:
        print(f"🔍 Processing: {log_file}")
        try:
            with open(log_file, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line:
                        if '404' in line or 'POST' in line or 'admin' in line:
                            alerts.append({
                                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                'log_file': os.path.basename(log_file),
                                'line_number': line_num,
                                'log_entry': line[:100],
                                'threat_level': 'HIGH',
                                'description': 'Suspicious activity detected'
                            })
        except Exception as e:
            print(f"Error processing {log_file}: {e}")
    
    if alerts:
        df = pd.DataFrame(alerts)
        df.to_csv(output_file, index=False)
        print(f"✅ {len(alerts)} alerts saved to {output_file}")
        print("Alerts Summary:")
        print(df[['log_file', 'threat_level', 'description']])
    else:
        print("✅ No threats detected")
        pd.DataFrame(columns=['timestamp','log_file','line_number','log_entry','threat_level','description']).to_csv(output_file, index=False)

if __name__ == "__main__":
    print("🚀 Starting malware detection...")
    model = load_model()
    process_logs()
    print("🎯 Detection completed")
