import os
import re

dir_renames = {
    'lib/screens/kaam': 'lib/screens/tasks',
    'lib/screens/milan': 'lib/screens/connections',
    'lib/screens/swipe': 'lib/screens/discover',
    'lib/screens/client': 'lib/screens/poster',
    'lib/screens/worker': 'lib/screens/earner',
}

file_renames = [
    ('lib/parts/swipe_card.dart', 'discover_card.dart'),
    ('lib/screens/discover/swipe_feed_screen.dart', 'discover_feed_screen.dart'),
    ('lib/screens/poster/client_dashboard_screen.dart', 'poster_dashboard_screen.dart'),
    ('lib/screens/earner/worker_dashboard_screen.dart', 'earner_dashboard_screen.dart'),
]

# Case-sensitive combinations or special text replacements
replacements = {
    '/swipe_feed_screen.dart': '/discover_feed_screen.dart',
    '/swipe_card.dart': '/discover_card.dart',
    '/client_dashboard_screen.dart': '/poster_dashboard_screen.dart',
    '/worker_dashboard_screen.dart': '/earner_dashboard_screen.dart',
    '/kaam/': '/tasks/',
    '/milan/': '/connections/',
    '/swipe/': '/discover/',
    '/client/': '/poster/',
    '/worker/': '/earner/',
    'SwipeFeed': 'DiscoverFeed',
    'SwipeCard': 'DiscoverCard',
    'ClientDashboard': 'PosterDashboard',
    'WorkerDashboard': 'EarnerDashboard',
    'swipe_feed': 'discover_feed',
    'swipe_card': 'discover_card',
    'client_dashboard': 'poster_dashboard',
    'worker_dashboard': 'earner_dashboard',
    'zomato': 'zupp_upp',
    'Zomato': 'ZUPP-UPP',
    'ZOMATO': 'ZUPP-UPP',
    'swiggy': 'zupp_upp',
    'Swiggy': 'ZUPP-UPP',
    'SWIGGY': 'ZUPP-UPP',
    'tinder': 'zupp_upp',
    'Tinder': 'ZUPP-UPP',
    'TINDER': 'ZUPP-UPP',
    'matches_list_screen': 'connections_list_screen',
    'MatchesListScreen': 'ConnectionsListScreen'
}

# we need to rename matches_list_screen.dart to connections_list_screen.dart
file_renames.append(('lib/screens/connections/matches_list_screen.dart', 'connections_list_screen.dart'))

def replace_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf8') as f:
            content = f.read()
    except Exception as e:
        return
    
    orig_content = content
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    if content != orig_content:
        with open(filepath, 'w', encoding='utf8') as f:
            f.write(content)

# 1. Rename directories
for old_path, new_path in dir_renames.items():
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        print(f"Renamed {old_path} to {new_path}")

# 2. Rename specific files (checking new dir paths)
for old_filepath, new_filename in file_renames:
    # Update dir path if it was renamed above
    for old_dir, new_dir in dir_renames.items():
        if old_filepath.startswith(old_dir):
            old_filepath = old_filepath.replace(old_dir, new_dir)
            break
            
    if os.path.exists(old_filepath):
        new_filepath = os.path.join(os.path.dirname(old_filepath), new_filename)
        os.rename(old_filepath, new_filepath)
        print(f"Renamed file {old_filepath} to {new_filepath}")

# 3. Replace in files
for root, dirs, files in os.walk('lib'):
    for file in files:
        if file.endswith('.dart'):
            filepath = os.path.join(root, file)
            filepath = filepath.replace("\\", "/") 
            replace_in_file(filepath)

# Let's also replace in pubspec.yaml and README (or other root files if needed)
for root_file in ['README.md', 'pubspec.yaml', 'lib/config/constants.dart', 'lib/config/router.dart']:
    if os.path.exists(root_file):
        replace_in_file(root_file)
        print(f"Replaced text in {root_file}")

print("Renaming and refactoring complete.")
