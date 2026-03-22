import argparse
import json
import os
from datetime import datetime
from substack_api import Newsletter

def main():
    parser = argparse.ArgumentParser(description="Fetch latest posts from a Substack newsletter and sync metadata.")
    parser.add_argument("url", nargs="?", default="https://lambpetros.substack.com", help="The Substack newsletter URL")
    parser.add_argument("--limit", type=int, default=9999, help="Number of posts to fetch")
    parser.add_argument("--output", default="substack_metadata/metadata.json", help="Output JSON file for metadata")
    
    args = parser.parse_args()
    
    print(f"Fetching {args.limit} recent posts from {args.url}...\n")
    try:
        newsletter = Newsletter(args.url)
        posts = newsletter.get_posts(limit=args.limit)
        
        metadata_log = []
        for i, post in enumerate(posts, 1):
            meta = post.get_metadata()
            print(f"{i}. {meta.get('title', 'Unknown Title')}")
            
            # Build clean metadata entry
            entry = {
                "title": meta.get('title'),
                "url": meta.get('canonical_url'),
                "post_date": meta.get('post_date'),
                "audience": meta.get('audience'),
                "fetched_at": datetime.now().isoformat()
            }
            metadata_log.append(entry)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        
        # Save payload
        with open(args.output, "w") as f:
            json.dump(metadata_log, f, indent=2)
            
        print(f"\nMetadata successfully saved to {args.output}")

    except Exception as e:
        print(f"Error fetching posts: {e}")

if __name__ == "__main__":
    main()
