import google.generativeai as genai
import os
from PIL import Image
from IPython.display import Markdown
# Load an image
img = Image.open("image1.jpg")
# for video

import cv2
import shutil

genai.configure(api_key = "AIzaSyCB2vqDZPG-c5RoqEns1zJxzobfZISBlc8")


#video processing
#====================================================================================================

video_file_name = "dl_1.mp4"
video_time = 19

# Create or cleanup existing extracted image frames directory.
FRAME_EXTRACTION_DIRECTORY = "./content/frames"
FRAME_PREFIX = "_frame"
def create_frame_output_dir(output_dir):
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)
  else:
    shutil.rmtree(output_dir)
    os.makedirs(output_dir)

def extract_frame_from_video(video_file_path):
  print(f"Extracting {video_file_path} at 1 frame per second. This might take a bit...")
  create_frame_output_dir(FRAME_EXTRACTION_DIRECTORY)
  vidcap = cv2.VideoCapture(video_file_path)
  fps = vidcap.get(cv2.CAP_PROP_FPS)
  frame_duration = 1 / fps  # Time interval between frames (in seconds)
  output_file_prefix = os.path.basename(video_file_path).replace('.', '_')
  frame_count = 0
  count = 0
 
  while vidcap.isOpened():
      success, frame = vidcap.read()
      if not success: # End of video
          break
      if int(count / fps) == frame_count: # Extract a frame every second
          min = frame_count // 60
          sec = frame_count % 60
          time_string = f"{min:02d}:{sec:02d}"
          image_name = f"{output_file_prefix}{FRAME_PREFIX}{time_string}.jpg"
          output_filename = os.path.join(FRAME_EXTRACTION_DIRECTORY, image_name)
          cv2.imwrite(output_filename, frame)
          frame_count += 1
      count += 1
  vidcap.release() # Release the capture object\n",
  video_file_length = int(frame_count / fps)
  print(f"Completed video frame extraction!\n\nExtracted: {frame_count} frames")

extract_frame_from_video(video_file_name)

#upload frames
class File:
  def __init__(self, file_path: str, display_name: str = None):
    self.file_path = file_path
    if display_name:
      self.display_name = display_name
    self.timestamp = get_timestamp(file_path)

  def set_file_response(self, response):
    self.response = response

def get_timestamp(filename):
  """Extracts the frame count (as an integer) from a filename with the format
     'output_file_prefix_frame00:00.jpg'.
  """
  parts = filename.split(FRAME_PREFIX)
  if len(parts) != 2:
      return None  # Indicates the filename might be incorrectly formatted
  return parts[1].split('.')[0]

# Process each frame in the output directory
files = os.listdir(FRAME_EXTRACTION_DIRECTORY)
files = sorted(files)
files_to_upload = []
for file in files:
  files_to_upload.append(
      File(file_path=os.path.join(FRAME_EXTRACTION_DIRECTORY, file)))

# Upload the files to the API
# Only upload a 10 second slice of files to reduce upload time.
# Change full_video to True to upload the whole video.
full_video = True

uploaded_files = []
print(f'Uploading {len(files_to_upload) if full_video else 10} files. This might take a bit...')

for file in files_to_upload if full_video else files_to_upload[40:50]:
  print(f'Uploading: {file.file_path}...')
  response = genai.upload_file(path=file.file_path)
  file.set_file_response(response)
  uploaded_files.append(file)

print(f"Completed file uploads!\n\nUploaded: {len(uploaded_files)} files")


# Create the prompt.
prompt = """Generate a 60 words summary for the video.
The purpose of the summary is to be used to generate text embedding 
that will help with searching/identifying the video"""

# Set the model to Gemini 1.5 Pro.
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

# Make GenerateContent request with the structure described above.
def make_request(prompt, files):
  request = [prompt]
  for file in files:
    request.append(file.timestamp)
    request.append(file.response)
  return request

# Make the LLM request.
request = make_request(prompt, uploaded_files)
response = model.generate_content(request,
                                  request_options={"timeout": 600})
print(response.text)
video_summary = response