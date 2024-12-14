from users.models import Units
import zmq
import math

#-----------------------------------------------------------------------------#
# Interface with Microservice A
#-----------------------------------------------------------------------------#
def convert(activities):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    # send activities to msA
    socket.send_json({"action": "convert", "data": activities})
    print("Sending conversion request to Microservice A!!")
    converted_activities = socket.recv_json()
    print(f"Received the following converted data from Microservice A:\n{converted_activities}")

    return converted_activities

#-----------------------------------------------------------------------------#
# Interface with Microservice B
#-----------------------------------------------------------------------------#
def retrieve_stats(time, activities, is_metric):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5556")

    # parse activities into data we need
    data = []
    for activity in activities:
        date_string = activity.date.strftime("%Y-%m-%d")
        distance = float(activity.distance)
        duration = activity.duration
        elev = activity.elevation
        data.append({'date': date_string, 'distance': distance, 'duration': duration, 'elevation': elev})

    # send activities to msB
    socket.send_json({"time": time, "data": data})
    print("Sending stat request to Microservice B!!")
    retrieved_stats = socket.recv_json()
    print(f"Received the following data from Microservice B:\n{retrieved_stats}")
    data = retrieved_stats
    if is_metric:
        # send it to msA
        data = convert([retrieved_stats])[0]
    formatted_data = {
                    "activities": str(data['activities']),
                    "time": get_duration_string(data['duration']),
                    "distance": get_distance_string(data['distance'], is_metric),
                    "elevation": get_elevation_string(data['elevation'], is_metric)
    }
    return formatted_data

#-----------------------------------------------------------------------------#
# Interface with Microservice C
#-----------------------------------------------------------------------------#
def average_stats(time, activities, is_metric):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5557")

    # parse activities into data we need
    data = []
    for activity in activities:
        date_string = activity.date.strftime("%Y-%m-%d")
        distance = float(activity.distance)
        duration = activity.duration
        elev = activity.elevation
        data.append({'date': date_string, 'distance': distance, 'duration': duration, 'elevation': elev})

    # send activities to msC
    socket.send_json({"time": time, "data": data})
    print("Sending stat request to Microservice C!!")
    retrieved_stats = socket.recv_json()
    print(f"Received the following data from Microservice C:\n{retrieved_stats}")
    data = retrieved_stats
    if is_metric:
        # send it to msA
        data = convert([retrieved_stats])[0]
    formatted_data = {
                    "activities": str(data['activities']),
                    "time": get_duration_string(data['duration']),
                    "distance": get_distance_string(data['distance'], is_metric),
                    "elevation": get_elevation_string(data['elevation'], is_metric)
    }
    return formatted_data

#-----------------------------------------------------------------------------#
# Interface with Microservice D
#-----------------------------------------------------------------------------#
def snapshot_stats(activities, is_metric):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5558")

    # parse activities into data we need
    data = []
    for activity in activities:
        date_string = activity.date.strftime("%Y-%m-%d")
        distance = float(activity.distance)
        duration = activity.duration
        elev = activity.elevation
        data.append({'date': date_string, 'distance': distance, 'duration': duration, 'elevation': elev})

    # send activities to msD
    socket.send_json({"data": data})
    print("Sending snapshot request to Microservice D!!")
    retrieved_stats = socket.recv_json()
    print(f"Received the following data from Microservice D:\n{retrieved_stats}")
    data = retrieved_stats
    if is_metric:
        # send it to msA
        data = convert([retrieved_stats])[0]
    formatted_data = {
                    "activities": str(data['activities']),
                    "time": get_duration_string(data['duration']),
                    "distance": get_distance_string(data['distance'], is_metric)
    }
    return formatted_data
#-----------------------------------------------------------------------------#
# Helper Methods
#-----------------------------------------------------------------------------#
def get_duration_string(activity_duration):
    ''' This method calculates and returns a string containing the hours and
        minutes for an activity duration.
        :param activity_duration: Duration in seconds (int)
        :return: String representing the activity duration example: "1hr 32min"
        '''
    duration_hours = math.floor(activity_duration / 3600)
    duration_minutes = math.floor(60*((activity_duration/3600) - duration_hours))
    if duration_hours > 0:
        return f"{duration_hours}h {duration_minutes}m"
    return f"{duration_minutes}m"

def get_distance_string(distance, is_metric):
    if is_metric:
        return f"{distance:.1f} km"
    return f"{distance:.1f} mi"

def get_elevation_string(elev, is_metric):
    if is_metric:
        return f"{elev:.1f} m"
    return f"{elev:.1f} ft"
