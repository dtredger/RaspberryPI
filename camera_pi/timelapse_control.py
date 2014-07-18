import os
import time

TIMELAPSE_DIRECTORY = os.environ.get("TIMELAPSE_DIRECTORY","/500gb_hd/timelapse/")

def capture_timelapse_images(interval_minutes):
    timestamp = int(time.time())
        
    # Define the size of the image you wish to capture. 
    img_width = "800" # Max = 2592 
    img_height = "600" # Max = 1944
    
    # Capture the image using raspistill. Set to capture with added sharpening, 
    # auto white balance and average metering mode
    os.system("raspistill -w " + img_width + " -h " + img_height + " -o " + \
        TIMELAPSE_DIRECTORY + str(timestamp) + ".jpg -sh 40 -awb auto -mm average -v")
    
    # 60 seconds * 60 = 1/hr
    time.sleep(60*int(interval_minutes))


if __name__ == "__main__":
    import sys
    try:
        while True:
            capture_timelapse_images(sys.argv[1])
    except KeyboardInterrupt:
        pass