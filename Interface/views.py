from django.shortcuts import render, redirect
from .forms import VideoUploadForm
from .models import Video
import uuid
from .ambu import detect_ambulance_in_video
from .vehicle_detection import count_vehicles_in_video

def calculate_priority(processed_result, count):
    """
    Calculate the priority of a video based on the presence of an emergency vehicle and the count of vehicles.
    
    Args:
    - processed_result (bool): True if an emergency vehicle is detected, otherwise False.
    - count (int): Number of vehicles detected in the video.
    
    Returns:
    - int: Priority score.
    """
    ans = 0
    if processed_result:
        ans = count + 10  # Higher priority for emergency vehicles
    else:
        ans = count
    return ans

def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            session_id = uuid.uuid4()  # Generate a new session ID
            video_files = [form.cleaned_data['video1'], form.cleaned_data['video2'],
                           form.cleaned_data['video3'], form.cleaned_data['video4']]
            video_files = [video for video in video_files if video]

            # Save each video with the session ID
            for video_file in video_files:
                Video.objects.create(title=video_file.name, video_file=video_file, session_id=session_id)

            # Store session ID in session data
            request.session['session_id'] = str(session_id)

            return redirect('abc')
    else:
        form = VideoUploadForm()

    return render(request, 'upload_video.html', {'form': form})

def video_list(request):
    session_id = request.session.get('session_id')
    if session_id:
        videos = Video.objects.filter(session_id=session_id)
    else:
        videos = []

    return render(request, 'video_list.html', {'videos': videos})

def abc(request):
    session_id = request.session.get('session_id')
    if session_id:
        # Retrieve videos for the current session
        videos = Video.objects.filter(session_id=session_id)
        
        # Process each video and collect results
        results = []
        for video in videos:
            # Process the video file
            processed_result = detect_ambulance_in_video(video.video_file.path)
            count = count_vehicles_in_video(video.video_file.path)
            priority_score = calculate_priority(processed_result, count)
            results.append({
                'title': video.title,
                'result': processed_result,
                'count': count,
                'priority': priority_score
            })
        
        # Sort results by priority (highest priority first)
        results.sort(key=lambda x: -x['priority'])

        # Calculate timing for each video
        num_videos = len(results)
        for i, result in enumerate(results):
            result['start_time'] = i * 10  # Starting time in seconds
            result['end_time'] = (i + 1) * 10  # Ending time in seconds
        
        return render(request, 'abc.html', {'results': results})
    else:
        return render(request, 'abc.html', {'error': 'No videos found for this session.'})
