"""
Automated GTFS Data Downloader for US Cities
Downloads real transit data from public APIs
"""
import requests
import zipfile
import os
from pathlib import Path

# GTFS Data Sources (Direct Download Links)
GTFS_SOURCES = {
    'NYC': {
        'url': 'http://web.mta.info/developers/data/nyct/subway/google_transit.zip',
        'name': 'New York MTA Subway'
    },
    'Chicago': {
        'url': 'https://www.transitchicago.com/downloads/sch_data/google_transit.zip',
        'name': 'Chicago CTA'
    },
    'SF': {
        'url': 'https://gtfs.sfmta.com/transitdata/google_transit.zip',
        'name': 'San Francisco MUNI'
    },
    'Boston': {
        'url': 'https://cdn.mbta.com/MBTA_GTFS.zip',
        'name': 'Boston MBTA'
    }
}

def download_gtfs(city_code, city_info):
    """Download and extract GTFS data for a city"""
    print(f"\n{'='*60}")
    print(f"Downloading: {city_info['name']}")
    print(f"{'='*60}")
    
    try:
        # Create output directory
        output_dir = Path(f'data/raw/gtfs_{city_code.lower()}')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Download ZIP file
        print(f"Fetching from: {city_info['url']}")
        response = requests.get(city_info['url'], timeout=120)
        response.raise_for_status()
        
        zip_path = output_dir / 'gtfs.zip'
        with open(zip_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Downloaded: {len(response.content) / 1024 / 1024:.2f} MB")
        
        # Extract ZIP
        print("Extracting files...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
        
        # List extracted files
        files = [f for f in os.listdir(output_dir) if f.endswith('.txt')]
        print(f"Extracted {len(files)} files:")
        for file in sorted(files):
            file_path = output_dir / file
            size_kb = os.path.getsize(file_path) / 1024
            print(f"  - {file} ({size_kb:.1f} KB)")
        
        # Remove ZIP file
        os.remove(zip_path)
        
        print(f"Success! Data saved to: {output_dir}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading: {e}")
        return False
    except zipfile.BadZipFile:
        print("Error: Downloaded file is not a valid ZIP")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def verify_gtfs_files(city_code):
    """Verify that essential GTFS files exist"""
    required_files = ['routes.txt', 'trips.txt', 'stops.txt', 'stop_times.txt']
    output_dir = Path(f'data/raw/gtfs_{city_code.lower()}')
    
    print(f"\nVerifying {city_code} GTFS files...")
    missing = []
    for file in required_files:
        if not (output_dir / file).exists():
            missing.append(file)
    
    if missing:
        print(f"  Warning: Missing files: {', '.join(missing)}")
        return False
    else:
        print(f"  All required files present")
        return True

def main():
    print("="*60)
    print("GTFS DATA DOWNLOADER - US CITIES")
    print("="*60)
    print(f"\nWill download GTFS data for {len(GTFS_SOURCES)} cities:")
    for code, info in GTFS_SOURCES.items():
        print(f"  - {info['name']}")
    
    print("\nThis may take a few minutes...")
    
    # Download all cities
    results = {}
    for city_code, city_info in GTFS_SOURCES.items():
        success = download_gtfs(city_code, city_info)
        results[city_code] = success
        
        if success:
            verify_gtfs_files(city_code)
    
    # Summary
    print("\n" + "="*60)
    print("DOWNLOAD SUMMARY")
    print("="*60)
    
    successful = sum(results.values())
    print(f"\nSuccessful: {successful}/{len(results)}")
    
    for city_code, success in results.items():
        status = "SUCCESS" if success else "FAILED"
        print(f"  {city_code}: {status}")
    
    if successful > 0:
        print(f"\nGTFS data downloaded to: data/raw/gtfs_*/")
        print("\nNext steps:")
        print("1. Check the downloaded files")
        print("2. Run the ETL pipeline to process the data")
        print("3. Combine with weather data for analysis")
    
    return successful == len(results)

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
